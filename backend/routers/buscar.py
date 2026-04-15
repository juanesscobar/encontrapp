from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Optional, List

from backend.deps import get_db
from backend.schemas.proveedor import ProveedorOut

router = APIRouter(tags=["buscar"])


@router.get("/buscar", response_model=List[ProveedorOut])
async def buscar(
    lat: float = Query(..., description="Latitud del centro de búsqueda"),
    lng: float = Query(..., description="Longitud del centro de búsqueda"),
    radio: float = Query(5.0, description="Radio en kilómetros"),
    categoria: Optional[str] = Query(None, description="Slug de categoría"),
    db: AsyncSession = Depends(get_db),
):
    radio_metros = radio * 1000
    sql = text("""
        SELECT
            p.id,
            p.usuario_id,
            p.nombre_negocio,
            p.descripcion,
            p.categoria_id,
            c.nombre  AS categoria_nombre,
            c.emoji   AS categoria_emoji,
            ST_Y(p.geom::geometry) AS lat,
            ST_X(p.geom::geometry) AS lng,
            p.direccion,
            p.telefono,
            p.whatsapp,
            p.activo,
            p.rating_promedio,
            p.total_resenas,
            ST_Distance(
                p.geom::geography,
                ST_MakePoint(:lng, :lat)::geography
            ) AS distancia_metros
        FROM proveedores p
        JOIN categorias c ON p.categoria_id = c.id
        WHERE
            ST_DWithin(
                p.geom::geography,
                ST_MakePoint(:lng, :lat)::geography,
                :radio_metros
            )
            AND (:categoria::text IS NULL OR c.slug = :categoria::text)
            AND p.activo = true
        ORDER BY distancia_metros ASC
    """)
    result = await db.execute(sql, {"lat": lat, "lng": lng, "radio_metros": radio_metros, "categoria": categoria})
    rows = result.mappings().all()
    return [ProveedorOut(**dict(row)) for row in rows]


@router.get("/categorias")
async def categorias(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT id, nombre, emoji, slug FROM categorias ORDER BY nombre"))
    return result.mappings().all()
