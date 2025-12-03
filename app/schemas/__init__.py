# app/schemas/__init__.py
"""
Módulo de esquemas Pydantic para la API.
Exporta todos los esquemas para fácil importación.
"""

from app.schemas.message import (
    MessageBase,
    MessageCreate,
    MessageResponse,
    MessageFilter,
    MessageListResponse,
    ErrorResponse,
    SuccessResponse
)

__all__ = [
    "MessageBase",
    "MessageCreate", 
    "MessageResponse",
    "MessageFilter",
    "MessageListResponse",
    "ErrorResponse",
    "SuccessResponse"
]