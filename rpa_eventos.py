#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script RPA para transferir eventos entre dos sistemas web
Autor: Asistente IA
Fecha: 2024
"""

import os
import time
import logging
import pandas as pd
import schedule
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rpa_eventos.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RPAEventos:
    def __init__(self):
        """Inicializar el RPA con configuración del navegador"""
        self.driver = None
        self.wait = None
        self.eventos_extraidos = []
        
        # Variables de entorno - REEMPLAZAR CON TUS VALORES REALES
        self.url_origen = os.environ.get('URL_ORIGEN')
        self.user_origen = os.environ.get('USER_ORIGEN')
        self.pass_origen = os.environ.get('PASS_ORIGEN')
        
        self.url_destino = os.environ.get('URL_DESTINO')
        self.user_destino = os.environ.get('USER_DESTINO')
        self.pass_destino = os.environ.get('PASS_DESTINO')
        
        # Verificar que las variables de entorno estén configuradas
        self._verificar_configuracion()
    
    def _verificar_configuracion(self):
        """Verificar que todas las variables de entorno estén configuradas"""
        variables_requeridas = [
            'URL_ORIGEN', 'USER_ORIGEN', 'PASS_ORIGEN',
            'URL_DESTINO', 'USER_DESTINO', 'PASS_DESTINO'
        ]
        
        variables_faltantes = []
        for var in variables_requeridas:
            if not os.environ.get(var):
                variables_faltantes.append(var)
        
        if variables_faltantes:
            logger.error(f"Variables de entorno faltantes: {', '.join(variables_faltantes)}")
            raise ValueError(f"Configura las siguientes variables de entorno: {', '.join(variables_faltantes)}")
    
    def _configurar_navegador(self):
        """Configurar el navegador Chrome con opciones optimizadas"""
        chrome_options = Options()
        
        # Configuración para modo headless (servidor)
        if os.environ.get('HEADLESS_MODE', 'true').lower() == 'true':
            chrome_options.add_argument('--headless')
        
        # Optimizaciones para estabilidad
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Inicializar el driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Configurar esperas explícitas
        self.wait = WebDriverWait(self.driver, 20)
        
        # Ejecutar script para ocultar automatización
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info("Navegador configurado correctamente")
    
    def _login_sistema_origen(self):
        """
        PASO 1: Login en el sistema origen
        REEMPLAZAR LOS SELECTORES CON LOS DE TU SISTEMA ORIGEN
        """
        logger.info("Iniciando login en sistema origen...")
        
        try:
            # Navegar a la URL origen
            self.driver.get(self.url_origen)
            logger.info(f"Navegando a: {self.url_origen}")
            
            # ESPERAR Y LOCALIZAR CAMPO DE USUARIO
            # REEMPLAZAR CON EL SELECTOR REAL DE TU SISTEMA
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))  # CAMBIAR ESTE SELECTOR
            )
            username_field.clear()
            username_field.send_keys(self.user_origen)
            logger.info("Usuario ingresado")
            
            # ESPERAR Y LOCALIZAR CAMPO DE CONTRASEÑA
            # REEMPLAZAR CON EL SELECTOR REAL DE TU SISTEMA
            password_field = self.driver.find_element(By.ID, "password")  # CAMBIAR ESTE SELECTOR
            password_field.clear()
            password_field.send_keys(self.pass_origen)
            logger.info("Contraseña ingresada")
            
            # LOCALIZAR Y HACER CLIC EN BOTÓN DE LOGIN
            # REEMPLAZAR CON EL SELECTOR REAL DE TU SISTEMA
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")  # CAMBIAR ESTE SELECTOR
            login_button.click()
            logger.info("Botón de login presionado")
            
            # VERIFICAR QUE EL LOGIN FUE EXITOSO
            # REEMPLAZAR CON UN ELEMENTO QUE APAREZCA DESPUÉS DEL LOGIN EXITOSO
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))  # CAMBIAR ESTE SELECTOR
            )
            logger.info("Login exitoso en sistema origen")
            
            return True
            
        except TimeoutException:
            logger.error("Timeout durante el login en sistema origen")
            return False
        except Exception as e:
            logger.error(f"Error durante el login en sistema origen: {str(e)}")
            return False
    
    def _extraer_eventos(self):
        """
        PASO 2: Extraer eventos del calendario
        REEMPLAZAR LOS SELECTORES CON LOS DE TU SISTEMA ORIGEN
        """
        logger.info("Iniciando extracción de eventos...")
        
        try:
            # NAVEGAR A LA VISTA DE EVENTOS/CALENDARIO
            # REEMPLAZAR CON LA URL O ACCIÓN PARA IR A LOS EVENTOS
            eventos_url = f"{self.url_origen}/eventos"  # CAMBIAR ESTA URL
            self.driver.get(eventos_url)
            logger.info(f"Navegando a vista de eventos: {eventos_url}")
            
            # ESPERAR A QUE CARGUE LA LISTA DE EVENTOS
            # REEMPLAZAR CON EL SELECTOR DEL CONTENEDOR DE EVENTOS
            eventos_container = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "eventos-lista"))  # CAMBIAR ESTE SELECTOR
            )
            
            # LOCALIZAR TODOS LOS EVENTOS
            # REEMPLAZAR CON EL SELECTOR DE CADA EVENTO INDIVIDUAL
            eventos = self.driver.find_elements(By.CLASS_NAME, "evento-item")  # CAMBIAR ESTE SELECTOR
            
            logger.info(f"Encontrados {len(eventos)} eventos")
            
            eventos_extraidos = []
            
            for i, evento in enumerate(eventos):
                try:
                    # EXTRAER DATOS DE CADA EVENTO
                    # REEMPLAZAR TODOS ESTOS SELECTORES CON LOS REALES DE TU SISTEMA
                    
                    evento_data = {
                        'NOMBRE_CLIENTE': evento.find_element(By.CLASS_NAME, "cliente-nombre").text.strip(),  # CAMBIAR
                        'TIPO_EVENTO': evento.find_element(By.CLASS_NAME, "tipo-evento").text.strip(),  # CAMBIAR
                        'AGASAJADO_A': evento.find_element(By.CLASS_NAME, "agasajado").text.strip(),  # CAMBIAR
                        'Fecha': evento.find_element(By.CLASS_NAME, "fecha-evento").text.strip(),  # CAMBIAR
                        'Horario_Evento': evento.find_element(By.CLASS_NAME, "horario-evento").text.strip(),  # CAMBIAR
                        'SalonAsignado': evento.find_element(By.CLASS_NAME, "salon").text.strip(),  # CAMBIAR
                        'ID_Unico_Origen': evento.get_attribute('data-id') or f"EVENTO_{i+1}"  # CAMBIAR
                    }
                    
                    eventos_extraidos.append(evento_data)
                    logger.info(f"Evento {i+1} extraído: {evento_data['NOMBRE_CLIENTE']}")
                    
                except Exception as e:
                    logger.warning(f"Error extrayendo evento {i+1}: {str(e)}")
                    continue
            
            self.eventos_extraidos = eventos_extraidos
            logger.info(f"Extracción completada: {len(eventos_extraidos)} eventos procesados")
            
            return True
            
        except Exception as e:
            logger.error(f"Error durante la extracción de eventos: {str(e)}")
            return False
    
    def _login_sistema_destino(self):
        """
        PASO 3A: Login en el sistema destino
        REEMPLAZAR LOS SELECTORES CON LOS DE TU SISTEMA DESTINO
        """
        logger.info("Iniciando login en sistema destino...")
        
        try:
            # Navegar a la URL destino
            self.driver.get(self.url_destino)
            logger.info(f"Navegando a: {self.url_destino}")
            
            # ESPERAR Y LOCALIZAR CAMPO DE USUARIO
            # REEMPLAZAR CON EL SELECTOR REAL DE TU SISTEMA DESTINO
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "usuario"))  # CAMBIAR ESTE SELECTOR
            )
            username_field.clear()
            username_field.send_keys(self.user_destino)
            logger.info("Usuario destino ingresado")
            
            # ESPERAR Y LOCALIZAR CAMPO DE CONTRASEÑA
            # REEMPLAZAR CON EL SELECTOR REAL DE TU SISTEMA DESTINO
            password_field = self.driver.find_element(By.ID, "clave")  # CAMBIAR ESTE SELECTOR
            password_field.clear()
            password_field.send_keys(self.pass_destino)
            logger.info("Contraseña destino ingresada")
            
            # LOCALIZAR Y HACER CLIC EN BOTÓN DE LOGIN
            # REEMPLAZAR CON EL SELECTOR REAL DE TU SISTEMA DESTINO
            login_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")  # CAMBIAR ESTE SELECTOR
            login_button.click()
            logger.info("Botón de login destino presionado")
            
            # VERIFICAR QUE EL LOGIN FUE EXITOSO
            # REEMPLAZAR CON UN ELEMENTO QUE APAREZCA DESPUÉS DEL LOGIN EXITOSO
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "menu-principal"))  # CAMBIAR ESTE SELECTOR
            )
            logger.info("Login exitoso en sistema destino")
            
            return True
            
        except TimeoutException:
            logger.error("Timeout durante el login en sistema destino")
            return False
        except Exception as e:
            logger.error(f"Error durante el login en sistema destino: {str(e)}")
            return False
    
    def _insertar_eventos(self):
        """
        PASO 3B: Insertar eventos en el sistema destino
        REEMPLAZAR LOS SELECTORES CON LOS DE TU SISTEMA DESTINO
        """
        logger.info("Iniciando inserción de eventos...")
        
        try:
            eventos_insertados = 0
            
            for i, evento in enumerate(self.eventos_extraidos):
                try:
                    logger.info(f"Procesando evento {i+1}/{len(self.eventos_extraidos)}: {evento['NOMBRE_CLIENTE']}")
                    
                    # NAVEGAR AL FORMULARIO DE NUEVO EVENTO
                    # REEMPLAZAR CON LA URL O ACCIÓN PARA CREAR NUEVO EVENTO
                    nuevo_evento_url = f"{self.url_destino}/nuevo-evento"  # CAMBIAR ESTA URL
                    self.driver.get(nuevo_evento_url)
                    
                    # ESPERAR A QUE CARGUE EL FORMULARIO
                    # REEMPLAZAR CON EL SELECTOR DEL FORMULARIO
                    formulario = self.wait.until(
                        EC.presence_of_element_located((By.ID, "formulario-evento"))  # CAMBIAR ESTE SELECTOR
                    )
                    
                    # LLENAR CAMPOS DEL FORMULARIO
                    # REEMPLAZAR TODOS ESTOS SELECTORES CON LOS REALES DE TU SISTEMA DESTINO
                    
                    # Campo Nombre Cliente
                    cliente_field = self.driver.find_element(By.ID, "nombre-cliente")  # CAMBIAR
                    cliente_field.clear()
                    cliente_field.send_keys(evento['NOMBRE_CLIENTE'])
                    
                    # Campo Tipo de Evento
                    tipo_field = self.driver.find_element(By.ID, "tipo-evento")  # CAMBIAR
                    tipo_field.clear()
                    tipo_field.send_keys(evento['TIPO_EVENTO'])
                    
                    # Campo Agasajado/a
                    agasajado_field = self.driver.find_element(By.ID, "agasajado")  # CAMBIAR
                    agasajado_field.clear()
                    agasajado_field.send_keys(evento['AGASAJADO_A'])
                    
                    # Campo Fecha
                    fecha_field = self.driver.find_element(By.ID, "fecha-evento")  # CAMBIAR
                    fecha_field.clear()
                    fecha_field.send_keys(evento['Fecha'])
                    
                    # Campo Horario
                    horario_field = self.driver.find_element(By.ID, "horario-evento")  # CAMBIAR
                    horario_field.clear()
                    horario_field.send_keys(evento['Horario_Evento'])
                    
                    # Campo Salón
                    salon_field = self.driver.find_element(By.ID, "salon-asignado")  # CAMBIAR
                    salon_field.clear()
                    salon_field.send_keys(evento['SalonAsignado'])
                    
                    logger.info("Campos del formulario completados")
                    
                    # GUARDAR EL EVENTO
                    # REEMPLAZAR CON EL SELECTOR DEL BOTÓN GUARDAR
                    guardar_button = self.driver.find_element(By.ID, "btn-guardar")  # CAMBIAR ESTE SELECTOR
                    guardar_button.click()
                    
                    # ESPERAR CONFIRMACIÓN DE GUARDADO
                    # REEMPLAZAR CON UN ELEMENTO QUE APAREZCA DESPUÉS DEL GUARDADO EXITOSO
                    self.wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "mensaje-exito"))  # CAMBIAR ESTE SELECTOR
                    )
                    
                    eventos_insertados += 1
                    logger.info(f"Evento {i+1} insertado exitosamente")
                    
                    # Pequeña pausa entre eventos
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error insertando evento {i+1}: {str(e)}")
                    continue
            
            logger.info(f"Inserción completada: {eventos_insertados}/{len(self.eventos_extraidos)} eventos insertados")
            return eventos_insertados > 0
            
        except Exception as e:
            logger.error(f"Error durante la inserción de eventos: {str(e)}")
            return False
    
    def ejecutar_rpa(self):
        """Ejecutar el proceso completo de RPA"""
        logger.info("=== INICIANDO PROCESO RPA ===")
        
        try:
            # Configurar navegador
            self._configurar_navegador()
            
            # PASO 1: Login sistema origen
            if not self._login_sistema_origen():
                raise Exception("Falló el login en sistema origen")
            
            # PASO 2: Extraer eventos
            if not self._extraer_eventos():
                raise Exception("Falló la extracción de eventos")
            
            if not self.eventos_extraidos:
                logger.warning("No se encontraron eventos para procesar")
                return False
            
            # PASO 3: Login sistema destino
            if not self._login_sistema_destino():
                raise Exception("Falló el login en sistema destino")
            
            # PASO 4: Insertar eventos
            if not self._insertar_eventos():
                raise Exception("Falló la inserción de eventos")
            
            logger.info("=== PROCESO RPA COMPLETADO EXITOSAMENTE ===")
            return True
            
        except Exception as e:
            logger.error(f"Error en el proceso RPA: {str(e)}")
            return False
        
        finally:
            # Cerrar navegador
            if self.driver:
                self.driver.quit()
                logger.info("Navegador cerrado")
    
    def ejecutar_programado(self):
        """Ejecutar el RPA de forma programada"""
        logger.info("Ejecutando RPA programado...")
        resultado = self.ejecutar_rpa()
        
        if resultado:
            logger.info("RPA ejecutado exitosamente")
        else:
            logger.error("RPA falló en la ejecución")
        
        return resultado

def main():
    """Función principal"""
    # Crear instancia del RPA
    rpa = RPAEventos()
    
    # Programar ejecución semanal (lunes a las 09:00)
    schedule.every().monday.at("09:00").do(rpa.ejecutar_programado)
    
    logger.info("RPA programado para ejecutarse todos los lunes a las 09:00")
    logger.info("Presiona Ctrl+C para detener el programa")
    
    # Mantener el programa ejecutándose
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verificar cada minuto
    except KeyboardInterrupt:
        logger.info("Programa detenido por el usuario")

if __name__ == "__main__":
    main()


