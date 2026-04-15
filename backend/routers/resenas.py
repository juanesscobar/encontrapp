from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from backend.deps import get_db, get_current_user
from backend.models.usuario import Usuario
from backend.models.proveedor import Proveedor
from backend.models.resena import Resena
from backend.schemas.resena import ResenaCreate, ResenaOut

router = APIRouter(prefix="/resenas", tags=["resenas"])


@router.post("", response_model=ResenaOut, status_code=status.HTTP_201_CREATED)
async def crear_resena(
    data: ResenaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    # Verificar que el proveedor existe
    prov_result = await db.execute(select(Proveedor).where(Proveedor.id == data.proveedor_id))
    proveedor = prov_result.scalar_one_or_none()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    # Un usuario no puede reseñar su propio negocio
    if proveedor.usuario_id == current_user.id:
        raise HTTPException(status_code=400, detail="No podés reseñar tu propio negocio")

    resena = Resena(
        proveedor_id=data.proveedor_id,
        usuario_id=current_user.id,
        rating=data.rating,
        comentario=data.comentario,
    )
    db.add(resena)
    await db.flush()

    # Actualizar rating promedio y total del proveedor
    await db.execute(text("""
        UPDATE proveedores
        SET
            total_resenas = total_resenas + 1,
            rating_promedio = (
                SELECT AVG(rating) FROM resenas WHERE proveedor_id = :pid
            )
        WHERE id = :pid
    """), {"pid": data.proveedor_id})

    await db.commit()
    await db.refresh(resena)
    return resena
