import requests
import json
from datetime import datetime

API_URL = "http://localhost:3002/api/coordinations"

def probar_deteccion_duplicados():
    """
    Prueba el sistema de detección de duplicados y cambios.
    """
    print("🧪 PROBANDO SISTEMA INTELIGENTE DE DETECCIÓN")
    print("=" * 50)
    
    # Datos de prueba
    coordinacion_test = {
        "title": "Test Event",
        "client_name": "Cliente Test",
        "celular": "1234567890",
        "celular_2": "0987654321",
        "event_date": "2025-01-15",
        "honoree_name": "Test Honoree",
        "codigo_evento": "TEST001",
        "pack": "Pack 1",
        "salon": "DOT",
        "event_type": "corporativo"
    }
    
    print("📤 Enviando coordinación de prueba...")
    
    # Primera vez - debería crear
    response1 = requests.post(API_URL, json=coordinacion_test)
    result1 = response1.json()
    print(f"Primera vez: {result1.get('accion', 'desconocido')} - {result1.get('message', '')}")
    
    # Segunda vez - debería detectar sin cambios
    response2 = requests.post(API_URL, json=coordinacion_test)
    result2 = response2.json()
    print(f"Segunda vez: {result2.get('accion', 'desconocido')} - {result2.get('message', '')}")
    
    # Tercera vez con cambios en datos
    coordinacion_modificada = coordinacion_test.copy()
    coordinacion_modificada["celular"] = "9999999999"  # Cambio en celular
    coordinacion_modificada["pack"] = "Pack 2"  # Cambio en pack
    
    response3 = requests.post(API_URL, json=coordinacion_modificada)
    result3 = response3.json()
    print(f"Con cambios: {result3.get('accion', 'desconocido')} - {result3.get('message', '')}")
    
    # Cuarta vez con cambios en identidad
    coordinacion_identidad = coordinacion_test.copy()
    coordinacion_identidad["client_name"] = "Cliente Modificado"  # Cambio en cliente
    coordinacion_identidad["event_date"] = "2025-02-15"  # Cambio en fecha
    
    response4 = requests.post(API_URL, json=coordinacion_identidad)
    result4 = response4.json()
    print(f"Cambio identidad: {result4.get('accion', 'desconocido')} - {result4.get('message', '')}")
    
    # Obtener estadísticas
    print("\n📊 Estadísticas del sistema:")
    stats_response = requests.get(f"{API_URL}/stats")
    if stats_response.status_code == 200:
        stats = stats_response.json()
        print(f"   Total coordinaciones: {stats['data']['total']}")
        print(f"   Duplicados potenciales: {len(stats['data']['duplicados_potenciales'])}")
    
    print("\n✅ Prueba completada")

def verificar_estado_actual():
    """
    Verifica el estado actual del sistema.
    """
    print("\n🔍 VERIFICANDO ESTADO ACTUAL")
    print("=" * 30)
    
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Total coordinaciones en el sistema: {data['total']}")
            
            # Mostrar algunas coordinaciones
            if data['data']:
                print("\n📋 Primeras 3 coordinaciones:")
                for i, coord in enumerate(data['data'][:3]):
                    print(f"   {i+1}. {coord.get('codigo_evento')} - {coord.get('client_name')} ({coord.get('created_at')})")
        else:
            print(f"❌ Error obteniendo coordinaciones: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_estado_actual()
    probar_deteccion_duplicados()
