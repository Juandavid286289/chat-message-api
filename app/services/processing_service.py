"""
Servicio de procesamiento de mensajes.
Contiene lógica para filtrar contenido y calcular metadatos.
"""
import re
from typing import Dict, Any, Tuple, List
from app.core.config import settings
from app.utils.helpers import calculate_message_stats

class ProcessingService:
    """
    Servicio para procesar mensajes de chat.
    Incluye filtrado de contenido inapropiado y cálculo de metadatos.
    """
    
    @staticmethod
    def filter_inappropriate_content(content: str) -> Tuple[str, bool, List[str]]:
        """
        Filtra contenido inapropiado de un mensaje.
        
        Args:
            content: Contenido del mensaje a filtrar
            
        Returns:
            Tuple[str, bool, List[str]]: 
                (contenido_filtrado, 
                 tiene_contenido_inapropiado, 
                 palabras_encontradas)
        """
        if not content:
            return "", False, []
        
        # Obtener lista de palabras inapropiadas desde configuración
        inappropriate_words = getattr(settings, 'inappropriate_words', [])
        if not inappropriate_words:
            return content, False, []
        
        content_lower = content.lower()
        found_words = []
        filtered_content = content
        
        # Para cada palabra inapropiada
        for word in inappropriate_words:
            word_lower = word.lower()
            
            # Buscar la palabra en el contenido (case-insensitive)
            pattern = re.compile(re.escape(word_lower), re.IGNORECASE)
            matches = pattern.findall(content)
            
            if matches:
                found_words.extend(matches)
                
                # Reemplazar cada ocurrencia con asteriscos
                for match in set(matches):  # Usar set para evitar duplicados
                    replacement = '*' * len(match)
                    filtered_content = pattern.sub(replacement, filtered_content)
        
        has_inappropriate = len(found_words) > 0
        
        return filtered_content, has_inappropriate, found_words
    
    @staticmethod
    def process_message(message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa completamente un mensaje.
        
        Args:
            message_data: Datos del mensaje a procesar
            
        Returns:
            Dict[str, Any]: Datos procesados con metadatos
        """
        # Copiar datos originales
        processed_data = message_data.copy()
        
        # 1. Obtener contenido original
        original_content = message_data.get('content', '')
        
        # 2. Filtrar contenido inapropiado
        filtered_content, has_inappropriate, found_words = ProcessingService.filter_inappropriate_content(original_content)
        
        # 3. Calcular estadísticas del contenido filtrado
        stats = calculate_message_stats(filtered_content)
        
        # 4. Agregar metadatos al mensaje procesado
        processed_data.update({
            'content': filtered_content,
            'original_content': original_content,
            'has_inappropriate_content': has_inappropriate,
            'inappropriate_words_found': found_words,
            'message_length': stats['message_length'],
            'word_count': stats['word_count'],
            'line_count': stats.get('line_count', 1)
        })
        
        return processed_data
    
    @staticmethod
    def sanitize_message_data(message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitiza los datos de un mensaje.
        
        Args:
            message_data: Datos del mensaje a sanitizar
            
        Returns:
            Dict[str, Any]: Datos sanitizados
        """
        from app.utils.helpers import sanitize_string
        
        sanitized_data = {}
        
        # Sanitizar campos de texto
        text_fields = ['message_id', 'session_id', 'content', 'sender']
        
        for field in text_fields:
            if field in message_data and isinstance(message_data[field], str):
                sanitized_data[field] = sanitize_string(message_data[field])
            elif field in message_data:
                sanitized_data[field] = message_data[field]
        
        # Mantener otros campos
        other_fields = ['timestamp', 'id', 'created_at', 'updated_at']
        for field in other_fields:
            if field in message_data:
                sanitized_data[field] = message_data[field]
        
        return sanitized_data
