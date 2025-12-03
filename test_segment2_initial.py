# test_segment2_complete.py
"""
Verificación completa del Segmento 2.
"""
import sys
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

def check_complete_structure():
    """Verificar estructura completa del Segmento 2"""
    print("📁 Verificando estructura completa del Segmento 2...")
    
    required_items = [
        ("app/schemas/", "directorio"),
        ("app/schemas/__init__.py", "archivo"),
        ("app/schemas/message.py", "archivo"),
        ("app/services/", "directorio"),
        ("app/services/__init__.py", "archivo"),
        ("app/services/validation_service.py", "archivo"),
        ("app/services/processing_service.py", "archivo"),
        ("app/utils/", "directorio"),
        ("app/utils/__init__.py", "archivo"),
        ("app/utils/helpers.py", "archivo"),
        ("app/repositories/", "directorio"),
        ("app/repositories/__init__.py", "archivo"),
        ("app/repositories/message_repository.py", "archivo"),
    ]
    
    all_ok = True
    
    for path, item_type in required_items:
        exists = Path(path).exists()
        icon = "✅" if exists else "❌"
        print(f"  {icon} {path} ({item_type})")
        
        if not exists:
            all_ok = False
    
    return all_ok

def test_all_imports():
    """Probar todos los imports"""
    print("\n🔍 Probando todos los imports...")
    
    imports_to_test = [
        ("app.schemas.message", "Esquemas"),
        ("app.services.validation_service", "Servicio de validación"),
        ("app.services.processing_service", "Servicio de procesamiento"),
        ("app.utils.helpers", "Utilidades"),
        ("app.repositories.message_repository", "Repositorio"),
    ]
    
    all_ok = True
    
    for module_path, description in imports_to_test:
        try:
            __import__(module_path)
            print(f"  ✅ {description}")
        except Exception as e:
            print(f"  ❌ {description}: {e}")
            all_ok = False
    
    return all_ok

