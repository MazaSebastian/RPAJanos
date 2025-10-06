#!/usr/bin/env python3
"""
Script para probar el workflow completo de N8N
Simula el procesamiento de todos los eventos del CSV
"""

import pandas as pd
import requests
import json
import time
from datetime import datetime

def procesar_csv_completo():
    """Procesa todos los eventos del CSV y los envía al API"""
    
    print("🚀 INICIANDO PRUEBA COMPLETA DEL WORKFLOW")
    print("=" * 50)
    
    # Leer CSV
    print("📖 Leyendo CSV...")
    df = pd.read_csv('todos_los_eventos_extraidos.csv')
    print(f"✅ CSV leído: {len(df)} eventos encontrados")
    
    # Configurar API
    api_url = "http://localhost:3002/api/coordinations"
    headers = {"Content-Type": "application/json"}
    
    # Contadores
    exitosos = 0
    fallidos = 0
    errores = []
    
    print("\n📤 PROCESANDO EVENTOS:")
    print("-" * 30)
    
    # Procesar cada evento
    for index, row in df.iterrows():
        try:
            # Preparar datos
            evento_data = {
                "title": f"{row['tipo_evento']} de {row['homenajeada']}",
                "client_name": row['cliente'],
                "celular": row['celular'],
                "celular_2": row['celular_2'],
                "event_date": row['fecha_evento'].split('(')[0].strip(),  # Remover día de la semana
                "honoree_name": row['homenajeada'],
                "codigo_evento": row['codigo_evento'],
                "pack": row['tipo_pack'],
                "salon": row['salon']
            }
            
            # Enviar al API
            response = requests.post(api_url, json=evento_data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                exitosos += 1
                print(f"✅ Evento {index+1}: {evento_data['title']} - {evento_data['client_name']}")
            else:
                fallidos += 1
                error_msg = f"Error {response.status_code}: {response.text}"
                errores.append({"evento": index+1, "error": error_msg})
                print(f"❌ Evento {index+1}: ERROR - {error_msg}")
                
        except Exception as e:
            fallidos += 1
            error_msg = f"Excepción: {str(e)}"
            errores.append({"evento": index+1, "error": error_msg})
            print(f"❌ Evento {index+1}: EXCEPCIÓN - {error_msg}")
        
        # Pequeña pausa para no sobrecargar el API
        time.sleep(0.1)
    
    # Generar reporte
    total = exitosos + fallidos
    tasa_exito = (exitosos / total * 100) if total > 0 else 0
    
    reporte = {
        "resumen": {
            "total_eventos": total,
            "exitosos": exitosos,
            "fallidos": fallidos,
            "tasa_exito": f"{tasa_exito:.1f}%",
            "timestamp": datetime.now().isoformat()
        },
        "errores": errores
    }
    
    # Guardar reporte
    with open('reporte_carga_masiva.json', 'w', encoding='utf-8') as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 50)
    print("📊 REPORTE FINAL:")
    print(f"   Total eventos: {total}")
    print(f"   Exitosos: {exitosos}")
    print(f"   Fallidos: {fallidos}")
    print(f"   Tasa de éxito: {tasa_exito:.1f}%")
    print(f"   Reporte guardado en: reporte_carga_masiva.json")
    
    # Verificar estado final del API
    print("\n🔍 VERIFICANDO ESTADO FINAL DEL API...")
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API respondiendo: {data['total']} coordinaciones totales")
        else:
            print(f"❌ Error verificando API: {response.status_code}")
    except Exception as e:
        print(f"❌ Error conectando al API: {e}")
    
    return reporte

if __name__ == "__main__":
    try:
        reporte = procesar_csv_completo()
        print("\n🎉 PRUEBA COMPLETA FINALIZADA")
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        exit(1)
