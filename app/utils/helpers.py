# app/utils/helpers.py
"""
Utilidades y funciones auxiliares para la aplicación.
"""
import re
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

def sanitize_string(text: str) -> str:
    """
    Limpia y sanitiza una cadena de texto.
    
    Args:
        text: Texto a sanitizar
        
    Returns:
        str: Texto sanitizado
    """
    if not text:
        return ""
    
    # Eliminar espacios al inicio y final
    text = text.strip()
    
    # Reemplazar múltiples espacios por uno solo
    text = re.sub(r'\s+', ' ', text)
    
    # Eliminar caracteres de control (excepto tab, newline, carriage return)
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    return text

def calculate_message_stats(content: str) -> Dict[str, int]:
    """
    Calcula estadísticas de un mensaje.
    
    Args:
        content: Contenido del mensaje
        
    Returns:
        Dict con: message_length, word_count, line_count
    """
    if not content:
        return {"message_length": 0, "word_count": 0, "line_count": 0}
    
    # Longitud del mensaje
    message_length = len(content)
    
    # Contar palabras (separadas por cualquier espacio)
    words = re.findall(r'\b\w+\b', content)
    word_count = len(words)
    
    # Contar líneas
    line_count = len(content.splitlines())
    
    return {
        "message_length": message_length,
        "word_count": word_count,
        "line_count": line_count
    }

def format_datetime(dt: datetime) -> str:
    """
    Formatea un datetime a string ISO 8601 con timezone UTC.
    
    Args:
        dt: datetime a formatear
        
    Returns:
        str: datetime en formato ISO 8601
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    
    return dt.isoformat().replace('+00:00', 'Z')

def parse_datetime(dt_str: str) -> Optional[datetime]:
    """
    Parsea un string ISO 8601 a datetime.
    
    Args:
        dt_str: String en formato ISO 8601
        
    Returns:
        datetime o None si no se puede parsear
    """
    try:
        from dateutil import parser
        return parser.isoparse(dt_str)
    except (ValueError, TypeError):
        return None

def generate_error_response(
    detail: str, 
    error_code: Optional[str] = None,
    field: Optional[str] = None
) -> Dict[str, Any]:
    """
    Genera una respuesta de error estandarizada.
    
    Args:
        detail: Descripción del error
        error_code: Código de error opcional
        field: Campo relacionado con el error
        
    Returns:
        Dict con la estructura de error
    """
    error_response = {"detail": detail}
    
    if error_code:
        error_response["error_code"] = error_code
    
    if field:
        error_response["field"] = field
    
    return error_response

def generate_success_response(
    message: str,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Genera una respuesta exitosa estandarizada.
    
    Args:
        message: Mensaje descriptivo
        data: Datos adicionales opcionales
        
    Returns:
        Dict con la estructura de éxito
    """
    response = {
        "status": "success",
        "message": message
    }
    
    if data:
        response["data"] = data
    
    return response

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Trunca texto a una longitud máxima, agregando "..." si es necesario.
    
    Args:
        text: Texto a truncar
        max_length: Longitud máxima
        
    Returns:
        str: Texto truncado
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."

def is_valid_uuid(uuid_string: str) -> bool:
    """
    Verifica si un string es un UUID válido.
    
    Args:
        uuid_string: String a verificar
        
    Returns:
        bool: True si es un UUID válido
    """
    import uuid
    try:
        uuid_obj = uuid.UUID(uuid_string, version=4)
        return str(uuid_obj) == uuid_string
    except ValueError:
        return False