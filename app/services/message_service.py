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
    
    async def get_messages_by_session(
        self, 
        session_id: str,
        filter_params: Optional[MessageFilter] = None
    ) -> Tuple[bool, str, Optional[dict]]:
        """
        Obtiene mensajes de una sesión con filtros.
        
        Args:
            session_id: ID de la sesión
            filter_params: Parámetros de filtrado opcionales
            
        Returns:
            Tuple[bool, str, Optional[dict]]: 
                (éxito, mensaje, resultado)
        """
        try:
            # 1. Validar session_id
            if not session_id or not session_id.strip():
                return False, "session_id cannot be empty", None
            
            # 2. Obtener mensajes del repositorio
            messages = self.repository.get_by_session_id(session_id, filter_params)
            
            # 3. Contar total para paginación
            total_count = self.repository.count_by_session(session_id)
            
            # 4. Verificar si hay mensajes
            if not messages:
                # No es un error, solo retornamos vacío
                result = {
                    "messages": [],
                    "total": 0,
                    "limit": filter_params.limit if filter_params else 50,
                    "offset": filter_params.offset if filter_params else 0,
                    "has_more": False
                }
                return True, f"No se encontraron mensajes para la sesión '{session_id}'", result
            
            # 5. Preparar respuesta completa
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
            
            return True, "Mensajes recuperados exitosamente", result
            
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
                return False, "ID de mensaje no válido", None
            
            message = self.repository.get_by_id(message_id)
            
            if not message:
                return False, f"Mensaje con ID {message_id} no encontrado", None
            
            return True, "Mensaje encontrado", message
            
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
                return False, "ID de mensaje no válido"
            
            deleted = self.repository.delete(message_id)
            
            if not deleted:
                return False, f"Mensaje con ID {message_id} no encontrado"
            
            return True, "Mensaje eliminado exitosamente"
            
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
                return False, "La consulta de búsqueda no puede estar vacía", None
            
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
            
            return True, "Búsqueda completada exitosamente", result
            
        except Exception as e:
            error_msg = f"Error en búsqueda: {str(e)}"
            return False, error_msg, None

