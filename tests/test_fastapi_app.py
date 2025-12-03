# tests/test_fastapi_app.py
"""
Pruebas para la aplicación FastAPI (Segmento 1)
"""
import pytest
from fastapi.testclient import TestClient

class TestFastAPIApp:
    """Pruebas de la aplicación FastAPI"""
    
    @pytest.fixture
    def client(self):
        """Fixture para cliente de prueba"""
        from app.main import app
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Probar el endpoint raíz"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"
        
        print(f"Respuesta raíz: {data}")
    
    def test_health_endpoint(self, client):
        """Probar el endpoint de health check"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "healthy"
        assert "timestamp" in data
        
        print(f"Health check: {data}")
    
    def test_docs_endpoints(self, client):
        """Probar que los endpoints de documentación existen"""
        # Swagger UI
        response = client.get("/docs")
        assert response.status_code == 200
        
        # ReDoc
        response = client.get("/redoc")
        assert response.status_code == 200
        
        # OpenAPI JSON
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        
        print("✅ Endpoints de documentación funcionando")
    
    def test_cors_headers(self, client):
        """Probar que los headers CORS están configurados"""
        response = client.get("/")
        
        # Verificar headers CORS
        headers = response.headers
        assert "access-control-allow-origin" in headers.lower()
        
        print(f"Headers CORS presentes")