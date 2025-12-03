"""
app/schemas/responses.py

Esquemas para respuestas estandarizadas de la API.
"""
from typing import Any, Optional, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime


class StandardResponse(BaseModel):
    """
    Respuesta estándar para todas las operaciones de la API.
    """
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo del resultado")
    data: Optional[Any] = Field(None, description="Datos de la respuesta")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Marca de tiempo de la respuesta")
    request_id: Optional[str] = Field(None, description="ID único de la solicitud para seguimiento")


class ErrorResponse(BaseModel):
    """
    Respuesta para errores específicos.
    """
    error: str = Field(..., description="Descripción del error")
    code: str = Field(..., description="Código de error único")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalles adicionales del error")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Marca de tiempo del error")


class PaginationInfo(BaseModel):
    """
    Información de paginación para respuestas con múltiples elementos.
    """
    total: int = Field(..., description="Total de elementos disponibles")
    limit: int = Field(..., description="Límite de elementos por página")
    offset: int = Field(..., description="Offset actual")
    has_more: bool = Field(..., description="Indica si hay más elementos disponibles")
    total_pages: Optional[int] = Field(None, description="Total de páginas disponibles")
    current_page: Optional[int] = Field(None, description="Página actual")


class PaginatedResponse(StandardResponse):
    """
    Respuesta paginada para listas de elementos.
    """
    pagination: PaginationInfo = Field(..., description="Información de paginación")


class MessageResponse(StandardResponse):
    """
    Respuesta específica para operaciones con mensajes.
    """
    data: Optional[Dict[str, Any]] = Field(None, description="Datos del mensaje")


class MessageListResponse(PaginatedResponse):
    """
    Respuesta para listas de mensajes.
    """
    data: List[Dict[str, Any]] = Field(default_factory=list, description="Lista de mensajes")


class HealthResponse(BaseModel):
    """
    Respuesta para endpoint de health check.
    """
    status: str = Field(..., description="Estado del servicio")
    version: str = Field(..., description="Versión de la API")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Marca de tiempo del check")
    database: str = Field(..., description="Estado de la base de datos")
    uptime: Optional[float] = Field(None, description="Tiempo de actividad en segundos")


class ValidationErrorDetail(BaseModel):
    """
    Detalle de error de validación para campos específicos.
    """
    field: str = Field(..., description="Campo con error de validación")
    error: str = Field(..., description="Descripción del error")
    value: Optional[Any] = Field(None, description="Valor que causó el error")


class ValidationErrorResponse(ErrorResponse):
    """
    Respuesta específica para errores de validación.
    """
    errors: List[ValidationErrorDetail] = Field(..., description="Lista de errores de validación")


class ConflictErrorResponse(ErrorResponse):
    """
    Respuesta específica para errores de conflicto (409).
    """
    conflicting_field: str = Field(..., description="Campo que causó el conflicto")
    existing_value: Any = Field(..., description="Valor existente que causó el conflicto")


class NotFoundErrorResponse(ErrorResponse):
    """
    Respuesta específica para errores de no encontrado (404).
    """
    resource_type: str = Field(..., description="Tipo de recurso no encontrado")
    resource_id: Any = Field(..., description="ID del recurso no encontrado")
