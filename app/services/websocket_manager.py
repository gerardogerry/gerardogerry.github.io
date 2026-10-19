import asyncio
from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    """Administrador de conexiones WebSocket canalizadas por vehiculo_id."""
    
    def __init__(self):
        # Mapea vehiculo_id -> Lista de websockets activos
        self.active_connections: Dict[int, List[WebSocket]] = {}
        # Controla si hay una DEMO en ejecución por vehículo
        self.demo_in_progress: Dict[int, bool] = {}

    async def connect(self, websocket: WebSocket, vehiculo_id: int, initial_state: dict):
        """Acepta la conexión WSS y envía de inmediato el último estado guardado en RDS."""
        await websocket.accept()
        if vehiculo_id not in self.active_connections:
            self.active_connections[vehiculo_id] = []
        self.active_connections[vehiculo_id].append(websocket)
        
        # Enviar el estado inicial recién conectado
        await websocket.send_json({
            "event": "INITIAL_STATE",
            "vehiculo_id": vehiculo_id,
            "data": initial_state
        })

    def disconnect(self, websocket: WebSocket, vehiculo_id: int):
        """Remueve una conexión cerrada."""
        if vehiculo_id in self.active_connections:
            if websocket in self.active_connections[vehiculo_id]:
                self.active_connections[vehiculo_id].remove(websocket)
            if not self.active_connections[vehiculo_id]:
                del self.active_connections[vehiculo_id]

    async def broadcast_to_vehicle(self, vehiculo_id: int, message: dict):
        """Transmite un mensaje JSON únicamente a los clientes conectados a un vehículo."""
        if vehiculo_id in self.active_connections:
            for connection in self.active_connections[vehiculo_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

    def is_demo_running(self, vehiculo_id: int) -> bool:
        return self.demo_in_progress.get(vehiculo_id, False)

    def set_demo_running(self, vehiculo_id: int, running: bool):
        self.demo_in_progress[vehiculo_id] = running

manager = ConnectionManager()