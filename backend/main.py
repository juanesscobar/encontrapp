from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from backend.routers import auth, buscar, proveedores, resenas

app = FastAPI(
    title="encontrapp API",
    description="Marketplace hiperlocal — conectá con servicios y productos cerca tuyo.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(buscar.router)
app.include_router(proveedores.router)
app.include_router(resenas.router)


@app.get("/")
async def root():
    return {"status": "ok", "app": "encontrapp", "docs": "/docs"}
