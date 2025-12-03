"""
app/utils/helpers.py

Funciones de utilidad para la aplicación.
"""
import re
import json
from typing import Dict, Any, Optional, List
from datetime import datetime


def calculate_message_stats(content: str) -> Dict[str, Any]:
    """
    Calcula estadísticas de un mensaje.
    
    Args:
        content: Contenido del mensaje
        
    Returns:
        Dict[str, Any]: Estadísticas calculadas
    """
    if not content:
        return {
            "message_length": 0,
            "word_count": 0
        }
    
    # Longitud del mensaje
    message_length = len(content)
    
    # Contar palabras (split por espacios)
    words = content.split()
    word_count = len(words)
    
    return {
        "message_length": message_length,
        "word_count": word_count
    }


def sanitize_string(text: str) -> str:
    """
    Sanitiza un string eliminando espacios extra y caracteres problemáticos.
    
    Args:
        text: Texto a sanitizar
        
    Returns:
        str: Texto sanitizado
    """
    if not isinstance(text, str):
        return str(text) if text else ""
    
    # Eliminar espacios al inicio y final
    text = text.strip()
    
    # Reemplazar múltiples espacios con uno solo
    text = re.sub(r'\s+', ' ', text)
    
    # Eliminar caracteres de control (excepto tab, newline, return)
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    return text


def is_valid_message_id(message_id: str) -> bool:
    """
    Valida el formato de un message_id.
    
    Args:
        message_id: ID a validar
        
    Returns:
        bool: True si es válido
    """
    if not message_id or not isinstance(message_id, str):
        return False
    
    # Permite letras, números, guiones, guiones bajos y puntos
    pattern = r'^[a-zA-Z0-9\-_\.]+$'
    return bool(re.match(pattern, message_id))


def format_datetime(dt: Any) -> str:
    """
    Formatea un datetime a string ISO.
    
    Args:
        dt: Objeto datetime o timestamp
        
    Returns:
        str: Timestamp formateado en ISO
    """
    if isinstance(dt, datetime):
        return dt.isoformat()
    elif isinstance(dt, str):
        return dt
    else:
        return str(dt)


def parse_datetime(dt_str: str) -> datetime:
    """
    Parsea un string a datetime.
    
    Args:
        dt_str: String con formato datetime
        
    Returns:
        datetime: Objeto datetime
    """
    # Si ya es datetime, devolverlo
    if isinstance(dt_str, datetime):
        return dt_str
    
    # Convertir a string
    dt_str = str(dt_str).strip()
    
    # Reemplazar Z por +00:00 para formato ISO
    if dt_str.endswith('Z'):
        dt_str = dt_str[:-1] + '+00:00'
    
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        # Intentar otros formatos comunes
        formats = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S.%f"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(dt_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"No se pudo parsear datetime: {dt_str}")


def validate_timestamp(timestamp: str) -> bool:
    """
    Valida que un timestamp tenga formato ISO válido.
    
    Args:
        timestamp: Timestamp a validar
        
    Returns:
        bool: True si es válido
    """
    try:
        parse_datetime(timestamp)
        return True
    except (ValueError, AttributeError):
        return False


def extract_metadata(content: str) -> Dict[str, Any]:
    """
    Extrae metadatos del contenido.
    
    Args:
        content: Contenido del mensaje
        
    Returns:
        Dict[str, Any]: Metadatos extraídos
    """
    stats = calculate_message_stats(content)
    
    # Detectar si tiene preguntas
    has_question = '?' in content
    
    # Detectar si tiene exclamaciones
    has_exclamation = '!' in content
    
    # Detectar si tiene URLs (simple)
    url_pattern = r'https?://[^\s]+'
    has_url = bool(re.search(url_pattern, content))
    
    # Detectar si tiene menciones (simple)
    mention_pattern = r'@\w+'
    has_mentions = bool(re.search(mention_pattern, content))
    
    return {
        **stats,
        "has_question": has_question,
        "has_exclamation": has_exclamation,
        "has_url": has_url,
        "has_mentions": has_mentions
    }


def generate_error_response(
    error_message: str, 
    error_code: str = "INTERNAL_ERROR",
    status_code: int = 500,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Genera una respuesta de error estandarizada.
    
    Args:
        error_message: Mensaje de error
        error_code: Código de error
        status_code: Código HTTP
        details: Detalles adicionales
        
    Returns:
        Dict[str, Any]: Respuesta de error
    """
    response = {
        "error": error_message,
        "code": error_code,
        "status": status_code,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if details:
        response["details"] = details
    
    return response


def generate_success_response(
    message: str,
    data: Optional[Any] = None,
    status_code: int = 200
) -> Dict[str, Any]:
    """
    Genera una respuesta exitosa estandarizada.
    
    Args:
        message: Mensaje de éxito
        data: Datos a incluir
        status_code: Código HTTP
        
    Returns:
        Dict[str, Any]: Respuesta exitosa
    """
    response = {
        "success": True,
        "message": message,
        "status": status_code,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if data is not None:
        response["data"] = data
    
    return response


def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    """
    Valida datos contra un esquema simple.
    
    Args:
        data: Datos a validar
        schema: Esquema de validación
        
    Returns:
        List[str]: Lista de errores (vacía si es válido)
    """
    errors = []
    
    for field, field_schema in schema.items():
        # Verificar campos requeridos
        if field_schema.get("required", False) and field not in data:
            errors.append(f"Campo '{field}' es requerido")
            continue
        
        if field in data:
            value = data[field]
            expected_type = field_schema.get("type")
            
            # Validar tipo
            if expected_type == "string" and not isinstance(value, str):
                errors.append(f"Campo '{field}' debe ser string")
            elif expected_type == "integer" and not isinstance(value, int):
                errors.append(f"Campo '{field}' debe ser integer")
            elif expected_type == "datetime":
                if not isinstance(value, (str, datetime)):
                    errors.append(f"Campo '{field}' debe ser datetime o string ISO")
                elif isinstance(value, str):
                    try:
                        parse_datetime(value)
                    except ValueError:
                        errors.append(f"Campo '{field}' tiene formato datetime inválido")
            
            # Validar longitud mínima para strings
            if expected_type == "string" and isinstance(value, str):
                min_length = field_schema.get("min_length")
                if min_length and len(value) < min_length:
                    errors.append(f"Campo '{field}' debe tener al menos {min_length} caracteres")
                
                max_length = field_schema.get("max_length")
                if max_length and len(value) > max_length:
                    errors.append(f"Campo '{field}' no puede exceder {max_length} caracteres")
            
            # Validar valores permitidos
            allowed_values = field_schema.get("allowed_values")
            if allowed_values and value not in allowed_values:
                errors.append(f"Campo '{field}' debe ser uno de: {', '.join(allowed_values)}")
    
    return errors


def create_message_schema() -> Dict[str, Any]:
    """
    Crea el esquema de validación para mensajes.
    
    Returns:
        Dict[str, Any]: Esquema de validación
    """
    return {
        "message_id": {
            "type": "string",
            "required": True,
            "min_length": 1,
            "max_length": 100
        },
        "session_id": {
            "type": "string",
            "required": True,
            "min_length": 1,
            "max_length": 100
        },
        "content": {
            "type": "string",
            "required": True,
            "min_length": 1,
            "max_length": 5000
        },
        "timestamp": {
            "type": "datetime",
            "required": True
        },
        "sender": {
            "type": "string",
            "required": True,
            "allowed_values": ["user", "system"]
        }
    }
