# tests/conftest.py
"""
Configuración global de pytest para el Segmento 1
"""
import pytest
import os
import sys
from pathlib import Path

# Añadir el directorio app al path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """Configurar entorno de pruebas"""
    # Crear archivo .env de prueba si no existe
    env_test_path = Path(".env.test")
    if not env_test_path.exists():
        env_test_path.write_text("""
APP_NAME="Chat Message API - Test"
DEBUG=True
ENVIRONMENT="test"
DATABASE_URL="sqlite:///./test_chat.db"
INAPPROPRIATE_WORDS=["badword1","badword2","inappropriate"]
""")
    
    # Usar .env.test para las pruebas
    os.environ["ENV_FILE"] = ".env.test"
    yield
    # Limpieza después de las pruebas
    if env_test_path.exists():
        env_test_path.unlink()