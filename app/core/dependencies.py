"""
app/core/dependencies.py

Dependencias para inyección en los endpoints de FastAPI.
"""
from typing import Generator
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Obtiene una sesión de base de datos.
    
    Yields:
        Session: Sesión de SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_settings():
    """
    Obtiene la configuración de la aplicación.
    
    Returns:
        Settings: Configuración de la aplicación
    """
    return settings
