"""
app/services/processing_service.py - VERSIÓN CORRECTA
Usa SOLO los campos que existen en MessageModel.
"""
import re
from typing import Dict, Any, Tuple

class ProcessingService:
    """
    Servicio de procesamiento que solo usa campos válidos de MessageModel.
    """
    
    # Lista de palabras inapropiadas
    INAPPROPRIATE_WORDS = ["badword1", "badword2", "inappropriate", "offensive"]
    
    @staticmethod
    def filter_inappropriate_content(content: str) -> Tuple[str, bool]:
        """
        Filtra contenido inapropiado.
        
        Returns:
            Tuple[str, bool]: (contenido_filtrado, tiene_inapropiado)
        """
        if not content:
            return "", False
        
        has_inappropriate = False
        filtered_content = content
        
        for word in ProcessingService.INAPPROPRIATE_WORDS:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            if pattern.search(content):
                has_inappropriate = True
                # Reemplazar palabra completa con asteriscos
                filtered_content = pattern.sub('*' * len(word), filtered_content)
        
        return filtered_content, has_inappropriate
    
    @staticmethod
    def calculate_message_stats(content: str) -> Dict[str, int]:
        """
        Calcula estadísticas del mensaje.
        
        Returns:
            Dict[str, int]: {message_length, word_count}
        """
        if not content:
            return {"message_length": 0, "word_count": 0}
        
        message_length = len(content)
        word_count = len(content.split())
        
        return {
            "message_length": message_length,
            "word_count": word_count
        }
    
    @staticmethod
    def process_message(message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa completamente un mensaje.
        
        Solo incluye campos que existen en MessageModel:
        - id (generado por BD)
        - message_id (del input)
        - session_id (del input)
        - content (filtrado)
        - original_content (del input)
        - has_inappropriate_content (calculado)
        - timestamp (del input)
        - sender (del input)
        - message_length (calculado)
        - word_count (calculado)
        - created_at (generado por BD)
        - updated_at (generado por BD)
        """
        # Copiar datos originales
        processed = message_data.copy()
        
        # Obtener contenido original
        original_content = str(message_data.get('content', ''))
        
        # Filtrar contenido inapropiado
        filtered_content, has_inappropriate = ProcessingService.filter_inappropriate_content(original_content)
        
        # Calcular estadísticas
        stats = ProcessingService.calculate_message_stats(filtered_content)
        
        # Actualizar SOLO con campos válidos de MessageModel
        processed.update({
            'content': filtered_content,  # Contenido filtrado
            'original_content': original_content,  # Contenido original
            'has_inappropriate_content': has_inappropriate,  # Bandera de contenido inapropiado
            'message_length': stats['message_length'],  # Longitud calculada
            'word_count': stats['word_count']  # Conteo de palabras
        })
        
        return processed
    
    @staticmethod
    def sanitize_message_data(message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Limpia los datos del mensaje.
        """
        sanitized = {}
        
        # Campos de texto a sanitizar
        text_fields = [
            'message_id', 'session_id', 'content', 
            'original_content', 'sender'
        ]
        
        for field in text_fields:
            if field in message_data and isinstance(message_data[field], str):
                sanitized[field] = message_data[field].strip()
            elif field in message_data:
                sanitized[field] = message_data[field]
        
        # Mantener otros campos válidos
        other_fields = [
            'id', 'timestamp', 'created_at', 'updated_at',
            'has_inappropriate_content', 'message_length', 'word_count'
        ]
        
        for field in other_fields:
            if field in message_data:
                sanitized[field] = message_data[field]
        
        return sanitized
