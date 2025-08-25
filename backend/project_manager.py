"""
Project Manager for BMAD UI Backend
Handles project creation, configuration, and lifecycle management
"""

import os
import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class ProjectManager:
    """Manages BMAD project lifecycle and configuration"""
    
    def __init__(self):
        self.projects_path = Path(__file__).parent / "../projects_data"
        self.projects_path.mkdir(exist_ok=True)
        self.active_projects: Dict[str, Dict] = {}
        self._load_existing_projects()
    
    def _load_existing_projects(self):
        """Load existing projects from disk"""
        try:
            for project_file in self.projects_path.glob("*.json"):
                project_id = project_file.stem
                with open(project_file, 'r') as f:
                    project_data = json.load(f)
                self.active_projects[project_id] = project_data
            
            print(f"📂 Loaded {len(self.active_projects)} existing projects")
        except Exception as e:
            print(f"❌ Error loading projects: {e}")
    
    async def create_project(self, config: Dict) -> str:
        """Create new BMAD project"""
        try:
            project_id = str(uuid.uuid4())[:8]  # Short UUID
            
            project_data = {
                "id": project_id,
                "name": config.get("name", f"Project-{project_id}"),
                "description": config.get("description", ""),
                "type": config.get("type", "greenfield-fullstack"),
                "tech_stack": config.get("techStack", {}),
                "agent_team": config.get("agentTeam", "team-fullstack"),
                "objectives": config.get("objectives", []),
                "status": "created",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "workflow_history": [],
                "generated_files": [],
                "metrics": {
                    "creation_time": datetime.now().isoformat(),
                    "workflows_executed": 0,
                    "files_generated": 0,
                    "agents_deployed": 0
                }
            }
            
            # Save to disk
            project_file = self.projects_path / f"{project_id}.json"
            with open(project_file, 'w') as f:
                json.dump(project_data, f, indent=2)
            
            # Store in memory
            self.active_projects[project_id] = project_data
            
            # Create project workspace directory
            workspace_path = self._get_project_workspace(project_id)
            workspace_path.mkdir(parents=True, exist_ok=True)
            
            print(f"✅ Project {project_id} ({project_data['name']}) created successfully")
            
            return project_id
            
        except Exception as e:
            print(f"❌ Failed to create project: {e}")
            raise
    
    async def get_project(self, project_id: str) -> Optional[Dict]:
        """Get project by ID"""
        return self.active_projects.get(project_id)
    
    async def update_project(self, project_id: str, updates: Dict) -> bool:
        """Update project configuration"""
        try:
            if project_id not in self.active_projects:
                return False
            
            project = self.active_projects[project_id]
            
            # Update fields
            for key, value in updates.items():
                if key != "id":  # Prevent ID changes
                    project[key] = value
            
            project["updated_at"] = datetime.now().isoformat()
            
            # Save to disk
            project_file = self.projects_path / f"{project_id}.json"
            with open(project_file, 'w') as f:
                json.dump(project, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to update project {project_id}: {e}")
            return False
    
    async def delete_project(self, project_id: str) -> bool:
        """Delete project"""
        try:
            if project_id not in self.active_projects:
                return False
            
            # Remove from memory
            del self.active_projects[project_id]
            
            # Remove from disk
            project_file = self.projects_path / f"{project_id}.json"
            if project_file.exists():
                project_file.unlink()
            
            # Remove workspace directory
            workspace_path = self._get_project_workspace(project_id)
            if workspace_path.exists():
                import shutil
                shutil.rmtree(workspace_path)
            
            print(f"🗑️ Project {project_id} deleted successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to delete project {project_id}: {e}")
            return False
    
    async def list_projects(self) -> List[Dict]:
        """List all projects"""
        return [
            {
                "id": project_id,
                "name": project["name"],
                "description": project["description"],
                "type": project["type"],
                "status": project["status"],
                "created_at": project["created_at"],
                "updated_at": project["updated_at"],
                "metrics": project.get("metrics", {})
            }
            for project_id, project in self.active_projects.items()
        ]
    
    async def add_workflow_execution(self, project_id: str, workflow_data: Dict) -> bool:
        """Record workflow execution"""
        try:
            if project_id not in self.active_projects:
                return False
            
            project = self.active_projects[project_id]
            
            workflow_record = {
                "workflow_id": workflow_data.get("workflow_id", str(uuid.uuid4())[:8]),
                "workflow_type": workflow_data.get("type", "unknown"),
                "status": workflow_data.get("status", "running"),
                "started_at": workflow_data.get("started_at", datetime.now().isoformat()),
                "completed_at": workflow_data.get("completed_at"),
                "agents_used": workflow_data.get("agents_used", []),
                "steps_completed": workflow_data.get("steps_completed", 0),
                "outputs": workflow_data.get("outputs", [])
            }
            
            project["workflow_history"].append(workflow_record)
            project["metrics"]["workflows_executed"] += 1
            project["status"] = workflow_data.get("status", "running")
            
            return await self.update_project(project_id, project)
            
        except Exception as e:
            print(f"❌ Failed to add workflow execution: {e}")
            return False
    
    async def add_generated_file(self, project_id: str, file_info: Dict) -> bool:
        """Record generated file"""
        try:
            if project_id not in self.active_projects:
                return False
            
            project = self.active_projects[project_id]
            
            file_record = {
                "filename": file_info.get("filename", "unknown"),
                "path": file_info.get("path", ""),
                "type": file_info.get("type", "unknown"),
                "size": file_info.get("size", 0),
                "generated_at": datetime.now().isoformat(),
                "agent": file_info.get("agent", "unknown"),
                "checksum": file_info.get("checksum")
            }
            
            project["generated_files"].append(file_record)
            project["metrics"]["files_generated"] += 1
            
            return await self.update_project(project_id, project)
            
        except Exception as e:
            print(f"❌ Failed to add generated file: {e}")
            return False
    
    def _get_project_workspace(self, project_id: str) -> Path:
        """Get project workspace directory"""
        return self.projects_path / project_id / "workspace"
    
    async def get_project_workspace_path(self, project_id: str) -> Optional[str]:
        """Get project workspace path"""
        if project_id not in self.active_projects:
            return None
        
        workspace_path = self._get_project_workspace(project_id)
        workspace_path.mkdir(parents=True, exist_ok=True)
        return str(workspace_path)
    
    async def get_project_stats(self) -> Dict:
        """Get project statistics"""
        total_projects = len(self.active_projects)
        
        status_counts = {}
        type_counts = {}
        team_counts = {}
        
        for project in self.active_projects.values():
            # Status counts
            status = project.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
            
            # Type counts  
            proj_type = project.get("type", "unknown")
            type_counts[proj_type] = type_counts.get(proj_type, 0) + 1
            
            # Team counts
            team = project.get("agent_team", "unknown")
            team_counts[team] = team_counts.get(team, 0) + 1
        
        total_workflows = sum(
            project.get("metrics", {}).get("workflows_executed", 0)
            for project in self.active_projects.values()
        )
        
        total_files = sum(
            project.get("metrics", {}).get("files_generated", 0) 
            for project in self.active_projects.values()
        )
        
        return {
            "total_projects": total_projects,
            "status_distribution": status_counts,
            "type_distribution": type_counts,
            "team_distribution": team_counts,
            "total_workflows_executed": total_workflows,
            "total_files_generated": total_files,
            "workspace_path": str(self.projects_path)
        }