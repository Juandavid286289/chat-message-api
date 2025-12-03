# app/models/message.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Index
from sqlalchemy.sql import func
from datetime import datetime
import uuid
from app.models.database import Base

class MessageModel(Base):
    """
    Modelo SQLAlchemy para mensajes de chat.
    Representa la tabla 'messages' en la base de datos.
    """
    __tablename__ = "messages"
    
    # Columnas principales
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message_id = Column(String(255), unique=True, nullable=False, index=True)
    session_id = Column(String(255), nullable=False, index=True)
    
    # Contenido del mensaje
    content = Column(Text, nullable=False)  # Contenido procesado/filtrado
    original_content = Column(Text, nullable=False)  # Contenido original
    has_inappropriate_content = Column(Boolean, default=False)
    
    # Metadatos
    timestamp = Column(DateTime, nullable=False)  # Timestamp del mensaje
    sender = Column(String(50), nullable=False)  # 'user' o 'system'
    
    # Estadísticas calculadas
    message_length = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)
    
    # Metadatos del sistema
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, 
        server_default=func.now(), 
        onupdate=func.now(),
        nullable=False
    )
    
    # Índices compuestos para mejor rendimiento
    __table_args__ = (
        Index('idx_session_sender', 'session_id', 'sender'),
        Index('idx_session_timestamp', 'session_id', 'timestamp'),
        Index('idx_created_at', 'created_at'),
    )
    
    def __repr__(self):
        """Representación string del modelo para debugging"""
        return f"<Message(id={self.id}, message_id='{self.message_id}', session_id='{self.session_id}')>"
    
    def to_dict(self):
        """Convertir modelo a diccionario (útil para JSON)"""
        return {
            "id": self.id,
            "message_id": self.message_id,
            "session_id": self.session_id,
            "content": self.content,
            "original_content": self.original_content,
            "has_inappropriate_content": self.has_inappropriate_content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "sender": self.sender,
            "message_length": self.message_length,
            "word_count": self.word_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crear instancia desde diccionario"""
        # Convertir strings de timestamp a objetos datetime si es necesario
        if "timestamp" in data and isinstance(data["timestamp"], str):
            from datetime import datetime
            data["timestamp"] = datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
        
        return cls(**data)

# Alias para compatibilidad
Message = MessageModel