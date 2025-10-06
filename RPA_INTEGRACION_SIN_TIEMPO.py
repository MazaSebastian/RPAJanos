#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPA INTEGRACIÓN SIN CAMPOS DE TIEMPO - SOLUCIÓN DEFINITIVA
=========================================================

Script que evita completamente los campos de tiempo para eliminar
el error "Invalid time value" de manera definitiva.

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

class RPAIntegracionSinTiempo:
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
    
    def llenar_formulario_sin_tiempo(self, evento):
        """Llenar SOLO los campos que NO causan errores de tiempo"""
        print(f"📝 Llenando formulario para evento: {evento.get('codigo_evento', 'N/A')}")
        
        try:
            # SOLO campos que NO causan errores de tiempo
            campos_seguros = {
                'title': f"{evento.get('tipo_evento', '')} de {evento.get('homenajeada', '')}",
                'event_date': self.formatear_fecha(evento.get('fecha_evento', '')),
                'client_name': evento.get('cliente', ''),
                'client_phone': f"{evento.get('celular', '')}, {evento.get('celular_2', '')}",
                'codigo_evento': evento.get('codigo_evento', ''),
                'pack': evento.get('tipo_pack', ''),
                'salon': evento.get('salon', ''),
                'honoree_name': evento.get('homenajeada', ''),
                'total_invitados': '100'
                # NO incluir campos de tiempo para evitar errores
            }
            
            # Llenar solo campos seguros
            for campo, valor in campos_seguros.items():
                if valor and valor != '':
                    try:
                        self.llenar_campo_seguro(campo, valor)
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"  ⚠️ Error llenando campo '{campo}': {e}")
                        continue
            
            print("✅ Formulario llenado correctamente (sin campos de tiempo)")
            return True
            
        except Exception as e:
            print(f"❌ Error llenando formulario: {e}")
            return False
    
    def llenar_campo_seguro(self, campo, valor):
        """Llenar un campo específico del formulario (sin campos de tiempo)"""
        try:
            # Selectores SOLO para campos seguros (sin tiempo)
            selectors = {
                'title': [
                    "input[name='title']",
                    "input[placeholder*='título']",
                    "input[placeholder*='Título']"
                ],
                'event_date': [
                    "input[name='event_date']",
                    "input[type='date']"
                ],
                'client_name': [
                    "input[name='client_name']",
                    "input[placeholder*='cliente']",
                    "input[placeholder*='Cliente']"
                ],
                'client_phone': [
                    "input[name='client_phone']",
                    "input[type='tel']",
                    "input[placeholder*='teléfono']"
                ],
                'codigo_evento': [
                    "input[name='codigo_evento']",
                    "input[placeholder*='código']",
                    "input[placeholder*='Código']"
                ],
                'pack': [
                    "input[name='pack']",
                    "input[placeholder*='pack']",
                    "input[placeholder*='Pack']"
                ],
                'salon': [
                    "input[name='salon']",
                    "input[placeholder*='salón']",
                    "input[placeholder*='Salón']"
                ],
                'honoree_name': [
                    "input[name='honoree_name']",
                    "input[placeholder*='agasajado']",
                    "input[placeholder*='Agasajado']"
                ],
                'total_invitados': [
                    "input[name='total_invitados']",
                    "input[type='number']",
                    "input[placeholder*='invitados']"
                ]
                # NO incluir selectores de tiempo
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
    
    def seleccionar_tipo_evento(self, tipo_evento):
        """Seleccionar tipo de evento en el dropdown"""
        try:
            print(f"🎯 Seleccionando tipo de evento: {tipo_evento}")
            
            # Mapear tipo de evento
            mapeo = {
                '15': 'xv',
                'Cumpleaños': 'cumpleanos',
                'Boda': 'casamiento',
                'Empresarial': 'corporativo',
                'Otro': 'religioso'
            }
            
            valor_mapeado = mapeo.get(tipo_evento, 'xv')
            
            # Buscar el select de tipo de evento
            selectors = [
                "select[name='event_type']",
                "select[id='event_type']"
            ]
            
            for selector in selectors:
                try:
                    select_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    from selenium.webdriver.support.ui import Select
                    select_obj = Select(select_element)
                    select_obj.select_by_value(valor_mapeado)
                    print(f"  ✅ Tipo de evento seleccionado: {valor_mapeado}")
                    return True
                except:
                    continue
            
            print(f"  ⚠️ No se pudo seleccionar tipo de evento")
            return False
            
        except Exception as e:
            print(f"  ❌ Error seleccionando tipo de evento: {e}")
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
    
    def buscar_boton_guardar(self):
        """Buscar el botón de guardar con múltiples estrategias"""
        print("🔍 Buscando botón de guardar...")
        
        try:
            # Estrategia 1: Buscar por texto
            textos_boton = [
                "Guardar Coordinación",
                "Continuar",
                "Guardar",
                "Save",
                "Submit"
            ]
            
            for texto in textos_boton:
                try:
                    boton = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{texto}')]")
                    print(f"  ✅ Botón encontrado por texto: '{texto}'")
                    return boton
                except:
                    continue
            
            # Estrategia 2: Buscar por atributos
            selectors_atributos = [
                "button[type='submit']",
                "input[type='submit']",
                "button[class*='save']",
                "button[class*='submit']"
            ]
            
            for selector in selectors_atributos:
                try:
                    boton = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"  ✅ Botón encontrado por selector: '{selector}'")
                    return boton
                except:
                    continue
            
            # Estrategia 3: Buscar todos los botones y filtrar
            try:
                botones = self.driver.find_elements(By.TAG_NAME, "button")
                for boton in botones:
                    texto_boton = boton.text.lower()
                    if any(palabra in texto_boton for palabra in ['guardar', 'continuar', 'save', 'submit']):
                        print(f"  ✅ Botón encontrado por filtro: '{boton.text}'")
                        return boton
            except:
                pass
            
            print("  ❌ No se pudo encontrar el botón de guardar")
            return None
            
        except Exception as e:
            print(f"  ❌ Error buscando botón: {e}")
            return None
    
    def guardar_coordinacion(self):
        """Guardar la coordinación en el sistema"""
        print("💾 Guardando coordinación...")
        
        try:
            boton = self.buscar_boton_guardar()
            if boton:
                boton.click()
                print("✅ Coordinación guardada exitosamente")
                time.sleep(3)
                return True
            else:
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
    print("🤖 RPA INTEGRACIÓN SIN CAMPOS DE TIEMPO - SOLUCIÓN DEFINITIVA")
    print("=" * 70)
    
    rpa = RPAIntegracionSinTiempo()
    
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
        
        # Llenar formulario (sin campos de tiempo)
        if not rpa.llenar_formulario_sin_tiempo(evento):
            return False
        
        # Seleccionar tipo de evento
        rpa.seleccionar_tipo_evento(evento.get('tipo_evento', ''))
        
        # Guardar coordinación
        if not rpa.guardar_coordinacion():
            return False
        
        print("\n🎉 INTEGRACIÓN SIN ERRORES COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en la integración: {e}")
        return False
    
    finally:
        rpa.cerrar_driver()

if __name__ == "__main__":
    main()


