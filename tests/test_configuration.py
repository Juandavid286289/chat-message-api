# tests/test_configuration.py
"""
Pruebas para la configuración de la aplicación (Segmento 1)
"""
import pytest
import os
from pathlib import Path

class TestConfiguration:
    """Pruebas de configuración base"""
    
    def test_required_files_exist(self):
        """Verificar que los archivos requeridos existen"""
        required_files = [
            "app/main.py",
            "app/core/config.py", 
            "app/models/database.py",
            "app/models/message.py",
            "requirements.txt",
            ".env.example",
            ".gitignore"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        assert len(missing_files) == 0, f"Archivos faltantes: {missing_files}"
    
    def test_config_module_imports(self):
        """Probar que el módulo de configuración se importa correctamente"""
        from app.core.config import settings
        
        assert settings is not None
        assert hasattr(settings, 'APP_NAME')
        assert hasattr(settings, 'DEBUG')
        assert hasattr(settings, 'DATABASE_URL')
        
        print(f"Configuración cargada: {settings.APP_NAME}")
    
    def test_database_module_imports(self):
        """Probar que el módulo de base de datos se importa correctamente"""
        from app.models.database import engine, get_db, init_db, SessionLocal
        
        assert engine is not None
        assert callable(get_db)
        assert callable(init_db)
        assert SessionLocal is not None
        
        print(f"Engine de BD: {engine}")
    
    def test_message_model_imports(self):
        """Probar que el modelo de mensaje se importa correctamente"""
        from app.models.message import MessageModel, Message
        
        assert MessageModel is not None
        assert Message is not None  # Alias
        
        # Verificar atributos del modelo
        assert hasattr(MessageModel, '__tablename__')
        assert MessageModel.__tablename__ == 'messages'
        
        print(f"Modelo: {MessageModel.__name__}, Tabla: {MessageModel.__tablename__}")
    
    def test_main_app_imports(self):
        """Probar que la aplicación FastAPI se importa correctamente"""
        from app.main import app
        
        assert app is not None
        assert hasattr(app, 'title')
        assert hasattr(app, 'version')
        
        print(f"Aplicación: {app.title} v{app.version}")
    
    def test_environment_variables(self):
        """Probar que las variables de entorno se cargan correctamente"""
        from app.core.config import settings
        
        # Verificar valores por defecto o cargados de .env.test
        assert isinstance(settings.APP_NAME, str)
        assert isinstance(settings.DEBUG, bool)
        assert "sqlite" in settings.DATABASE_URL  # Debería usar SQLite
        
        print(f"BD URL: {settings.DATABASE_URL}")