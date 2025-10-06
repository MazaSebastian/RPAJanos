#!/usr/bin/env python3
"""
Script para iniciar el API de Control del Sistema
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    try:
        import flask
        import flask_cors
        import pandas
        print("✅ Dependencias verificadas")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("📦 Instalando dependencias...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'flask', 'flask-cors', 'pandas'])
        return True

def check_coordis_api():
    """Verificar que el API de COORDIS esté funcionando"""
    try:
        response = requests.get('http://localhost:3002/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ API de COORDIS funcionando")
            return True
    except:
        pass
    
    print("⚠️ API de COORDIS no disponible en puerto 3002")
    print("💡 Asegúrate de que el API de COORDIS esté ejecutándose")
    return False

def main():
    print("🚀 INICIANDO API DE CONTROL DEL SISTEMA")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        print("❌ Error verificando dependencias")
        return
    
    # Verificar API de COORDIS
    if not check_coordis_api():
        print("⚠️ Continuando sin verificación del API de COORDIS")
    
    # Verificar que los archivos necesarios existan
    required_files = [
        'RPA_MULTIPLES_EVENTOS.py',
        'probar_workflow_completo.py',
        'control_sistema_api.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        return
    
    print("✅ Todos los archivos necesarios encontrados")
    
    # Iniciar el API
    print("\n🌐 Iniciando API de Control del Sistema...")
    print("📡 Puerto: 3003")
    print("🔗 URL: http://localhost:3003")
    print("\n📋 Endpoints disponibles:")
    print("   GET  /api/system/status - Estado del sistema")
    print("   POST /api/system/rpa/execute - Ejecutar RPA")
    print("   POST /api/system/n8n/execute - Ejecutar N8N")
    print("   GET  /api/system/csv/download - Descargar CSV")
    print("   GET  /api/system/logs/<service> - Logs del servicio")
    print("   GET  /api/system/coordinations/count - Contar coordinaciones")
    print("   GET  /api/system/health - Salud del sistema")
    
    print("\n🎛️ Panel de Control disponible en:")
    print("   http://localhost:3001/system-control")
    
    print("\n⏹️ Para detener: Ctrl+C")
    print("=" * 50)
    
    try:
        # Ejecutar el API
        subprocess.run([sys.executable, 'control_sistema_api.py'])
    except KeyboardInterrupt:
        print("\n🛑 API de Control del Sistema detenido")
    except Exception as e:
        print(f"\n❌ Error ejecutando API: {e}")

if __name__ == "__main__":
    main()
