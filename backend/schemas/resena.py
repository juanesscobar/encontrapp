from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class ResenaCreate(BaseModel):
    proveedor_id: int
    rating: int
    comentario: Optional[str] = None

    @field_validator("rating")
    @classmethod
    def rating_valido(cls, v: int) -> int:
        if not 1 <= v <= 5:
            raise ValueError("El rating debe estar entre 1 y 5")
        return v


class ResenaOut(BaseModel):
    id: int
    proveedor_id: int
    usuario_id: int
    rating: int
    comentario: Optional[str]
    fecha: datetime

    model_config = {"from_attributes": True}
