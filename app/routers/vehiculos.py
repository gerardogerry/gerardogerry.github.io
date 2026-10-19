from fastapi import APIRouter, HTTPException, status
from typing import List
from app.services.vehiculo_service import VehiculoService
from app.models.vehiculo import MovimientoRequest, EstadoUpdate
from app.services.websocket_manager import manager  # <--- Importar el manager

router = APIRouter(
    prefix="/api/v1/vehiculos",
    tags=["Vehículos y Comandos"]
)

# ==========================================
# ENDPOINTS GET
# ==========================================
@router.get("", summary="Obtener todos los vehículos")
def listar_vehiculos():
    return VehiculoService.obtener_vehiculos()

@router.get("/{vehiculo_id}", summary="Obtener vehículo por ID")
def obtener_vehiculo(vehiculo_id: int):
    vehiculo = VehiculoService.obtener_vehiculo_por_id(vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo

@router.get("/comandos/lista", summary="Obtener catálogo de comandos")
def listar_comandos():
    return VehiculoService.obtener_comandos()

@router.get("/{vehiculo_id}/estado", summary="Obtener el último estado del vehículo")
def obtener_ultimo_estado(vehiculo_id: int):
    estado = VehiculoService.obtener_ultimo_estado(vehiculo_id)
    if not estado:
        raise HTTPException(status_code=404, detail="No se encontró estado para este vehículo")
    return estado

@router.get("/{vehiculo_id}/historial", summary="Obtener el historial reciente (máximo 10)")
def obtener_historial_reciente(vehiculo_id: int):
    """Retorna los 10 movimientos individuales más recientes en orden descendente."""
    historial = VehiculoService.obtener_historial_reciente(vehiculo_id, limite=10)
    return historial

# ==========================================
# ENDPOINTS POST
# ==========================================
@router.post("/{vehiculo_id}/movimiento", summary="Ejecutar un movimiento individual")
async def registrar_movimiento_individual(vehiculo_id: int, request: MovimientoRequest):
    """
    Valida el vehículo y comando, actualiza el estado, guarda el registro
    en el historial y notifica por WebSocket a los clientes conectados.
    """
    # 1. Validar que el vehículo exista
    vehiculo = VehiculoService.obtener_vehiculo_por_id(vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    # 2. Validar que el comando exista
    comando = VehiculoService.obtener_comando_por_id(request.comando_id)
    if not comando:
        raise HTTPException(status_code=404, detail="Comando no válido")

    try:
        # 3. Registrar en historial y actualizar estado (transacción)
        VehiculoService.registrar_movimiento_historial(
            vehiculo_id=vehiculo_id,
            comando_id=request.comando_id,
            detalle=request.detalle
        )
        
        # Actualizamos el estado del vehículo según la instrucción del comando
        nuevo_estado = VehiculoService.actualizar_estado(
            vehiculo_id=vehiculo_id,
            estado=comando.get("instruccion", "EJECUTANDO"),
            posicion_x=0.0,
            posicion_y=0.0
        )

        # NOTIFICAR A TODOS LOS CLIENTES WSS CONECTADOS A ESTE VEHÍCULO
        await manager.broadcast_to_vehicle(vehiculo_id, {
            "event": "MOVIMIENTO_INDIVIDUAL",
            "vehiculo_id": vehiculo_id,
            "comando": comando.get("nombre"),
            "instruccion": comando.get("instruccion"),
            "detalle": request.detalle
        })

        return {
            "status": "success",
            "message": "Movimiento registrado y estado actualizado con éxito",
            "vehiculo_id": vehiculo_id,
            "comando": comando.get("nombre")
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la transacción: {str(e)}"
        )