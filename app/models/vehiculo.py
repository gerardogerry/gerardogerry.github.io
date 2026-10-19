from pydantic import BaseModel
from typing import Optional

class MovimientoRequest(BaseModel):
    comando_id: int
    detalle: Optional[str] = "Movimiento individual POST"

class EstadoUpdate(BaseModel):
    estado: str
    posicion_x: float
    posicion_y: float