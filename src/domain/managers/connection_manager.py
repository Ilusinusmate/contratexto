from fastapi import WebSocket
from typing import Dict
from uuid import uuid4

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> str:
        await websocket.accept()
        connection_id = str(uuid4())
        self.active_connections[connection_id] = websocket
        return connection_id

    def disconnect(self, connection_id: str):
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]

    async def send_personal_json(self, message: dict, connection_id: str):
        if connection_id in self.active_connections:
            websocket = self.active_connections[connection_id]
            try:
                await websocket.send_json(message)
            except:
                await self.disconnect(connection_id)

    async def broadcast(self, message: dict):
        for connection_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except:
                self.disconnect(connection_id)
    