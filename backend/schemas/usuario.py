from pydantic import BaseModel, EmailStr
from datetime import datetime


class UsuarioRegistro(BaseModel):
    nombre: str
    email: EmailStr
    password: str


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    es_proveedor: bool
    fecha_registro: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
