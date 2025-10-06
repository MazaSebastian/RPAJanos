#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPA INTEGRACIÓN COMPLETA - JANOS + COORDIS
==========================================

Script que integra la extracción de datos del sistema Janos
con la automatización del formulario de COORDIS.

Funcionalidades:
1. Extrae datos del sistema Janos (RPA existente)
2. Navega al software COORDIS
3. Llena automáticamente el formulario "NUEVA COORDINACIÓN"
4. Guarda cada coordinación

Autor: Sistema RPA Janos
Fecha: 05/10/2025
"""

import os
import sys
import time
import pandas as pd
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

class RPAIntegracionCoordis:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.datos_eventos = []
        
    def configurar_driver(self):
        """Configurar el driver de Chrome para la integración"""
        print("🔧 Configurando driver de Chrome...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        # chrome_options.add_argument("--headless")  # Comentado para ver el proceso
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            print("✅ Driver configurado correctamente")
            return True
        except Exception as e:
            print(f"❌ Error configurando driver: {e}")
            return False
    
    def extraer_datos_janos(self):
        """Extraer datos del sistema Janos usando el RPA existente"""
        print("📊 Extrayendo datos del sistema Janos...")
        
        try:
            # Cargar datos extraídos previamente
            if os.path.exists('todos_los_eventos_extraidos.csv'):
                df = pd.read_csv('todos_los_eventos_extraidos.csv')
                print(f"✅ Cargados {len(df)} eventos desde CSV")
                return df
            else:
                print("❌ No se encontró el archivo de datos extraídos")
                return None
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return None
    
    def navegar_a_coordis(self):
        """Navegar al software COORDIS"""
        print("🌐 Navegando al software COORDIS...")
        
        try:
            # Navegar a localhost:3001 (COORDIS)
            self.driver.get("http://localhost:3001")
            time.sleep(3)
            
            # Verificar que la página cargó correctamente
            if "Jano's" in self.driver.title or "Coordinaciones" in self.driver.title:
                print("✅ Acceso exitoso al software COORDIS")
                return True
            else:
                print("❌ No se pudo acceder al software COORDIS")
                return False
                
        except Exception as e:
            print(f"❌ Error navegando a COORDIS: {e}")
            return False
    
    def hacer_clic_nueva_coordinacion(self):
        """Hacer clic en el botón 'NUEVA COORDINACIÓN'"""
        print("🖱️ Buscando botón 'NUEVA COORDINACIÓN'...")
        
        try:
            # Buscar el botón en la barra lateral
            boton_selectors = [
                "//button[contains(text(), 'Nueva Coordinación')]",
                "//a[contains(text(), 'Nueva Coordinación')]",
                "//button[contains(@class, 'ActionButton')]",
                "//a[contains(@href, '/coordinations/new')]"
            ]
            
            for selector in boton_selectors:
                try:
                    boton = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    boton.click()
                    print("✅ Botón 'NUEVA COORDINACIÓN' encontrado y clickeado")
                    time.sleep(2)
                    return True
                except:
                    continue
            
            print("❌ No se pudo encontrar el botón 'NUEVA COORDINACIÓN'")
            return False
            
        except Exception as e:
            print(f"❌ Error haciendo clic en el botón: {e}")
            return False
    
    def llenar_formulario_coordinacion(self, evento):
        """Llenar el formulario de coordinación con los datos del evento"""
        print(f"📝 Llenando formulario para evento: {evento.get('codigo_evento', 'N/A')}")
        
        try:
            # Mapeo de campos OBLIGATORIOS únicamente (evitar errores de tiempo)
            mapeo_campos = {
                'title': f"{evento.get('tipo_evento', '')} de {evento.get('homenajeada', '')}",
                'event_date': self.formatear_fecha(evento.get('fecha_evento', '')),
                'client_name': evento.get('cliente', ''),
                'client_phone': f"{evento.get('celular', '')}, {evento.get('celular_2', '')}",
                'event_type': self.mapear_tipo_evento(evento.get('tipo_evento', '')),
                # Campos opcionales solo si tienen valor
                'codigo_evento': evento.get('codigo_evento', '') if evento.get('codigo_evento') else None,
                'pack': evento.get('tipo_pack', '') if evento.get('tipo_pack') else None,
                'salon': evento.get('salon', '') if evento.get('salon') else None,
                'honoree_name': evento.get('homenajeada', '') if evento.get('homenajeada') else None
                # NO incluir campos de tiempo para evitar errores
            }
            
            # Llenar cada campo (solo campos con valor válido)
            for campo, valor in mapeo_campos.items():
                if valor and valor != '' and valor != '-' and valor is not None:
                    try:
                        self.llenar_campo(campo, valor)
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"  ⚠️ Error llenando campo '{campo}': {e}")
                        continue
                else:
                    print(f"  ⏭️ Saltando campo '{campo}' (sin valor válido)")
            
            print("✅ Formulario llenado correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error llenando formulario: {e}")
            return False
    
    def llenar_campo(self, campo, valor):
        """Llenar un campo específico del formulario"""
        try:
            # Selectores para campos OBLIGATORIOS únicamente (sin campos de tiempo)
            selectors = {
                'title': ["input[name='title']", "input[placeholder*='título']"],
                'event_date': ["input[name='event_date']", "input[type='date']"],
                'client_name': ["input[name='client_name']", "input[placeholder*='cliente']"],
                'client_phone': ["input[name='client_phone']", "input[type='tel']"],
                'event_type': ["select[name='event_type']"],
                'codigo_evento': ["input[name='codigo_evento']", "input[placeholder*='código']"],
                'pack': ["input[name='pack']", "input[placeholder*='pack']"],
                'salon': ["input[name='salon']", "input[placeholder*='salón']"],
                'honoree_name': ["input[name='honoree_name']", "input[placeholder*='agasajado']"]
                # NO incluir selectores de tiempo para evitar errores
            }
            
            if campo in selectors:
                for selector in selectors[campo]:
                    try:
                        elemento = self.driver.find_element(By.CSS_SELECTOR, selector)
                        elemento.clear()
                        elemento.send_keys(str(valor))
                        print(f"  ✅ Campo '{campo}': {valor}")
                        return True
                    except:
                        continue
            
            print(f"  ⚠️ Campo '{campo}' no encontrado")
            return False
            
        except Exception as e:
            print(f"  ❌ Error llenando campo '{campo}': {e}")
            return False
    
    def mapear_tipo_evento(self, tipo_evento):
        """Mapear tipo de evento del RPA al selector de COORDIS"""
        mapeo = {
            '15': 'xv',
            'Cumpleaños': 'cumpleanos',
            'Boda': 'casamiento',
            'Empresarial': 'corporativo',
            'Otro': 'religioso'
        }
        return mapeo.get(tipo_evento, 'xv')
    
    def formatear_fecha(self, fecha_str):
        """Formatear fecha para el input de fecha"""
        try:
            if not fecha_str:
                return ''
            
            # Si ya está en formato YYYY-MM-DD, devolverlo
            if len(fecha_str) == 10 and fecha_str.count('-') == 2:
                return fecha_str
            
            # Intentar parsear diferentes formatos
            from datetime import datetime
            
            # Formato: DD/MM/YYYY(Día)
            if '(' in fecha_str:
                fecha_limpia = fecha_str.split('(')[0].strip()
                fecha_obj = datetime.strptime(fecha_limpia, '%d/%m/%Y')
                return fecha_obj.strftime('%Y-%m-%d')
            
            return fecha_str
            
        except Exception as e:
            print(f"⚠️ Error formateando fecha '{fecha_str}': {e}")
            return fecha_str
    
    def guardar_coordinacion(self):
        """Guardar la coordinación en el sistema"""
        print("💾 Guardando coordinación...")
        
        try:
            # Buscar botón de guardar
            botones_guardar = [
                "button[type='submit']",
                "button:contains('Guardar')",
                "button:contains('Continuar')",
                "//button[contains(text(), 'Guardar')]",
                "//button[contains(text(), 'Continuar')]"
            ]
            
            for selector in botones_guardar:
                try:
                    if selector.startswith('//'):
                        boton = self.driver.find_element(By.XPATH, selector)
                    else:
                        boton = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    boton.click()
                    print("✅ Coordinación guardada exitosamente")
                    time.sleep(3)
                    return True
                except:
                    continue
            
            print("❌ No se pudo encontrar el botón de guardar")
            return False
            
        except Exception as e:
            print(f"❌ Error guardando coordinación: {e}")
            return False
    
    def procesar_todos_los_eventos(self):
        """Procesar todos los eventos extraídos"""
        print("🚀 Iniciando procesamiento de todos los eventos...")
        
        # 1. Extraer datos
        df = self.extraer_datos_janos()
        if df is None or len(df) == 0:
            print("❌ No hay datos para procesar")
            return False
        
        # 2. Navegar a COORDIS
        if not self.navegar_a_coordis():
            return False
        
        eventos_procesados = 0
        eventos_exitosos = 0
        
        for index, evento in df.iterrows():
            print(f"\n📋 Procesando evento {index + 1}/{len(df)}: {evento.get('codigo_evento', 'N/A')}")
            
            try:
                # Hacer clic en "NUEVA COORDINACIÓN"
                if not self.hacer_clic_nueva_coordinacion():
                    print("❌ No se pudo acceder al formulario")
                    continue
                
                # Llenar formulario
                if not self.llenar_formulario_coordinacion(evento):
                    print("❌ Error llenando formulario")
                    continue
                
                # Guardar coordinación
                if not self.guardar_coordinacion():
                    print("❌ Error guardando coordinación")
                    continue
                
                eventos_exitosos += 1
                print(f"✅ Evento {index + 1} procesado exitosamente")
                
                # Esperar antes del siguiente evento
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error procesando evento {index + 1}: {e}")
                continue
            
            eventos_procesados += 1
        
        print(f"\n📊 RESUMEN FINAL:")
        print(f"   Total eventos: {len(df)}")
        print(f"   Procesados: {eventos_procesados}")
        print(f"   Exitosos: {eventos_exitosos}")
        print(f"   Fallidos: {eventos_procesados - eventos_exitosos}")
        
        return eventos_exitosos > 0
    
    def cerrar_driver(self):
        """Cerrar el driver"""
        if self.driver:
            self.driver.quit()
            print("🔒 Driver cerrado")

def main():
    """Función principal"""
    print("🤖 RPA INTEGRACIÓN JANOS + COORDIS")
    print("=" * 50)
    
    rpa = RPAIntegracionCoordis()
    
    try:
        # Configurar driver
        if not rpa.configurar_driver():
            return False
        
        # Procesar todos los eventos
        exito = rpa.procesar_todos_los_eventos()
        
        if exito:
            print("\n🎉 INTEGRACIÓN COMPLETADA EXITOSAMENTE")
        else:
            print("\n❌ INTEGRACIÓN FALLÓ")
        
        return exito
        
    except Exception as e:
        print(f"\n❌ Error en la integración: {e}")
        return False
    
    finally:
        rpa.cerrar_driver()

if __name__ == "__main__":
    main()
