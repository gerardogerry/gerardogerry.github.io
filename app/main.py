from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse # <-- AGREGADO
from app.routers import vehiculos, demo
from app.services.websocket_manager import manager
from app.services.vehiculo_service import VehiculoService

app = FastAPI(
    title="API Vehículo IoT - Examen 2.6",
    description="API pública para control de vehículo IoT con Amazon RDS y WebSocket",
    version="1.0.0"
)

# Configurar CORS para acceso desde clientes externos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers HTTP y de la DEMO
app.include_router(vehiculos.router)
app.include_router(demo.router)

# ==========================================
# ENDPOINT WEBSOCKET POR VEHÍCULO
# ==========================================
@app.websocket("/ws/vehiculos/{vehiculo_id}")
async def websocket_endpoint(websocket: WebSocket, vehiculo_id: int):
    ultimo_estado = VehiculoService.obtener_ultimo_estado(vehiculo_id) or {}
    await manager.connect(websocket, vehiculo_id, ultimo_estado)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, vehiculo_id)

# Servir directamente la interfaz de usuario al entrar a http://50.19.210.179:8000/
@app.get("/", response_class=FileResponse, tags=["Root"])
def root():
    return "index.html"