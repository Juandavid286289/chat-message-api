# app/services/validation_service.py
"""
Servicio de validación de mensajes.
Contiene lógica para validar formato, contenido y reglas de negocio.
"""
import re
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime, timezone
from app.core.config import settings

class ValidationService:
    """
    Servicio para validar mensajes de chat.
    Implementa validaciones de formato, contenido y reglas de negocio.
    """
    
    # Expresiones regulares para validaciones
    MESSAGE_ID_PATTERN = re.compile(r'^[a-zA-Z0-9\-_\.]+$')
    SESSION_ID_PATTERN = re.compile(r'^[a-zA-Z0-9\-_]+$')
    
    @staticmethod
    def validate_message_structure(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida la estructura básica del mensaje.
        
        Args:
            data: Diccionario con los datos del mensaje
            
        Returns:
            Tuple[bool, List[str]]: (es_válido, lista_de_errores)
        """
        errors = []
        
        # Campos requeridos
        required_fields = ["message_id", "session_id", "content", "timestamp", "sender"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Campo requerido faltante: {field}")
        
        # Tipos de datos básicos
        if "content" in data and not isinstance(data["content"], str):
            errors.append("El campo 'content' debe ser una cadena de texto")
        
        if "sender" in data and not isinstance(data["sender"], str):
            errors.append("El campo 'sender' debe ser una cadena de texto")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_message_content(content: str) -> Tuple[bool, List[str]]:
        """
        Valida el contenido del mensaje.
        
        Args:
            content: Contenido del mensaje a validar
            
        Returns:
            Tuple[bool, List[str]]: (es_válido, lista_de_errores)
        """
        errors = []
        
        # Longitud mínima
        if not content or len(content.strip()) == 0:
            errors.append("El contenido del mensaje no puede estar vacío")
            return False, errors
        
        # Longitud máxima
        max_length = getattr(settings, 'max_content_length', 5000)
        if len(content) > max_length:
            errors.append(f"El contenido excede la longitud máxima de {max_length} caracteres")
        
        # Contenido solo espacios en blanco
        if content.strip() == "":
            errors.append("El contenido no puede ser solo espacios en blanco")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_message_id(message_id: str) -> Tuple[bool, List[str]]:
        """
        Valida el formato del message_id.
        
        Args:
            message_id: ID del mensaje a validar
            
        Returns:
            Tuple[bool, List[str]]: (es_válido, lista_de_errores)
        """
        errors = []
        
        # Longitud
        max_length = getattr(settings, 'max_message_id_length', 100)
        if len(message_id) > max_length:
            errors.append(f"message_id excede la longitud máxima de {max_length} caracteres")
        
        # Formato
        if not ValidationService.MESSAGE_ID_PATTERN.match(message_id):
            errors.append("message_id solo puede contener letras, números, guiones, guiones bajos y puntos")
        
        # No vacío
        if not message_id or not message_id.strip():
            errors.append("message_id no puede estar vacío")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_session_id(session_id: str) -> Tuple[bool, List[str]]:
        """
        Valida el formato del session_id.
        
        Args:
            session_id: ID de sesión a validar
            
        Returns:
            Tuple[bool, List[str]]: (es_válido, lista_de_errores)
        """
        errors = []
        
        # Longitud
        max_length = getattr(settings, 'max_session_id_length', 100)
        if len(session_id) > max_length:
            errors.append(f"session_id excede la longitud máxima de {max_length} caracteres")
        
        # Formato básico
        if not ValidationService.SESSION_ID_PATTERN.match(session_id):
            errors.append("session_id solo puede contener letras, números, guiones y guiones bajos")
        
        # No vacío
        if not session_id or not session_id.strip():
            errors.append("session_id no puede estar vacío")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_sender(sender: str) -> Tuple[bool, List[str]]:
        """
        Valida el remitente del mensaje.
        
        Args:
            sender: Remitente a validar ('user' o 'system')
            
        Returns:
            Tuple[bool, List[str]]: (es_válido, lista_de_errores)
        """
        errors = []
        allowed_senders = ['user', 'system']
        
        if sender not in allowed_senders:
            errors.append(f"El remitente debe ser uno de: {', '.join(allowed_senders)}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_timestamp(timestamp: datetime) -> Tuple[bool, List[str]]:
        """
        Valida la marca de tiempo del mensaje.
        
        Args:
            timestamp: Marca de tiempo a validar
            
        Returns:
            Tuple[bool, List[str]]: (es_válido, lista_de_errores)
        """
        errors = []

        now = datetime.now(timezone.utc)
        one_year_ago = now.replace(year=now.year - 1)
        
        # No puede ser futura
        if timestamp > now:
            errors.append("La marca de tiempo no puede ser en el futuro")
        
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_complete_message(data: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Valida completamente un mensaje.
        
        Args:
            data: Datos completos del mensaje
            
        Returns:
            Tuple[bool, List[str], Dict[str, Any]]: 
                (es_válido, lista_de_errores, datos_validados)
        """
        all_errors = []
        validated_data = data.copy()
        
        # 1. Validar estructura básica
        structure_valid, structure_errors = ValidationService.validate_message_structure(data)
        all_errors.extend(structure_errors)
        
        if not structure_valid:
            return False, all_errors, {}
        
        # 2. Validar campos individuales
        # message_id
        msg_id_valid, msg_id_errors = ValidationService.validate_message_id(data.get("message_id", ""))
        all_errors.extend(msg_id_errors)
        
        # session_id
        session_valid, session_errors = ValidationService.validate_session_id(data.get("session_id", ""))
        all_errors.extend(session_errors)
        
        # content
        content_valid, content_errors = ValidationService.validate_message_content(data.get("content", ""))
        all_errors.extend(content_errors)
        
        # sender
        sender_valid, sender_errors = ValidationService.validate_sender(data.get("sender", ""))
        all_errors.extend(sender_errors)
        
        # timestamp (convertir string a datetime si es necesario)
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            try:
                from dateutil import parser
                timestamp = parser.isoparse(timestamp)
                validated_data["timestamp"] = timestamp
            except (ValueError, TypeError):
                all_errors.append("Formato de timestamp inválido. Use ISO 8601")
        
        if isinstance(timestamp, datetime):
            time_valid, time_errors = ValidationService.validate_timestamp(timestamp)
            all_errors.extend(time_errors)
        else:
            all_errors.append("timestamp debe ser una fecha/hora válida")
        
        # Retornar resultado
        is_valid = len(all_errors) == 0
        return is_valid, all_errors, validated_data if is_valid else {}