def test_schemas_corrected():
    """Probar esquemas con validadores corregidos"""
    print("\n📋 Probando esquemas Pydantic (corregidos)...")
    
    try:
        from app.schemas.message import MessageCreate, MessageFilter
        
        # Test MessageCreate válido
        test_message = {
            "message_id": "test-msg-001",
            "session_id": "session-123",
            "content": "Hola mundo",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sender": "user"
        }
        
        message = MessageCreate(**test_message)
        print(f"  ✅ MessageCreate creado: {message.message_id}")
        
        # Test validaciones
        print("  🔍 Probando validaciones corregidas...")
        
        # Test 1: sender inválido
        try:
            invalid_message = test_message.copy()
            invalid_message["sender"] = "invalid_sender"
            MessageCreate(**invalid_message)
            print("  ❌ Validación de sender debería haber fallado")
            return False
        except ValueError as e:
            print(f"  ✅ Validación de sender funciona: {str(e)[:50]}...")
        
        # Test 2: timestamp futuro
        try:
            future_time = datetime.now(timezone.utc) + timedelta(days=1)
            invalid_message = test_message.copy()
            invalid_message["timestamp"] = future_time.isoformat()
            MessageCreate(**invalid_message)
            print("  ❌ Validación de timestamp debería haber fallado")
            return False
        except ValueError as e:
            print(f"  ✅ Validación de timestamp funciona: {str(e)[:50]}...")
        
        # Test 3: message_id con caracteres inválidos
        try:
            invalid_message = test_message.copy()
            invalid_message["message_id"] = "test@123"  # @ no permitido
            MessageCreate(**invalid_message)
            print("  ❌ Validación de message_id debería haber fallado")
            return False
        except ValueError as e:
            print(f"  ✅ Validación de message_id funciona: {str(e)[:50]}...")
        
        # Test 4: content vacío
        try:
            invalid_message = test_message.copy()
            invalid_message["content"] = "   "
            MessageCreate(**invalid_message)
            print("  ❌ Validación de content debería haber fallado")
            return False
        except ValueError as e:
            print(f"  ✅ Validación de content funciona: {str(e)[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error en esquemas: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_processing_service():
    """Probar servicio de procesamiento"""
    print("\n⚙️  Probando servicio de procesamiento...")
    
    try:
        from app.services.processing_service import ProcessingService
        
        # Test filtrado de contenido
        print("  🔍 Probando filtrado de contenido...")
        
        content_with_bad_words = "Este es un mensaje con una badword1 y otra inappropriate palabra"
        filtered, has_inappropriate, found_words = ProcessingService.filter_inappropriate_content(
            content_with_bad_words
        )
        
        if has_inappropriate and found_words:
            print(f"  ✅ Filtrado detectó palabras inapropiadas: {found_words}")
            print(f"     Contenido original: {content_with_bad_words}")
            print(f"     Contenido filtrado: {filtered}")
        else:
            print(f"  ❌ Filtrado debería haber detectado palabras inapropiadas")
            return False
        
        # Test procesamiento completo
        print("  🔄 Probando procesamiento completo...")
        
        message_data = {
            "message_id": "test-process-001",
            "session_id": "session-process",
            "content": "Hola, esto es un badword1 test",
            "timestamp": datetime.now(timezone.utc),
            "sender": "user"
        }
        
        processed = ProcessingService.process_message(message_data)
        
        if "original_content" in processed and "content" in processed:
            print(f"  ✅ Procesamiento completo: OK")
            print(f"     Original: {processed['original_content']}")
            print(f"     Filtrado: {processed['content']}")
            print(f"     Longitud: {processed.get('message_length')}")
            print(f"     Palabras: {processed.get('word_count')}")
            print(f"     Inapropiado: {processed.get('has_inappropriate_content')}")
        else:
            print(f"  ❌ Procesamiento incompleto")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error en servicio de procesamiento: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Probar integración entre componentes"""
    print("\n🔗 Probando integración entre componentes...")
    
    try:
        from app.schemas.message import MessageCreate
        from app.services.validation_service import ValidationService
        from app.services.processing_service import ProcessingService
        
        # Crear mensaje con esquema
        message_data = {
            "message_id": "integration-test-001",
            "session_id": "integration-session",
            "content": "Este es un mensaje de integración con badword1",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sender": "system"
        }
        
        # 1. Validar con esquema
        message_schema = MessageCreate(**message_data)
        print(f"  ✅ Esquema creado: {message_schema.message_id}")
        
        # 2. Validar con servicio
        is_valid, errors, validated = ValidationService.validate_complete_message(
            message_schema.model_dump()
        )
        
        if is_valid:
            print(f"  ✅ Validación del servicio exitosa")
        else:
            print(f"  ❌ Validación del servicio falló: {errors}")
            return False
        
        # 3. Procesar con servicio
        processed = ProcessingService.process_message(validated)
        
        if "has_inappropriate_content" in processed and processed["has_inappropriate_content"]:
            print(f"  ✅ Procesamiento detectó contenido inapropiado")
            print(f"     Contenido filtrado: {processed['content']}")
        else:
            print(f"  ❌ Procesamiento debería haber detectado contenido inapropiado")
            return False
        
        print("\n🎯 Flujo completo de validación y procesamiento funcionando")
        return True
        
    except Exception as e:
        print(f"  ❌ Error en integración: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("="*60)
    print("🚀 VERIFICACIÓN COMPLETA DEL SEGMENTO 2")
    print("="*60)
    
    # 1. Verificar estructura
    if not check_complete_structure():
        print("\n❌ Faltan archivos/carpetas.")
        return False
    
    # 2. Probar imports
    if not test_all_imports():
        print("\n⚠️  Problemas con imports.")
        return False
    
    # 3. Probar esquemas corregidos
    if not test_schemas_corrected():
        print("\n⚠️  Problemas con esquemas Pydantic.")
        return False
    
    # 4. Probar servicio de procesamiento
    if not test_processing_service():
        print("\n⚠️  Problemas con servicio de procesamiento.")
        return False
    
    # 5. Probar integración
    if not test_integration():
        print("\n⚠️  Problemas con integración.")
        return False
    
    print("\n" + "="*60)
    print("🎉 ¡SEGMENTO 2 COMPLETADO EXITOSAMENTE!")
    print("="*60)
    
    print("\n✅ Lo que hemos creado y probado:")
    print("   📋 Esquemas Pydantic con validadores funcionando")
    print("   🔧 Servicio de validación con múltiples reglas")
    print("   ⚙️  Servicio de procesamiento con filtrado de contenido")
    print("   🛠️  Utilidades auxiliares")
    print("   🗄️  Repositorio para acceso a datos")
    print("   🔗 Integración completa entre componentes")
    
    print("\n📝 Siguiente paso: Segmento 3 - Endpoints de la API")
    print("   1. Crear endpoints POST /api/messages/")
    print("   2. Crear endpoints GET /api/messages/{session_id}")
    print("   3. Implementar manejo de errores")
    print("   4. Documentación automática con FastAPI")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        input("\nPresiona Enter para salir...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Verificación cancelada")
        sys.exit(1)