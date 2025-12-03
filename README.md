# Chat Message Processing API

## Descripción

API RESTful para procesamiento de mensajes de chat construida con FastAPI y Python 3.10+. Esta API permite crear, procesar, almacenar y recuperar mensajes de chat con características como validación, filtrado de contenido inapropiado y paginación.

## Características Principales

- ✅ **CRUD de Mensajes**: Crear y recuperar mensajes de chat
- ✅ **Validación Rigurosa**: Validación de formato y campos requeridos
- ✅ **Filtrado de Contenido**: Detección y filtrado de palabras inapropiadas
- ✅ **Metadatos Automáticos**: Cálculo de longitud y conteo de palabras
- ✅ **Paginación y Filtros**: Recuperación paginada con filtros por remitente
- ✅ **Manejo de Errores**: Respuestas HTTP apropiadas y mensajes claros
- ✅ **Pruebas Unitarias**: Cobertura completa de pruebas
- ✅ **Documentación Automática**: Swagger UI y ReDoc integrados
- ✅ **Arquitectura Limpia**: Separación de responsabilidades (Repositorio-Servicio-Controlador)

## Tecnologías Utilizadas

- **Python 3.10+**
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para manejo de base de datos
- **SQLite** - Base de datos ligera (por simplicidad)
- **Pydantic** - Validación de datos y serialización
- **Pytest** - Framework de pruebas

## Estructura del Proyecto

```
chat-message-api/
├── app/
│   ├── __init__.py
│   ├── main.py                      # Aplicación principal FastAPI
│   ├── api/                         # Capa de presentación
│   │   ├── __init__.py
│   │   ├── endpoints/               # Controladores/Endpoints
│   │   │   ├── __init__.py
│   │   │   ├── messages.py          # Endpoints de mensajes
│   │   │   └── health.py            # Endpoint de health check
│   ├── core/                        # Configuración y utilidades core
│   │   ├── __init__.py
│   │   ├── config.py                # Configuración de la aplicación
│   │   ├── dependencies.py          # Inyección de dependencias
│   │   └── security.py              # Seguridad (si se implementa)
│   ├── models/                      # Modelos de datos
│   │   ├── __init__.py
│   │   ├── message.py               # Modelo SQLAlchemy
│   │   └── database.py              # Configuración de base de datos
│   ├── schemas/                     # Esquemas Pydantic
│   │   ├── __init__.py
│   │   ├── message.py               # Esquemas de mensajes
│   │   └── responses.py             # Respuestas estandarizadas
│   ├── services/                    # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── message_service.py       # Servicio principal
│   │   ├── processing_service.py    # Procesamiento de mensajes
│   │   └── validation_service.py    # Validación de mensajes
│   ├── repositories/                # Capa de acceso a datos
│   │   ├── __init__.py
│   │   └── message_repository.py    # Operaciones CRUD
│   └── utils/                       # Utilidades generales
│       ├── __init__.py
│       └── helpers.py               # Funciones auxiliares
├── tests/                           # Pruebas unitarias e integración
│   ├── __init__.py
│   ├── conftest.py                  # Configuración de pytest
│   ├── test_models.py               # Pruebas de modelos
│   ├── test_services.py             # Pruebas de servicios
│   ├── test_repositories.py         # Pruebas de repositorios
│   └── test_endpoints.py            # Pruebas de endpoints
├── .env.example                     # Variables de entorno de ejemplo
├── .gitignore                       # Archivos ignorados por Git
├── requirements.txt                 # Dependencias del proyecto
├── setup.py                         # Configuración del paquete
└── README.md                        # Este archivo
```

## Instalación y Configuración

### Prerrequisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git (opcional)

### Instalación Local

