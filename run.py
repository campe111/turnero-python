#!/usr/bin/env python3
# =============================================================================
# SISTEMA DE TURNOS - SCRIPT DE INICIO
# =============================================================================
"""
Script de inicio para el Sistema de Turnos
Proporciona una interfaz de línea de comandos para ejecutar la aplicación
"""

# =============================================================================
# IMPORTS
# =============================================================================
import os
import sys
from app import app, db

# =============================================================================
# FUNCION PRINCIPAL
# =============================================================================
def main():
    """Función principal para ejecutar la aplicación"""
    
    # =============================================================================
    # CABECERA Y PRESENTACION
    # =============================================================================
    print("=" * 50)
    print("🚀 SISTEMA DE TURNOS CON PYTHON Y FLASK")
    print("=" * 50)
    
    # =============================================================================
    # VERIFICACION DE BASE DE DATOS
    # =============================================================================
    # Verificar si existe la base de datos
    if not os.path.exists('turnero.db'):
        print("📊 Creando base de datos...")
        with app.app_context():
            db.create_all()
            print("✅ Base de datos creada exitosamente")
    
    # =============================================================================
    # INFORMACION DEL SISTEMA
    # =============================================================================
    # Mostrar información de la aplicación
    print("\n📋 Información del sistema:")
    print(f"   • Puerto: 5000")
    print(f"   • Host: 0.0.0.0 (accesible desde cualquier IP)")
    print(f"   • URL: http://localhost:5000")
    
    print("\n👤 Credenciales de administrador:")
    print(f"   • Email: admin@turnero.com")
    print(f"   • Contraseña: admin123")
    
    print("\n🎯 Funcionalidades disponibles:")
    print(f"   • Sacar turnos (acceso público)")
    print(f"   • Panel de administración")
    print(f"   • Gestión de categorías")
    print(f"   • Estadísticas en tiempo real")
    
    # =============================================================================
    # INICIO DEL SERVIDOR
    # =============================================================================
    print("\n" + "=" * 50)
    print("🌐 Iniciando servidor...")
    print("   Presiona Ctrl+C para detener")
    print("=" * 50)
    
    try:
        # Ejecutar la aplicación
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        # =============================================================================
        # MANEJO DE INTERRUPCION
        # =============================================================================
        print("\n\n🛑 Servidor detenido por el usuario")
        print("¡Gracias por usar el Sistema de Turnos!")
        sys.exit(0)
    except Exception as e:
        # =============================================================================
        # MANEJO DE ERRORES
        # =============================================================================
        print(f"\n❌ Error al iniciar el servidor: {e}")
        sys.exit(1)

# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
if __name__ == '__main__':
    main() 