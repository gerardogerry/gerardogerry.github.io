from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routers import vehiculos, demo
from app.services.websocket_manager import manager
from app.services.vehiculo_service import VehiculoService

app = FastAPI(
    title="API Vehículo IoT - Examen 2.6",
    description="API pública para control de vehículo IoT con Amazon RDS y WebSocket",
    version="1.0.0"
)

# Configurar CORS para acceso desde clientes externos (Thunder Client / Swagger)
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
    # Obtener el último estado guardado para enviarlo al conectar
    ultimo_estado = VehiculoService.obtener_ultimo_estado(vehiculo_id) or {}
    await manager.connect(websocket, vehiculo_id, ultimo_estado)
    try:
        while True:
            # Mantener la conexión escuchando
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, vehiculo_id)

@app.get("/", tags=["Root"])
def root():
    return {"message": "API Vehículo IoT operando correctamente"}