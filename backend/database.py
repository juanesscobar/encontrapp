from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=True)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://juan:encontrapp123@localhost:5432/encontrapp")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        from backend.models import categoria, usuario, proveedor, resena  # noqa: F401
        await conn.run_sync(Base.metadata.create_all)
    print("Base de datos inicializada.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())
