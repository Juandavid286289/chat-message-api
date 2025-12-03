"""
Repositorio para operaciones de base de datos con mensajes.
Implementa el patrón Repository para separar la lógica de acceso a datos.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.message import MessageModel
from app.schemas.message import MessageFilter

class MessageRepository:
    """
    Repositorio para operaciones CRUD con mensajes.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, message_data: Dict[str, Any]) -> MessageModel:
        """
        Crea un nuevo mensaje en la base de datos.
        
        Args:
            message_data: Datos del mensaje a crear
            
        Returns:
            MessageModel: Mensaje creado
        """
        db_message = MessageModel(**message_data)
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message
    
    def get_by_id(self, message_id: int) -> Optional[MessageModel]:
        """
        Obtiene un mensaje por su ID.
        
        Args:
            message_id: ID del mensaje
            
        Returns:
            Optional[MessageModel]: Mensaje encontrado o None
        """
        return self.db.query(MessageModel).filter(MessageModel.id == message_id).first()
    
    def get_by_message_id(self, message_identifier: str) -> Optional[MessageModel]:
        """
        Obtiene un mensaje por su message_id único.
        
        Args:
            message_identifier: message_id único del mensaje
            
        Returns:
            Optional[MessageModel]: Mensaje encontrado o None
        """
        return self.db.query(MessageModel).filter(
            MessageModel.message_id == message_identifier
        ).first()
    
    def get_by_session_id(
        self, 
        session_id: str, 
        filter_params: Optional[MessageFilter] = None
    ) -> List[MessageModel]:
        """
        Obtiene todos los mensajes de una sesión.
        
        Args:
            session_id: ID de la sesión
            filter_params: Parámetros de filtrado opcionales
            
        Returns:
            List[MessageModel]: Lista de mensajes de la sesión
        """
        query = self.db.query(MessageModel).filter(
            MessageModel.session_id == session_id
        )
        
        # Aplicar filtros si se proporcionan
        if filter_params:
            if filter_params.sender:
                query = query.filter(MessageModel.sender == filter_params.sender)
            
            # Ordenar por timestamp descendente (más reciente primero)
            query = query.order_by(desc(MessageModel.timestamp))
            
            # Aplicar paginación
            query = query.offset(filter_params.offset).limit(filter_params.limit)
        else:
            # Orden por defecto
            query = query.order_by(desc(MessageModel.timestamp))
        
        return query.all()
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[MessageModel]:
        """
        Obtiene todos los mensajes con paginación.
        
        Args:
            limit: Límite de resultados
            offset: Offset para paginación
            
        Returns:
            List[MessageModel]: Lista de mensajes
        """
        return self.db.query(MessageModel)\
            .order_by(desc(MessageModel.created_at))\
            .offset(offset)\
            .limit(limit)\
            .all()
    
    def update(self, message_id: int, update_data: Dict[str, Any]) -> Optional[MessageModel]:
        """
        Actualiza un mensaje existente.
        
        Args:
            message_id: ID del mensaje a actualizar
            update_data: Datos a actualizar
            
        Returns:
            Optional[MessageModel]: Mensaje actualizado o None si no existe
        """
        db_message = self.get_by_id(message_id)
        if not db_message:
            return None
        
        # Actualizar campos
        for key, value in update_data.items():
            if hasattr(db_message, key):
                setattr(db_message, key, value)
        
        self.db.commit()
        self.db.refresh(db_message)
        return db_message
    
    def delete(self, message_id: int) -> bool:
        """
        Elimina un mensaje por su ID.
        
        Args:
            message_id: ID del mensaje a eliminar
            
        Returns:
            bool: True si se eliminó, False si no existe
        """
        db_message = self.get_by_id(message_id)
        if not db_message:
            return False
        
        self.db.delete(db_message)
        self.db.commit()
        return True
    
    def count_by_session(self, session_id: str) -> int:
        """
        Cuenta los mensajes de una sesión.
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            int: Número de mensajes en la sesión
        """
        return self.db.query(MessageModel).filter(
            MessageModel.session_id == session_id
        ).count()
