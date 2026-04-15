from pydantic import BaseModel
from typing import Optional


class ProveedorCreate(BaseModel):
    nombre_negocio: str
    descripcion: Optional[str] = None
    categoria_id: int
    lat: float
    lng: float
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    whatsapp: Optional[str] = None


class ProveedorUpdate(BaseModel):
    nombre_negocio: Optional[str] = None
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    whatsapp: Optional[str] = None
    activo: Optional[bool] = None


class ProveedorOut(BaseModel):
    id: int
    usuario_id: int
    nombre_negocio: str
    descripcion: Optional[str]
    categoria_id: int
    categoria_nombre: Optional[str] = None
    categoria_emoji: Optional[str] = None
    lat: float
    lng: float
    direccion: Optional[str]
    telefono: Optional[str]
    whatsapp: Optional[str]
    activo: bool
    rating_promedio: float
    total_resenas: int
    distancia_metros: Optional[float] = None

    model_config = {"from_attributes": True}
