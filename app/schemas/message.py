# app/schemas/message.py - VERSIÓN CORREGIDA
"""
Esquemas Pydantic para validación de mensajes.
Define la estructura de datos para entrada/salida de la API.
"""
from pydantic import BaseModel, Field, validator, ConfigDict
from datetime import datetime, timezone
from typing import Optional, List
import re

class MessageBase(BaseModel):
    """Esquema base con validaciones comunes"""
    message_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Identificador único del mensaje",
        examples=["msg-123456", "chat-abc-789"]
    )
    
    session_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Identificador de sesión de chat",
        examples=["session-abcdef", "user-123-conversation"]
    )
    
    content: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Contenido del mensaje",
        examples=["Hola, ¿cómo estás?", "Necesito ayuda con mi pedido"]
    )
    
    timestamp: datetime = Field(
        ...,
        description="Marca de tiempo ISO 8601 del mensaje",
        examples=["2023-12-01T10:30:00Z", "2023-12-01T14:45:30.123456+00:00"]
    )
    
    sender: str = Field(
        ...,
        description="Remitente del mensaje",
        examples=["user", "system"]
    )
    
    # Validaciones
    @validator('sender')
    def validate_sender(cls, v):
        """Validar que el remitente sea 'user' o 'system'"""
        allowed_senders = ['user', 'system']
        if v not in allowed_senders:
            raise ValueError(f'sender must be one of: {", ".join(allowed_senders)}')
        return v
    
    @validator('timestamp')
    def validate_timestamp_not_future(cls, v):
        """Validar que la marca de tiempo no sea en el futuro"""
        # Asegurar que el timestamp tenga timezone
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        if v > now:
            raise ValueError(f'timestamp cannot be in the future. Timestamp: {v}, Now: {now}')
        return v
    
    @validator('timestamp')
    def ensure_aware_timestamp(cls, v):
        """Convertir timestamp naive → aware (UTC)"""
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v
    
    @validator('message_id')
    def validate_message_id_format(cls, v):
        """Validar formato del ID del mensaje"""
        # Permite: letras, números, guiones, puntos, guiones bajos
        if not re.match(r'^[a-zA-Z0-9\-_\.]+$', v):
            raise ValueError('message_id can only contain letters, numbers, hyphens, underscores and dots')
        return v
    
    @validator('content')
    def validate_content_not_empty(cls, v):
        """Validar que el contenido no sea solo espacios en blanco"""
        if not v or not v.strip():
            raise ValueError('content cannot be empty or whitespace only')
        return v.strip()

class MessageCreate(MessageBase):
    """
    Esquema para crear un nuevo mensaje.
    Usado en el endpoint POST /api/messages/
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message_id": "msg-123456",
                "session_id": "session-abcdef",
                "content": "Hola, ¿cómo puedo ayudarte hoy?",
                "timestamp": "2023-12-01T10:30:00Z",
                "sender": "system"
            }
        }
    )

class MessageResponse(MessageBase):
    """
    Esquema para respuesta de mensaje.
    Incluye todos los campos calculados y metadatos.
    """
    id: int = Field(..., description="ID único en la base de datos")
    original_content: str = Field(..., description="Contenido original antes de cualquier procesamiento")
    message_length: int = Field(..., description="Longitud del mensaje en caracteres", ge=1)
    word_count: int = Field(..., description="Número de palabras en el mensaje", ge=1)
    has_inappropriate_content: bool = Field(
        False,
        description="Indica si el mensaje contenía palabras inapropiadas"
    )
    created_at: datetime = Field(..., description="Fecha de creación en la base de datos")
    updated_at: datetime = Field(..., description="Fecha de última actualización")
    
    model_config = ConfigDict(from_attributes=True)  # Para ORM SQLAlchemy

class MessageFilter(BaseModel):
    """
    Esquema para filtrar mensajes en consultas.
    Usado en el endpoint GET /api/messages/{session_id}
    """
    sender: Optional[str] = Field(
        None,
        description="Filtrar por remitente (user/system)",
        examples=["user", "system"]
    )
    
    limit: int = Field(
        50,
        ge=1,
        le=100,
        description="Número máximo de mensajes a retornar"
    )
    
    offset: int = Field(
        0,
        ge=0,
        description="Número de mensajes a omitir (para paginación)"
    )
    
    @validator('sender')
    def validate_filter_sender(cls, v):
        """Validar sender en filtros"""
        if v is not None and v not in ['user', 'system']:
            raise ValueError('sender filter must be either "user", "system" or None')
        return v

class MessageListResponse(BaseModel):
    """
    Esquema para respuesta de lista de mensajes.
    Incluye metadatos de paginación.
    """
    messages: List[MessageResponse]
    total: int = Field(..., description="Total de mensajes que coinciden con el filtro")
    limit: int = Field(..., description="Límite usado en la consulta")
    offset: int = Field(..., description="Offset usado en la consulta")
    has_more: bool = Field(..., description="Indica si hay más mensajes disponibles")

class ErrorResponse(BaseModel):
    """
    Esquema para respuestas de error estandarizadas.
    """
    detail: str = Field(..., description="Descripción del error")
    error_code: Optional[str] = Field(None, description="Código de error opcional")
    field: Optional[str] = Field(None, description="Campo relacionado con el error")

class SuccessResponse(BaseModel):
    """
    Esquema para respuestas exitosas estandarizadas.
    """
    status: str = Field("success", description="Estado de la operación")
    message: str = Field(..., description="Mensaje descriptivo")
    data: Optional[dict] = Field(None, description="Datos de la respuesta")