"""
app/services/message_service.py

Servicio principal de mensajes.
Orquesta la validación, procesamiento y almacenamiento de mensajes.
"""
from typing import Dict, Any, Tuple, Optional
from datetime import datetime

from app.schemas.message import MessageCreate, MessageFilter
from app.services.validation_service import ValidationService
from app.services.processing_service import ProcessingService
from app.repositories.message_repository import MessageRepository
from app.models.message import MessageModel


class MessageService:
    """
    Servicio principal para manejar la lógica de negocio de mensajes.
    Coordina validación, procesamiento y almacenamiento.
    """
    
    def __init__(self, repository: MessageRepository):
        self.repository = repository
    
    async def create_message(self, message_data: Dict[str, Any]) -> Tuple[bool, str, Optional[MessageModel]]:
        """
        Crea un nuevo mensaje con validación y procesamiento completo.
        
        Args:
            message_data: Datos del mensaje a crear
            
        Returns:
            Tuple[bool, str, Optional[MessageModel]]: 
                (éxito, mensaje, mensaje_creado)
        """
        try:
            # 1. Validar datos con esquema Pydantic
            try:
                message_create = MessageCreate(**message_data)
            except Exception as e:
                return False, f"Error de validación de esquema: {str(e)}", None
            
            # 2. Validar datos con servicio de validación
            is_valid, errors, validated_data = ValidationService.validate_complete_message(
                message_data
            )
            
            if not is_valid:
                error_msg = ", ".join(errors) if errors else "Datos inválidos"
                return False, error_msg, None
            
            # 3. Verificar que el message_id no exista
            existing_message = self.repository.get_by_message_id(
                validated_data["message_id"]
            )
            
            if existing_message:
                return False, f"Message with ID '{validated_data['message_id']}' already exists", None
            
            # 4. Procesar el mensaje
            processed_data = ProcessingService.process_message(validated_data)
            
            # 5. Sanitizar datos
            sanitized_data = ProcessingService.sanitize_message_data(processed_data)
            
            # 6. Asegurar campos requeridos
            if "created_at" not in sanitized_data:
                sanitized_data["created_at"] = datetime.utcnow()
            if "updated_at" not in sanitized_data:
                sanitized_data["updated_at"] = datetime.utcnow()
            
            # 7. Crear en base de datos
            db_message = self.repository.create(sanitized_data)
            
            return True, "Message created successfully", db_message
            
        except Exception as e:
            # Manejo de errores inesperados
            error_msg = f"Error interno al crear mensaje: {str(e)}"
            return False, error_msg, None
    
    async def get_messages_by_session(
        self, 
        session_id: str,
        filter_params: Optional[MessageFilter] = None
    ) -> Tuple[bool, str, Optional[list]]:
        """
        Obtiene mensajes de una sesión con filtros.
        
        Args:
            session_id: ID de la sesión
            filter_params: Parámetros de filtrado opcionales
            
        Returns:
            Tuple[bool, str, Optional[list]]: 
                (éxito, mensaje, lista_mensajes)
        """
        try:
            # 1. Validar session_id
            if not session_id or not session_id.strip():
                return False, "session_id cannot be empty", None
            
            # 2. Obtener mensajes del repositorio
            messages = self.repository.get_by_session_id(session_id, filter_params)
            
            # 3. Verificar si hay mensajes
            if not messages:
                return True, f"No messages found for session '{session_id}'", []
            
            # 4. Contar total para paginación
            total_count = self.repository.count_by_session(session_id)
            
            # 5. Preparar respuesta
            result = {
                "messages": messages,
                "total": total_count,
                "limit": filter_params.limit if filter_params else 50,
                "offset": filter_params.offset if filter_params else 0,
                "has_more": total_count > (
                    (filter_params.offset if filter_params else 0) + 
                    (filter_params.limit if filter_params else 50)
                )
            }
            
            return True, "Messages retrieved successfully", result
            
        except Exception as e:
            error_msg = f"Error al obtener mensajes: {str(e)}"
            return False, error_msg, None
    
    async def get_message_by_id(self, message_id: int) -> Tuple[bool, str, Optional[MessageModel]]:
        """
        Obtiene un mensaje por su ID.
        
        Args:
            message_id: ID del mensaje
            
        Returns:
            Tuple[bool, str, Optional[MessageModel]]: 
                (éxito, mensaje, mensaje_encontrado)
        """
        try:
            if not message_id or message_id <= 0:
                return False, "Invalid message ID", None
            
            message = self.repository.get_by_id(message_id)
            
            if not message:
                return False, f"Message with ID {message_id} not found", None
            
            return True, "Message found", message
            
        except Exception as e:
            error_msg = f"Error al obtener mensaje: {str(e)}"
            return False, error_msg, None
    
    async def delete_message(self, message_id: int) -> Tuple[bool, str]:
        """
        Elimina un mensaje por su ID.
        
        Args:
            message_id: ID del mensaje a eliminar
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        try:
            if not message_id or message_id <= 0:
                return False, "Invalid message ID"
            
            deleted = self.repository.delete(message_id)
            
            if not deleted:
                return False, f"Message with ID {message_id} not found"
            
            return True, "Message deleted successfully"
            
        except Exception as e:
            error_msg = f"Error al eliminar mensaje: {str(e)}"
            return False, error_msg
    
    async def search_messages(
        self, 
        query: str,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[bool, str, Optional[list]]:
        """
        Busca mensajes por contenido (búsqueda simple).
        
        Args:
            query: Texto a buscar
            limit: Límite de resultados
            offset: Offset para paginación
            
        Returns:
            Tuple[bool, str, Optional[list]]: 
                (éxito, mensaje, lista_mensajes)
        """
        try:
            # Validar query
            if not query or not query.strip():
                return False, "Search query cannot be empty", None
            
            # En una implementación real, aquí iría la lógica de búsqueda
            # Por simplicidad, obtendremos todos y filtraremos localmente
            all_messages = self.repository.get_all(limit=1000)  # Límite razonable
            
            # Búsqueda simple (case-insensitive)
            query_lower = query.lower()
            results = []
            
            for message in all_messages:
                if (query_lower in message.content.lower() or 
                    query_lower in message.original_content.lower()):
                    results.append(message)
            
            # Aplicar paginación
            paginated_results = results[offset:offset + limit]
            
            result = {
                "messages": paginated_results,
                "total": len(results),
                "limit": limit,
                "offset": offset,
                "has_more": len(results) > (offset + limit)
            }
            
            return True, "Search completed", result
            
        except Exception as e:
            error_msg = f"Error en búsqueda: {str(e)}"
            return False, error_msg, None
