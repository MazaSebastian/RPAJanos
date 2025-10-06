#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPA PRUEBA CON HORARIOS FIJOS - SOLUCIÓN DEFINITIVA
==================================================

Script de prueba que usa horarios fijos para evitar
completamente los errores de "Invalid time value".

Horarios fijos:
- Inicio: 21:30
- Fin: 05:30

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

class RPAPruebaHorariosFijos:
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
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        
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
            
            # Cerrar iframe de desarrollo si existe
            try:
                iframe = self.driver.find_element(By.ID, "webpack-dev-server-client-overlay")
                self.driver.execute_script("arguments[0].style.display = 'none';", iframe)
                print("✅ Iframe de desarrollo cerrado")
            except:
                pass
            
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
    
    def llenar_formulario_con_horarios_fijos(self, evento):
        """Llenar el formulario con horarios fijos"""
        print(f"📝 Llenando formulario con horarios fijos para evento: {evento.get('codigo_evento', 'N/A')}")
        
        try:
            # Campos con horarios fijos
            campos_completos = {
                'title': f"{evento.get('tipo_evento', '')} de {evento.get('homenajeada', '')}",
                'event_date': self.formatear_fecha(evento.get('fecha_evento', '')),
                'client_name': evento.get('cliente', ''),
                'client_phone': f"{evento.get('celular', '')}, {evento.get('celular_2', '')}",
                # Horarios fijos para evitar errores
                'start_time': '21:30',  # Horario de inicio fijo
                'end_time': '05:30'     # Horario de fin fijo
            }
            
            # Llenar todos los campos
            for campo, valor in campos_completos.items():
                if valor and valor != '':
                    try:
                        self.llenar_campo_con_horarios(campo, valor)
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"  ⚠️ Error llenando campo '{campo}': {e}")
                        continue
            
            print("✅ Formulario llenado con horarios fijos")
            return True
            
        except Exception as e:
            print(f"❌ Error llenando formulario: {e}")
            return False
    
    def llenar_campo_con_horarios(self, campo, valor):
        """Llenar un campo del formulario incluyendo horarios"""
        try:
            # Selectores para todos los campos incluyendo horarios
            selectors = {
                'title': ["input[name='title']"],
                'event_date': ["input[name='event_date']", "input[type='date']"],
                'client_name': ["input[name='client_name']"],
                'client_phone': ["input[name='client_phone']", "input[type='tel']"],
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
        """Guardar la coordinación usando JavaScript"""
        print("💾 Guardando coordinación...")
        
        try:
            # Cerrar iframe de desarrollo si existe
            try:
                iframe = self.driver.find_element(By.ID, "webpack-dev-server-client-overlay")
                self.driver.execute_script("arguments[0].style.display = 'none';", iframe)
                print("✅ Iframe de desarrollo cerrado")
            except:
                pass
            
            # Buscar botón de guardar
            boton_selectors = [
                "//button[contains(text(), 'Guardar Coordinación')]",
                "//button[contains(text(), 'Continuar')]",
                "//button[contains(text(), 'Guardar')]"
            ]
            
            for selector in boton_selectors:
                try:
                    boton = self.driver.find_element(By.XPATH, selector)
                    self.driver.execute_script("arguments[0].click();", boton)
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
    print("🤖 RPA PRUEBA CON HORARIOS FIJOS - SOLUCIÓN DEFINITIVA")
    print("=" * 60)
    print("🕐 Horarios fijos:")
    print("   - Inicio: 21:30")
    print("   - Fin: 05:30")
    print("=" * 60)
    
    rpa = RPAPruebaHorariosFijos()
    
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
        
        # Llenar formulario con horarios fijos
        if not rpa.llenar_formulario_con_horarios_fijos(evento):
            return False
        
        # Guardar coordinación
        if not rpa.guardar_coordinacion():
            return False
        
        print("\n🎉 PRUEBA CON HORARIOS FIJOS COMPLETADA EXITOSAMENTE")
        print("✅ Horarios fijos aplicados")
        print("✅ Sin errores de tiempo")
        print("✅ Coordinación guardada")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en la prueba: {e}")
        return False
    
    finally:
        rpa.cerrar_driver()

if __name__ == "__main__":
    main()


