#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPA INTEGRACIÓN SIMPLE - PRUEBA UN EVENTO
==========================================

Script simplificado para probar la integración con un solo evento.
Evita campos de tiempo para prevenir errores.

Autor: Sistema RPA Janos
Fecha: 05/10/2025
"""

import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class RPAIntegracionSimple:
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def configurar_driver(self):
        """Configurar el driver de Chrome"""
        print("🔧 Configurando driver de Chrome...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            print("✅ Driver configurado correctamente")
            return True
        except Exception as e:
            print(f"❌ Error configurando driver: {e}")
            return False
    
    def cargar_datos(self):
        """Cargar un evento de prueba"""
        print("📊 Cargando datos de prueba...")
        
        try:
            df = pd.read_csv('todos_los_eventos_extraidos.csv')
            if len(df) > 0:
                evento = df.iloc[0]  # Primer evento
                print(f"✅ Evento cargado: {evento.get('codigo_evento', 'N/A')}")
                return evento
            else:
                print("❌ No hay eventos disponibles")
                return None
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return None
    
    def navegar_a_coordis(self):
        """Navegar al software COORDIS"""
        print("🌐 Navegando al software COORDIS...")
        
        try:
            self.driver.get("http://localhost:3001")
            time.sleep(3)
            
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
                "//a[contains(@href, '/coordinations/new')]"
            ]
            
            for selector in boton_selectors:
                try:
                    boton = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    boton.click()
                    print("✅ Botón 'NUEVA COORDINACIÓN' encontrado y clickeado")
                    time.sleep(3)
                    return True
                except:
                    continue
            
            print("❌ No se pudo encontrar el botón 'NUEVA COORDINACIÓN'")
            return False
            
        except Exception as e:
            print(f"❌ Error haciendo clic en el botón: {e}")
            return False
    
    def llenar_formulario_simple(self, evento):
        """Llenar solo los campos obligatorios"""
        print(f"📝 Llenando formulario para evento: {evento.get('codigo_evento', 'N/A')}")
        
        try:
            # Campos obligatorios + campos de tiempo con datos ficticios válidos
            campos_obligatorios = {
                'title': f"{evento.get('tipo_evento', '')} de {evento.get('homenajeada', '')}",
                'event_date': self.formatear_fecha(evento.get('fecha_evento', '')),
                'client_name': evento.get('cliente', ''),
                'client_phone': f"{evento.get('celular', '')}, {evento.get('celular_2', '')}",
                'event_type': self.mapear_tipo_evento(evento.get('tipo_evento', '')),
                # Campos de tiempo con datos ficticios válidos para evitar errores
                'start_time': '20:00',  # Hora de inicio ficticia
                'end_time': '02:00'     # Hora de fin ficticia
            }
            
            # Llenar solo campos obligatorios
            for campo, valor in campos_obligatorios.items():
                if valor and valor != '':
                    try:
                        self.llenar_campo_simple(campo, valor)
                        time.sleep(1)
                    except Exception as e:
                        print(f"  ⚠️ Error llenando campo '{campo}': {e}")
                        continue
            
            print("✅ Formulario llenado correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error llenando formulario: {e}")
            return False
    
    def llenar_campo_simple(self, campo, valor):
        """Llenar un campo específico del formulario"""
        try:
            # Selectores para campos obligatorios + campos de tiempo
            selectors = {
                'title': ["input[name='title']"],
                'event_date': ["input[name='event_date']", "input[type='date']"],
                'client_name': ["input[name='client_name']"],
                'client_phone': ["input[name='client_phone']", "input[type='tel']"],
                'event_type': ["select[name='event_type']"],
                'start_time': ["input[name='start_time']", "input[placeholder*='inicio']"],
                'end_time': ["input[name='end_time']", "input[placeholder*='fin']"]
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
            
            # Formato: DD/MM/YYYY(Día)
            if '(' in fecha_str:
                fecha_limpia = fecha_str.split('(')[0].strip()
                from datetime import datetime
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
    
    def cerrar_driver(self):
        """Cerrar el driver"""
        if self.driver:
            self.driver.quit()
            print("🔒 Driver cerrado")

def main():
    """Función principal"""
    print("🤖 RPA INTEGRACIÓN SIMPLE - PRUEBA UN EVENTO")
    print("=" * 50)
    
    rpa = RPAIntegracionSimple()
    
    try:
        # Configurar driver
        if not rpa.configurar_driver():
            return False
        
        # Cargar datos
        evento = rpa.cargar_datos()
        if evento is None:
            return False
        
        # Navegar a COORDIS
        if not rpa.navegar_a_coordis():
            return False
        
        # Hacer clic en "NUEVA COORDINACIÓN"
        if not rpa.hacer_clic_nueva_coordinacion():
            return False
        
        # Llenar formulario
        if not rpa.llenar_formulario_simple(evento):
            return False
        
        # Guardar coordinación
        if not rpa.guardar_coordinacion():
            return False
        
        print("\n🎉 INTEGRACIÓN SIMPLE COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en la integración: {e}")
        return False
    
    finally:
        rpa.cerrar_driver()

if __name__ == "__main__":
    main()
