"""
app/api/endpoints/health.py

Endpoint para verificación de salud de la API.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.dependencies import get_db
from app.schemas.responses import HealthResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Verifica el estado de salud de la API y sus dependencias."
)
async def health_check(db: Session = Depends(get_db)):
    """
    Health Check Endpoint
    
    Verifica:
    - Estado general de la API
    - Conexión a la base de datos
    - Tiempo de actividad
    
    Retorna el estado de todos los componentes críticos.
    """
    try:
        # 1. Verificar conexión a base de datos
        db_status = "healthy"
        try:
            db.execute("SELECT 1")
        except Exception as e:
            db_status = f"unhealthy: {str(e)}"
        
        # 2. Obtener información del sistema
        from app.core.config import settings
        
        return HealthResponse(
            status="healthy" if db_status == "healthy" else "degraded",
            version=getattr(settings, "VERSION", "1.0.0"),
            timestamp=datetime.utcnow(),
            database=db_status,
            uptime=None  # Podríamos implementar esto si guardamos start_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}"
        )


@router.get(
    "/health/live",
    status_code=status.HTTP_200_OK,
    summary="Liveness Probe",
    description="Verifica si la API está viva y respondiendo."
)
async def liveness_probe():
    """
    Liveness Probe
    
    Endpoint simple para verificar que la API está viva.
    Usado por orquestadores como Kubernetes.
    """
    return {"status": "alive"}


@router.get(
    "/health/ready",
    status_code=status.HTTP_200_OK,
    summary="Readiness Probe",
    description="Verifica si la API está lista para recibir tráfico."
)
async def readiness_probe(db: Session = Depends(get_db)):
    """
    Readiness Probe
    
    Verifica que la API y sus dependencias estén listas.
    """
    try:
        # Verificar base de datos
        db.execute("SELECT 1")
        
        return {"status": "ready", "database": "connected"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service not ready: {str(e)}"
        )
