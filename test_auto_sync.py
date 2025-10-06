#!/usr/bin/env python3
"""
Script de prueba para verificar la sincronización automática
"""

import requests
import time
import json

def test_auto_sync():
    print("🧪 PRUEBA DE SINCRONIZACIÓN AUTOMÁTICA")
    print("=====================================")
    
    # 1. Verificar que el API inteligente esté funcionando
    try:
        response = requests.get('http://localhost:3002/api/coordinations')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API inteligente funcionando: {len(data['data'])} coordinaciones")
        else:
            print(f"❌ Error en API: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error conectando al API: {e}")
        return
    
    # 2. Simular ejecución de N8N
    print("\n🔄 Simulando ejecución de N8N...")
    
    # Crear una coordinación de prueba
    test_coordination = {
        "title": "Prueba Auto-Sync",
        "client_name": "Cliente Test Auto-Sync",
        "celular": "1234567890",
        "celular_2": "0987654321",
        "event_date": "2025-12-31",
        "honoree_name": "Test Auto-Sync",
        "codigo_evento": "TEST_AUTO_SYNC",
        "pack": "Pack Test",
        "salon": "Test - AUTO-SYNC"
    }
    
    try:
        response = requests.post('http://localhost:3002/api/coordinations', json=test_coordination)
        if response.status_code == 200:
            print("✅ Coordinación de prueba creada")
        else:
            print(f"❌ Error creando coordinación: {response.status_code}")
    except Exception as e:
        print(f"❌ Error enviando coordinación: {e}")
    
    # 3. Verificar que la coordinación se agregó
    time.sleep(2)  # Esperar un poco
    
    try:
        response = requests.get('http://localhost:3002/api/coordinations')
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Total coordinaciones en API: {len(data['data'])}")
            
            # Buscar nuestra coordinación de prueba
            test_found = any(coord.get('codigo_evento') == 'TEST_AUTO_SYNC' for coord in data['data'])
            if test_found:
                print("✅ Coordinación de prueba encontrada en API")
            else:
                print("❌ Coordinación de prueba NO encontrada en API")
        else:
            print(f"❌ Error verificando API: {response.status_code}")
    except Exception as e:
        print(f"❌ Error verificando API: {e}")
    
    print("\n🎯 INSTRUCCIONES:")
    print("1. Ve a http://localhost:3001")
    print("2. Observa el indicador 'Auto-sync activo' en el header")
    print("3. Las coordinaciones deberían aparecer automáticamente en 10 segundos")
    print("4. Si no aparecen, ejecuta el script de consola manual")
    
    print("\n📝 Script de consola de respaldo:")
    print("""
// Script de sincronización manual (si es necesario)
fetch('http://localhost:3002/api/coordinations')
  .then(response => response.json())
  .then(data => {
    const coordinaciones = data.data.map(coord => ({
      id: coord.id,
      title: coord.title,
      client_name: coord.client_name,
      celular: coord.celular,
      celular_2: coord.celular_2,
      honoree_name: coord.honoree_name,
      event_type: coord.event_type || 'corporativo',
      event_date: coord.event_date,
      codigo_evento: coord.codigo_evento,
      pack: coord.pack,
      salon: coord.salon,
      status: coord.status || 'pendiente',
      notes: coord.notes || `Importado automáticamente el ${new Date().toLocaleString()}`,
      created_at: coord.created_at,
      updated_at: coord.updated_at,
      salon_id: 1,
      salon_name: "DOT"
    }));
    
    localStorage.setItem('coordinations', JSON.stringify(coordinaciones));
    localStorage.setItem('salon_1_coordinations', JSON.stringify(coordinaciones));
    localStorage.setItem('salon_DOT_coordinations', JSON.stringify(coordinaciones));
    
    console.log(`✅ ${coordinaciones.length} coordinaciones sincronizadas`);
    window.location.reload();
  });
    """)

if __name__ == "__main__":
    test_auto_sync()
