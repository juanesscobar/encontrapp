# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is encontrapp?

Marketplace hiperlocal que conecta personas con servicios y productos dentro de un radio configurable. El usuario define su ubicación y radio (ej: 5 km) y el mapa muestra proveedores ordenados de más cercano a más lejano.

## Commands

```bash
# Levantar solo la base de datos
docker-compose up -d db

# Levantar todo
docker-compose up -d

# Instalar dependencias Python
pip install -r backend/requirements.txt

# Inicializar tablas (crea extensión PostGIS + tablas)
python backend/database.py

# Cargar datos de prueba
python backend/seed.py

# Levantar servidor de desarrollo
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Verificar API
# Docs interactivos: http://localhost:8000/docs
# Test búsqueda:    http://localhost:8000/buscar?lat=-25.5116&lng=-54.6105&radio=5
```

## Architecture

### Request flow

```
frontend/encontrapp_v2.html  (Leaflet.js + fetch API)
        ↓ HTTP
backend/main.py              (FastAPI app, monta routers, configura CORS)
        ↓
backend/routers/             (un archivo por dominio)
        ↓
backend/services/geo.py      (lógica geoespacial, llamadas a Nominatim)
        ↓
backend/database.py          (AsyncSession via asyncpg)
        ↓
PostgreSQL 16 + PostGIS 3.4
```

### Key design rules

- **Todo async**: SQLAlchemy 2.0 async + asyncpg. Nunca usar sesiones síncronas.
- **Geometría**: campo `geom` usa `Geometry('POINT', srid=4326)`. Insertar con `ST_MakePoint(lng, lat)` — primero lng, luego lat.
- **Auth**: JWT Bearer token via `python-jose`. Rutas protegidas dependen de `deps.py::get_current_user`.
- **CORS**: habilitado para `localhost:5500`, `127.0.0.1:5500`, `localhost:3000`.

### Core geospatial query (buscar endpoint)

```sql
SELECT p.*, c.nombre, c.emoji,
  ST_Y(p.geom::geometry) AS lat,
  ST_X(p.geom::geometry) AS lng,
  ST_Distance(p.geom::geography, ST_MakePoint(:lng, :lat)::geography) AS distancia_metros
FROM proveedores p
JOIN categorias c ON p.categoria_id = c.id
WHERE ST_DWithin(p.geom::geography, ST_MakePoint(:lng, :lat)::geography, :radio_metros)
  AND (:categoria IS NULL OR c.slug = :categoria)
  AND p.activo = true
ORDER BY distancia_metros ASC;
```

### Data models

| Modelo     | Campos clave |
|------------|-------------|
| Usuario    | id, nombre, email, password_hash, es_proveedor, activo |
| Proveedor  | id, usuario_id (FK), nombre_negocio, categoria_id (FK), geom (PostGIS Point), telefono, whatsapp, rating_promedio, total_resenas, activo |
| Categoria  | id, nombre, emoji, slug |
| Resena     | id, proveedor_id (FK), usuario_id (FK), rating (1-5), comentario, fecha |

### Environment variables (backend/.env)

```
DATABASE_URL=postgresql+asyncpg://juan:encontrapp123@localhost:5432/encontrapp
SECRET_KEY=<clave larga aleatoria>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=7
NOMINATIM_USER_AGENT=encontrapp/1.0
```

### API endpoints

| Método | Ruta | Auth |
|--------|------|------|
| GET | `/buscar?lat=&lng=&radio=&categoria=` | No |
| GET | `/categorias` | No |
| GET | `/proveedores/{id}` | No |
| POST | `/auth/registro` | No |
| POST | `/auth/login` | No |
| POST | `/proveedores` | Bearer |
| PUT | `/proveedores/{id}` | Bearer |
| POST | `/resenas` | Bearer |
| GET | `/me` | Bearer |

## Development order (for building from scratch)

1. `docker-compose.yml`
2. `backend/requirements.txt` + `backend/.env.example`
3. `backend/database.py` — init_db() crea extensión PostGIS + tablas
4. `backend/models/` — orden: categoria → usuario → proveedor → resena
5. `backend/schemas/` — espeja los modelos con Pydantic v2
6. `backend/deps.py` — get_db(), get_current_user()
7. `backend/routers/auth.py` → `buscar.py` → `proveedores.py` → `resenas.py`
8. `backend/main.py` — monta todos los routers
9. `backend/seed.py` — 10+ proveedores alrededor de lat=-25.5116, lng=-54.6105

## Frontend

`frontend/encontrapp_v2.html` es un single-file app (HTML+CSS+JS). No modificar salvo que se pida explícitamente. Usa Leaflet.js con tiles de CartoDB y llama al backend vía fetch.
