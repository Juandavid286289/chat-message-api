"""
Configuración simple y funcional - Sin pydantic-settings
"""
import os
import sys
from typing import List

# Cargar variables de entorno si es posible
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # No hay problema si dotenv no está instalado

class Settings:
    """Configuración ultra simple - Siempre funciona"""
    
    def __init__(self):
        # Valores por defecto que SIEMPRE funcionan
        self.APP_NAME = os.getenv("APP_NAME", "Chat Message API")
        self.DEBUG = os.getenv("DEBUG", "True").lower() == "true"
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chat_messages.db")
        
        # Manejo seguro de lista de palabras
        words_str = os.getenv("INAPPROPRIATE_WORDS", "badword1,badword2,inappropriate")
        if words_str.startswith("[") and words_str.endswith("]"):
            # Intentar como JSON
            try:
                import json
                self.INAPPROPRIATE_WORDS = json.loads(words_str)
            except:
                self.INAPPROPRIATE_WORDS = ["badword1", "badword2", "inappropriate", "offensive"]
        else:
            # Separar por comas
            self.INAPPROPRIATE_WORDS = [w.strip() for w in words_str.split(",") if w.strip()]
    
    # Propiedades en snake_case para compatibilidad
    @property
    def app_name(self):
        return self.APP_NAME
    
    @property
    def debug(self):
        return self.DEBUG
    
    @property
    def database_url(self):
        return self.DATABASE_URL
    
    @property
    def inappropriate_words(self):
        return self.INAPPROPRIATE_WORDS

# Instancia global
settings = Settings()

# Mostrar si estamos en debug
if settings.debug:
    print(f" Configuración cargada:", file=sys.stderr)
    print(f"   App: {settings.app_name}", file=sys.stderr)
    print(f"   Debug: {settings.debug}", file=sys.stderr)
    print(f"   DB: {settings.database_url}", file=sys.stderr)
