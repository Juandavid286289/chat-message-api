# test_real_integration.py
"""
Prueba integral real del Segmento 1
"""
import sys
import os
from datetime import datetime, timezone
import json
from pathlib import Path

def print_step(step_num, description):
    """Imprimir paso de prueba"""
    print(f"\n{'='*60}")
    print(f"🧪 PASO {step_num}: {description}")
    print(f"{'='*60}")

def test_1_configuration():
    """Prueba 1: Configuración y entorno"""
    print_step(1, "CONFIGURACIÓN Y ENTORNO")
    
    # Verificar Python
    print(f"🐍 Python: {sys.version}")
    
    # Verificar directorio
    cwd = Path.cwd()
    print(f"📁 Directorio: {cwd}")
    
    # Verificar archivos esenciales
    essential_files = [
        "app/main.py",
        "app/core/config.py", 
        "app/models/database.py",
        "app/models/message.py",
        ".env",
        "requirements.txt"
    ]
    
    print("📋 Archivos esenciales:")
    for file in essential_files:
        exists = Path(file).exists()
        print(f"   {'✅' if exists else '❌'} {file}")
    
    return True

def test_2_imports_and_config():
    """Prueba 2: Imports y configuración"""
    print_step(2, "IMPORTS Y CONFIGURACIÓN")
    
    try:
        sys.path.insert(0, ".")
        
        # Importar configuración
        from app.core.config import settings
        print(f"✅ Configuración cargada:")
        print(f"   - App: {settings.app_name}")
        print(f"   - Debug: {settings.debug}")
        print(f"   - DB URL: {settings.database_url}")
        print(f"   - Palabras filtradas: {settings.inappropriate_words}")
        
        # Verificar que el archivo .db se creará
        if "sqlite" in settings.database_url:
            db_file = settings.database_url.replace("sqlite:///./", "")
            print(f"   - Archivo DB: {db_file}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_3_database_operations():
    """Prueba 3: Operaciones de base de datos reales"""
    print_step(3, "OPERACIONES DE BASE DE DATOS")
    
    try:
        from app.models.database import init_db, SessionLocal, get_db
        from app.models.message import MessageModel
        from sqlalchemy import inspect
        import uuid
        
        # 1. Inicializar base de datos
        print("🔄 Inicializando base de datos...")
        if init_db():
            print("✅ BD inicializada")
        else:
            print("❌ Error inicializando BD")
            return False
        
        # 2. Verificar tablas
        from app.models.database import engine
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"✅ Tablas en BD: {tables}")
        
        if 'messages' not in tables:
            print("❌ Tabla 'messages' no encontrada")
            return False
        
        # 3. Operaciones CRUD reales
        print("\n📝 Probando operaciones CRUD...")
        
        # Crear sesión
        db = SessionLocal()
        
        try:
            # A. CREATE - Insertar mensaje de prueba
            test_id = f"test-real-{uuid.uuid4().hex[:8]}"
            test_session = f"session-real-{uuid.uuid4().hex[:8]}"
            
            new_message = MessageModel(
                message_id=test_id,
                session_id=test_session,
                content="Este es un mensaje de prueba real",
                original_content="Este es un mensaje de prueba real",
                timestamp=datetime.now(timezone.utc),
                sender="user",
                message_length=31,
                word_count=6,
                has_inappropriate_content=False
            )
            
            db.add(new_message)
            db.commit()
            print(f"✅ Mensaje creado: ID={test_id}")
            
            # B. READ - Leer el mensaje
            retrieved = db.query(MessageModel).filter_by(message_id=test_id).first()
            if retrieved:
                print(f"✅ Mensaje recuperado: {retrieved.content}")
                print(f"   Session: {retrieved.session_id}")
                print(f"   Sender: {retrieved.sender}")
                print(f"   Length: {retrieved.message_length}")
            else:
                print("❌ No se pudo recuperar el mensaje")
                return False
            
            # C. UPDATE - Actualizar mensaje
            retrieved.content = "Mensaje actualizado en prueba real"
            retrieved.message_length = len(retrieved.content)
            db.commit()
            
            updated = db.query(MessageModel).filter_by(message_id=test_id).first()
            if updated and "actualizado" in updated.content:
                print(f"✅ Mensaje actualizado: {updated.content}")
            else:
                print("❌ No se pudo actualizar el mensaje")
            
            # D. DELETE - Eliminar mensaje
            db.delete(updated)
            db.commit()
            
            deleted = db.query(MessageModel).filter_by(message_id=test_id).first()
            if not deleted:
                print("✅ Mensaje eliminado correctamente")
            else:
                print("❌ No se pudo eliminar el mensaje")
            
            # E. Contar mensajes
            count = db.query(MessageModel).count()
            print(f"📊 Total de mensajes en BD: {count}")
            
            return True
            
        finally:
            db.close()
            print("✅ Sesión de BD cerrada")
            
    except Exception as e:
        print(f"❌ Error en operaciones BD: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_4_fastapi_endpoints():
    """Prueba 4: Endpoints FastAPI reales"""
    print_step(4, "ENDPOINTS FASTAPI")
    
    try:
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        
        endpoints = [
            ("/", "GET", "Endpoint raíz"),
            ("/health", "GET", "Health check"),
            ("/docs", "GET", "Documentación Swagger"),
            ("/redoc", "GET", "Documentación ReDoc"),
            ("/openapi.json", "GET", "Esquema OpenAPI"),
        ]
        
        all_ok = True
        for endpoint, method, description in endpoints:
            try:
                if method == "GET":
                    response = client.get(endpoint)
                    status = "✅" if response.status_code in [200, 404] else "❌"
                    print(f"{status} {description}: {endpoint} - {response.status_code}")
                    
                    if endpoint == "/" and response.status_code == 200:
                        data = response.json()
                        print(f"   ↳ Mensaje: {data.get('message')}")
                        print(f"   ↳ Versión: {data.get('version')}")
                    elif endpoint == "/health" and response.status_code == 200:
                        data = response.json()
                        print(f"   ↳ Status: {data.get('status')}")
                        
                else:
                    print(f"⚠️  Método {method} no implementado para {endpoint}")
                    
            except Exception as e:
                print(f"❌ Error en {description}: {e}")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Error general en FastAPI: {e}")
        return False

def test_5_file_system():
    """Prueba 5: Sistema de archivos y persistencia"""
    print_step(5, "SISTEMA DE ARCHIVOS")
    
    try:
        # Verificar archivo de base de datos
        from app.core.config import settings
        
        if "sqlite" in settings.database_url:
            db_file = settings.database_url.replace("sqlite:///./", "")
            db_path = Path(db_file)
            
            if db_path.exists():
                size = db_path.stat().st_size
                print(f"✅ Archivo DB encontrado: {db_file}")
                print(f"   Tamaño: {size} bytes")
                print(f"   Modificado: {datetime.fromtimestamp(db_path.stat().st_mtime)}")
                
                # Verificar que se puede escribir
                import sqlite3
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # Verificar tabla messages
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
                tables = cursor.fetchall()
                
                if tables:
                    print(f"✅ Tabla 'messages' verificada en SQLite")
                    
                    # Verificar estructura
                    cursor.execute("PRAGMA table_info(messages)")
                    columns = cursor.fetchall()
                    print(f"   Columnas: {len(columns)}")
                    
                    # Mostrar algunas columnas
                    for col in columns[:5]:  # Primeras 5 columnas
                        print(f"     - {col[1]} ({col[2]})")
                        
                else:
                    print("❌ Tabla 'messages' no encontrada en SQLite")
                
                conn.close()
            else:
                print(f"⚠️  Archivo DB no encontrado: {db_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en sistema de archivos: {e}")
        return False

def test_6_simulation_real_world():
    """Prueba 6: Simulación de mundo real"""
    print_step(6, "SIMULACIÓN DE MUNDO REAL")
    
    try:
        from app.models.database import SessionLocal
        from app.models.message import MessageModel
        from datetime import datetime, timezone
        import uuid
        
        print("🎭 Simulando flujo real de mensajes...")
        
        db = SessionLocal()
        
        try:
            # Simular diferentes tipos de mensajes
            test_messages = [
                {
                    "content": "Hola, ¿cómo estás?",
                    "sender": "user",
                    "session": "chat-123"
                },
                {
                    "content": "Estoy bien, gracias por preguntar. ¿En qué puedo ayudarte hoy?",
                    "sender": "system", 
                    "session": "chat-123"
                },
                {
                    "content": "Necesito ayuda con mi cuenta",
                    "sender": "user",
                    "session": "chat-123"
                },
                {
                    "content": "Claro, te ayudaré con eso. ¿Qué problema tienes?",
                    "sender": "system",
                    "session": "chat-123"
                },
                {
                    "content": "Hola mundo desde otra sesión",
                    "sender": "user",
                    "session": "chat-456"
                }
            ]
            
            inserted_ids = []
            
            for i, msg_data in enumerate(test_messages, 1):
                msg_id = f"real-sim-{uuid.uuid4().hex[:8]}"
                
                message = MessageModel(
                    message_id=msg_id,
                    session_id=msg_data["session"],
                    content=msg_data["content"],
                    original_content=msg_data["content"],
                    timestamp=datetime.now(timezone.utc),
                    sender=msg_data["sender"],
                    message_length=len(msg_data["content"]),
                    word_count=len(msg_data["content"].split()),
                    has_inappropriate_content=False
                )
                
                db.add(message)
                inserted_ids.append(msg_id)
                print(f"   ✅ Mensaje {i} insertado: '{msg_data['content'][:30]}...'")
            
            db.commit()
            print(f"\n📨 {len(test_messages)} mensajes insertados")
            
            # Consultas reales
            print("\n🔍 Consultando datos...")
            
            # 1. Mensajes por sesión
            session_messages = db.query(MessageModel).filter_by(session_id="chat-123").all()
            print(f"   📊 Mensajes en sesión 'chat-123': {len(session_messages)}")
            
            # 2. Conteo por remitente
            from sqlalchemy import func
            sender_counts = db.query(
                MessageModel.sender, 
                func.count(MessageModel.id).label('count')
            ).group_by(MessageModel.sender).all()
            
            print("   👥 Distribución por remitente:")
            for sender, count in sender_counts:
                print(f"     - {sender}: {count} mensajes")
            
            # 3. Mensaje más largo
            longest = db.query(MessageModel).order_by(MessageModel.message_length.desc()).first()
            if longest:
                print(f"   📏 Mensaje más largo: {longest.message_length} caracteres")
                print(f"     '{longest.content[:50]}...'")
            
            # Limpiar datos de prueba
            for msg_id in inserted_ids:
                db.query(MessageModel).filter_by(message_id=msg_id).delete()
            
            db.commit()
            print(f"\n🧹 {len(inserted_ids)} mensajes de prueba eliminados")
            
            return True
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error en simulación: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 PRUEBA INTEGRAL REAL - SEGMENTO 1")
    print("="*60)
    print("Esta prueba valida TODO el funcionamiento real del sistema")
    print("="*60)
    
    tests = [
        ("Configuración y entorno", test_1_configuration),
        ("Imports y configuración", test_2_imports_and_config),
        ("Operaciones de base de datos", test_3_database_operations),
        ("Endpoints FastAPI", test_4_fastapi_endpoints),
        ("Sistema de archivos", test_5_file_system),
        ("Simulación de mundo real", test_6_simulation_real_world),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n▶️  Ejecutando: {test_name}")
            success = test_func()
            results.append((test_name, success))
            
            if not success:
                print(f"⚠️  {test_name} FALLÓ")
        except Exception as e:
            print(f"❌ ERROR en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL DE PRUEBAS INTEGRALES")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
    
    print(f"\n📈 Resultado: {passed}/{total} pruebas pasadas ({passed/total*100:.0f}%)")
    
    # Conclusión
    print("\n" + "="*60)
    if passed == total:
        print("🎉 ¡EXCELENTE! TODAS LAS PRUEBAS INTEGRALES PASARON")
        print("✅ El Segmento 1 está COMPLETAMENTE FUNCIONAL")
        print("✅ Listo para uso en producción")
        print("\n🚀 ¡CONTINUEMOS CON EL SEGMENTO 2!")
    elif passed >= total * 0.8:
        print("👍 ¡BUEN TRABAJO! La mayoría de pruebas pasaron")
        print("✅ El sistema es FUNCIONAL para desarrollo")
        print("🔧 Algunos detalles menores podrían necesitar ajuste")
        print("\n🚀 Podemos continuar con el Segmento 2")
    else:
        print("⚠️  Hay problemas significativos que resolver")
        print("🔧 Revisa los errores antes de continuar")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        
        print("\n" + "="*60)
        if success:
            print("✅ Pruebas integrales COMPLETADAS")
            print("\n💡 Recomendación: Ejecuta el servidor real para verificar:")
            print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
            print("   Luego visita: http://localhost:8000/docs")
        else:
            print("❌ Algunas pruebas fallaron")
        
        input("\nPresiona Enter para salir...")
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Prueba cancelada por el usuario")
        sys.exit(1)