from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    emoji: Mapped[str] = mapped_column(String(10), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    proveedores: Mapped[list["Proveedor"]] = relationship("Proveedor", back_populates="categoria")
