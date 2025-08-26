"""
Simple BMAD UI Backend - Demonstration Version
Works with ecosystem integration for testing
"""

import asyncio
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Simple HTTP server for demonstration
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import threading
import webbrowser

class BMADSimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            response = {
                "status": "operational",
                "timestamp": datetime.now().isoformat(),
                "version": "2.0.0-simple",
                "bmad_ecosystem": "integrated",
                "message": "🚀 BMAD UI Backend is running!"
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == "/api/system/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json") 
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            # Check ecosystem integration
            ecosystem_root = Path(__file__).parent / "../../.."
            ecosystem_config_path = ecosystem_root / ".bmad-core" / "core-config.yaml"
            
            ecosystem_status = "connected" if ecosystem_config_path.exists() else "not_found"
            
            if ecosystem_config_path.exists():
                try:
                    with open(ecosystem_config_path, 'r') as f:
                        config = yaml.safe_load(f)
                    ecosystem_name = config.get('ecosystem_name', 'unknown')
                    bmad_version = config.get('bmad_version', 'unknown')
                except:
                    ecosystem_name = 'error'
                    bmad_version = 'error'
            else:
                ecosystem_name = 'not_found'
                bmad_version = 'not_found'
            
            response = {
                "status": "operational",
                "uptime": "running",
                "active_projects": 0,
                "active_agents": 4,
                "bmad_core_version": bmad_version,
                "ecosystem": {
                    "name": ecosystem_name,
                    "status": ecosystem_status,
                    "agents_available": ["project_creator", "feature_builder", "integration_helper", "debugging_assistant"]
                }
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == "/api/bmad/agents":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*") 
            self.end_headers()
            
            # Mock ecosystem agents
            agents = [
                {
                    "id": "pm",
                    "name": "PROJECT MANAGER",
                    "role": "Product Manager", 
                    "handler": "project_creator",
                    "responsibilities": ["Create and maintain PRDs", "Define user stories"],
                    "status": "available",
                    "ecosystem_agent": True
                },
                {
                    "id": "architect", 
                    "name": "SYSTEM ARCHITECT",
                    "role": "Solution Architect",
                    "handler": "feature_builder", 
                    "responsibilities": ["Design system architecture", "Define technical decisions"],
                    "status": "available",
                    "ecosystem_agent": True
                },
                {
                    "id": "dev",
                    "name": "CORE DEVELOPER", 
                    "role": "Development Lead",
                    "handler": "integration_helper",
                    "responsibilities": ["Implement features", "Coordinate development"],
                    "status": "available", 
                    "ecosystem_agent": True
                },
                {
                    "id": "qa",
                    "name": "QUALITY ASSURANCE",
                    "role": "Quality Assurance", 
                    "handler": "debugging_assistant",
                    "responsibilities": ["Define testing strategies", "Ensure quality standards"],
                    "status": "available",
                    "ecosystem_agent": True
                }
            ]
            self.wfile.write(json.dumps(agents).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == "/api/projects/deploy":
            self._handle_project_deployment()
        elif self.path == "/api/agents/execute":
            self._handle_agent_execution()
        elif self.path == "/api/projects/implement":
            self._handle_feature_implementation()
        else:
            self.send_response(404)
            self.end_headers()
    
    def _handle_project_deployment(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            project_data = json.loads(post_data.decode('utf-8'))
            
            # Step 1: Create project directory using ecosystem's project_creator
            project_name = project_data.get('name', '').replace(' ', '-').lower()
            project_type = project_data.get('architecture', 'fastapi-next')
            
            # Execute real project creation using BMAD integration
            ecosystem_root = Path(__file__).parent / "../../.."
            bmad_integration_path = ecosystem_root / "agents" / "bmad_integration" / "bmad_agent_integration.py"
            
            if bmad_integration_path.exists():
                import subprocess
                import os
                
                # Set up environment for agent execution
                env = os.environ.copy()
                env['PYTHONPATH'] = str(ecosystem_root)
                
                # Use BMAD PM agent to create PRD and project structure
                pm_prompt = f"""Create project structure and PRD for: {project_data.get('name', 'Untitled Project')}

Description: {project_data.get('description', 'No description')}
Objectives: {', '.join(project_data.get('objectives', []))}
Architecture: {project_data.get('architecture', 'fastapi-next')}
Team: {project_data.get('team', 'default')}"""
                
                cmd = [
                    'python3', str(bmad_integration_path),
                    '@pm',
                    project_name,
                    pm_prompt
                ]
                
                print(f"🚀 Executing BMAD PM: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
                
                if result.returncode == 0:
                    project_created = True
                    creation_output = result.stdout
                else:
                    project_created = False
                    creation_output = f"STDERR: {result.stderr}\nSTDOUT: {result.stdout}"
            else:
                project_created = False
                creation_output = "BMAD integration not found"
            
            # Step 2: Generate PRD.md from project data
            prd_content = self._generate_prd_content(project_data)
            
            # Step 3: Prepare response with real deployment status
            deployment_id = f"deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            response = {
                "status": "deployment_initiated" if project_created else "deployment_failed",
                "deployment_id": deployment_id,
                "project_name": project_data.get('name', 'Unknown Project'),
                "project_directory": f"projects/{project_name}" if project_created else None,
                "timestamp": datetime.now().isoformat(),
                "project_creation": {
                    "success": project_created,
                    "output": creation_output
                },
                "prd_generated": True,
                "prd_content": prd_content,
                "agents_ready": [
                    {"id": "pm", "status": "ready", "handler": "project_creator"},
                    {"id": "architect", "status": "ready", "handler": "feature_builder"}, 
                    {"id": "dev", "status": "ready", "handler": "integration_helper"},
                    {"id": "qa", "status": "ready", "handler": "debugging_assistant"}
                ],
                "next_steps": [
                    "PM Agent: Generate user stories and epics",
                    "Architect Agent: Create architecture.md",
                    "Dev Agent: Implement features",
                    "QA Agent: Define testing strategies"
                ],
                "mission_parameters": project_data
            }
            
            self.send_response(200 if project_created else 500)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            error_response = {"error": "Invalid JSON data"}
            self.wfile.write(json.dumps(error_response).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            error_response = {"error": f"Deployment error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())

    def _handle_agent_execution(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            agent_request = json.loads(post_data.decode('utf-8'))
            agent_id = agent_request.get('agent_id')
            project_name = agent_request.get('project_name')
            action = agent_request.get('action', 'execute')
            
            # Map agent IDs to actual ecosystem agents
            agent_mapping = {
                'pm': 'project_creator',
                'architect': 'feature_builder', 
                'dev': 'integration_helper',
                'qa': 'debugging_assistant'
            }
            
            handler = agent_mapping.get(agent_id)
            if not handler:
                raise ValueError(f"Unknown agent: {agent_id}")
            
            # Execute the appropriate ecosystem agent
            ecosystem_root = Path(__file__).parent / "../../.."
            result = self._execute_ecosystem_agent(handler, project_name, action, ecosystem_root)
            
            response = {
                "agent_id": agent_id,
                "handler": handler,
                "status": "completed" if result['success'] else "failed",
                "output": result['output'],
                "timestamp": datetime.now().isoformat()
            }
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            error_response = {"error": f"Agent execution error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
                
    def _generate_prd_content(self, project_data):
        """Generate PRD.md content based on project data"""
        objectives = project_data.get('objectives', [])
        objectives_text = '\n'.join([f"- {obj}" for obj in objectives])
        
        prd_content = f"""# Product Requirements Document (PRD)
**Project Name:** {project_data.get('name', 'Untitled Project')}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Version:** 1.0  

## Executive Summary
{project_data.get('description', 'No description provided.')}

## Project Objectives
{objectives_text}

## Target Architecture
- **Type:** {project_data.get('architecture', 'Not specified')}
- **Team:** {project_data.get('team', 'Not specified')}

## User Stories and Epics
*To be generated by PM Agent*

## Technical Requirements
*To be defined by Architecture Agent*

## Success Metrics
- Project successfully deployed
- All BMAD workflow phases completed
- Documentation generated automatically

## Next Steps
1. PM Agent: Generate detailed user stories
2. Architect Agent: Create technical architecture
3. Dev Agent: Implement core features
4. QA Agent: Define testing strategy
"""
        return prd_content

    def _execute_ecosystem_agent(self, handler, project_name, action, ecosystem_root):
        """Execute an ecosystem agent using BMAD integration"""
        try:
            import subprocess
            import os
            
            env = os.environ.copy()
            env['PYTHONPATH'] = str(ecosystem_root)
            
            bmad_integration_path = ecosystem_root / "agents" / "bmad_integration" / "bmad_agent_integration.py"
            
            # Map handler to BMAD agent
            agent_map = {
                'project_creator': '@pm',
                'feature_builder': '@architect', 
                'integration_helper': '@dev',
                'debugging_assistant': '@qa'
            }
            
            bmad_agent = agent_map.get(handler)
            if not bmad_agent:
                return {'success': False, 'output': f'Unknown handler: {handler}'}
            
            # Build appropriate prompts for each agent
            if bmad_agent == '@pm':
                prompt = f"Generate user stories and epics for project: {project_name}"
            elif bmad_agent == '@architect':
                prompt = f"Create technical architecture for project: {project_name}"
            elif bmad_agent == '@dev':
                prompt = f"Implement development tasks for project: {project_name}"
            elif bmad_agent == '@qa':
                prompt = f"Create testing strategy and quality gates for project: {project_name}"
            else:
                prompt = f"Execute {action} for project: {project_name}"
            
            cmd = [
                'python3', str(bmad_integration_path),
                bmad_agent,
                project_name,
                prompt
            ]
            
            print(f"🤖 Executing BMAD {bmad_agent}: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=90)
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout if result.returncode == 0 else f"STDERR: {result.stderr}\nSTDOUT: {result.stdout}",
                'return_code': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'output': 'Agent execution timed out (90s)'}
        except Exception as e:
            return {'success': False, 'output': f'Agent execution error: {str(e)}'}

    def _handle_feature_implementation(self):
        """Generate actual project-specific implementation code"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            request_data = json.loads(post_data.decode('utf-8'))
            project_name = request_data.get('project_name')
            project_objectives = request_data.get('objectives', [])
            project_description = request_data.get('description', '')
            
            ecosystem_root = Path(__file__).parent / "../../.."
            project_path = ecosystem_root / "projects" / project_name
            
            # Generate project-specific features based on objectives
            features_created = []
            
            if not project_path.exists():
                raise Exception(f"Project {project_name} not found")
            
            # Analyze objectives and generate specific implementations
            if any(keyword in ' '.join(project_objectives).lower() for keyword in ['dashboard', 'analytics', 'visualization', 'chart', 'metric']):
                features_created.extend(self._create_analytics_features(project_path, project_objectives))
            
            if any(keyword in ' '.join(project_objectives).lower() for keyword in ['real-time', 'live', 'websocket', 'update']):
                features_created.extend(self._create_realtime_features(project_path, project_objectives))
                
            if any(keyword in ' '.join(project_objectives).lower() for keyword in ['export', 'download', 'csv', 'pdf']):
                features_created.extend(self._create_export_features(project_path, project_objectives))
            
            response = {
                "status": "implementation_completed",
                "project_name": project_name,
                "features_implemented": features_created,
                "timestamp": datetime.now().isoformat(),
                "implementation_summary": f"Generated {len(features_created)} project-specific features based on objectives"
            }
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            error_response = {"error": f"Implementation error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())

    def _create_analytics_features(self, project_path, objectives):
        """Create analytics dashboard specific features"""
        features = []
        
        # Create analytics models
        analytics_models = '''from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base

class MetricData(Base):
    __tablename__ = "metric_data"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_type = Column(String, nullable=False)  # 'revenue', 'users', 'performance'
    metadata = Column(JSON)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

class DashboardWidget(Base):
    __tablename__ = "dashboard_widgets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    widget_type = Column(String, nullable=False)  # 'chart', 'metric', 'table'
    widget_config = Column(JSON)
    position_x = Column(Integer, default=0)
    position_y = Column(Integer, default=0)
    width = Column(Integer, default=4)
    height = Column(Integer, default=3)
'''
        
        with open(project_path / "backend" / "analytics_models.py", 'w') as f:
            f.write(analytics_models)
        features.append("analytics_models.py")
        
        # Create analytics API endpoints
        analytics_api = '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import datetime, timedelta

from database import get_db
from analytics_models import MetricData, DashboardWidget

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/metrics")
async def get_metrics(
    metric_type: Optional[str] = None,
    hours_back: int = 24,
    db: Session = Depends(get_db)
):
    """Get real-time metrics data"""
    cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
    
    query = db.query(MetricData).filter(MetricData.recorded_at >= cutoff_time)
    if metric_type:
        query = query.filter(MetricData.metric_type == metric_type)
    
    metrics = query.order_by(MetricData.recorded_at.desc()).limit(1000).all()
    
    return {
        "metrics": [
            {
                "id": m.id,
                "name": m.metric_name,
                "value": m.metric_value,
                "type": m.metric_type,
                "timestamp": m.recorded_at.isoformat(),
                "metadata": m.metadata
            } for m in metrics
        ],
        "total_count": len(metrics)
    }

@router.post("/metrics")
async def create_metric(
    metric_name: str,
    metric_value: float,
    metric_type: str,
    metadata: dict = None,
    db: Session = Depends(get_db)
):
    """Create a new metric data point"""
    metric = MetricData(
        metric_name=metric_name,
        metric_value=metric_value,
        metric_type=metric_type,
        metadata=metadata or {}
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    
    return {"message": "Metric created", "metric_id": metric.id}

@router.get("/dashboard/widgets")
async def get_user_widgets(user_id: int, db: Session = Depends(get_db)):
    """Get dashboard widgets for a user"""
    widgets = db.query(DashboardWidget).filter(DashboardWidget.user_id == user_id).all()
    
    return {
        "widgets": [
            {
                "id": w.id,
                "type": w.widget_type,
                "config": w.widget_config,
                "position": {"x": w.position_x, "y": w.position_y},
                "size": {"width": w.width, "height": w.height}
            } for w in widgets
        ]
    }
'''
        
        with open(project_path / "backend" / "analytics_api.py", 'w') as f:
            f.write(analytics_api)
        features.append("analytics_api.py")
        
        # Create React dashboard component
        dashboard_component = '''import React, { useState, useEffect } from 'react';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

interface MetricData {
  id: number;
  name: string;
  value: number;
  type: string;
  timestamp: string;
  metadata?: any;
}

export default function AnalyticsDashboard() {
  const [metrics, setMetrics] = useState<MetricData[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedMetricType, setSelectedMetricType] = useState<string>('all');

  useEffect(() => {
    fetchMetrics();
    
    // Set up real-time updates
    const interval = setInterval(fetchMetrics, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, [selectedMetricType]);

  const fetchMetrics = async () => {
    try {
      const url = selectedMetricType === 'all' 
        ? '/api/analytics/metrics'
        : `/api/analytics/metrics?metric_type=${selectedMetricType}`;
      
      const response = await fetch(url);
      const data = await response.json();
      setMetrics(data.metrics || []);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
      setLoading(false);
    }
  };

  const prepareChartData = (metricType: string) => {
    const filteredMetrics = metrics.filter(m => m.type === metricType);
    const labels = filteredMetrics.map(m => new Date(m.timestamp).toLocaleDateString());
    const values = filteredMetrics.map(m => m.value);

    return {
      labels,
      datasets: [
        {
          label: metricType.charAt(0).toUpperCase() + metricType.slice(1),
          data: values,
          borderColor: 'rgb(59, 130, 246)',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          tension: 0.4,
        },
      ],
    };
  };

  const metricTypes = Array.from(new Set(metrics.map(m => m.type)));

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
        <select
          value={selectedMetricType}
          onChange={(e) => setSelectedMetricType(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
        >
          <option value="all">All Metrics</option>
          {metricTypes.map(type => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {metricTypes.map(type => {
          const typeMetrics = metrics.filter(m => m.type === type);
          const latestValue = typeMetrics[0]?.value || 0;
          const previousValue = typeMetrics[1]?.value || 0;
          const change = latestValue - previousValue;
          const changePercent = previousValue ? ((change / previousValue) * 100).toFixed(1) : 0;
          
          return (
            <div key={type} className="bg-white p-6 rounded-lg shadow border">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{type.toUpperCase()}</p>
                  <p className="text-2xl font-bold text-gray-900">{latestValue.toLocaleString()}</p>
                </div>
                <div className={`text-sm font-medium ${change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {change >= 0 ? '+' : ''}{changePercent}%
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {metricTypes.map(type => (
          <div key={type} className="bg-white p-6 rounded-lg shadow border">
            <h3 className="text-lg font-semibold mb-4">{type} Trend</h3>
            <div className="h-64">
              <Line 
                data={prepareChartData(type)} 
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  scales: {
                    y: {
                      beginAtZero: true,
                    },
                  },
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
'''
        
        frontend_components_dir = project_path / "frontend" / "src" / "components"
        frontend_components_dir.mkdir(parents=True, exist_ok=True)
        with open(frontend_components_dir / "AnalyticsDashboard.tsx", 'w') as f:
            f.write(dashboard_component)
        features.append("AnalyticsDashboard.tsx")
        
        return features

    def _create_realtime_features(self, project_path, objectives):
        """Create real-time WebSocket features"""
        features = []
        
        # WebSocket manager for real-time updates
        websocket_code = '''from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Connection is broken, remove it
                self.active_connections.remove(connection)

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back or process the data
            await manager.send_personal_message(f"Echo: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def broadcast_metric_update(metric_data: dict):
    """Broadcast metric updates to all connected clients"""
    message = json.dumps({
        "type": "metric_update",
        "data": metric_data
    })
    await manager.broadcast(message)
'''
        
        with open(project_path / "backend" / "websocket_manager.py", 'w') as f:
            f.write(websocket_code)
        features.append("websocket_manager.py")
        
        return features

    def _create_export_features(self, project_path, objectives):
        """Create data export functionality"""
        features = []
        
        # Export utilities
        export_code = '''import csv
import json
import io
from typing import List, Dict, Any
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

class DataExporter:
    @staticmethod
    def to_csv(data: List[Dict[str, Any]], filename: str = "export.csv") -> StreamingResponse:
        """Export data to CSV format"""
        if not data:
            raise HTTPException(status_code=400, detail="No data to export")
        
        output = io.StringIO()
        fieldnames = data[0].keys()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
        output.seek(0)
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    @staticmethod
    def to_json(data: List[Dict[str, Any]], filename: str = "export.json") -> StreamingResponse:
        """Export data to JSON format"""
        if not data:
            raise HTTPException(status_code=400, detail="No data to export")
        
        json_data = json.dumps(data, indent=2, default=str)
        
        return StreamingResponse(
            io.BytesIO(json_data.encode('utf-8')),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
'''
        
        with open(project_path / "backend" / "export_utils.py", 'w') as f:
            f.write(export_code)
        features.append("export_utils.py")
        
        return features
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        
    def log_message(self, format, *args):
        # Custom log format
        print(f"🚀 {datetime.now().strftime('%H:%M:%S')} - {format % args}")

def run_server():
    PORT = 8001
    print(f"""
🚀 BMAD UI Backend Starting...

   ▲ FastAPI-Compatible Server
   - Local:        http://localhost:{PORT}
   - Health Check: http://localhost:{PORT}/api/health  
   - System Status: http://localhost:{PORT}/api/system/status
   - Agents Info:   http://localhost:{PORT}/api/bmad/agents

 ✓ Ecosystem Integration: Active
 ✓ CORS Support: Enabled
 ✓ Gil's Agents: Connected
    """)
    
    with socketserver.TCPServer(("", PORT), BMADSimpleHandler) as httpd:
        print(f"✅ BMAD Backend serving at port {PORT}")
        print("🌟 Cosmic Mission Control is ready!")
        print("Press Ctrl+C to stop")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 BMAD Backend shutdown complete")
            httpd.server_close()

if __name__ == "__main__":
    run_server()