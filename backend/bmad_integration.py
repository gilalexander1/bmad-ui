"""
BMAD Core Integration Module
Integrates with the BMAD core system found in the ecosystem and provides
a customized interface for the BMAD UI project
"""

import os
import json
import yaml
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class BMADCoreIntegration:
    """Integration layer for BMAD Core methodology"""
    
    def __init__(self):
        self.bmad_core_path = Path(__file__).parent / "../bmad-core"
        self.ecosystem_root = Path(__file__).parent / "../../.."
        self.ecosystem_config_path = self.ecosystem_root / ".bmad-core" / "core-config.yaml"
        self.config = {}
        self.ecosystem_config = {}
        self.agents = {}
        self.workflows = {}
        self.templates = {}
        self.custom_agents = {}
        
    async def initialize(self):
        """Initialize BMAD Core integration"""
        try:
            await self._load_ecosystem_config()
            await self._load_core_config()
            await self._load_ecosystem_agents()
            await self._load_agents()
            await self._load_workflows() 
            await self._load_templates()
            await self._setup_ecosystem_integration()
            
            print("✅ BMAD Core integration initialized successfully")
            print(f"🌟 Ecosystem: {self.ecosystem_config.get('ecosystem_name', 'gil-dev-ecosystem')}")
            print(f"📂 Core Path: {self.bmad_core_path}")
            print(f"🎯 BMAD Agents: {len(self.agents)}")
            print(f"🤖 Custom Agents: {len(self.custom_agents)}")
            print(f"🔄 Workflows: {len(self.workflows)}")
            print(f"📋 Templates: {len(self.templates)}")
            
        except Exception as e:
            print(f"❌ Failed to initialize BMAD Core: {str(e)}")
            raise
    
    async def _load_ecosystem_config(self):
        """Load Gil's ecosystem BMAD configuration"""
        if self.ecosystem_config_path.exists():
            with open(self.ecosystem_config_path, 'r') as f:
                self.ecosystem_config = yaml.safe_load(f)
            print(f"📋 Loaded ecosystem config: {self.ecosystem_config.get('name', 'unknown')}")
        else:
            print("⚠️ Ecosystem config not found, using defaults")
            self.ecosystem_config = {}
    
    async def _load_core_config(self):
        """Load BMAD core configuration"""
        config_path = self.bmad_core_path / "core-config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            # Use ecosystem config as fallback with defaults
            self.config = {
                "name": self.ecosystem_config.get("name", "BMAD Core"),
                "version": self.ecosystem_config.get("bmad_version", "4.40.1"),
                "description": "Business Method for Agile Development - Gil's Ecosystem",
                "ecosystem_integration": True
            }
    
    async def _load_ecosystem_agents(self):
        """Load Gil's custom agents from ecosystem config"""
        if not self.ecosystem_config:
            return
            
        # Load BMAD agents configuration
        bmad_agents = self.ecosystem_config.get("bmad_agents", {})
        for agent_id, agent_config in bmad_agents.items():
            self.custom_agents[agent_id] = {
                "id": agent_id,
                "name": agent_config.get("role", agent_id.upper()),
                "handler": agent_config.get("handler", "unknown"),
                "role": agent_config.get("role", "Specialist"),
                "responsibilities": agent_config.get("responsibilities", []),
                "outputs": agent_config.get("outputs", []),
                "status": "available",
                "ecosystem_agent": True
            }
        
        # Load command references for custom agents
        command_refs = self.ecosystem_config.get("command_reference", {})
        for agent_handler, command_info in command_refs.items():
            # Find corresponding agent
            for agent in self.custom_agents.values():
                if agent["handler"] == agent_handler:
                    agent["cli_command"] = command_info.get("cli", "")
                    agent["description"] = command_info.get("description", "")
                    break
    
    async def _load_agents(self):
        """Load available BMAD agents"""
        agents_path = self.bmad_core_path / "agents"
        if agents_path.exists():
            for agent_file in agents_path.glob("*.md"):
                agent_name = agent_file.stem
                with open(agent_file, 'r') as f:
                    content = f.read()
                    
                self.agents[agent_name] = {
                    "name": agent_name.upper().replace('-', ' '),
                    "file": str(agent_file),
                    "content": content,
                    "status": "available",
                    "capabilities": self._extract_capabilities(content)
                }
    
    async def _load_workflows(self):
        """Load available BMAD workflows"""
        workflows_path = self.bmad_core_path / "workflows"
        if workflows_path.exists():
            for workflow_file in workflows_path.glob("*.yaml"):
                workflow_name = workflow_file.stem
                with open(workflow_file, 'r') as f:
                    workflow_config = yaml.safe_load(f)
                
                self.workflows[workflow_name] = {
                    "name": workflow_name.replace('-', ' ').title(),
                    "config": workflow_config,
                    "file": str(workflow_file),
                    "type": self._determine_workflow_type(workflow_name)
                }
    
    async def _load_templates(self):
        """Load BMAD templates"""
        templates_path = self.bmad_core_path / "templates"
        if templates_path.exists():
            for template_file in templates_path.glob("*.yaml"):
                template_name = template_file.stem
                with open(template_file, 'r') as f:
                    template_config = yaml.safe_load(f)
                
                self.templates[template_name] = {
                    "name": template_name.replace('-tmpl', '').replace('-', ' ').title(),
                    "config": template_config,
                    "file": str(template_file),
                    "category": self._determine_template_category(template_name)
                }
    
    async def _setup_ecosystem_integration(self):
        """Setup integration with Gil's dev ecosystem"""
        # Check for ecosystem-specific configurations
        ecosystem_bmad_config = self.ecosystem_root / "agents" / "bmad_integration" / "bmad_agent_integration.py"
        if ecosystem_bmad_config.exists():
            self.config["ecosystem_integration"] = True
            self.config["ecosystem_path"] = str(self.ecosystem_root)
        
        # Setup project templates path
        templates_path = self.ecosystem_root / "infrastructure" / "templates"
        if templates_path.exists():
            self.config["ecosystem_templates"] = str(templates_path)
    
    def _extract_capabilities(self, content: str) -> List[str]:
        """Extract agent capabilities from markdown content"""
        capabilities = []
        lines = content.split('\n')
        
        for line in lines:
            if 'capability' in line.lower() or 'can:' in line.lower():
                capabilities.append(line.strip())
        
        if not capabilities:
            # Default capabilities based on common patterns
            if 'pm' in content.lower():
                capabilities = ["project management", "coordination", "planning"]
            elif 'architect' in content.lower():
                capabilities = ["system design", "architecture", "technical planning"]
            elif 'dev' in content.lower():
                capabilities = ["code development", "implementation", "debugging"]
            elif 'qa' in content.lower():
                capabilities = ["testing", "quality assurance", "validation"]
        
        return capabilities[:5]  # Limit to 5 capabilities
    
    def _determine_workflow_type(self, workflow_name: str) -> str:
        """Determine workflow type from name"""
        if 'greenfield' in workflow_name:
            return 'new_project'
        elif 'brownfield' in workflow_name:
            return 'existing_project'
        elif 'fullstack' in workflow_name:
            return 'full_stack'
        elif 'ui' in workflow_name:
            return 'frontend'
        elif 'service' in workflow_name:
            return 'backend'
        else:
            return 'general'
    
    def _determine_template_category(self, template_name: str) -> str:
        """Determine template category"""
        if 'prd' in template_name:
            return 'requirements'
        elif 'architecture' in template_name:
            return 'architecture'
        elif 'story' in template_name:
            return 'user_stories'
        elif 'qa' in template_name:
            return 'quality'
        else:
            return 'general'
    
    async def get_status(self) -> str:
        """Get BMAD core status"""
        return "integrated" if self.config else "not_available"
    
    async def get_version(self) -> str:
        """Get BMAD core version"""
        return self.config.get("version", "unknown")
    
    async def get_available_agents(self) -> List[Dict]:
        """Get list of available agents"""
        return [
            {
                "id": agent_id,
                "name": agent["name"],
                "capabilities": agent["capabilities"],
                "status": agent["status"]
            }
            for agent_id, agent in self.agents.items()
        ]
    
    async def get_available_workflows(self) -> List[Dict]:
        """Get list of available workflows"""
        return [
            {
                "id": workflow_id,
                "name": workflow["name"],
                "type": workflow["type"],
                "description": workflow["config"].get("description", ""),
                "steps": len(workflow["config"].get("steps", []))
            }
            for workflow_id, workflow in self.workflows.items()
        ]
    
    async def get_project_templates(self) -> List[Dict]:
        """Get available project templates"""
        return [
            {
                "id": template_id,
                "name": template["name"],
                "category": template["category"],
                "description": template["config"].get("description", "")
            }
            for template_id, template in self.templates.items()
        ]
    
    async def initialize_project(self, project_id: str, config: Dict) -> Dict:
        """Initialize a new project with BMAD methodology"""
        try:
            # Determine appropriate workflow based on project config
            project_type = config.get("type", "greenfield-fullstack")
            workflow_name = self._map_project_type_to_workflow(project_type)
            
            if workflow_name not in self.workflows:
                # Fallback to default workflow
                workflow_name = "greenfield-fullstack"
            
            workflow_config = self.workflows[workflow_name]["config"].copy()
            
            # Customize workflow for project
            workflow_config["project_id"] = project_id
            workflow_config["project_config"] = config
            workflow_config["agents_assigned"] = self._assign_agents(config)
            
            return {
                "success": True,
                "workflow": workflow_name,
                "config": workflow_config
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_workflow_config(self, project_id: str) -> Dict:
        """Get workflow configuration for a project"""
        # This would be stored/retrieved from database in production
        # For now, return a default configuration
        return {
            "steps": [
                {
                    "id": "planning",
                    "name": "MISSION PLANNING",
                    "description": "Requirements analysis and project scope definition",
                    "agents": ["pm", "architect"],
                    "estimated_duration": "2-4 minutes",
                    "outputs": ["requirements.md", "project_brief.md"]
                },
                {
                    "id": "architecture", 
                    "name": "SYSTEM ARCHITECTURE",
                    "description": "Technical design and infrastructure planning",
                    "agents": ["architect", "dev"],
                    "estimated_duration": "3-6 minutes", 
                    "outputs": ["architecture.md", "api_spec.yaml"]
                },
                {
                    "id": "development",
                    "name": "CODE DEPLOYMENT", 
                    "description": "Implementation of core functionality",
                    "agents": ["dev", "architect"],
                    "estimated_duration": "8-15 minutes",
                    "outputs": ["source_code", "config_files"]
                },
                {
                    "id": "testing",
                    "name": "QUALITY VALIDATION",
                    "description": "Testing and performance optimization",
                    "agents": ["qa", "dev"], 
                    "estimated_duration": "4-8 minutes",
                    "outputs": ["test_results.md", "quality_report.md"]
                },
                {
                    "id": "deployment",
                    "name": "MISSION DEPLOYMENT",
                    "description": "Final deployment and system activation", 
                    "agents": ["pm", "dev", "qa"],
                    "estimated_duration": "2-3 minutes",
                    "outputs": ["deployment_log.md", "system_status.md"]
                }
            ],
            "agents": [
                {
                    "id": "pm",
                    "name": "PROJECT MANAGER", 
                    "role": "Mission Coordinator",
                    "status": "idle"
                },
                {
                    "id": "architect",
                    "name": "SYSTEM ARCHITECT",
                    "role": "Infrastructure Designer", 
                    "status": "idle"
                },
                {
                    "id": "dev", 
                    "name": "CORE DEVELOPER",
                    "role": "Code Implementation Specialist",
                    "status": "idle"
                },
                {
                    "id": "qa",
                    "name": "QUALITY ASSURANCE",
                    "role": "Testing and Validation Unit",
                    "status": "idle"
                }
            ]
        }
    
    async def execute_step(self, project_id: str, step: Dict) -> Dict:
        """Execute a workflow step"""
        # Simulate step execution with BMAD core
        step_id = step.get("id", "unknown")
        
        # This would interface with actual BMAD core execution
        result = {
            "step_id": step_id,
            "status": "completed",
            "duration": f"{step.get('estimated_duration', '1-2 minutes')}",
            "outputs": step.get("outputs", []),
            "agents_used": step.get("agents", []),
            "timestamp": datetime.now().isoformat(),
            "logs": [
                f"Step {step_id} initiated",
                f"Agents deployed: {', '.join(step.get('agents', []))}",
                f"Processing {step.get('description', '')}",
                f"Step {step_id} completed successfully"
            ]
        }
        
        return result
    
    async def get_project_result(self, project_id: str) -> Dict:
        """Get final project result"""
        return {
            "project_id": project_id,
            "status": "completed",
            "completion_time": datetime.now().isoformat(),
            "artifacts_generated": [
                "Project Requirements Document",
                "Technical Architecture",
                "Source Code Implementation", 
                "Quality Assurance Report",
                "Deployment Configuration"
            ],
            "metrics": {
                "total_steps": 5,
                "successful_steps": 5,
                "agents_deployed": 4,
                "execution_time": "15-30 minutes"
            }
        }
    
    def _map_project_type_to_workflow(self, project_type: str) -> str:
        """Map project type to appropriate workflow"""
        mapping = {
            "greenfield-fullstack": "greenfield-fullstack",
            "brownfield-fullstack": "brownfield-fullstack", 
            "greenfield-ui": "greenfield-ui",
            "brownfield-ui": "brownfield-ui"
        }
        return mapping.get(project_type, "greenfield-fullstack")
    
    def _assign_agents(self, config: Dict) -> List[str]:
        """Assign appropriate agents based on project config"""
        team = config.get("agentTeam", "team-fullstack")
        
        team_mapping = {
            "team-fullstack": ["pm", "architect", "dev", "qa"],
            "team-frontend": ["pm", "dev", "qa"],
            "team-backend": ["pm", "architect", "dev", "qa"], 
            "team-minimal": ["pm", "dev"]
        }
        
        return team_mapping.get(team, ["pm", "architect", "dev", "qa"])
    
    async def cleanup(self):
        """Cleanup resources"""
        # Cleanup any resources if needed
        pass