1. **Clonar el repositorio** (si aplica):
```bash
git clone <repo-url>
cd chat-message-api
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**:
```bash
cp .env.example .env
# Editar .env según sea necesario
```

5. **Inicializar la base de datos**:
```bash
# Esto creará la base de datos SQLite con las tablas necesarias
python -c "from app.models.database import init_db; init_db()"
```

6. **Ejecutar la aplicación**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Usando Docker

1. **Construir y ejecutar con Docker Compose**:
```bash
docker-compose up --build
```

2. **Solo con Docker**:
```bash
docker build -t chat-message-api .
docker run -p 8000:8000 chat-message-api
```

## Uso de la API

### Documentación Interactiva

Una vez ejecutada la aplicación, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principales

#### 1. Crear un Mensaje
**POST** `/api/messages/`

Crea un nuevo mensaje de chat con procesamiento automático.

**Request Body**:
```json
{
  "message_id": "msg-123456",
  "session_id": "session-abcdef",
  "content": "Hola, ¿cómo puedo ayudarte hoy?",
  "timestamp": "2023-12-01T10:30:00Z",
  "sender": "system"
}
```

**Respuesta Exitosa (201 Created)**:
```json
{
  "message_id": "msg-123456",
  "session_id": "session-abcdef",
  "content": "Hola, ¿cómo puedo ayudarte hoy?",
  "timestamp": "2023-12-01T10:30:00Z",
  "sender": "system",
  "id": 1,
  "original_content": "Hola, ¿cómo puedo ayudarte hoy?",
  "message_length": 27,
  "word_count": 5,
  "created_at": "2023-12-01T10:30:01Z"
}
```

#### 2. Obtener Mensajes por Sesión
**GET** `/api/messages/{session_id}`

Recupera todos los mensajes de una sesión específica con paginación.

**Parámetros de Query**:
- `sender` (opcional): Filtrar por remitente ("user" o "system")
- `limit` (opcional, default: 50): Número máximo de mensajes a retornar (1-100)
- `offset` (opcional, default: 0): Número de mensajes a saltar (para paginación)

**Ejemplo**:
```
GET /api/messages/session-abcdef?sender=user&limit=20&offset=0
```

**Respuesta Exitosa (200 OK)**:
```json
[
  {
    "message_id": "msg-123456",
    "session_id": "session-abcdef",
    "content": "Hola, ¿cómo puedo ayudarte hoy?",
    "timestamp": "2023-12-01T10:30:00Z",
    "sender": "system",
    "id": 1,
    "original_content": "Hola, ¿cómo puedo ayudarte hoy?",
    "message_length": 27,
    "word_count": 5,
    "created_at": "2023-12-01T10:30:01Z"
  }
]
```

#### 3. Health Check
**GET** `/health/`

Verifica el estado de la API.

**Respuesta**:
```json
{
  "status": "healthy"
}
```

## Ejemplos de Uso

### Usando curl

```bash
# Crear un mensaje
curl -X POST "http://localhost:8000/api/messages/" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "msg-001",
    "session_id": "session-123",
    "content": "Hello, this is a test message",
    "timestamp": "2023-12-01T10:30:00Z",
    "sender": "user"
  }'

# Obtener mensajes de una sesión
curl "http://localhost:8000/api/messages/session-123?limit=10&offset=0"
```

### Usando Python (requests)

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Crear mensaje
message_data = {
    "message_id": "msg-python-001",
    "session_id": "session-python-456",
    "content": "Mensaje desde Python",
    "timestamp": "2023-12-01T10:30:00Z",
    "sender": "system"
}

response = requests.post(f"{BASE_URL}/api/messages/", json=message_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Obtener mensajes
response = requests.get(
    f"{BASE_URL}/api/messages/session-python-456",
    params={"limit": 10, "offset": 0}
)
messages = response.json()
print(f"Total messages: {len(messages)}")
```

## Características de Procesamiento

### Validación
- Campos requeridos: `message_id`, `session_id`, `content`, `timestamp`, `sender`
- `sender` solo acepta "user" o "system"
- `timestamp` no puede ser en el futuro
- `content` no puede estar vacío
- `message_id` debe ser único

