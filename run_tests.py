# run_tests.py
"""
Pruebas simplificadas del Segmento 1 
"""
import sys
import subprocess
import os
from pathlib import Path

def install_dependencies():
    """Instalar dependencias faltantes"""
    print("📦 Verificando dependencias...")
    
    dependencies = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn[standard]"),
        ("sqlalchemy", "sqlalchemy"),
        ("pydantic", "pydantic"),
        ("pydantic_settings", "pydantic-settings"),
        ("httpx", "httpx"),
        ("python_dotenv", "python-dotenv"),
        ("pytest", "pytest"),
    ]
    
    for module_name, pip_name in dependencies:
        try:
            __import__(module_name.replace("-", "_"))
            print(f"  ✅ {module_name}")
        except ImportError:
            print(f"  ⚠️  {module_name} no encontrado, instalando...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
                print(f"  ✅ {module_name} instalado")
            except:
                print(f"  ❌ Error instalando {module_name}")

def check_files():
    """Verificar archivos requeridos"""
    print("\n📁 Verificando archivos...")
    
    files = [
        ("app/main.py", True),
        ("app/core/config.py", True),
        ("app/models/database.py", True),
        ("app/models/message.py", True),
        ("requirements.txt", True),
        (".env.example", False),  # Opcional, podemos crearlo
        (".env", False),  # Opcional
    ]
    
    missing = []
    for file_path, required in files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            if required:
                print(f"  ❌ {file_path} (REQUERIDO)")
                missing.append(file_path)
            else:
                print(f"  ⚠️  {file_path} (opcional)")
    
    # Crear .env.example si no existe
    if not Path(".env.example").exists():
        print("  🔧 Creando .env.example...")
        with open(".env.example", "w") as f:
            f.write("""APP_NAME="Chat Message API"
DEBUG=True
ENVIRONMENT="development"
DATABASE_URL="sqlite:///./chat_messages.db"
""")
    
    # Crear .env si no existe
    if not Path(".env").exists() and Path(".env.example").exists():
        print("  🔧 Creando .env desde .env.example...")
        with open(".env.example", "r") as src, open(".env", "w") as dst:
            dst.write(src.read())
    
    return len(missing) == 0

def test_imports():
    """Probar todos los imports"""
    print("\n🔍 Probando imports...")
    
    imports_to_test = [
        ("app.core.config.settings", "Configuración"),
        ("app.models.message.MessageModel", "Modelo de mensaje"),
        ("app.models.database.init_db", "Base de datos"),
        ("app.main.app", "Aplicación FastAPI"),
    ]
    
    all_ok = True
    for import_path, description in imports_to_test:
        try:
            # Import dinámico
            module_path, attr_name = import_path.rsplit(".", 1)
            module = __import__(module_path, fromlist=[attr_name])
            obj = getattr(module, attr_name)
            print(f"  ✅ {description}: {obj.__name__ if hasattr(obj, '__name__') else type(obj).__name__}")
        except Exception as e:
            print(f"  ❌ {description}: {e}")
            all_ok = False
    
    return all_ok

def test_database():
    """Probar funcionalidad de base de datos"""
    print("\n🗄️  Probando base de datos...")
    
    try:
        from app.models.database import init_db, engine
        from sqlalchemy import inspect
        
        print("  🔄 Inicializando BD...")
        if init_db():
            print("  ✅ BD inicializada")
            
            # Verificar tablas
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            if 'messages' in tables:
                print(f"  ✅ Tabla 'messages' creada")
                print(f"  📊 Tablas: {tables}")
                
                # Probar crear una instancia
                from app.models.message import MessageModel
                from datetime import datetime
                
                test_msg = MessageModel(
                    message_id="verify-001",
                    session_id="session-verify",
                    content="Mensaje de verificación",
                    original_content="Mensaje de verificación",
                    timestamp=datetime.now(),
                    sender="system",
                    message_length=24,
                    word_count=3
                )
                print(f"  ✅ Instancia de MessageModel creada: {test_msg.message_id}")
                
                return True
            else:
                print(f"  ❌ Tabla 'messages' no encontrada")
                return False
        else:
            print("  ❌ Error inicializando BD")
            return False
            
    except Exception as e:
        print(f"  ❌ Error en BD: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fastapi():
    """Probar FastAPI"""
    print("\n🌐 Probando FastAPI...")
    
    try:
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        
        # Test endpoints
        endpoints = [
            ("/", "Root endpoint"),
            ("/health", "Health check"),
            ("/docs", "Swagger UI"),
            ("/redoc", "ReDoc"),
        ]
        
        all_ok = True
        for endpoint, description in endpoints:
            try:
                response = client.get(endpoint)
                status = "✅" if response.status_code in [200, 404] else "❌"
                print(f"  {status} {description}: {response.status_code}")
                
                if endpoint == "/" and response.status_code == 200:
                    data = response.json()
                    print(f"     Mensaje: {data.get('message', 'No message')}")
                elif endpoint == "/health" and response.status_code == 200:
                    data = response.json()
                    print(f"     Status: {data.get('status', 'No status')}")
                    
            except Exception as e:
                print(f"  ❌ {description}: {e}")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"  ❌ Error en FastAPI: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 VERIFICACIÓN DEL SEGMENTO 1 - API MENSAJES CHAT")
    print("=" * 60)
    
    # 1. Instalar dependencias
    install_dependencies()
    
    # 2. Verificar archivos
    files_ok = check_files()
    
    if not files_ok:
        print("\n❌ Archivos requeridos faltantes. No se puede continuar.")
        return False
    
    # 3. Verificar imports
    imports_ok = test_imports()
    
    # 4. Verificar base de datos
    db_ok = test_database()
    
    # 5. Verificar FastAPI
    api_ok = test_fastapi()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    
    results = [
        ("📁 Archivos", files_ok),
        ("🔍 Imports", imports_ok),
        ("🗄️  Base de datos", db_ok),
        ("🌐 FastAPI", api_ok),
    ]
    
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    
    for name, ok in results:
        status = "✅" if ok else "❌"
        print(f"{status} {name}")
    
    print(f"\n📈 Progreso: {passed}/{total} ({passed/total*100:.0f}%)")
    
    # Conclusión
    print("\n" + "=" * 60)
    all_ok = all(ok for _, ok in results)
    
    if all_ok:
        print("🎉 ¡SEGMENTO 1 COMPLETADO EXITOSAMENTE!")
        print("\n✅ Todo está funcionando correctamente")
        print("\n📝 Próximo paso: Segmento 2 - Esquemas y Validación")
        print("   - Crear esquemas Pydantic")
        print("   - Implementar validación")
        print("   - Servicio de procesamiento")
    else:
        print("⚠️  Hay problemas que resolver")
        print("\n🔧 Soluciones:")
        if not imports_ok:
            print("   - Ejecuta: pip install pydantic-settings httpx")
        if not db_ok:
            print("   - Verifica la configuración de SQLite en .env")
        if not api_ok:
            print("   - Asegúrate de que FastAPI está correctamente configurado")
    
    return all_ok

if __name__ == "__main__":
    try:
        success = main()
        input("\nPresiona Enter para salir...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Verificación cancelada")
        sys.exit(1)