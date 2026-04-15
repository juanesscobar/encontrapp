\# encontrapp



Marketplace hiperlocal — conectá con servicios y productos cerca tuyo.



encontrapp conecta personas con profesionales, negocios y productos

disponibles dentro de un radio de distancia configurable. El usuario

define su ubicación y el mapa muestra oportunidades a su alrededor,

ordenadas de más cercanas a más lejanas.



\---



\## Stack



\- Backend: Python 3.11 + FastAPI + Uvicorn

\- Base de datos: PostgreSQL 16 + PostGIS 3.4

\- ORM: SQLAlchemy 2.0 async + GeoAlchemy2

\- Auth: JWT + bcrypt

\- Mapa: Leaflet.js + OpenStreetMap (CartoDB) — sin costo

\- Geocoding: Nominatim — sin API key

\- DevOps: Docker + docker-compose



\---



\## Requisitos previos



\- Python 3.11+

\- Docker Desktop

\- Git



\---



\## Instalación



1\. Clonar el repositorio

git clone https://github.com/juanesscobar/encontrapp.git

cd encontrapp



2\. Crear archivo de entorno

cp backend/.env.example backend/.env

Editá backend/.env con tus valores.



3\. Levantar PostgreSQL + PostGIS

docker-compose up -d db



4\. Instalar dependencias Python

pip install -r backend/requirements.txt



5\. Inicializar base de datos

python backend/database.py



6\. Cargar datos de prueba

python backend/seed.py



7\. Levantar el servidor

uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000



8\. Verificar

Documentación: http://localhost:8000/docs

Búsqueda test: http://localhost:8000/buscar?lat=-25.5116\&lng=-54.6105\&radio=5



\---



\## Endpoints principales



GET  /buscar?lat=\&lng=\&radio=\&categoria=   <- búsqueda geoespacial

GET  /categorias                           <- lista de categorías

GET  /proveedores/{id}                     <- perfil público

POST /auth/registro                        <- registro de usuario

POST /auth/login                           <- login, devuelve JWT

POST /proveedores                          <- crear perfil (auth)

PUT  /proveedores/{id}                     <- editar perfil (auth)

POST /resenas                              <- dejar reseña (auth)

GET  /me                                   <- usuario autenticado



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

&#x20;   ├── .env.example

&#x20;   ├── models/

&#x20;   ├── routers/

&#x20;   ├── schemas/

&#x20;   └── services/



\---



\## Comandos Docker



docker-compose up -d db       <- solo base de datos

docker-compose up -d          <- todo

docker-compose down           <- detener

docker-compose logs -f db     <- ver logs



\---



\## Cómo usar con Claude Code



cd encontrapp

claude



Claude Code leerá CLAUDE.md automáticamente.

Primer comando: /init



\---



\## Roadmap



\[x] Frontend con mapa interactivo

\[x] Búsqueda por radio con slider

\[x] Filtros por categoría

\[x] Geolocalización real del navegador

\[ ] Backend FastAPI + PostGIS

\[ ] Autenticación JWT

\[ ] Registro de proveedores

\[ ] Sistema de reseñas

\[ ] Geocoding de direcciones

\[ ] Notificaciones WhatsApp

\[ ] App móvil (PWA)

\[ ] Panel de administración



\---



Desarrollado en Ciudad del Este, Paraguay

