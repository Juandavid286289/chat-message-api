# app/models/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.pool import StaticPool  # Para SQLite
from app.core.config import settings
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base para modelos SQLAlchemy
Base = declarative_base()

# Configurar engine de base de datos
def get_database_engine():
    """Crea y retorna el engine de SQLAlchemy"""
    database_url = settings.database_url
    
    # Configuración especial para SQLite
    connect_args = {}
    if "sqlite" in database_url:
        connect_args = {"check_same_thread": False}
        logger.info("🔧 Usando SQLite con configuración para threading")
    
    try:
        engine = create_engine(
            database_url,
            connect_args=connect_args,
            echo=settings.debug,  # Mostrar SQL en consola si DEBUG=True
            pool_pre_ping=True,   # Verificar conexión antes de usar
        )
        logger.info(f"✅ Engine de base de datos creado para: {database_url}")
        return engine
    except Exception as e:
        logger.error(f"❌ Error creando engine de base de datos: {e}")
        raise

# Crear engine y sessionmaker
engine = get_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener sesión de base de datos
def get_db():
    """
    Proveedor de dependencia para sesiones de base de datos.
    Usar con FastAPI Depends.
    """
    db = SessionLocal()
    try:
        logger.debug("📊 Sesión de base de datos creada")
        yield db
    except Exception as e:
        logger.error(f"❌ Error en sesión de BD: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        logger.debug("📊 Sesión de base de datos cerrada")

# Función para inicializar la base de datos
def init_db():
    """
    Crea todas las tablas en la base de datos.
    Ejecutar al inicio de la aplicación.
    """
    try:
        # Importar todos los modelos aquí para que SQLAlchemy los reconozca
        from app.models.message import MessageModel
        
        logger.info("🔄 Creando tablas en la base de datos...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas creadas exitosamente")
        
        # Contar mensajes existentes
        db = SessionLocal()
        count = db.query(MessageModel).count()
        db.close()
        
        logger.info(f"📊 Base de datos lista. Mensajes existentes: {count}")
        return True
    except Exception as e:
        logger.error(f"❌ Error inicializando base de datos: {e}")
        return False

# Función para limpiar la base de datos (solo desarrollo/test)
def drop_db():
    """Elimina todas las tablas (¡CUIDADO! Solo para desarrollo)"""
    if settings.ENVIRONMENT == "production":
        logger.error("🚫 No se puede dropar BD en producción!")
        return False
    
    try:
        logger.warning("⚠️  Eliminando todas las tablas...")
        Base.metadata.drop_all(bind=engine)
        logger.warning("✅ Tablas eliminadas")
        return True
    except Exception as e:
        logger.error(f"❌ Error eliminando tablas: {e}")
        return False
