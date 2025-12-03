# tests/test_database.py
"""
Pruebas para la base de datos (Segmento 1)
"""
import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

class TestDatabase:
    """Pruebas de funcionalidad de base de datos"""
    
    def test_database_initialization(self):
        """Probar que la base de datos se inicializa correctamente"""
        from app.models.database import init_db, engine
        from sqlalchemy import inspect
        
        # Inicializar la base de datos
        result = init_db()
        assert result is True
        
        # Verificar que el engine está configurado
        assert engine is not None
        
        # Verificar que las tablas existen
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        assert 'messages' in tables
        print(f"Tablas creadas: {tables}")
    
    def test_message_model_creation(self):
        """Probar la creación de instancias del modelo Message"""
        from app.models.message import MessageModel
        from datetime import datetime
        
        # Crear una instancia del modelo
        test_message = MessageModel(
            message_id="test-001",
            session_id="session-001",
            content="Test content",
            original_content="Test content",
            timestamp=datetime.now(),
            sender="user",
            message_length=12,
            word_count=2
        )
        
        # Verificar atributos
        assert test_message.message_id == "test-001"
        assert test_message.session_id == "session-001"
        assert test_message.content == "Test content"
        assert test_message.sender == "user"
        assert test_message.message_length == 12
        assert test_message.word_count == 2
        
        print(f"Mensaje creado: {test_message}")
    
    def test_message_to_dict(self):
        """Probar el método to_dict del modelo"""
        from app.models.message import MessageModel
        from datetime import datetime
        
        # Crear mensaje de prueba
        timestamp = datetime.now()
        message = MessageModel(
            message_id="test-dict-001",
            session_id="session-dict-001",
            content="Dict test",
            original_content="Dict test",
            timestamp=timestamp,
            sender="system",
            message_length=9,
            word_count=2
        )
        
        # Convertir a diccionario
        message_dict = message.to_dict()
        
        # Verificar estructura
        assert isinstance(message_dict, dict)
        assert message_dict['message_id'] == "test-dict-001"
        assert message_dict['session_id'] == "session-dict-001"
        assert message_dict['content'] == "Dict test"
        assert message_dict['sender'] == "system"
        assert message_dict['message_length'] == 9
        assert 'created_at' in message_dict
        
        print(f"Dict result: {message_dict}")
    
    def test_database_session(self):
        """Probar que se puede obtener una sesión de base de datos"""
        from app.models.database import SessionLocal, get_db
        from app.models.message import MessageModel
        from datetime import datetime
        
        # Obtener sesión usando SessionLocal directamente
        db = SessionLocal()
        try:
            # Verificar que la sesión funciona
            assert db is not None
            
            # Contar mensajes (debería ser 0 inicialmente)
            count = db.query(MessageModel).count()
            print(f"Mensajes en BD: {count}")
            
            # Insertar un mensaje de prueba
            test_message = MessageModel(
                message_id="test-session-001",
                session_id="session-test-001",
                content="Session test",
                original_content="Session test",
                timestamp=datetime.now(),
                sender="user",
                message_length=12,
                word_count=2
            )
            
            db.add(test_message)
            db.commit()
            
            # Verificar que se insertó
            count_after = db.query(MessageModel).count()
            assert count_after == count + 1
            
            # Limpiar
            db.query(MessageModel).filter_by(message_id="test-session-001").delete()
            db.commit()
            
        finally:
            db.close()
        
        print("✅ Sesión de BD probada exitosamente")
    
    @pytest.fixture
    def test_db_session(self):
        """Fixture para sesión de prueba"""
        from app.models.database import SessionLocal
        
        db = SessionLocal()
        yield db
        db.close()
    
    def test_message_crud_operations(self, test_db_session):
        """Probar operaciones CRUD básicas"""
        from app.models.message import MessageModel
        from datetime import datetime
        import uuid
        
        db = test_db_session
        
        # Generar IDs únicos
        message_id = f"test-crud-{uuid.uuid4().hex[:8]}"
        session_id = f"session-crud-{uuid.uuid4().hex[:8]}"
        
        # 1. CREATE
        new_message = MessageModel(
            message_id=message_id,
            session_id=session_id,
            content="CRUD test content",
            original_content="CRUD test content",
            timestamp=datetime.now(),
            sender="system",
            message_length=18,
            word_count=3
        )
        
        db.add(new_message)
        db.commit()
        
        # 2. READ
        retrieved = db.query(MessageModel).filter_by(message_id=message_id).first()
        assert retrieved is not None
        assert retrieved.content == "CRUD test content"
        assert retrieved.sender == "system"
        
        # 3. UPDATE
        retrieved.content = "Updated content"
        retrieved.message_length = len("Updated content")
        db.commit()
        
        updated = db.query(MessageModel).filter_by(message_id=message_id).first()
        assert updated.content == "Updated content"
        
        # 4. DELETE
        db.delete(updated)
        db.commit()
        
        deleted = db.query(MessageModel).filter_by(message_id=message_id).first()
        assert deleted is None
        
        print("✅ Operaciones CRUD probadas exitosamente")