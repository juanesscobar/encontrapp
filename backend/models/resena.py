from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from backend.database import Base


class Resena(Base):
    __tablename__ = "resenas"
    __table_args__ = (CheckConstraint("rating >= 1 AND rating <= 5", name="rating_rango"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    proveedor_id: Mapped[int] = mapped_column(Integer, ForeignKey("proveedores.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comentario: Mapped[str] = mapped_column(String(1000), nullable=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    proveedor: Mapped["Proveedor"] = relationship("Proveedor", back_populates="resenas")
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="resenas")
