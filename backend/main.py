"""
BMAD UI Backend - Enhanced FastAPI server with WebSocket support
Integrates with BMAD Core methodology and Gil's ecosystem structure
"""

import os
import asyncio
import json
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

from bmad_integration import BMADCoreIntegration
from websocket_manager import ConnectionManager
from project_manager import ProjectManager
from agent_orchestrator import AgentOrchestrator

app = FastAPI(
    title="BMAD UI Backend",
    description="Enhanced Backend for BMAD Agent Methodology Interface",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
manager = ConnectionManager()
project_manager = ProjectManager()
bmad_integration = BMADCoreIntegration()
agent_orchestrator = AgentOrchestrator()

# Pydantic models
class ProjectConfig(BaseModel):
    name: str
    description: str
    type: str
    techStack: Dict[str, str]
    agentTeam: str
    objectives: List[str]

class WorkflowStatus(BaseModel):
    status: str
    currentStep: int
    steps: List[Dict[str, Any]]
    agents: List[Dict[str, Any]]
    logs: List[str]

class SystemStatus(BaseModel):
    status: str
    uptime: str
    active_projects: int
    active_agents: int
    bmad_core_version: str

# Global state
active_workflows: Dict[str, Dict] = {}
system_stats = {
    "start_time": datetime.now(),
    "projects_created": 0,
    "workflows_executed": 0
}

@app.on_event("startup")
async def startup_event():
    """Initialize BMAD Core integration and load configurations"""
    await bmad_integration.initialize()
    await agent_orchestrator.initialize()
    print("🚀 BMAD UI Backend initialized successfully!")
    print(f"📊 System Status: {await get_system_status()}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources"""
    await bmad_integration.cleanup()
    await manager.disconnect_all()
    print("🛑 BMAD UI Backend shutdown complete")

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """System health check"""
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "bmad_core": await bmad_integration.get_status()
    }

@app.get("/api/system/status")
async def get_system_status():
    """Get detailed system status"""
    uptime = datetime.now() - system_stats["start_time"]
    
    return SystemStatus(
        status="operational",
        uptime=str(uptime),
        active_projects=len(active_workflows),
        active_agents=await agent_orchestrator.get_active_agent_count(),
        bmad_core_version=await bmad_integration.get_version()
    )

@app.get("/api/bmad/agents")
async def get_available_agents():
    """Get list of available BMAD agents"""
    return await bmad_integration.get_available_agents()

@app.get("/api/bmad/workflows")
async def get_available_workflows():
    """Get list of available BMAD workflows"""
    return await bmad_integration.get_available_workflows()

@app.get("/api/bmad/templates")
async def get_project_templates():
    """Get available project templates from BMAD core"""
    return await bmad_integration.get_project_templates()

@app.post("/api/projects/create")
async def create_project(config: ProjectConfig, background_tasks: BackgroundTasks):
    """Create a new project with BMAD methodology"""
    try:
        project_id = await project_manager.create_project(config.dict())
        
        # Initialize project with BMAD core
        await bmad_integration.initialize_project(project_id, config.dict())
        
        # Update stats
        system_stats["projects_created"] += 1
        
        # Notify connected clients
        await manager.broadcast({
            "type": "project_created",
            "project_id": project_id,
            "config": config.dict()
        })
        
        return {
            "success": True,
            "project_id": project_id,
            "message": "Project created successfully",
            "bmad_integration": True
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

@app.post("/api/workflows/{project_id}/start")
async def start_workflow(project_id: str, background_tasks: BackgroundTasks):
    """Start BMAD workflow for a project"""
    try:
        if project_id in active_workflows:
            raise HTTPException(status_code=400, detail="Workflow already running")
        
        # Initialize workflow state
        workflow_config = await bmad_integration.get_workflow_config(project_id)
        
        active_workflows[project_id] = {
            "status": "running",
            "start_time": datetime.now(),
            "current_step": 0,
            "steps": workflow_config.get("steps", []),
            "agents": workflow_config.get("agents", [])
        }
        
        # Start workflow execution
        background_tasks.add_task(execute_workflow, project_id)
        
        # Update stats
        system_stats["workflows_executed"] += 1
        
        return {
            "success": True,
            "project_id": project_id,
            "workflow_id": project_id,
            "status": "started"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start workflow: {str(e)}")

@app.post("/api/workflows/{project_id}/pause")
async def pause_workflow(project_id: str):
    """Pause running workflow"""
    if project_id not in active_workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    active_workflows[project_id]["status"] = "paused"
    
    await manager.broadcast({
        "type": "workflow_paused",
        "project_id": project_id
    })
    
    return {"success": True, "status": "paused"}

@app.post("/api/workflows/{project_id}/stop")
async def stop_workflow(project_id: str):
    """Stop and cleanup workflow"""
    if project_id in active_workflows:
        active_workflows[project_id]["status"] = "stopped"
        await asyncio.sleep(1)  # Allow cleanup
        del active_workflows[project_id]
    
    await manager.broadcast({
        "type": "workflow_stopped",
        "project_id": project_id
    })
    
    return {"success": True, "status": "stopped"}

@app.get("/api/workflows/{project_id}/status")
async def get_workflow_status(project_id: str):
    """Get current workflow status"""
    if project_id not in active_workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = active_workflows[project_id]
    
    return WorkflowStatus(
        status=workflow["status"],
        currentStep=workflow["current_step"],
        steps=workflow["steps"],
        agents=workflow["agents"],
        logs=workflow.get("logs", [])
    )

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket connection for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
            elif message.get("type") == "subscribe":
                # Subscribe to specific project updates
                project_id = message.get("project_id")
                if project_id:
                    await manager.subscribe_to_project(websocket, project_id)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

async def execute_workflow(project_id: str):
    """Execute BMAD workflow with real-time updates"""
    workflow = active_workflows.get(project_id)
    if not workflow:
        return
    
    try:
        workflow_steps = workflow["steps"]
        
        for step_index, step in enumerate(workflow_steps):
            if workflow["status"] != "running":
                break
            
            # Update current step
            workflow["current_step"] = step_index
            
            # Notify clients of step start
            await manager.broadcast({
                "type": "step_started",
                "project_id": project_id,
                "step_index": step_index,
                "step": step
            })
            
            # Execute step with BMAD core
            step_result = await bmad_integration.execute_step(project_id, step)
            
            # Update step progress
            for progress in range(0, 101, 10):
                if workflow["status"] != "running":
                    break
                
                await manager.broadcast({
                    "type": "step_progress",
                    "project_id": project_id,
                    "step_index": step_index,
                    "progress": progress,
                    "agents": await agent_orchestrator.get_step_agents(project_id, step_index)
                })
                
                await asyncio.sleep(0.5)  # Simulate work
            
            # Complete step
            workflow["steps"][step_index]["status"] = "completed"
            workflow["steps"][step_index]["result"] = step_result
            
            await manager.broadcast({
                "type": "step_completed",
                "project_id": project_id,
                "step_index": step_index,
                "result": step_result
            })
            
            await asyncio.sleep(1)  # Pause between steps
        
        # Mark workflow as completed
        if workflow["status"] == "running":
            workflow["status"] = "completed"
            
            await manager.broadcast({
                "type": "workflow_completed",
                "project_id": project_id,
                "final_result": await bmad_integration.get_project_result(project_id)
            })
    
    except Exception as e:
        workflow["status"] = "error"
        workflow["error"] = str(e)
        
        await manager.broadcast({
            "type": "workflow_error",
            "project_id": project_id,
            "error": str(e)
        })

# Development endpoint
@app.get("/")
async def root():
    """Root endpoint with system info"""
    return {
        "name": "BMAD UI Backend",
        "version": "2.0.0",
        "status": "operational",
        "docs": "/api/docs",
        "websocket": "/ws",
        "system_stats": system_stats
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )