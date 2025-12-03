# scripts/init_db.py
#!/usr/bin/env python3
"""
Script para inicializar la base de datos.
Ejecutar: python scripts/init_db.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.database import init_db, drop_db
import argparse

def main():
    parser = argparse.ArgumentParser(description="Gestión de base de datos")
    parser.add_argument("--init", action="store_true", help="Inicializar base de datos")
    parser.add_argument("--drop", action="store_true", help="Eliminar tablas (solo dev)")
    parser.add_argument("--reset", action="store_true", help="Reiniciar base de datos")
    
    args = parser.parse_args()
    
    if args.drop or args.reset:
        print("⚠️  Eliminando tablas...")
        if drop_db():
            print("✅ Tablas eliminadas")
        else:
            print("❌ Error eliminando tablas")
    
    if args.init or args.reset:
        print("🔄 Creando tablas...")
        if init_db():
            print("✅ Base de datos inicializada exitosamente")
        else:
            print("❌ Error inicializando base de datos")

if __name__ == "__main__":
    main()