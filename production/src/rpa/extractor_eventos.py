#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extractor de Eventos - RPA Jano's Eventos
==========================================
Módulo principal de extracción de eventos del sistema Janos
Versión de producción con manejo robusto de errores y logging profesional
"""

import time
import re
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    NoSuchElementException, 
    TimeoutException, 
    StaleElementReferenceException,
    WebDriverException
)

# Importar configuración y logger del sistema
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import config
from utils.logger import logger


class ExtractorEventos:
    """
    Extractor de eventos del sistema Janos
    Implementa RPA para extracción automatizada de eventos
    """
    
    def __init__(self):
        """Inicializa el extractor"""
        self.driver = None
        self.wait = None
        self.eventos_extraidos = []
        self.start_time = None
        self.errores = []
        
        logger.info("🎯 Inicializando Extractor de Eventos")
        
        # Validar configuración
        is_valid, errors = config.validate()
        if not is_valid:
            logger.error(f"❌ Configuración inválida: {errors}")
            raise ValueError(f"Configuración inválida: {errors}")
    
    def _configurar_driver(self) -> webdriver.Chrome:
        """
        Configura y retorna el driver de Chrome con opciones optimizadas
        
        Returns:
            Driver de Chrome configurado
        """
        logger.info("🔧 Configurando driver de Chrome")
        
        options = Options()
        
        # Opciones básicas
        if config.headless_mode:
            options.add_argument("--headless")
            logger.debug("Modo headless habilitado")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Opciones para evitar detección
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service()
            driver = webdriver.Chrome(service=service, options=options)
            
            # Ocultar que es webdriver
            driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            # Configurar timeouts
            driver.set_page_load_timeout(config.browser_timeout)
            driver.implicitly_wait(config.implicit_wait)
            
            logger.info("✅ Driver configurado exitosamente")
            return driver
            
        except Exception as e:
            logger.exception(f"❌ Error configurando driver: {e}")
            raise
    
    def _login(self) -> bool:
        """
        Realiza login en el sistema Janos
        
        Returns:
            True si login exitoso, False en caso contrario
        """
        logger.log_rpa_start("Login")
        
        try:
            # Navegar a la página de login
            logger.log_browser_action("Navegando a página de login")
            self.driver.get(config.url_origen)
            time.sleep(3)
            
            # Ingresar usuario
            logger.log_browser_action("Ingresando usuario")
            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.clear()
            username_field.send_keys(config.user_origen)
            
            # Ingresar contraseña
            logger.log_browser_action("Ingresando contraseña")
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(config.pass_origen)
            
            # Click en botón login
            logger.log_browser_action("Haciendo click en login")
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button"))
            )
            login_button.click()
            
            # Esperar redirección
            self.wait.until(lambda d: "login.php" not in d.current_url)
            
            logger.log_rpa_end("Login", success=True)
            return True
            
        except Exception as e:
            logger.exception(f"❌ Error en login: {e}")
            self.errores.append({"paso": "login", "error": str(e)})
            return False
    
    def _navegar_adicionales(self) -> bool:
        """
        Navega a la sección de Adicionales
        
        Returns:
            True si navegación exitosa
        """
        logger.log_rpa_start("Navegación a Adicionales")
        
        try:
            # Abrir menú lateral
            logger.log_browser_action("Abriendo menú lateral")
            open_nav = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@onclick='openNav()']"))
            )
            open_nav.click()
            time.sleep(2)
            
            # Encontrar y hacer click en Adicionales
            logger.log_browser_action("Buscando enlace Adicionales")
            side_menu = self.driver.find_element(By.ID, "sideMenu")
            enlaces = side_menu.find_elements(By.TAG_NAME, "a")
            
            for enlace in enlaces:
                if "adicionales" in enlace.text.lower():
                    logger.log_browser_action("Click en Adicionales")
                    enlace.click()
                    time.sleep(5)
                    break
            
            # Cambiar al frame principal
            logger.log_browser_action("Cambiando a mainFrame")
            main_frame = self.wait.until(
                EC.presence_of_element_located((By.ID, "mainFrame"))
            )
            self.driver.switch_to.frame(main_frame)
            
            logger.log_rpa_end("Navegación a Adicionales", success=True)
            return True
            
        except Exception as e:
            logger.exception(f"❌ Error navegando a Adicionales: {e}")
            self.errores.append({"paso": "navegar_adicionales", "error": str(e)})
            return False
    
    def _aplicar_filtros(self, salon: str = "DOT", zona: str = "CABA", ano: str = "2025") -> bool:
        """
        Aplica filtros de búsqueda
        
        Args:
            salon: Nombre del salón
            zona: Zona/cluster
            ano: Año
            
        Returns:
            True si filtros aplicados exitosamente
        """
        logger.log_rpa_start(f"Aplicando filtros: {salon}, {zona}, {ano}")
        
        try:
            # Filtro Salón
            logger.log_browser_action("Aplicando filtro Salón", salon)
            salon_select = Select(
                self.wait.until(EC.presence_of_element_located((By.ID, "salon")))
            )
            salon_select.select_by_visible_text(salon)
            
            # Filtro Zona
            logger.log_browser_action("Aplicando filtro Zona", zona)
            zona_select = Select(self.driver.find_element(By.ID, "cluster"))
            zona_select.select_by_visible_text(zona)
            
            # Filtro Año
            logger.log_browser_action("Aplicando filtro Año", ano)
            ano_select = Select(self.driver.find_element(By.ID, "ano"))
            ano_select.select_by_visible_text(ano)
            
            # Hacer click en Filtrar
            logger.log_browser_action("Ejecutando filtro")
            filtrar_buttons = self.driver.find_elements(By.XPATH, "//input[@value='Filtrar']")
            if filtrar_buttons:
                filtrar_buttons[0].click()
                time.sleep(5)
            
            logger.log_rpa_end("Aplicación de filtros", success=True)
            return True
            
        except Exception as e:
            logger.exception(f"❌ Error aplicando filtros: {e}")
            self.errores.append({"paso": "aplicar_filtros", "error": str(e)})
            return False
    
    def _obtener_fechas_con_eventos(self) -> List[Dict]:
        """
        Obtiene todas las fechas del calendario que tienen eventos
        
        Returns:
            Lista de diccionarios con información de fechas
        """
        logger.log_rpa_start("Obtención de fechas con eventos")
        
        try:
            # Buscar fechas coral (con eventos)
            fechas_coral = self.driver.find_elements(
                By.CSS_SELECTOR, 
                "div.boton[style*='background: coral']"
            )
            
            if not fechas_coral:
                # Búsqueda alternativa
                logger.debug("Búsqueda alternativa de fechas con color")
                todas_fechas = self.driver.find_elements(By.CSS_SELECTOR, "div.boton")
                fechas_coral = [
                    f for f in todas_fechas 
                    if f.text.strip().isdigit() and f.is_displayed() and 
                    'background:' in f.get_attribute('style')
                ]
            
            logger.info(f"📅 Encontradas {len(fechas_coral)} fechas con eventos")
            
            # Extraer información
            fechas_info = []
            for i, fecha in enumerate(fechas_coral):
                try:
                    fecha_texto = fecha.text.strip()
                    fechas_info.append({
                        'indice': i,
                        'fecha': fecha_texto,
                        'elemento': fecha
                    })
                except StaleElementReferenceException:
                    logger.warning(f"⚠️ Elemento stale para fecha {i}")
                    continue
            
            logger.log_rpa_end("Obtención de fechas con eventos", success=True)
            return fechas_info
            
        except Exception as e:
            logger.exception(f"❌ Error obteniendo fechas: {e}")
            self.errores.append({"paso": "obtener_fechas", "error": str(e)})
            return []
    
    def _procesar_fecha(self, fecha_info: Dict) -> List[Dict]:
        """
        Procesa una fecha específica y extrae todos sus eventos
        
        Args:
            fecha_info: Diccionario con información de la fecha
            
        Returns:
            Lista de eventos extraídos
        """
        fecha_texto = fecha_info['fecha']
        logger.info(f"📆 Procesando fecha: {fecha_texto}")
        
        eventos_fecha = []
        
        try:
            # Hacer click en la fecha
            fecha_info['elemento'].click()
            time.sleep(3)
            
            # Verificar si hay eventos
            try:
                # Buscar lista de eventos
                eventos_lista = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.modal-content, div.eventos-lista"))
                )
                
                # Buscar todos los eventos de la fecha
                items_eventos = self.driver.find_elements(By.CSS_SELECTOR, "div.evento-item, tr.evento")
                
                logger.info(f"   Encontrados {len(items_eventos)} eventos")
                
                for idx, item in enumerate(items_eventos):
                    try:
                        evento_datos = self._extraer_datos_evento(item, fecha_texto)
                        if evento_datos:
                            eventos_fecha.append(evento_datos)
                            logger.debug(f"   ✓ Evento {idx+1} extraído")
                    except Exception as e:
                        logger.warning(f"   ⚠️ Error extrayendo evento {idx+1}: {e}")
                        continue
                
                # Cerrar modal si existe
                try:
                    cerrar_btn = self.driver.find_element(By.CSS_SELECTOR, ".close, .cerrar, button.close")
                    cerrar_btn.click()
                    time.sleep(1)
                except:
                    pass
                    
            except TimeoutException:
                logger.debug(f"   Sin eventos en fecha {fecha_texto}")
            
        except Exception as e:
            logger.warning(f"⚠️ Error procesando fecha {fecha_texto}: {e}")
            self.errores.append({"paso": f"procesar_fecha_{fecha_texto}", "error": str(e)})
        
        return eventos_fecha
    
    def _extraer_datos_evento(self, elemento, fecha: str) -> Optional[Dict]:
        """
        Extrae datos de un evento individual
        
        Args:
            elemento: Elemento HTML del evento
            fecha: Fecha del evento
            
        Returns:
            Diccionario con datos del evento o None
        """
        try:
            # Extraer campos según estructura HTML
            # (Adaptar según la estructura real)
            
            datos = {
                'fecha_evento': fecha,
                'cliente': '',
                'homenajeada': '',
                'tipo_evento': '',
                'codigo_evento': '',
                'salon': '',
                'horario': '',
                'celular': '',
                'celular_2': '',
                'tipo_pack': '',
                'fecha_extraccion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Intentar extraer datos con diferentes selectores
            try:
                datos['cliente'] = elemento.find_element(By.CSS_SELECTOR, ".cliente, .client-name").text.strip()
            except:
                pass
            
            try:
                datos['homenajeada'] = elemento.find_element(By.CSS_SELECTOR, ".homenajeada, .honoree").text.strip()
            except:
                pass
            
            try:
                datos['tipo_evento'] = elemento.find_element(By.CSS_SELECTOR, ".tipo, .event-type").text.strip()
            except:
                pass
            
            try:
                datos['codigo_evento'] = elemento.find_element(By.CSS_SELECTOR, ".codigo, .event-code").text.strip()
            except:
                pass
            
            try:
                datos['salon'] = elemento.find_element(By.CSS_SELECTOR, ".salon, .venue").text.strip()
            except:
                pass
            
            try:
                datos['horario'] = elemento.find_element(By.CSS_SELECTOR, ".horario, .time").text.strip()
            except:
                pass
            
            # Validar que al menos tenga código o cliente
            if datos['codigo_evento'] or datos['cliente']:
                return datos
            
            return None
            
        except Exception as e:
            logger.debug(f"Error extrayendo datos de evento: {e}")
            return None
    
    def extraer_todos_eventos(self) -> bool:
        """
        Ejecuta el proceso completo de extracción de eventos
        
        Returns:
            True si extracción exitosa
        """
        self.start_time = time.time()
        logger.log_rpa_start("EXTRACCIÓN COMPLETA DE EVENTOS")
        
        try:
            # Configurar driver
            self.driver = self._configurar_driver()
            self.wait = WebDriverWait(self.driver, config.browser_timeout)
            
            # Login
            if not self._login():
                return False
            
            # Navegar a Adicionales
            if not self._navegar_adicionales():
                return False
            
            # Aplicar filtros
            if not self._aplicar_filtros():
                return False
            
            # Obtener fechas con eventos
            fechas = self._obtener_fechas_con_eventos()
            if not fechas:
                logger.warning("⚠️ No se encontraron fechas con eventos")
                return False
            
            # Procesar cada fecha
            total_eventos = 0
            for fecha_info in fechas:
                eventos = self._procesar_fecha(fecha_info)
                self.eventos_extraidos.extend(eventos)
                total_eventos += len(eventos)
            
            logger.log_extraction(total_eventos, "Sistema Janos")
            
            # Guardar resultados
            if self.eventos_extraidos:
                self._guardar_csv()
            
            duration = time.time() - self.start_time
            logger.log_rpa_end("EXTRACCIÓN COMPLETA", duration=duration, success=True)
            
            return True
            
        except Exception as e:
            logger.exception(f"❌ Error en extracción completa: {e}")
            return False
            
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("🔒 Driver cerrado")
    
    def _guardar_csv(self):
        """Guarda los eventos extraídos en CSV"""
        try:
            df = pd.DataFrame(self.eventos_extraidos)
            csv_path = config.csv_output_path
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            
            logger.info(f"💾 CSV guardado: {csv_path} ({len(df)} registros)")
            
            # Backup si está habilitado
            if config.backup_enabled:
                backup_path = config.BACKUP_DIR / f"eventos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(backup_path, index=False, encoding='utf-8-sig')
                logger.info(f"💾 Backup guardado: {backup_path}")
                
        except Exception as e:
            logger.exception(f"❌ Error guardando CSV: {e}")
    
    def obtener_estadisticas(self) -> Dict:
        """Retorna estadísticas de la extracción"""
        return {
            'total_eventos': len(self.eventos_extraidos),
            'total_errores': len(self.errores),
            'duracion': time.time() - self.start_time if self.start_time else 0,
            'timestamp': datetime.now().isoformat()
        }


if __name__ == "__main__":
    # Ejecución directa
    extractor = ExtractorEventos()
    exito = extractor.extraer_todos_eventos()
    
    if exito:
        stats = extractor.obtener_estadisticas()
        logger.info(f"✅ Extracción completada: {stats}")
        exit(0)
    else:
        logger.error("❌ Extracción fallida")
        exit(1)

