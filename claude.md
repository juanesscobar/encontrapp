\# CLAUDE.md — encontrapp



Este archivo le indica a Claude Code cómo trabajar en este proyecto.

Leelo completo antes de ejecutar cualquier tarea.



\---



\## ¿Qué es encontrapp?



Marketplace hiperlocal que conecta personas con servicios y productos

dentro de un radio de distancia configurable. El usuario define su ubicación

y un radio (ej: 5 km), y el mapa muestra proveedores disponibles en esa área.



\---



\## Stack tecnológico



| Capa       | Tecnología                              |

|------------|-----------------------------------------|

| Backend    | Python 3.11 · FastAPI · Uvicorn         |

| Base datos | PostgreSQL 16 · PostGIS 3.4             |

| ORM        | SQLAlchemy 2.0 async · GeoAlchemy2      |

| Auth       | JWT (python-jose) · bcrypt · passlib    |

| Geocoding  | Nominatim (OpenStreetMap) — sin costo   |

| Frontend   | HTML/CSS/JS · Leaflet.js · CartoDB OSM  |

| DevOps     | Docker · docker-compose                 |



\---



\## Estructura del proyecto



encontrapp/

├── CLAUDE.md

├── README.md

├── docker-compose.yml

├── frontend/

│   └── encontrapp\_v2.html

└── backend/

&#x20;   ├── main.py

&#x20;   ├── database.py

&#x20;   ├── deps.py

&#x20;   ├── seed.py

&#x20;   ├── requirements.txt

&#x20;   ├── .env

&#x20;   ├── .env.example

&#x20;   ├── models/

&#x20;   │   ├── \_\_init\_\_.py

&#x20;   │   ├── usuario.py

&#x20;   │   ├── proveedor.py

&#x20;   │   ├── categoria.py

&#x20;   │   └── resena.py

&#x20;   ├── routers/

&#x20;   │   ├── \_\_init\_\_.py

&#x20;   │   ├── auth.py

&#x20;   │   ├── buscar.py

&#x20;   │   ├── proveedores.py

&#x20;   │   └── resenas.py

&#x20;   ├── schemas/

&#x20;   │   ├── \_\_init\_\_.py

&#x20;   │   ├── usuario.py

&#x20;   │   ├── proveedor.py

&#x20;   │   └── resena.py

&#x20;   └── services/

&#x20;       ├── \_\_init\_\_.py

&#x20;       └── geo.py



\---



\## Variables de entorno (.env)



DATABASE\_URL=postgresql+asyncpg://juan:encontrapp123@localhost:5432/encontrapp

SECRET\_KEY=cambia-esta-clave-por-una-muy-larga-y-aleatoria

ALGORITHM=HS256

ACCESS\_TOKEN\_EXPIRE\_DAYS=7

NOMINATIM\_USER\_AGENT=encontrapp/1.0



\---



\## Modelos de base de datos



\### Usuario

id, nombre, email, password\_hash, es\_proveedor (bool),

fecha\_registro (datetime), activo (bool)



\### Proveedor

id, usuario\_id (FK), nombre\_negocio, descripcion,

categoria\_id (FK), geom (Point PostGIS),

direccion, telefono, whatsapp, activo (bool),

rating\_promedio (float), total\_resenas (int)



\### Categoria

id, nombre, emoji, slug



\### Resena

id, proveedor\_id (FK), usuario\_id (FK),

rating (int 1-5), comentario (text), fecha (datetime)



\---



\## Endpoints de la API



\### Públicos (sin auth)

GET  /buscar?lat=float\&lng=float\&radio=float\&categoria=str

GET  /proveedores/{id}

GET  /categorias

POST /auth/registro

POST /auth/login



\### Protegidos (requieren Bearer token)

POST /proveedores

PUT  /proveedores/{id}

POST /resenas

GET  /me



\---



\## Query geoespacial principal



SELECT

&#x20; p.\*,

&#x20; c.nombre AS categoria\_nombre,

&#x20; c.emoji  AS categoria\_emoji,

&#x20; ST\_Y(p.geom::geometry) AS lat,

&#x20; ST\_X(p.geom::geometry) AS lng,

&#x20; ST\_Distance(

&#x20;   p.geom::geography,

&#x20;   ST\_MakePoint(:lng, :lat)::geography

&#x20; ) AS distancia\_metros

FROM proveedores p

JOIN categorias c ON p.categoria\_id = c.id

WHERE

&#x20; ST\_DWithin(

&#x20;   p.geom::geography,

&#x20;   ST\_MakePoint(:lng, :lat)::geography,

&#x20;   :radio\_metros

&#x20; )

&#x20; AND (:categoria IS NULL OR c.slug = :categoria)

&#x20; AND p.activo = true

ORDER BY distancia\_metros ASC;



\---



\## Datos de prueba (seed.py)



Categorías: electricidad, mecanica, gastronomia, belleza,

tecnologia, salud, educacion, hogar, transporte, mascotas



Proveedores: mínimo 10, alrededor de lat=-25.5116, lng=-54.6105

Variá coordenadas entre 0.001 y 0.020 grados.



\---



\## Reglas para Claude Code



1\. Siempre usar async/await — toda la DB es asíncrona (asyncpg)

2\. Nunca hardcodear credenciales — todo viene del .env

3\. Validar con Pydantic — todos los inputs y outputs tienen schema

4\. CORS habilitado para localhost:5500, 127.0.0.1:5500, localhost:3000

5\. Habilitar PostGIS con CREATE EXTENSION IF NOT EXISTS postgis en init\_db()

6\. El campo geom usa Geometry('POINT', srid=4326) de GeoAlchemy2

7\. Insertar coordenadas con ST\_MakePoint(lng, lat) — primero lng, luego lat

8\. No modificar frontend/encontrapp\_v2.html salvo que se pida explícitamente

9\. Un archivo por tarea — no mezclar modelos, routers y schemas

10\. Después de cada archivo creado, verificar que los imports sean correctos



\---



\## Orden de ejecución recomendado



1\. Crear estructura de carpetas

2\. requirements.txt + .env.example

3\. docker-compose.yml

4\. database.py

5\. models/ (orden: categoria, usuario, proveedor, resena)

6\. schemas/

7\. deps.py

8\. routers/auth.py

9\. routers/buscar.py

10\.

