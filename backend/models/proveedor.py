from sqlalchemy import Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry
from backend.database import Base


class Proveedor(Base):
    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nombre_negocio: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(1000), nullable=True)
    categoria_id: Mapped[int] = mapped_column(Integer, ForeignKey("categorias.id"), nullable=False)
    geom = mapped_column(Geometry("POINT", srid=4326), nullable=False)
    direccion: Mapped[str] = mapped_column(String(300), nullable=True)
    telefono: Mapped[str] = mapped_column(String(30), nullable=True)
    whatsapp: Mapped[str] = mapped_column(String(30), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    rating_promedio: Mapped[float] = mapped_column(Float, default=0.0)
    total_resenas: Mapped[int] = mapped_column(Integer, default=0)

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="proveedor")
    categoria: Mapped["Categoria"] = relationship("Categoria", back_populates="proveedores")
    resenas: Mapped[list["Resena"]] = relationship("Resena", back_populates="proveedor")