### Filtrado de Contenido
La API detecta y filtra automáticamente palabras inapropiadas:
- Palabras filtradas: ["badword1", "badword2", "inappropriate"]
- Las palabras inapropiadas son reemplazadas por asteriscos
- Se preserva el contenido original en `original_content`

### Metadatos Automáticos
Para cada mensaje, se calculan:
- `message_length`: Longitud del contenido filtrado
- `word_count`: Número de palabras en el contenido

## Manejo de Errores

La API retorna códigos HTTP apropiados:

| Código | Descripción | Ejemplo |
|--------|-------------|---------|
| 200 | OK | Operación exitosa |
| 201 | Created | Mensaje creado exitosamente |
| 400 | Bad Request | Datos inválidos en la solicitud |
| 404 | Not Found | Sesión no encontrada |
| 409 | Conflict | ID de mensaje duplicado |
| 422 | Unprocessable Entity | Error de validación de datos |
| 500 | Internal Server Error | Error interno del servidor |

**Ejemplo de error**:
```json
{
  "detail": "Message with ID msg-123456 already exists"
}
```

## Ejecución de Pruebas

### Pruebas Unitarias

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas con cobertura
pytest --cov=app --cov-report=term-missing

# Generar reporte HTML de cobertura
pytest --cov=app --cov-report=html
```

### Tipos de Pruebas

1. **Pruebas de Modelos**: Verifican el comportamiento de los modelos de datos
2. **Pruebas de Repositorios**: Prueban las operaciones de base de datos
3. **Pruebas de Servicios**: Verifican la lógica de negocio
4. **Pruebas de Endpoints**: Pruebas de integración de la API

## Configuración Avanzada

### Variables de Entorno

Crea un archivo `.env` con las siguientes variables:

```env
# Entorno de ejecución
APP_NAME="Chat Message API"
DEBUG=False

# Base de datos
DATABASE_URL="sqlite:///./chat_messages.db"

# Para producción, puedes usar PostgreSQL:
# DATABASE_URL="postgresql://user:password@localhost/chat_db"

# Configuración de servidor
HOST="0.0.0.0"
PORT=8000
```

### Usando PostgreSQL

1. Cambiar `DATABASE_URL` en `.env`:
```env
DATABASE_URL="postgresql://postgres:password@localhost/chat_db"
```

2. Instalar dependencias adicionales:
```bash
pip install psycopg2-binary
```

3. Actualizar `requirements.txt`

## Puntos Extra Implementados

### Dockerización
- **Dockerfile** para contenerización de la aplicación
- **docker-compose.yml** para orquestación
- Base de datos SQLite persistente en volumen

### Arquitectura Limpia
- Separación clara de responsabilidades
- Patrón Repositorio para acceso a datos
- Servicios para lógica de negocio
- Inyección de dependencias

### Documentación Completa
- Documentación automática con Swagger
- README detallado
- Ejemplos de uso
- Configuración paso a paso

## Posibles Mejoras Futuras

1. **Autenticación**: Implementar JWT o API keys
2. **Rate Limiting**: Limitar peticiones por usuario/IP
3. **WebSocket**: Endpoint para mensajes en tiempo real
4. **Búsqueda**: Funcionalidad de búsqueda full-text
5. **Métricas**: Integración con Prometheus/Grafana
6. **Logging**: Sistema de logging estructurado
7. **Cache**: Implementar Redis para caché
8. **Mensajería**: Integración con RabbitMQ/Kafka

## Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte o preguntas:
1. Revisa la documentación en `/docs`
2. Abre un issue en el repositorio
3. Contacta al equipo de desarrollo

---

**Nota**: Esta es una API de ejemplo para evaluación técnica. En producción, considera implementar autenticación, rate limiting, y usar una base de datos más robusta como PostgreSQL.