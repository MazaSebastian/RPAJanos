#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sincronizador - RPA Jano's Eventos
===================================
Sincroniza datos del API con el frontend COORDIS
Versión de producción con manejo robusto de errores
"""

import requests
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import time

# Importar configuración y logger
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import config
from utils.logger import logger


class Sincronizador:
    """
    Sincroniza datos entre el API y el frontend COORDIS
    """
    
    def __init__(self):
        """Inicializa el sincronizador"""
        self.api_url = config.api_coordis
        self.coordis_url = config.url_coordis
        self.timeout = config.browser_timeout
        
        logger.info("🔄 Inicializando Sincronizador")
    
    def _obtener_coordinaciones_api(self) -> Optional[List[Dict]]:
        """
        Obtiene coordinaciones desde el API
        
        Returns:
            Lista de coordinaciones o None si hay error
        """
        logger.log_rpa_start("Obtención de coordinaciones desde API")
        
        try:
            url = f"{self.api_url}/api/coordinations"
            logger.log_api_request("GET", url, 0)
            
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            logger.log_api_request("GET", url, response.status_code)
            
            data = response.json()
            coordinations = data.get('data', [])
            
            logger.log_extraction(len(coordinations), "API")
            return coordinations
            
        except requests.exceptions.RequestException as e:
            logger.log_api_error("GET", url, str(e))
            return None
        except Exception as e:
            logger.exception(f"❌ Error obteniendo coordinaciones: {e}")
            return None
    
    def _formatear_fecha(self, fecha_str: str) -> str:
        """
        Formatea fecha a formato DD/MM/YYYY
        
        Args:
            fecha_str: Fecha en formato YYYY-MM-DD o similar
            
        Returns:
            Fecha formateada DD/MM/YYYY
        """
        try:
            # Intentar varios formatos
            formatos = ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d', '%d-%m-%Y']
            
            for formato in formatos:
                try:
                    fecha = datetime.strptime(fecha_str, formato)
                    return fecha.strftime('%d/%m/%Y')
                except:
                    continue
            
            # Si ninguno funciona, devolver original
            return fecha_str
            
        except:
            return fecha_str
    
    def _mapear_tipo_evento(self, tipo: str) -> str:
        """
        Mapea tipo de evento al formato de COORDIS
        
        Args:
            tipo: Tipo de evento original
            
        Returns:
            Tipo mapeado
        """
        mapeo = {
            '15 años': '15años',
            'cumpleaños': 'cumpleaños',
            'casamiento': 'casamiento',
            'corporativo': 'corporativo',
            'aniversario': 'aniversario',
            'otros': 'otros'
        }
        
        tipo_lower = tipo.lower() if tipo else ''
        
        for key, value in mapeo.items():
            if key in tipo_lower:
                return value
        
        return 'corporativo'
    
    def _convertir_a_formato_coordis(self, coordinations: List[Dict]) -> List[Dict]:
        """
        Convierte coordinaciones del API al formato de COORDIS
        
        Args:
            coordinations: Lista de coordinaciones del API
            
        Returns:
            Lista en formato COORDIS
        """
        logger.info(f"🔄 Convirtiendo {len(coordinations)} coordinaciones a formato COORDIS")
        
        coordis_data = []
        
        for coord in coordinations:
            try:
                # Formatear fecha
                event_date = self._formatear_fecha(coord.get('event_date', ''))
                
                # Mapear tipo de evento
                event_type = self._mapear_tipo_evento(coord.get('event_type', ''))
                
                # Crear objeto en formato COORDIS
                coordis_coord = {
                    "id": coord.get('id'),
                    "title": coord.get('title', ''),
                    "client_name": coord.get('client_name', ''),
                    "celular": str(coord.get('celular', '')),
                    "celular_2": str(coord.get('celular_2', '')),
                    "honoree_name": coord.get('honoree_name', ''),
                    "event_type": event_type,
                    "event_date": event_date,
                    "codigo_evento": str(coord.get('codigo_evento', '')),
                    "pack": coord.get('pack', ''),
                    "salon": coord.get('salon', ''),
                    "status": coord.get('status', 'pendiente'),
                    "notes": coord.get('notes', ''),
                    "created_at": coord.get('created_at', ''),
                    "updated_at": coord.get('updated_at', ''),
                    # Campos específicos de COORDIS
                    "salon_id": 1,  # DOT
                    "salon_name": "DOT"
                }
                
                coordis_data.append(coordis_coord)
                
            except Exception as e:
                logger.warning(f"⚠️ Error convirtiendo coordinación {coord.get('id')}: {e}")
                continue
        
        logger.info(f"✅ {len(coordis_data)} coordinaciones convertidas exitosamente")
        return coordis_data
    
    def generar_script_sincronizacion(self, coordinations: List[Dict]) -> str:
        """
        Genera script JavaScript para inyectar en COORDIS
        
        Args:
            coordinations: Lista de coordinaciones en formato COORDIS
            
        Returns:
            Script JavaScript
        """
        logger.info("📝 Generando script de sincronización")
        
        script = f"""
// ========================================
// Script de Sincronización Automática
// RPA Jano's Eventos -> COORDIS
// Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// ========================================

console.log('🔄 Iniciando sincronización de coordinaciones...');

const coordinaciones = {json.dumps(coordinations, ensure_ascii=False, indent=2)};

