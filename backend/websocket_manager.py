"""
WebSocket Connection Manager for real-time updates
Handles client connections and broadcasts for BMAD UI
"""

import json
from typing import List, Dict, Set
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    """Manages WebSocket connections and real-time communication"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.project_subscriptions: Dict[str, Set[WebSocket]] = {}
        self.connection_metadata: Dict[WebSocket, Dict] = {}
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_metadata[websocket] = {
            "connected_at": self._get_timestamp(),
            "subscriptions": set()
        }
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connection_established",
            "message": "Connected to BMAD UI real-time system",
            "timestamp": self._get_timestamp()
        }, websocket)
        
        print(f"🔌 New WebSocket connection established. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        # Clean up subscriptions
        if websocket in self.connection_metadata:
            subscriptions = self.connection_metadata[websocket].get("subscriptions", set())
            for project_id in subscriptions:
                if project_id in self.project_subscriptions:
                    self.project_subscriptions[project_id].discard(websocket)
                    if not self.project_subscriptions[project_id]:
                        del self.project_subscriptions[project_id]
            
            del self.connection_metadata[websocket]
        
        print(f"🔌 WebSocket connection closed. Remaining: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific WebSocket connection"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            print(f"❌ Failed to send personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            return
        
        message_str = json.dumps(message)
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message_str)
            except Exception as e:
                print(f"❌ Failed to broadcast to connection: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
        
        print(f"📡 Broadcast sent to {len(self.active_connections)} clients")
    
    async def broadcast_to_project(self, project_id: str, message: dict):
        """Broadcast message to clients subscribed to specific project"""
        if project_id not in self.project_subscriptions:
            return
        
        message_str = json.dumps(message)
        disconnected = []
        subscribers = list(self.project_subscriptions[project_id])
        
        for connection in subscribers:
            try:
                await connection.send_text(message_str)
            except Exception as e:
                print(f"❌ Failed to send project message: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
        
        print(f"📡 Project {project_id} broadcast sent to {len(subscribers)} subscribers")
    
    async def subscribe_to_project(self, websocket: WebSocket, project_id: str):
        """Subscribe WebSocket to project updates"""
        if project_id not in self.project_subscriptions:
            self.project_subscriptions[project_id] = set()
        
        self.project_subscriptions[project_id].add(websocket)
        
        if websocket in self.connection_metadata:
            self.connection_metadata[websocket]["subscriptions"].add(project_id)
        
        await self.send_personal_message({
            "type": "subscription_confirmed",
            "project_id": project_id,
            "message": f"Subscribed to project {project_id} updates"
        }, websocket)
        
        print(f"📝 WebSocket subscribed to project {project_id}")
    
    async def unsubscribe_from_project(self, websocket: WebSocket, project_id: str):
        """Unsubscribe WebSocket from project updates"""
        if project_id in self.project_subscriptions:
            self.project_subscriptions[project_id].discard(websocket)
            if not self.project_subscriptions[project_id]:
                del self.project_subscriptions[project_id]
        
        if websocket in self.connection_metadata:
            self.connection_metadata[websocket]["subscriptions"].discard(project_id)
        
        await self.send_personal_message({
            "type": "subscription_removed", 
            "project_id": project_id,
            "message": f"Unsubscribed from project {project_id} updates"
        }, websocket)
    
    async def disconnect_all(self):
        """Disconnect all WebSocket connections"""
        disconnected = []
        for connection in self.active_connections.copy():
            try:
                await connection.close()
                disconnected.append(connection)
            except Exception as e:
                print(f"❌ Error closing connection: {e}")
        
        for connection in disconnected:
            self.disconnect(connection)
        
        print(f"🔌 All WebSocket connections closed: {len(disconnected)}")
    
    def get_connection_stats(self) -> Dict:
        """Get connection statistics"""
        return {
            "total_connections": len(self.active_connections),
            "project_subscriptions": len(self.project_subscriptions),
            "subscriptions_detail": {
                project_id: len(connections) 
                for project_id, connections in self.project_subscriptions.items()
            }
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()