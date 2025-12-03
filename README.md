# Chat Message Processing API

## 🎯 Descripción

API RESTful para procesamiento de mensajes de chat construida con FastAPI y Python 3.10+. Esta API implementa completamente los requisitos de la prueba técnica, permitiendo crear, procesar, almacenar y recuperar mensajes de chat con validación robusta, filtrado de contenido inapropiado, paginación y manejo profesional de errores.

## ✨ Características Principales

### ✅ **Funcionalidades Implementadas**
- **POST `/api/messages/`** - Creación de mensajes con validación completa
- **GET `/api/messages/{session_id}`** - Recuperación con paginación y filtros
- **Validación Rigurosa** - Esquemas Pydantic + servicios de validación
- **Filtrado de Contenido** - Detección y reemplazo de palabras inapropiadas
- **Metadatos Automáticos** - Cálculo de longitud y conteo de palabras
- **Manejo de Errores** - Respuestas HTTP apropiadas y mensajes claros
- **Documentación Automática** - Swagger UI y ReDoc integrados
- **Arquitectura Limpia** - Separación Repositorio-Servicio-Controlador

### 🏗️ **Arquitectura Profesional**
- **Patrón Repository** - Acceso a datos abstracto y testable
- **Servicios de Negocio** - Lógica centralizada y reutilizable
- **Inyección de Dependencias** - Configuración flexible y testable
- **Validación por Capas** - Pydantic + servicios personalizados
- **Base de Datos Relacional** - SQLAlchemy con SQLite

## 🚀 Demo Rápida

### **Probar en 1 minuto:**
```bash
# 1. Clonar y configurar
git clone <repo-url>
cd chat-message-api
pip install -r requirements.txt

# 2. Inicializar base de datos
python -c "from app.models.database import init_db; init_db()"

# 3. Ejecutar API
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 4. Abrir documentación interactiva
# http://localhost:8000/docs
# http://localhost:8000/redoc
```

### **Ejemplo de Prueba Técnica Funcionando:**
```bash
# Usar el ejemplo EXACTO de la prueba técnica
curl -X POST "http://localhost:8000/api/messages/" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "msg-123456",
    "session_id": "session-abcdef",
    "content": "Hola, ¿cómo puedo ayudarte hoy?",
    "timestamp": "2023-12-01T10:30:00Z",
    "sender": "system"
  }'
```

## 📋 Tabla de Contenidos

- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Instalación Rápida](#-instalación-rápida)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Esquemas de Datos](#-esquemas-de-datos)
- [Flujos de Procesamiento](#-flujos-de-procesamiento)
- [Manejo de Errores](#-manejo-de-errores)
- [Ejemplos de Uso](#-ejemplos-de-uso)
- [Pruebas](#-pruebas)
- [Desarrollo](#-desarrollo)
- [Despliegue](#-despliegue)

## 🏗️ Arquitectura del Sistema

### **Diagrama de Componentes**
```
┌─────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │  Endpoints  │  │   Routers   │  │ Middleware  │  │
│  │  (Controllers)│  │            │  │             │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │
└─────────┼─────────────────┼─────────────────┼─────────┘
          │                 │                 │
┌─────────┼─────────────────┼─────────────────┼─────────┐
│         ▼                 ▼                 ▼         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Services  │  │ Validation  │  │ Processing  │  │
│  │   Layer     │  │  Service    │  │  Service    │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │
└─────────┼─────────────────┼─────────────────┼─────────┘
          │                 │                 │
┌─────────┼─────────────────┼─────────────────┼─────────┐
│         ▼                 ▼                 ▼         │
│  ┌─────────────┐  ┌───────────────────────────────┐  │
│  │ Repository  │  │      Data Models Layer        │  │
│  │   Layer     │  │  (SQLAlchemy + Pydantic)      │  │
│  └──────┬──────┘  └──────────────┬────────────────┘  │
└─────────┼─────────────────────────┼───────────────────┘
          │                         │
          ▼                         ▼
┌─────────────────────────────────────────────────────┐
│              Database (SQLite)                      │
└─────────────────────────────────────────────────────┘
```

### **Estructura del Proyecto**
```
chat-message-api/
├── app/
│   ├── main.py                      # Aplicación FastAPI
│   ├── api/endpoints/               # Controladores
│   │   ├── messages.py              # POST/GET mensajes
│   │   └── health.py                # Health check
│   ├── core/                        # Configuración
│   │   ├── config.py                # Variables de entorno
│   │   └── dependencies.py          # Inyección de dependencias
│   ├── models/                      # Modelos SQLAlchemy
│   │   ├── message.py               # Modelo Message
│   │   └── database.py              # Configuración BD
│   ├── schemas/                     # Esquemas Pydantic
│   │   ├── message.py               # MessageCreate, Response
│   │   └── responses.py             # Respuestas estandarizadas
│   ├── services/                    # Lógica de negocio
│   │   ├── message_service.py       # Servicio principal
│   │   ├── validation_service.py    # Validación avanzada
│   │   └── processing_service.py    # Procesamiento contenido
│   ├── repositories/                # Acceso a datos
│   │   └── message_repository.py    # Operaciones CRUD
│   └── utils/                       # Utilidades
│       └── helpers.py               # Funciones auxiliares
├── tests/                           # Suite de pruebas
├── requirements.txt                 # Dependencias
├── .env.example                     # Variables de entorno
└── README.md                        # Documentación
```

## ⚡ Instalación Rápida

### **Prerrequisitos**
- Python 3.10 o superior
- pip (gestor de paquetes)

### **Instalación en 4 pasos**

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd chat-message-api

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar e inicializar
cp .env.example .env
python -c "from app.models.database import init_db; init_db()"
```

### **Ejecutar la API**

```bash
# Desarrollo (con recarga automática)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Producción
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### **Acceder a Documentación**
- **Swagger UI (Interactivo):** http://localhost:8000/docs
- **ReDoc (Alternativa):** http://localhost:8000/redoc
- **OpenAPI Spec:** http://localhost:8000/openapi.json

## 🌐 Endpoints de la API

### **1. POST `/api/messages/` - Crear Mensaje**

**Descripción:** Crea un nuevo mensaje con validación completa y procesamiento.

**Request:**
```json
{
  "message_id": "msg-123456",
  "session_id": "session-abcdef",
  "content": "Hola, ¿cómo puedo ayudarte hoy?",
  "timestamp": "2023-12-01T10:30:00Z",
  "sender": "system"
}
```

**Validaciones aplicadas:**
- ✅ Campos requeridos presentes
- ✅ `sender` solo "user" o "system"
- ✅ `timestamp` no puede ser futuro
- ✅ `message_id` único (no duplicado)
- ✅ `content` no vacío

**Procesamiento automático:**
1. **Filtrado de contenido:** Palabras inapropiadas → asteriscos
2. **Cálculo de metadatos:** Longitud y conteo de palabras
3. **Almacenamiento:** Persistencia en SQLite

**Respuesta Exitosa (201):**
```json
{
  "success": true,
  "message": "Message created successfully",
  "data": {
    "id": 1,
    "message_id": "msg-123456",
    "session_id": "session-abcdef",
    "content": "Hola, ¿cómo puedo ayudarte hoy?",
    "original_content": "Hola, ¿cómo puedo ayudarte hoy?",
    "has_inappropriate_content": false,
    "timestamp": "2023-12-01T10:30:00",
    "sender": "system",
    "message_length": 31,
    "word_count": 5,
    "created_at": "2025-12-03T19:17:55.685688",
    "updated_at": "2025-12-03T19:17:55.685695"
  },
  "timestamp": "2025-12-03T19:17:55.705945"
}
```

### **2. GET `/api/messages/{session_id}` - Obtener Mensajes por Sesión**

**Descripción:** Recupera mensajes con paginación y filtros.

**Parámetros de Query:**
| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `sender` | string | null | Filtrar por "user" o "system" |
| `limit` | integer | 50 | Máximo resultados (1-100) |
| `offset` | integer | 0 | Para paginación |

**Ejemplos:**
```
GET /api/messages/session-abcdef
GET /api/messages/session-abcdef?sender=user
GET /api/messages/session-abcdef?limit=10&offset=0
GET /api/messages/session-abcdef?sender=system&limit=20&offset=10
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Messages retrieved successfully",
  "data": [...],
  "pagination": {
    "total": 15,
    "limit": 10,
    "offset": 0,
    "has_more": true
  }
}
```

### **3. GET `/health` - Health Check**

**Descripción:** Verifica estado de la API y dependencias.

**Respuesta:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-12-03T19:18:39.748614",
  "database": "healthy"
}
```

### **4. GET `/` - Página Principal**

**Descripción:** Información básica y endpoints disponibles.

**Respuesta:**
```json
{
  "message": "Welcome to the Chat Message Processing API",
  "version": "1.0.0",
  "docs": "/docs",
  "endpoints": {
    "create_message": "POST /api/messages/",
    "get_messages": "GET /api/messages/{session_id}",
    "health": "GET /health"
  }
}
```

## 📊 Esquemas de Datos

### **Message Model (SQLAlchemy)**
```python
class MessageModel(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String(255), unique=True, nullable=False, index=True)
    session_id = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)  # Contenido filtrado
    original_content = Column(Text, nullable=False)  # Contenido original
    has_inappropriate_content = Column(Boolean, default=False)
    timestamp = Column(DateTime, nullable=False)
    sender = Column(String(50), nullable=False)  # "user" o "system"
    message_length = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### **Esquemas Pydantic**

#### **MessageCreate (Entrada)**
```python
class MessageCreate(MessageBase):
    """Esquema para crear mensajes"""
    
    @validator('sender')
    def validate_sender(cls, v):
        if v not in ['user', 'system']:
            raise ValueError('sender must be "user" or "system"')
        return v
    
    @validator('timestamp')
    def validate_timestamp_not_future(cls, v):
        if v > datetime.now(timezone.utc):
            raise ValueError('timestamp cannot be in the future')
        return v
```

#### **MessageResponse (Salida)**
```python
class MessageResponse(MessageBase):
    """Esquema para respuestas de mensajes"""
    id: int
    original_content: str
    message_length: int
    word_count: int
    has_inappropriate_content: bool
    created_at: datetime
    updated_at: datetime
```

## 🔄 Flujos de Procesamiento

### **Flujo: Creación de Mensaje**

```
1. Cliente → POST /api/messages/ → JSON
2. FastAPI → MessageCreate Schema → Validación básica
3. ValidationService → Validación avanzada
   - Estructura campos
   - Contenido y formato
   - Timestamp válido
4. ProcessingService → Procesamiento
   - Filtrar contenido inapropiado
   - Calcular metadatos
   - Sanitizar datos
5. MessageRepository → Persistencia
   - Verificar duplicados
   - Crear en SQLite
6. MessageResponse → Serialización → Cliente
```

### **Flujo: Filtrado de Contenido**

```python
# Ejemplo de filtrado
entrada = "Este mensaje tiene badword1 contenido"
procesado = "Este mensaje tiene ******** contenido"
has_inappropriate = True
```

**Palabras filtradas por defecto:**
- `badword1`
- `badword2` 
- `inappropriate`
- `offensive`

### **Flujo: Cálculo de Metadatos**

```python
content = "Hola, ¿cómo estás?"
message_length = len(content)  # 17 caracteres
word_count = len(content.split())  # 3 palabras
```

## ⚠️ Manejo de Errores

### **Códigos HTTP y Significado**

| Código | Descripción | Ejemplo |
|--------|-------------|---------|
| 200 | OK | Operación exitosa |
| 201 | Created | Mensaje creado exitosamente |
| 400 | Bad Request | Datos inválidos en solicitud |
| 409 | Conflict | ID de mensaje duplicado |
| 422 | Unprocessable Entity | Error validación Pydantic |
| 500 | Internal Server Error | Error interno del servidor |

### **Ejemplos de Respuestas de Error**

**Error de Validación (400):**
```json
{
  "error": "sender debe ser 'user' o 'system'",
  "code": "VALIDATION_ERROR",
  "status": 400,
  "timestamp": "2025-12-03T19:17:55.705945"
}
```

**Mensaje Duplicado (409):**
```json
{
  "error": "Message with ID 'msg-123456' already exists",
  "code": "DUPLICATE_MESSAGE",
  "status": 409
}
```

**Error de Esquema Pydantic (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "timestamp"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## 💡 Ejemplos de Uso

### **Usando curl**

```bash
# 1. Health check
curl -X GET "http://localhost:8000/health"

# 2. Crear mensaje (ejemplo prueba técnica)
curl -X POST "http://localhost:8000/api/messages/" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "msg-123456",
    "session_id": "session-abcdef",
    "content": "Hola, ¿cómo puedo ayudarte hoy?",
    "timestamp": "2023-12-01T10:30:00Z",
    "sender": "system"
  }'

# 3. Crear mensaje con contenido inapropiado
curl -X POST "http://localhost:8000/api/messages/" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "msg-bad-001",
    "session_id": "session-test",
    "content": "Mensaje con badword1 contenido",
    "timestamp": "2023-12-01T10:30:00Z",
    "sender": "user"
  }'

# 4. Obtener mensajes
curl -X GET "http://localhost:8000/api/messages/session-abcdef"

# 5. Obtener con filtros
curl -X GET "http://localhost:8000/api/messages/session-abcdef?sender=system&limit=5"
```

### **Usando Python (requests)**

```python
import requests
from datetime import datetime, timezone

BASE_URL = "http://localhost:8000"

# 1. Crear mensaje
message = {
    "message_id": f"msg-{datetime.now().strftime('%Y%m%d%H%M%S')}",
    "session_id": "session-python-client",
    "content": "Mensaje desde Python con badword1",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "sender": "user"
}

response = requests.post(f"{BASE_URL}/api/messages/", json=message)
print(f"Status: {response.status_code}")
print(f"Mensaje creado: {response.json()['data']['id']}")

# 2. Obtener mensajes
response = requests.get(f"{BASE_URL}/api/messages/session-python-client")
messages = response.json()['data']
print(f"Mensajes obtenidos: {len(messages)}")
```

### **Usando Swagger UI Interactivo**
1. Navegar a: `http://localhost:8000/docs`
2. Expandir `POST /api/messages/`
3. Hacer clic en "Try it out"
4. Pegar JSON de ejemplo
5. Hacer clic en "Execute"
6. Ver respuesta en tiempo real

## 🧪 Pruebas

### **Ejecutar Pruebas**

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con cobertura
pytest --cov=app --cov-report=term-missing

# Ejecutar pruebas específicas
pytest tests/test_services.py -v
pytest tests/test_endpoints.py -v

# Generar reporte HTML de cobertura
pytest --cov=app --cov-report=html
```

### **Tipos de Pruebas Implementadas**

1. **Pruebas de Servicios** (`tests/test_services.py`)
   - Validación de mensajes
   - Procesamiento de contenido
   - Lógica de negocio

2. **Pruebas de Endpoints** (`tests/test_endpoints.py`)
   - Creación de mensajes
   - Recuperación con filtros
   - Manejo de errores

3. **Pruebas de Repositorio** (`tests/test_repositories.py`)
   - Operaciones CRUD
   - Consultas con filtros
   - Manejo de transacciones

### **Ejemplo de Prueba**

```python
def test_create_message_with_bad_words():
    """Prueba que el filtrado de contenido funciona"""
    service = ProcessingService()
    
    content = "Mensaje con badword1 ofensivo"
    filtered, has_inappropriate = service.filter_inappropriate_content(content)
    
    assert has_inappropriate == True
    assert "badword1" not in filtered
    assert "********" in filtered
```

## 🛠️ Desarrollo

### **Configuración de Desarrollo**

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd chat-message-api

# 2. Configurar entorno de desarrollo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Dependencias desarrollo

# 3. Configurar pre-commit hooks (opcional)
pre-commit install

# 4. Ejecutar en modo desarrollo
python -m uvicorn app.main:app --reload
```

### **Estructura de Commits**

```bash
# Convención de commits
git commit -m "feat: add message validation service"
git commit -m "fix: resolve duplicate message_id issue"
git commit -m "docs: update API documentation"
git commit -m "test: add integration tests for endpoints"
```

### **Código de Ejemplo: Agregar Nueva Función**

```python
# En app/services/processing_service.py
class ProcessingService:
    
    @staticmethod
    def new_feature(content: str) -> Dict[str, Any]:
        """
        Nueva funcionalidad de ejemplo.
        
        Args:
            content: Contenido a procesar
            
        Returns:
            Dict[str, Any]: Resultados del procesamiento
        """
        # Implementación aquí
        return {"result": "processed"}
```

## 🚀 Despliegue

### **Configuración para Producción**

```env
# .env para producción
APP_NAME="Chat Message API"
DEBUG=False
DATABASE_URL="sqlite:///./prod_messages.db"
HOST="0.0.0.0"
PORT=8000
```

### **Usando Docker**

```bash
# Construir imagen
docker build -t chat-message-api .

# Ejecutar contenedor
docker run -p 8000:8000 \
  -e DATABASE_URL="sqlite:///./data/chat_messages.db" \
  -v ./data:/app/data \
  chat-message-api
```

### **Usando Docker Compose**

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./data/chat_messages.db
    volumes:
      - ./data:/app/data
```

### **Despliegue en Servidores**

```bash
# 1. Copiar código al servidor
scp -r chat-message-api user@server:/opt/

# 2. Instalar dependencias
ssh user@server "cd /opt/chat-message-api && pip install -r requirements.txt"

# 3. Configurar systemd service
sudo cp chat-message-api.service /etc/systemd/system/
sudo systemctl enable chat-message-api
sudo systemctl start chat-message-api

# 4. Configurar nginx como reverse proxy
# /etc/nginx/sites-available/chat-api
server {
    listen 80;
    server_name api.tudominio.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📈 Monitoreo y Métricas

### **Endpoints de Salud**

```bash
# Health check básico
GET /health

# Liveness probe (Kubernetes)
GET /health/live

# Readiness probe (Kubernetes)  
GET /health/ready
```

### **Métricas Recomendadas**

```python
# Puntos de instrumentación
metrics = {
    "messages_created_total": "Contador de mensajes creados",
    "messages_retrieved_total": "Contador de mensajes recuperados",
    "messages_with_inappropriate_content": "Mensajes filtrados",
    "api_request_duration_seconds": "Duración de peticiones",
    "api_errors_total": "Errores por tipo"
}
```

## 🔧 Configuración Avanzada

### **Personalizar Palabras Inapropiadas**

```python
# En app/services/processing_service.py
class ProcessingService:
    INAPPROPRIATE_WORDS = [
        "badword1",
        "badword2", 
        "inappropriate",
        "offensive",
        # Agregar nuevas palabras
        "nuevapalabra",
        "otrapalabra"
    ]
```

### **Cambiar a PostgreSQL**

```env
# .env
DATABASE_URL="postgresql://user:password@localhost/chat_db"
```

```bash
# Instalar driver PostgreSQL
pip install psycopg2-binary

# Actualizar requirements.txt
echo "psycopg2-binary==2.9.6" >> requirements.txt
```

### **Configurar Logging**

```python
# En app/core/config.py
import logging

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "default",
        }
    },
    "loggers": {
        "app": {
            "handlers": ["console", "file"],
            "level": "INFO",
        }
    }
}
```

## 🤝 Contribución

### **Proceso de Contribución**

1. **Fork** el repositorio
2. **Crear rama** para tu feature:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. **Commit** tus cambios:
   ```bash
   git commit -m "feat: add nueva funcionalidad"
   ```
4. **Push** a la rama:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. **Abrir Pull Request**

### **Guías de Estilo**

- **Código:** PEP 8, type hints, docstrings
- **Commits:** Conventional Commits
- **Documentación:** Markdown con ejemplos claros
- **Pruebas:** pytest con cobertura >80%

### **Reportar Issues**

Al reportar un issue, incluir:
1. Versión de la API
2. Pasos para reproducir
3. Comportamiento esperado vs actual
4. Logs de error relevantes
5. Entorno (SO, Python version, etc.)

## 📚 Recursos Adicionales

### **Documentación Oficial**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pytest Documentation](https://docs.pytest.org/)

### **Tutoriales Relacionados**
- [Building REST APIs with FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [Testing FastAPI Applications](https://fastapi.tiangolo.com/tutorial/testing/)

### **Herramientas Recomendadas**
- **Postman/Insomnia:** Para probar endpoints
- **SQLite Browser:** Para inspeccionar base de datos
- **pytest-cov:** Para cobertura de pruebas
- **pre-commit:** Para hooks de git

## 🏆 Cumplimiento de Requisitos Técnicos

### **✅ Requisitos Funcionales Completados**

| Requisito | Estado | Detalles |
|-----------|--------|----------|
| POST /api/messages/ | ✅ | Validación, procesamiento, almacenamiento |
| GET /api/messages/{session_id} | ✅ | Paginación, filtros por sender |
| Validación formato mensaje | ✅ | Pydantic + servicios personalizados |
| Procesamiento mensajes | ✅ | Filtrado contenido + metadatos |
| Almacenamiento SQLite | ✅ | SQLAlchemy con modelo completo |
| Manejo errores apropiado | ✅ | Códigos HTTP + mensajes claros |

### **✅ Organización del Código**

| Principio | Implementación |
|-----------|----------------|
| Separación responsabilidades | ✅ Controllers/Services/Repositories |
| Inyección dependencias | ✅ FastAPI Depends |
| Principios SOLID | ✅ Cumplidos en arquitectura |
| Código mantenible | ✅ Estructura clara, documentada |


## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.


## 📞 Soporte

Para soporte o preguntas:

1. **Revisar documentación:** `/docs` y este README
2. **Abrir issue:** En el repositorio GitHub
3. **Contactar desarrollo:** Para consultas específicas

