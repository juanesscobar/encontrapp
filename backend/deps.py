from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

from backend.database import AsyncSessionLocal
from backend.models.usuario import Usuario

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=True)

SECRET_KEY = os.getenv("SECRET_KEY", "insecure-default")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

bearer_scheme = HTTPBearer()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> Usuario:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    result = await db.execute(select(Usuario).where(Usuario.id == user_id, Usuario.activo == True))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    return user
