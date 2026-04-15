"""Carga datos de prueba en la base de datos."""
import asyncio
from sqlalchemy import text
from backend.database import engine, init_db
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

CATEGORIAS = [
    ("Electricidad", "⚡", "electricidad"),
    ("Mecánica", "🔧", "mecanica"),
    ("Gastronomía", "🍕", "gastronomia"),
    ("Belleza", "💅", "belleza"),
    ("Tecnología", "💻", "tecnologia"),
    ("Salud", "🏥", "salud"),
    ("Educación", "📚", "educacion"),
    ("Hogar", "🏠", "hogar"),
    ("Transporte", "🚗", "transporte"),
    ("Mascotas", "🐾", "mascotas"),
]

# Coordenadas base: Ciudad del Este, Paraguay
BASE_LAT = -25.5116
BASE_LNG = -54.6105

PROVEEDORES = [
    ("Carlos Electricista", "Instalaciones eléctricas residenciales y comerciales.", "electricidad", 0.002, 0.003, "Av. Monseñor Rodríguez 123", "+595971111001", "+595971111001"),
    ("Mecánica El Turco", "Servicio de mecánica general y alineación.", "mecanica", -0.005, 0.007, "Ruta 7 km 3", "+595971111002", "+595971111002"),
    ("Pizzería Don Mario", "Pizzas artesanales y empanadas.", "gastronomia", 0.008, -0.004, "Calle Curupayty 45", "+595971111003", "+595971111003"),
    ("Salón Bella Vista", "Cortes, tintes y tratamientos capilares.", "belleza", -0.003, -0.009, "Shopping del Este Local 12", "+595971111004", "+595971111004"),
    ("TecnoFix CDE", "Reparación de celulares, laptops y tablets.", "tecnologia", 0.010, 0.005, "Av. Adrian Jara 78", "+595971111005", "+595971111005"),
    ("Farmacia San José", "Medicamentos y cosméticos.", "salud", -0.007, 0.012, "Av. Bernardino Caballero 200", "+595971111006", "+595971111006"),
    ("Profe Laura — Inglés", "Clases de inglés para adultos y niños.", "educacion", 0.015, -0.006, "Barrio San Jorge", "+595971111007", "+595971111007"),
    ("HomeFix Plomería", "Plomería, pintura y reparaciones del hogar.", "hogar", -0.012, 0.001, "Barrio Obrero", "+595971111008", "+595971111008"),
    ("Remis 24h", "Traslados dentro de CDE y alrededores.", "transporte", 0.001, 0.016, "Ciudad del Este", "+595971111009", "+595971111009"),
    ("Veterinaria Patitas", "Consultas, vacunas y peluquería canina.", "mascotas", -0.009, -0.014, "Av. San Blas 567", "+595971111010", "+595971111010"),
    ("Ana Cocinera", "Almuerzo casero a domicilio, pedidos desde las 8hs.", "gastronomia", 0.018, 0.002, "Barrio San Miguel", "+595971111011", "+595971111011"),
    ("PC Soluciones", "Armado de PCs, redes y CCTV.", "tecnologia", -0.004, 0.019, "Microcentro", "+595971111012", "+595971111012"),
]


async def seed():
    await init_db()

    async with engine.begin() as conn:
        # Insertar categorías
        for nombre, emoji, slug in CATEGORIAS:
            await conn.execute(text("""
                INSERT INTO categorias (nombre, emoji, slug)
                VALUES (:nombre, :emoji, :slug)
                ON CONFLICT (slug) DO NOTHING
            """), {"nombre": nombre, "emoji": emoji, "slug": slug})

        # Crear usuario demo
        existing = await conn.execute(text("SELECT id FROM usuarios WHERE email = 'demo@encontrapp.com'"))
        row = existing.fetchone()
        if not row:
            result = await conn.execute(text("""
                INSERT INTO usuarios (nombre, email, password_hash, es_proveedor, activo)
                VALUES ('Demo Admin', 'demo@encontrapp.com', :ph, true, true)
                RETURNING id
            """), {"ph": pwd_ctx.hash("demo1234")})
            user_id = result.scalar_one()
        else:
            user_id = row[0]

        # Insertar proveedores
        for nombre_neg, desc, cat_slug, dlat, dlng, dir_, tel, wa in PROVEEDORES:
            cat_result = await conn.execute(
                text("SELECT id FROM categorias WHERE slug = :slug"), {"slug": cat_slug}
            )
            cat_id = cat_result.scalar_one()
            lat = BASE_LAT + dlat
            lng = BASE_LNG + dlng
            await conn.execute(text("""
                INSERT INTO proveedores
                    (usuario_id, nombre_negocio, descripcion, categoria_id, geom, direccion, telefono, whatsapp, activo, rating_promedio, total_resenas)
                VALUES
                    (:uid, :nombre, :desc, :cat_id, ST_MakePoint(:lng, :lat), :dir, :tel, :wa, true, 0.0, 0)
                ON CONFLICT DO NOTHING
            """), {
                "uid": user_id, "nombre": nombre_neg, "desc": desc, "cat_id": cat_id,
                "lat": lat, "lng": lng, "dir": dir_, "tel": tel, "wa": wa,
            })

    print(f"Seed completado: {len(CATEGORIAS)} categorías, {len(PROVEEDORES)} proveedores.")


if __name__ == "__main__":
    asyncio.run(seed())