try {{
    // Guardar en localStorage
    localStorage.setItem('coordinations', JSON.stringify(coordinaciones));
    
    // Guardar también en formato de salón específico
    localStorage.setItem('salon_1_coordinations', JSON.stringify(coordinaciones));
    
    console.log(`✅ ${{coordinaciones.length}} coordinaciones sincronizadas exitosamente`);
    console.log('📊 Datos guardados en localStorage');
    
    // Disparar evento personalizado para que la UI se actualice
    window.dispatchEvent(new Event('coordinationsUpdated'));
    
    // Recargar la página para mostrar los cambios
    setTimeout(() => {{
        console.log('🔄 Recargando página...');
        window.location.reload();
    }}, 1000);
    
}} catch (error) {{
    console.error('❌ Error durante la sincronización:', error);
}}
"""
        
        return script
    
    def sincronizar(self) -> bool:
        """
        Ejecuta el proceso completo de sincronización
        
        Returns:
            True si sincronización exitosa
        """
        logger.log_rpa_start("SINCRONIZACIÓN COMPLETA")
        start_time = time.time()
        
        try:
            # Obtener coordinaciones del API
            coordinations = self._obtener_coordinaciones_api()
            
            if not coordinations:
                logger.warning("⚠️ No hay coordinaciones para sincronizar")
                return False
            
            # Convertir a formato COORDIS
            coordis_data = self._convertir_a_formato_coordis(coordinations)
            
            if not coordis_data:
                logger.warning("⚠️ No se pudieron convertir las coordinaciones")
                return False
            
            # Generar script
            script = self.generar_script_sincronizacion(coordis_data)
            
            # Guardar script en archivo
            script_path = config.DATA_DIR / 'sync_script.js'
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script)
            
            logger.info(f"💾 Script guardado: {script_path}")
            
            # Mostrar instrucciones
            self._mostrar_instrucciones(script_path)
            
            duration = time.time() - start_time
            logger.log_rpa_end("SINCRONIZACIÓN COMPLETA", duration=duration, success=True)
            logger.log_sync("completada", len(coordis_data))
            
            return True
            
        except Exception as e:
            logger.exception(f"❌ Error en sincronización: {e}")
            return False
    
    def _mostrar_instrucciones(self, script_path: Path):
        """Muestra instrucciones para completar la sincronización"""
        print("\n" + "="*60)
        print("📋 INSTRUCCIONES PARA COMPLETAR LA SINCRONIZACIÓN")
        print("="*60)
        print(f"\n1. Abre {self.coordis_url} en tu navegador")
        print("2. Abre las Herramientas de Desarrollador (F12)")
        print("3. Ve a la pestaña 'Console'")
        print(f"4. Copia y pega el contenido de: {script_path}")
        print("5. Presiona Enter para ejecutar")
        print("6. La página se recargará automáticamente")
        print("\n" + "="*60 + "\n")
    
    def sincronizar_desde_csv(self, csv_path: Path) -> bool:
        """
        Sincroniza coordinaciones desde un archivo CSV
        
        Args:
            csv_path: Ruta al archivo CSV
            
        Returns:
            True si sincronización exitosa
        """
        logger.log_rpa_start(f"Sincronización desde CSV: {csv_path}")
        
        try:
            # Leer CSV
            if not csv_path.exists():
                logger.error(f"❌ Archivo CSV no encontrado: {csv_path}")
                return False
            
            df = pd.read_csv(csv_path)
            logger.info(f"📊 CSV cargado: {len(df)} registros")
            
            # Convertir a lista de diccionarios
            coordinations = df.to_dict('records')
            
            # Enviar al API
            exito = self._enviar_al_api(coordinations)
            
            if exito:
                # Sincronizar con COORDIS
                return self.sincronizar()
            
            return False
            
        except Exception as e:
            logger.exception(f"❌ Error sincronizando desde CSV: {e}")
            return False
    
    def _enviar_al_api(self, coordinations: List[Dict]) -> bool:
        """
        Envía coordinaciones al API (carga masiva)
        
        Args:
            coordinations: Lista de coordinaciones
            
        Returns:
            True si envío exitoso
        """
        logger.info(f"📤 Enviando {len(coordinations)} coordinaciones al API")
        
        try:
            url = f"{self.api_url}/api/coordinations/bulk"
            payload = {"coordinations": coordinations}
            
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            
            resultado = response.json()
            
            if resultado.get('success'):
                resultados = resultado.get('resultados', {})
                logger.info(f"✅ Carga completada:")
                logger.info(f"   - Creadas: {resultados.get('creadas', 0)}")
                logger.info(f"   - Actualizadas: {resultados.get('actualizadas', 0)}")
                logger.info(f"   - Sin cambios: {resultados.get('sin_cambios', 0)}")
                logger.info(f"   - Errores: {resultados.get('errores', 0)}")
                return True
            else:
                logger.error(f"❌ Error en API: {resultado.get('message')}")
                return False
                
        except Exception as e:
            logger.exception(f"❌ Error enviando al API: {e}")
            return False


if __name__ == "__main__":
    # Ejecución directa
    sync = Sincronizador()
    
    # Verificar si hay CSV para sincronizar
    csv_path = config.csv_output_path
    
    if csv_path.exists():
        logger.info(f"📊 Encontrado CSV: {csv_path}")
        exito = sync.sincronizar_desde_csv(csv_path)
    else:
        logger.info("🔄 Sincronizando desde API")
        exito = sync.sincronizar()
    
    if exito:
        logger.info("✅ Sincronización completada")
        exit(0)
    else:
        logger.error("❌ Sincronización fallida")
        exit(1)

