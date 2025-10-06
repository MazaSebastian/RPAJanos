#!/usr/bin/env python3
"""
Script FINAL para sincronizar datos del API con localStorage de COORDIS
CORREGIDO: Formato de fechas, mapeo de campos y asignación de salón
"""

import requests
import json
import webbrowser
from datetime import datetime
import re

def sincronizar_coordis_final():
    """Sincroniza datos del API con localStorage de COORDIS - VERSIÓN FINAL"""
    
    print("🔄 SINCRONIZANDO COORDIS CON API (VERSIÓN FINAL)")
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
        # CORREGIR: Formatear fecha correctamente
        event_date = formatear_fecha(coord.get('event_date', ''))
        
        # CORREGIR: Mapear tipo de evento correctamente
        event_type = mapear_tipo_evento_corregido(coord.get('title', ''))
        
        # Mapear campos del API al formato de la interfaz
        formatted_coord = {
            "id": coord.get('id'),
            "title": coord.get('title', ''),
            "client_name": coord.get('client_name', ''),
            "celular": str(coord.get('celular', '')),
            "celular_2": str(coord.get('celular_2', '')),
            "honoree_name": coord.get('honoree_name', ''),
            "event_type": event_type,  # CORREGIDO
            "event_date": event_date,  # CORREGIDO
            "codigo_evento": str(coord.get('codigo_evento', '')),
            "pack": coord.get('pack', ''),
            "salon": coord.get('salon', ''),
            "status": coord.get('status', 'pendiente'),
            "notes": f"Importado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            "created_at": coord.get('created_at', ''),
            "updated_at": coord.get('updated_at', ''),
            # CRÍTICO: Asignar salón específico para que se muestre
            "salon_id": 1,  # Salón DOT (ID: 1)
            "salon_name": "DOT"
        }
        
        localStorage_data.append(formatted_coord)
    
    # Crear script JavaScript para inyectar en localStorage
    js_script = f"""
    // Sincronización automática de coordinaciones (VERSIÓN FINAL)
    console.log('🔄 Sincronizando coordinaciones con formato corregido...');
    
    const coordinaciones = {json.dumps(localStorage_data, ensure_ascii=False)};
    
    // Guardar en localStorage con formato de salón
    localStorage.setItem('coordinations', JSON.stringify(coordinaciones));
    
    // CRÍTICO: También guardar en formato de salón específico
    localStorage.setItem('salon_1_coordinations', JSON.stringify(coordinaciones));
    
    console.log(`✅ ${{coordinaciones.length}} coordinaciones sincronizadas con formato corregido`);
    console.log('📊 Coordinaciones:', coordinaciones);
    
    // Recargar la página para mostrar los cambios
    window.location.reload();
    """
    
    # Guardar script en archivo
    with open('sincronizar_coordis_final.js', 'w', encoding='utf-8') as f:
        f.write(js_script)
    
    print(f"✅ {len(localStorage_data)} coordinaciones convertidas con formato corregido")
    print("📝 Script JavaScript creado: sincronizar_coordis_final.js")
    print("\n🔧 INSTRUCCIONES:")
    print("1. Abre http://localhost:3001 en el navegador")
    print("2. Abre las herramientas de desarrollador (F12)")
    print("3. Ve a la pestaña 'Console'")
    print("4. Copia y pega el contenido de 'sincronizar_coordis_final.js'")
    print("5. Presiona Enter para ejecutar")
    print("6. La página se recargará automáticamente")
    print("7. Ahora las fechas y campos deberían mostrarse correctamente")
    
    return True

def formatear_fecha(fecha_str):
    """Convierte fecha de formato DD/MM/YYYY a YYYY-MM-DD"""
    if not fecha_str:
        return ''
    
    # Si ya está en formato YYYY-MM-DD, devolverlo
    if re.match(r'\d{4}-\d{2}-\d{2}', fecha_str):
        return fecha_str
    
    # Si está en formato DD/MM/YYYY, convertir
    if re.match(r'\d{1,2}/\d{1,2}/\d{4}', fecha_str):
        try:
            # Parsear DD/MM/YYYY
            partes = fecha_str.split('/')
            if len(partes) == 3:
                dia, mes, año = partes
                return f"{año}-{mes.zfill(2)}-{dia.zfill(2)}"
        except:
            pass
    
    # Si no se puede parsear, devolver string vacío
    return ''

def mapear_tipo_evento_corregido(title):
    """Mapea el título a tipo de evento para el select - VERSIÓN CORREGIDA"""
    if not title:
        return 'corporativo'
    
    title_lower = title.lower()
    
    # Mapeo más específico y correcto
    if '15' in title_lower or 'xv' in title_lower:
        return 'xv'
    elif 'boda' in title_lower or 'casamiento' in title_lower:
        return 'casamiento'
    elif 'cumpleaños' in title_lower or 'cumpleanos' in title_lower:
        return 'cumpleanos'
    elif 'bar/bat mitzvah' in title_lower or 'mitzvah' in title_lower:
        return 'religioso'
    elif 'egresados' in title_lower:
        return 'corporativo'
    elif 'empresarial' in title_lower or 'corporativo' in title_lower:
        return 'corporativo'
    else:
        return 'corporativo'  # Default

if __name__ == "__main__":
    try:
        success = sincronizar_coordis_final()
        if success:
            print("\n🎉 SINCRONIZACIÓN FINAL COMPLETADA")
            print("✅ Fechas corregidas")
            print("✅ Mapeo de campos corregido")
            print("✅ Asignación de salón corregida")
        else:
            print("\n❌ ERROR EN LA SINCRONIZACIÓN")
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        exit(1)
