#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main - RPA Jano's Eventos
==========================
Script principal de orquestación del sistema
Ejecuta el flujo completo: Extracción -> API -> Sincronización
"""

import sys
import argparse
import time
from pathlib import Path
from datetime import datetime

# Agregar al path
sys.path.append(str(Path(__file__).parent))

from utils.config import config
from utils.logger import logger
from rpa.extractor_eventos import ExtractorEventos
from sync.sincronizador import Sincronizador


class RPAJanosManager:
    """
    Gestor principal del sistema RPA Jano's Eventos
    Orquesta todos los componentes del sistema
    """
    
    def __init__(self):
        """Inicializa el gestor"""
        self.extractor = None
        self.sincronizador = None
        self.start_time = None
        
        logger.info("="*60)
        logger.info("🚀 RPA JANO'S EVENTOS - SISTEMA DE PRODUCCIÓN")
        logger.info("="*60)
        logger.info(f"📅 Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"🌍 Ambiente: {config.environment}")
        logger.info(f"🐛 Debug: {config.debug}")
        logger.info("="*60)
    
    def ejecutar_extraccion(self) -> bool:
        """
        Ejecuta el proceso de extracción de eventos
        
        Returns:
            True si extracción exitosa
        """
        logger.info("\n" + "="*60)
        logger.info("📥 FASE 1: EXTRACCIÓN DE EVENTOS")
        logger.info("="*60)
        
        try:
            self.extractor = ExtractorEventos()
            exito = self.extractor.extraer_todos_eventos()
            
            if exito:
                stats = self.extractor.obtener_estadisticas()
                logger.info(f"✅ Extracción completada:")
                logger.info(f"   - Eventos extraídos: {stats['total_eventos']}")
                logger.info(f"   - Errores: {stats['total_errores']}")
                logger.info(f"   - Duración: {stats['duracion']:.2f}s")
            
            return exito
            
        except Exception as e:
            logger.exception(f"❌ Error en extracción: {e}")
            return False
    
    def ejecutar_sincronizacion(self) -> bool:
        """
        Ejecuta el proceso de sincronización
        
        Returns:
            True si sincronización exitosa
        """
        logger.info("\n" + "="*60)
        logger.info("🔄 FASE 2: SINCRONIZACIÓN")
        logger.info("="*60)
        
        try:
            self.sincronizador = Sincronizador()
            
            # Verificar si hay CSV para sincronizar
            csv_path = config.csv_output_path
            
            if csv_path.exists():
                logger.info(f"📊 Sincronizando desde CSV: {csv_path}")
                exito = self.sincronizador.sincronizar_desde_csv(csv_path)
            else:
                logger.info("🔄 Sincronizando desde API")
                exito = self.sincronizador.sincronizar()
            
            if exito:
                logger.info("✅ Sincronización completada")
            
            return exito
            
        except Exception as e:
            logger.exception(f"❌ Error en sincronización: {e}")
            return False
    
    def ejecutar_flujo_completo(self) -> bool:
        """
        Ejecuta el flujo completo del sistema
        
        Returns:
            True si flujo completo exitoso
        """
        self.start_time = time.time()
        
        logger.info("\n" + "="*60)
        logger.info("🎯 INICIANDO FLUJO COMPLETO")
        logger.info("="*60)
        
        try:
            # Fase 1: Extracción
            if not self.ejecutar_extraccion():
                logger.error("❌ Flujo abortado: Fallo en extracción")
                return False
            
            # Pequeña pausa entre fases
            time.sleep(2)
            
            # Fase 2: Sincronización
            if not self.ejecutar_sincronizacion():
                logger.error("❌ Flujo abortado: Fallo en sincronización")
                return False
            
            # Resumen final
            self._mostrar_resumen_final()
            
            return True
            
        except Exception as e:
            logger.exception(f"❌ Error en flujo completo: {e}")
            return False
    
    def _mostrar_resumen_final(self):
        """Muestra resumen final de la ejecución"""
        duration = time.time() - self.start_time
        
        logger.info("\n" + "="*60)
        logger.info("✅ FLUJO COMPLETO FINALIZADO")
        logger.info("="*60)
        
        if self.extractor:
            stats = self.extractor.obtener_estadisticas()
            logger.info(f"📊 Eventos extraídos: {stats['total_eventos']}")
            logger.info(f"⚠️ Errores de extracción: {stats['total_errores']}")
        
        logger.info(f"⏱️ Duración total: {duration:.2f}s")
        logger.info(f"📅 Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*60)
    
    def ejecutar_solo_sincronizacion(self) -> bool:
        """
        Ejecuta solo la sincronización (sin extracción)
        
        Returns:
            True si sincronización exitosa
        """
        logger.info("\n" + "="*60)
        logger.info("🔄 MODO: SOLO SINCRONIZACIÓN")
        logger.info("="*60)
        
        return self.ejecutar_sincronizacion()
    
    def verificar_salud(self) -> dict:
        """
        Verifica el estado de salud del sistema
        
        Returns:
            Diccionario con estado de salud
        """
        logger.info("🏥 Verificando salud del sistema...")
        
        salud = {
            'timestamp': datetime.now().isoformat(),
            'ambiente': config.environment,
            'configuracion': 'OK',
            'directorios': 'OK',
            'api': 'DESCONOCIDO',
            'coordis': 'DESCONOCIDO'
        }
        
        # Verificar configuración
        is_valid, errors = config.validate()
        if not is_valid:
            salud['configuracion'] = f'ERROR: {errors}'
            logger.error(f"❌ Configuración inválida: {errors}")
        else:
            logger.info("✅ Configuración válida")
        
        # Verificar directorios
        try:
            for directory in [config.LOG_DIR, config.DATA_DIR, config.BACKUP_DIR]:
                if not directory.exists():
                    directory.mkdir(parents=True, exist_ok=True)
            logger.info("✅ Directorios verificados")
        except Exception as e:
            salud['directorios'] = f'ERROR: {e}'
            logger.error(f"❌ Error en directorios: {e}")
        
        # Verificar API
        try:
            import requests
            response = requests.get(f"{config.api_coordis}/api/health", timeout=5)
            if response.status_code == 200:
                salud['api'] = 'OK'
                logger.info("✅ API accesible")
            else:
                salud['api'] = f'ERROR: Status {response.status_code}'
                logger.warning(f"⚠️ API respondió con status {response.status_code}")
        except Exception as e:
            salud['api'] = f'ERROR: {e}'
            logger.warning(f"⚠️ API no accesible: {e}")
        
        return salud


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='RPA Jano\'s Eventos - Sistema de Producción',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py                    # Ejecuta flujo completo
  python main.py --extract          # Solo extracción
  python main.py --sync             # Solo sincronización
  python main.py --health           # Verifica salud del sistema
        """
    )
    
    parser.add_argument(
        '--extract', 
        action='store_true',
        help='Ejecutar solo extracción de eventos'
    )
    
    parser.add_argument(
        '--sync',
        action='store_true',
        help='Ejecutar solo sincronización'
    )
    
    parser.add_argument(
        '--health',
        action='store_true',
        help='Verificar salud del sistema'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Modo verboso (más logs)'
    )
    
    args = parser.parse_args()
    
    # Crear gestor
    manager = RPAJanosManager()
    
    # Verificar salud si se solicita
    if args.health:
        salud = manager.verificar_salud()
        logger.info("📋 Estado de salud del sistema:")
        for key, value in salud.items():
            logger.info(f"   {key}: {value}")
        return 0 if salud['configuracion'] == 'OK' else 1
    
    # Ejecutar según argumentos
    exito = False
    
    if args.extract:
        # Solo extracción
        exito = manager.ejecutar_extraccion()
    elif args.sync:
        # Solo sincronización
        exito = manager.ejecutar_solo_sincronizacion()
    else:
        # Flujo completo (por defecto)
        exito = manager.ejecutar_flujo_completo()
    
    # Código de salida
    return 0 if exito else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.warning("\n⚠️ Interrupción por usuario")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"❌ Error fatal: {e}")
        sys.exit(1)

