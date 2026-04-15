from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from backend.deps import get_db, get_current_user
from backend.models.usuario import Usuario
from backend.models.proveedor import Proveedor
from backend.schemas.proveedor import ProveedorCreate, ProveedorUpdate, ProveedorOut

router = APIRouter(prefix="/proveedores", tags=["proveedores"])


@router.get("/{proveedor_id}", response_model=ProveedorOut)
async def get_proveedor(proveedor_id: int, db: AsyncSession = Depends(get_db)):
    sql = text("""
        SELECT
            p.id, p.usuario_id, p.nombre_negocio, p.descripcion, p.categoria_id,
            c.nombre AS categoria_nombre, c.emoji AS categoria_emoji,
            ST_Y(p.geom::geometry) AS lat,
            ST_X(p.geom::geometry) AS lng,
            p.direccion, p.telefono, p.whatsapp, p.activo,
            p.rating_promedio, p.total_resenas,
            NULL::float AS distancia_metros
        FROM proveedores p
        JOIN categorias c ON p.categoria_id = c.id
        WHERE p.id = :id
    """)
    result = await db.execute(sql, {"id": proveedor_id})
    row = result.mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return ProveedorOut(**dict(row))


@router.post("", response_model=ProveedorOut, status_code=status.HTTP_201_CREATED)
async def crear_proveedor(
    data: ProveedorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    existing = await db.execute(select(Proveedor).where(Proveedor.usuario_id == current_user.id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Ya tenés un perfil de proveedor")

    sql = text("""
        INSERT INTO proveedores
            (usuario_id, nombre_negocio, descripcion, categoria_id, geom, direccion, telefono, whatsapp)
        VALUES
            (:uid, :nombre, :desc, :cat_id, ST_MakePoint(:lng, :lat), :dir, :tel, :wa)
        RETURNING id
    """)
    result = await db.execute(sql, {
        "uid": current_user.id,
        "nombre": data.nombre_negocio,
        "desc": data.descripcion,
        "cat_id": data.categoria_id,
        "lat": data.lat,
        "lng": data.lng,
        "dir": data.direccion,
        "tel": data.telefono,
        "wa": data.whatsapp,
    })
    new_id = result.scalar_one()

    current_user.es_proveedor = True
    await db.commit()

    return await get_proveedor(new_id, db)


@router.put("/{proveedor_id}", response_model=ProveedorOut)
async def actualizar_proveedor(
    proveedor_id: int,
    data: ProveedorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    result = await db.execute(select(Proveedor).where(Proveedor.id == proveedor_id))
    proveedor = result.scalar_one_or_none()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    if proveedor.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tenés permiso para editar este perfil")

    updates = data.model_dump(exclude_unset=True)
    lat = updates.pop("lat", None)
    lng = updates.pop("lng", None)

    for field, value in updates.items():
        setattr(proveedor, field, value)

    if lat is not None and lng is not None:
        await db.execute(
            text("UPDATE proveedores SET geom = ST_MakePoint(:lng, :lat) WHERE id = :id"),
            {"lng": lng, "lat": lat, "id": proveedor_id},
        )

    await db.commit()
    return await get_proveedor(proveedor_id, db)
