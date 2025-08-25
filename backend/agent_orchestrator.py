"""
Agent Orchestrator for BMAD UI Backend
Manages agent deployment, coordination, and status tracking
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime

class AgentOrchestrator:
    """Orchestrates BMAD agents for workflow execution"""
    
    def __init__(self):
        self.active_agents: Dict[str, Dict] = {}
        self.agent_pool = {
            "pm": {
                "name": "PROJECT MANAGER",
                "role": "Mission Coordinator", 
                "capabilities": ["project planning", "coordination", "stakeholder management"],
                "status": "available",
                "current_task": None,
                "load": 0
            },
            "architect": {
                "name": "SYSTEM ARCHITECT",
                "role": "Infrastructure Designer",
                "capabilities": ["system design", "architecture planning", "technical documentation"],
                "status": "available", 
                "current_task": None,
                "load": 0
            },
            "dev": {
                "name": "CORE DEVELOPER",
                "role": "Code Implementation Specialist",
                "capabilities": ["code development", "implementation", "debugging", "testing"],
                "status": "available",
                "current_task": None,
                "load": 0
            },
            "qa": {
                "name": "QUALITY ASSURANCE", 
                "role": "Testing and Validation Unit",
                "capabilities": ["testing", "quality validation", "performance analysis"],
                "status": "available",
                "current_task": None,
                "load": 0
            },
            "ux-expert": {
                "name": "UX SPECIALIST",
                "role": "User Experience Designer",
                "capabilities": ["ui design", "user research", "accessibility"],
                "status": "available",
                "current_task": None,
                "load": 0
            },
            "po": {
                "name": "PRODUCT OWNER",
                "role": "Requirements and Vision Keeper", 
                "capabilities": ["requirements gathering", "user stories", "acceptance criteria"],
                "status": "available",
                "current_task": None,
                "load": 0
            }
        }
        
        self.deployment_history: List[Dict] = []
        self.performance_metrics: Dict[str, Dict] = {}
    
    async def initialize(self):
        """Initialize agent orchestrator"""
        print("🤖 Agent Orchestrator initialized")
        print(f"👥 Available agents: {len(self.agent_pool)}")
        
        # Initialize performance metrics
        for agent_id in self.agent_pool:
            self.performance_metrics[agent_id] = {
                "tasks_completed": 0,
                "total_execution_time": 0,
                "success_rate": 100.0,
                "last_deployment": None
            }
    
    async def deploy_agents(self, project_id: str, agent_ids: List[str], task: str) -> Dict:
        """Deploy agents for a specific task"""
        try:
            deployment_id = f"deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{project_id}"
            
            deployed_agents = []
            failed_deployments = []
            
            for agent_id in agent_ids:
                if agent_id not in self.agent_pool:
                    failed_deployments.append({
                        "agent_id": agent_id,
                        "reason": "Agent not found in pool"
                    })
                    continue
                
                agent = self.agent_pool[agent_id].copy()
                
                if agent["status"] != "available":
                    failed_deployments.append({
                        "agent_id": agent_id, 
                        "reason": f"Agent busy: {agent['status']}"
                    })
                    continue
                
                # Deploy agent
                agent_deployment = {
                    "deployment_id": deployment_id,
                    "agent_id": agent_id,
                    "project_id": project_id,
                    "task": task,
                    "deployed_at": datetime.now().isoformat(),
                    "status": "deployed",
                    "progress": 0,
                    "logs": [f"Agent {agent_id} deployed for task: {task}"],
                    **agent
                }
                
                # Update agent status
                self.agent_pool[agent_id]["status"] = "deployed"
                self.agent_pool[agent_id]["current_task"] = task
                self.agent_pool[agent_id]["load"] += 1
                
                # Store deployment
                self.active_agents[f"{deployment_id}_{agent_id}"] = agent_deployment
                deployed_agents.append(agent_deployment)
                
                # Update metrics
                self.performance_metrics[agent_id]["last_deployment"] = datetime.now().isoformat()
            
            # Record deployment history
            deployment_record = {
                "deployment_id": deployment_id,
                "project_id": project_id,
                "task": task,
                "agents_requested": agent_ids,
                "agents_deployed": [a["agent_id"] for a in deployed_agents],
                "failed_deployments": failed_deployments,
                "deployed_at": datetime.now().isoformat()
            }
            
            self.deployment_history.append(deployment_record)
            
            return {
                "success": len(deployed_agents) > 0,
                "deployment_id": deployment_id,
                "deployed_agents": deployed_agents,
                "failed_deployments": failed_deployments,
                "total_requested": len(agent_ids),
                "total_deployed": len(deployed_agents)
            }
            
        except Exception as e:
            print(f"❌ Agent deployment failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "deployed_agents": [],
                "failed_deployments": []
            }
    
    async def update_agent_progress(self, deployment_key: str, progress: int, logs: List[str] = None):
        """Update agent progress and logs"""
        if deployment_key in self.active_agents:
            agent = self.active_agents[deployment_key]
            agent["progress"] = min(100, max(0, progress))
            agent["updated_at"] = datetime.now().isoformat()
            
            if logs:
                agent["logs"].extend(logs)
                # Keep only last 50 log entries
                agent["logs"] = agent["logs"][-50:]
            
            # Update status based on progress
            if progress >= 100:
                agent["status"] = "completed"
                agent["completed_at"] = datetime.now().isoformat()
                
                # Update agent pool status
                agent_id = agent["agent_id"]
                self.agent_pool[agent_id]["status"] = "available"
                self.agent_pool[agent_id]["current_task"] = None
                self.agent_pool[agent_id]["load"] = max(0, self.agent_pool[agent_id]["load"] - 1)
                
                # Update metrics
                self.performance_metrics[agent_id]["tasks_completed"] += 1
            
            return True
        return False
    
    async def recall_agents(self, project_id: str) -> Dict:
        """Recall all agents from a project"""
        recalled_agents = []
        
        for key, agent in list(self.active_agents.items()):
            if agent["project_id"] == project_id:
                agent_id = agent["agent_id"]
                
                # Update agent status
                agent["status"] = "recalled"
                agent["recalled_at"] = datetime.now().isoformat()
                
                # Update agent pool
                self.agent_pool[agent_id]["status"] = "available" 
                self.agent_pool[agent_id]["current_task"] = None
                self.agent_pool[agent_id]["load"] = max(0, self.agent_pool[agent_id]["load"] - 1)
                
                recalled_agents.append(agent_id)
                del self.active_agents[key]
        
        return {
            "success": True,
            "recalled_agents": recalled_agents,
            "total_recalled": len(recalled_agents)
        }
    
    async def get_agent_status(self, agent_id: str) -> Optional[Dict]:
        """Get current status of an agent"""
        if agent_id not in self.agent_pool:
            return None
        
        agent = self.agent_pool[agent_id].copy()
        
        # Add performance metrics
        if agent_id in self.performance_metrics:
            agent["performance"] = self.performance_metrics[agent_id]
        
        # Find active deployments
        active_deployments = [
            deployment for deployment in self.active_agents.values()
            if deployment["agent_id"] == agent_id and deployment["status"] in ["deployed", "active"]
        ]
        
        agent["active_deployments"] = len(active_deployments)
        
        return agent
    
    async def get_all_agents_status(self) -> List[Dict]:
        """Get status of all agents"""
        agents_status = []
        
        for agent_id in self.agent_pool:
            agent_status = await self.get_agent_status(agent_id)
            if agent_status:
                agents_status.append(agent_status)
        
        return agents_status
    
    async def get_active_agent_count(self) -> int:
        """Get count of currently active agents"""
        return len([
            agent for agent in self.agent_pool.values()
            if agent["status"] in ["deployed", "active"]
        ])
    
    async def get_step_agents(self, project_id: str, step_index: int) -> List[Dict]:
        """Get agents working on a specific step"""
        step_agents = []
        
        for agent in self.active_agents.values():
            if (agent["project_id"] == project_id and 
                agent["status"] in ["deployed", "active"]):
                
                # Simulate agent assignment to steps
                agent_step = {
                    "agent_id": agent["agent_id"],
                    "name": agent["name"],
                    "role": agent["role"],
                    "status": agent["status"],
                    "progress": agent["progress"],
                    "current_task": agent["current_task"]
                }
                step_agents.append(agent_step)
        
        return step_agents
    
    async def get_orchestrator_stats(self) -> Dict:
        """Get orchestrator statistics"""
        total_deployments = len(self.deployment_history)
        active_deployments = len(self.active_agents)
        
        # Calculate agent utilization
        agent_utilization = {}
        for agent_id, agent in self.agent_pool.items():
            metrics = self.performance_metrics.get(agent_id, {})
            agent_utilization[agent_id] = {
                "status": agent["status"],
                "load": agent["load"],
                "tasks_completed": metrics.get("tasks_completed", 0),
                "success_rate": metrics.get("success_rate", 100.0)
            }
        
        return {
            "total_agents": len(self.agent_pool),
            "active_deployments": active_deployments,
            "total_deployments": total_deployments,
            "agent_utilization": agent_utilization,
            "deployment_history_size": len(self.deployment_history)
        }
    
    async def simulate_agent_work(self, deployment_key: str, duration_seconds: int = 30):
        """Simulate agent work progress (for demo purposes)"""
        if deployment_key not in self.active_agents:
            return
        
        agent = self.active_agents[deployment_key]
        agent["status"] = "active"
        
        # Simulate progress updates
        for progress in range(0, 101, 10):
            if deployment_key not in self.active_agents:
                break  # Agent was recalled
            
            await self.update_agent_progress(
                deployment_key, 
                progress,
                [f"Progress update: {progress}% complete"]
            )
            
            await asyncio.sleep(duration_seconds / 10)
        
        return True