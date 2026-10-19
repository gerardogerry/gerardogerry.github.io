from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import vehiculos

app = FastAPI(
    title="API Vehículo IoT - Examen 2.6",
    description="API pública para control de vehículo IoT con Amazon RDS y FastAPI",
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

# Incluir routers HTTP
app.include_router(vehiculos.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "API Vehículo IoT operando correctamente"}