from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

from backend.database import AsyncSessionLocal
from backend.deps import get_db, get_current_user
from backend.models.usuario import Usuario
from backend.schemas.usuario import UsuarioRegistro, UsuarioLogin, UsuarioOut, Token

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"), override=True)

SECRET_KEY = os.getenv("SECRET_KEY", "insecure-default")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", "7"))

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/auth", tags=["auth"])


def _hash(password: str) -> str:
    return pwd_ctx.hash(password)


def _verify(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)


def _create_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    return jwt.encode({"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/registro", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
async def registro(data: UsuarioRegistro, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Usuario).where(Usuario.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    user = Usuario(nombre=data.nombre, email=data.email, password_hash=_hash(data.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=Token)
async def login(data: UsuarioLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.email == data.email))
    user = result.scalar_one_or_none()
    if not user or not _verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    if not user.activo:
        raise HTTPException(status_code=403, detail="Cuenta desactivada")
    return Token(access_token=_create_token(user.id))


@router.get("/me", response_model=UsuarioOut)
async def me(current_user: Usuario = Depends(get_current_user)):
    return current_user
