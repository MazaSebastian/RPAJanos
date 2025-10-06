#!/usr/bin/env python3
"""
Script para sincronizar datos del API con localStorage de COORDIS
Convierte los datos del API al formato que espera la interfaz React
"""

import requests
import json
import webbrowser
from datetime import datetime

def sincronizar_coordis():
    """Sincroniza datos del API con localStorage de COORDIS"""
    
    print("🔄 SINCRONIZANDO COORDIS CON API")
    print("=" * 50)
    
    # Obtener datos del API
    try:
        response = requests.get('http://localhost:3002/api/coordinations', timeout=10)
        if response.status_code != 200:
            print(f"❌ Error del API: {response.status_code}")
            return False
            
        api_data = response.json()
        coordinations = api_data.get('data', [])
        print(f"📊 API tiene {len(coordinations)} coordinaciones")
        
    except Exception as e:
        print(f"❌ Error conectando al API: {e}")
        return False
    
    # Convertir datos del API al formato de localStorage
    localStorage_data = []
    
    for coord in coordinations:
        # Mapear campos del API al formato de la interfaz
        formatted_coord = {
            "id": coord.get('id'),
            "title": coord.get('title', ''),
            "client_name": coord.get('client_name', ''),
            "celular": coord.get('celular', ''),
            "celular_2": coord.get('celular_2', ''),
            "honoree_name": coord.get('honoree_name', ''),
            "event_type": mapear_tipo_evento(coord.get('title', '')),
            "event_date": coord.get('event_date', ''),
            "codigo_evento": coord.get('codigo_evento', ''),
            "pack": coord.get('pack', ''),
            "salon": coord.get('salon', ''),
            "status": coord.get('status', 'pendiente'),
            "notes": f"Importado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            "created_at": coord.get('created_at', ''),
            "updated_at": coord.get('updated_at', '')
        }
        
        localStorage_data.append(formatted_coord)
    
    # Crear script JavaScript para inyectar en localStorage
    js_script = f"""
    // Sincronización automática de coordinaciones
    console.log('🔄 Sincronizando coordinaciones...');
    
    const coordinaciones = {json.dumps(localStorage_data, ensure_ascii=False)};
    
    // Guardar en localStorage
    localStorage.setItem('coordinations', JSON.stringify(coordinaciones));
    
    console.log(`✅ ${{coordinaciones.length}} coordinaciones sincronizadas`);
    console.log('📊 Coordinaciones:', coordinaciones);
    
    // Recargar la página para mostrar los cambios
    window.location.reload();
    """
    
    # Guardar script en archivo
    with open('sincronizar_coordis.js', 'w', encoding='utf-8') as f:
        f.write(js_script)
    
    print(f"✅ {len(localStorage_data)} coordinaciones convertidas")
    print("📝 Script JavaScript creado: sincronizar_coordis.js")
    print("\n🔧 INSTRUCCIONES:")
    print("1. Abre http://localhost:3001 en el navegador")
    print("2. Abre las herramientas de desarrollador (F12)")
    print("3. Ve a la pestaña 'Console'")
    print("4. Copia y pega el contenido de 'sincronizar_coordis.js'")
    print("5. Presiona Enter para ejecutar")
    print("6. La página se recargará automáticamente")
    
    return True

def mapear_tipo_evento(title):
    """Mapea el título a tipo de evento para el select"""
    title_lower = title.lower()
    
    if '15' in title_lower or 'xv' in title_lower:
        return 'xv'
    elif 'boda' in title_lower or 'casamiento' in title_lower:
        return 'casamiento'
    elif 'cumpleaños' in title_lower or 'cumpleanos' in title_lower:
        return 'cumpleanos'
    elif 'empresarial' in title_lower or 'corporativo' in title_lower:
        return 'corporativo'
    elif 'religioso' in title_lower:
        return 'religioso'
    else:
        return 'corporativo'  # Default

if __name__ == "__main__":
    try:
        success = sincronizar_coordis()
        if success:
            print("\n🎉 SINCRONIZACIÓN COMPLETADA")
        else:
            print("\n❌ ERROR EN LA SINCRONIZACIÓN")
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        exit(1)
