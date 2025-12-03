"""
app/main.py

Aplicación principal FastAPI para la API de procesamiento de mensajes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.config import settings
from app.api.endpoints import messages, health

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API RESTful para procesamiento de mensajes de chat",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(messages.router, prefix="/api")
app.include_router(health.router)

@app.get("/", tags=["root"])
async def root():
    """
    Endpoint raíz de la API.
    
    Retorna información básica sobre la API.
    """
    return {
        "message": "Welcome to the Chat Message Processing API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "create_message": "POST /messages/",
            "get_messages": "GET /api/messages/{session_id}",
            "health": "GET /health",
            "liveness": "GET /health/live",
            "readiness": "GET /health/ready"
        }
    }


@app.on_event("startup")
async def startup_event():
    """
    Evento ejecutado al iniciar la aplicación.
    """
    print(f" Starting {settings.APP_NAME}...")
    print(f" Database: {settings.DATABASE_URL}")
    print(f" Debug mode: {settings.DEBUG}")
    
    # Inicializar base de datos
    from app.models.database import init_db
    init_db()
    print(" Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento ejecutado al detener la aplicación.
    """
    print(f" Shutting down {settings.APP_NAME}...")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
