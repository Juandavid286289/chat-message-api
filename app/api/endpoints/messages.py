"""
app/api/endpoints/messages.py

Endpoints de la API para manejo de mensajes.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.message import MessageCreate, MessageFilter, MessageResponse
from app.schemas.responses import StandardResponse, MessageListResponse, ErrorResponse

router = APIRouter(prefix="/api/messages", tags=["messages"])


@router.post(
    "/",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Message",
    description="Create a new chat message with validation and processing"
)
async def create_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new chat message.
    
    - **message_id**: Unique message identifier (required)
    - **session_id**: Session identifier (required)
    - **content**: Message content (required)
    - **timestamp**: ISO 8601 timestamp (required)
    - **sender**: Message sender: "user" or "system" (required)
    
    The message is validated, processed (content filtering), and stored in the database.
    """
    try:
        # Importar servicios aquí para evitar problemas circulares
        from app.repositories.message_repository import MessageRepository
        from app.services.message_service import MessageService
        
        # Crear servicio
        repository = MessageRepository(db)
        message_service = MessageService(repository)
        
        success, message, created_message = await message_service.create_message(
            message_data.model_dump()
        )
        
        if not success:
            if "already exists" in message.lower():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=message
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=message
                )
        
        # Convertir a dict si es necesario
        if hasattr(created_message, '__dict__'):
            message_dict = created_message.__dict__.copy()
            # Limpiar atributos internos de SQLAlchemy
            message_dict.pop('_sa_instance_state', None)
        else:
            message_dict = created_message
        
        return StandardResponse(
            success=True,
            message="Message created successfully",
            data=message_dict
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/{session_id}",
    response_model=MessageListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Session Messages",
    description="Retrieve all messages from a specific session"
)
async def get_messages_by_session(
    session_id: str,
    sender: Optional[str] = Query(None, description="Filter by sender (user/system)"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of messages to return"),
    offset: int = Query(0, ge=0, description="Number of messages to skip"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all messages from a session.
    
    - **session_id**: Session ID (required)
    - **sender**: Filter by sender (optional)
    - **limit**: Maximum number of messages (1-100, default: 50)
    - **offset**: For pagination (default: 0)
    
    Returns messages ordered by timestamp descending (most recent first).
    """
    try:
        # Importar servicios aquí para evitar problemas circulares
        from app.repositories.message_repository import MessageRepository
        from app.services.message_service import MessageService
        
        # Crear servicio
        repository = MessageRepository(db)
        message_service = MessageService(repository)
        
        # Crear filtros
        filter_params = None
        if sender or limit != 50 or offset != 0:
            filter_params = MessageFilter(
                sender=sender,
                limit=limit,
                offset=offset
            )
        
        success, message, result = await message_service.get_messages_by_session(
            session_id, filter_params
        )
        
        if not success:
            # Si no hay mensajes, no es un error, solo retornamos lista vacía
            if "no messages found" in message.lower():
                from app.schemas.responses import PaginationInfo
                return MessageListResponse(
                    success=True,
                    message=message,
                    data=[],
                    pagination=PaginationInfo(
                        total=0,
                        limit=limit,
                        offset=offset,
                        has_more=False
                    )
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=message
                )
        
        # Convertir mensajes a dict para respuesta
        messages_data = []
        if result and "messages" in result:
            for msg in result["messages"]:
                msg_dict = msg.__dict__.copy()
                # Limpiar atributos internos de SQLAlchemy
                msg_dict.pop('_sa_instance_state', None)
                messages_data.append(msg_dict)
        
        # Crear respuesta
        from app.schemas.responses import PaginationInfo
        
        return MessageListResponse(
            success=True,
            message=message,
            data=messages_data,
            pagination=PaginationInfo(
                total=result.get("total", 0),
                limit=result.get("limit", limit),
                offset=result.get("offset", offset),
                has_more=result.get("has_more", False)
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
