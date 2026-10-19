import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.vehiculo_service import VehiculoService
from app.services.websocket_manager import manager

router = APIRouter(
    prefix="/api/v1/vehiculos",
    tags=["DEMO y WebSocket"]
)

async def ejecutar_secuencia_demo(vehiculo_id: int, demo_id: int):
    """Tarea en segundo plano que ejecuta y transmite la DEMO temporizada."""
    try:
        manager.set_demo_running(vehiculo_id, True)
        movimientos = VehiculoService.obtener_movimientos_demo(demo_id)
        
        # 1. Notificar inicio de la DEMO
        await manager.broadcast_to_vehicle(vehiculo_id, {
            "event": "DEMO_INICIO",
            "vehiculo_id": vehiculo_id,
            "demo_id": demo_id,
            "total_pasos": len(movimientos)
        })

        # 2. Transmitir los N pasos respetando duraciones y pausas
        for paso in movimientos:
            if not manager.is_demo_running(vehiculo_id):
                # Si fue cancelada la DEMO
                await manager.broadcast_to_vehicle(vehiculo_id, {
                    "event": "DEMO_CANCELADA",
                    "vehiculo_id": vehiculo_id
                })
                break

            comando_id = paso.get("comando_id")
            duracion_ms = paso.get("duracion_ms", 1000)
            pausa_ms = paso.get("pausa_ms", 500)
            comando_info = VehiculoService.obtener_comando_por_id(comando_id)
            instruccion = comando_info.get("instruccion", "EJECUTANDO_DEMO") if comando_info else "DEMO"

            # Actualizar último estado en RDS (Sin registrar en el historial)
            VehiculoService.actualizar_estado(
                vehiculo_id=vehiculo_id,
                estado=instruccion,
                posicion_x=0.0,
                posicion_y=0.0
            )

            # Notificar paso por WebSocket
            await manager.broadcast_to_vehicle(vehiculo_id, {
                "event": "DEMO_PASO",
                "vehiculo_id": vehiculo_id,
                "orden": paso.get("orden"),
                "instruccion": instruccion,
                "duracion_ms": duracion_ms
            })

            # Esperar la duración del movimiento y la pausa
            await asyncio.sleep(duracion_ms / 1000.0)
            await asyncio.sleep(pausa_ms / 1000.0)

        # 3. Notificar finalización de la DEMO
        await manager.broadcast_to_vehicle(vehiculo_id, {
            "event": "DEMO_FIN",
            "vehiculo_id": vehiculo_id
        })
    finally:
        manager.set_demo_running(vehiculo_id, False)

@router.post("/{vehiculo_id}/demo/{demo_id}/iniciar", summary="Iniciar ejecución de una DEMO")
async def iniciar_demo(vehiculo_id: int, demo_id: int, background_tasks: BackgroundTasks):
    """Inicia la DEMO temporizada si no hay otra en ejecución para este vehículo."""
    # Validar vehículo
    vehiculo = VehiculoService.obtener_vehiculo_por_id(vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    # Validar DEMO
    demo = VehiculoService.obtener_demo_por_id(demo_id)
    if not demo:
        raise HTTPException(status_code=404, detail="DEMO no encontrada")

    # Control de simultaneidad
    if manager.is_demo_running(vehiculo_id):
        raise HTTPException(status_code=400, detail="Ya existe una DEMO en ejecución para este vehículo")

    # Ejecutar en segundo plano
    background_tasks.add_task(ejecutar_secuencia_demo, vehiculo_id, demo_id)

    return {
        "status": "success",
        "message": f"DEMO {demo_id} iniciada para el vehículo {vehiculo_id}"
    }

@router.post("/{vehiculo_id}/demo/cancelar", summary="Cancelar ejecución de DEMO")
async def cancelar_demo(vehiculo_id: int):
    if not manager.is_demo_running(vehiculo_id):
        raise HTTPException(status_code=400, detail="No hay ninguna DEMO en curso para este vehículo")
    
    manager.set_demo_running(vehiculo_id, False)
    return {"status": "success", "message": "Solicitud de cancelación enviada"}