import pandas as pd
import requests
import json
from datetime import datetime
import hashlib

# --- Configuración ---
CSV_PATH = 'todos_los_eventos_extraidos.csv'
API_URL = 'http://localhost:3002/api/coordinations'
REPORT_PATH = 'reporte_cambios_detectados.json'

def obtener_coordinaciones_existentes():
    """
    Obtiene todas las coordinaciones existentes del API de COORDIS.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Error obteniendo coordinaciones existentes: {e}")
        return []

def generar_hash_coordinacion(coord):
    """
    Genera un hash único para una coordinación basado en sus datos principales.
    """
    # Campos que definen la identidad de una coordinación
    campos_identidad = [
        str(coord.get('codigo_evento', '')),
        str(coord.get('cliente', '')),
        str(coord.get('homenajeada', '')),
        str(coord.get('fecha_evento', '')),
        str(coord.get('salon', ''))
    ]
    
    # Crear hash de los campos de identidad
    contenido = '|'.join(campos_identidad)
    return hashlib.md5(contenido.encode()).hexdigest()

def generar_hash_datos(coord):
    """
    Genera un hash para detectar cambios en los datos de una coordinación.
    """
    # Campos que pueden cambiar
    campos_datos = [
        str(coord.get('celular', '')),
        str(coord.get('celular_2', '')),
        str(coord.get('tipo_pack', '')),
        str(coord.get('tipo_evento', ''))
    ]
    
    contenido = '|'.join(campos_datos)
    return hashlib.md5(contenido.encode()).hexdigest()

def detectar_cambios_y_nuevos():
    """
    Detecta coordinaciones nuevas, modificadas y sin cambios.
    """
    print("🔍 DETECTANDO CAMBIOS Y NUEVAS COORDINACIONES")
    print("=" * 50)
    
    # 1. Leer datos del CSV (nuevos datos de Janos)
    try:
        df_nuevos = pd.read_csv(CSV_PATH)
        print(f"📊 CSV leído: {len(df_nuevos)} eventos de Janos")
    except FileNotFoundError:
        print(f"❌ Error: Archivo CSV no encontrado: {CSV_PATH}")
        return
    except Exception as e:
        print(f"❌ Error leyendo CSV: {e}")
        return
    
    # 2. Obtener coordinaciones existentes del API
    coordinaciones_existentes = obtener_coordinaciones_existentes()
    print(f"📊 API tiene: {len(coordinaciones_existentes)} coordinaciones existentes")
    
    # 3. Crear diccionarios para búsqueda rápida
    existentes_por_codigo = {}
    existentes_por_hash = {}
    
    for coord in coordinaciones_existentes:
        codigo = str(coord.get('codigo_evento', ''))
        hash_identidad = generar_hash_coordinacion(coord)
        existentes_por_codigo[codigo] = coord
        existentes_por_hash[hash_identidad] = coord
    
    # 4. Analizar cada evento del CSV
    nuevos = []
    modificados = []
    sin_cambios = []
    errores = []
    
    for index, row in df_nuevos.iterrows():
        try:
            evento = row.to_dict()
            codigo_evento = str(evento.get('codigo_evento', ''))
            
            # Verificar si existe por código de evento
            if codigo_evento in existentes_por_codigo:
                coord_existente = existentes_por_codigo[codigo_evento]
                
                # Generar hashes para comparar
                hash_identidad_nuevo = generar_hash_coordinacion(evento)
                hash_identidad_existente = generar_hash_coordinacion(coord_existente)
                hash_datos_nuevo = generar_hash_datos(evento)
                hash_datos_existente = generar_hash_datos(coord_existente)
                
                # Verificar si hay cambios
                if hash_identidad_nuevo != hash_identidad_existente:
                    print(f"⚠️  Evento {codigo_evento}: Cambio en datos de identidad")
                    modificados.append({
                        'evento': evento,
                        'existente': coord_existente,
                        'tipo_cambio': 'identidad'
                    })
                elif hash_datos_nuevo != hash_datos_existente:
                    print(f"🔄 Evento {codigo_evento}: Cambio en datos de contacto/pack")
                    modificados.append({
                        'evento': evento,
                        'existente': coord_existente,
                        'tipo_cambio': 'datos'
                    })
                else:
                    print(f"✅ Evento {codigo_evento}: Sin cambios")
                    sin_cambios.append(codigo_evento)
            else:
                print(f"🆕 Evento {codigo_evento}: Nuevo")
                nuevos.append(evento)
                
        except Exception as e:
            print(f"❌ Error procesando evento {index}: {e}")
            errores.append({'index': index, 'error': str(e)})
    
    # 5. Generar reporte
    reporte = {
        'timestamp': datetime.now().isoformat(),
        'resumen': {
            'total_csv': len(df_nuevos),
            'total_existentes': len(coordinaciones_existentes),
            'nuevos': len(nuevos),
            'modificados': len(modificados),
            'sin_cambios': len(sin_cambios),
            'errores': len(errores)
        },
        'detalles': {
            'nuevos': nuevos,
            'modificados': modificados,
            'sin_cambios': sin_cambios,
            'errores': errores
        }
    }
    
    # 6. Guardar reporte
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)
    
    # 7. Mostrar resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE DETECCIÓN DE CAMBIOS:")
    print(f"   📥 Total en CSV: {len(df_nuevos)}")
    print(f"   📦 Total existentes: {len(coordinaciones_existentes)}")
    print(f"   🆕 Nuevos: {len(nuevos)}")
    print(f"   🔄 Modificados: {len(modificados)}")
    print(f"   ✅ Sin cambios: {len(sin_cambios)}")
    print(f"   ❌ Errores: {len(errores)}")
    print(f"   📄 Reporte guardado: {REPORT_PATH}")
    
    return reporte

def procesar_solo_cambios():
    """
    Procesa solo las coordinaciones nuevas y modificadas.
    """
    print("\n🚀 PROCESANDO SOLO CAMBIOS")
    print("=" * 30)
    
    # Detectar cambios
    reporte = detectar_cambios_y_nuevos()
    
    if not reporte:
        return
    
    nuevos = reporte['detalles']['nuevos']
    modificados = reporte['detalles']['modificados']
    
    if not nuevos and not modificados:
        print("✅ No hay cambios que procesar")
        return
    
    # Procesar nuevos
    if nuevos:
        print(f"\n📤 Procesando {len(nuevos)} coordinaciones nuevas...")
        for evento in nuevos:
            # Aquí iría la lógica para crear la coordinación
            print(f"   🆕 Creando: {evento.get('codigo_evento')} - {evento.get('cliente')}")
    
    # Procesar modificados
    if modificados:
        print(f"\n🔄 Procesando {len(modificados)} coordinaciones modificadas...")
        for cambio in modificados:
            # Aquí iría la lógica para actualizar la coordinación
            print(f"   🔄 Actualizando: {cambio['evento'].get('codigo_evento')} - {cambio['tipo_cambio']}")

if __name__ == "__main__":
    procesar_solo_cambios()
