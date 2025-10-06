#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INSPECCIÓN DEL FORMULARIO - ENCONTRAR SELECTORES CORRECTOS
========================================================

Script para inspeccionar el formulario modificado y encontrar
los selectores correctos, especialmente para "Celular 2".

Autor: Sistema RPA Janos
Fecha: 05/10/2025
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class InspeccionarFormulario:
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
    
    def navegar_a_coordis(self):
        """Navegar al software COORDIS"""
        print("🌐 Navegando al software COORDIS...")
        
        try:
            self.driver.get("http://localhost:3001")
            time.sleep(5)  # Esperar más tiempo para que cargue
            
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
    
    def inspeccionar_formulario(self):
        """Inspeccionar todos los elementos del formulario"""
        print("🔍 Inspeccionando formulario...")
        
        try:
            # Buscar todos los inputs
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            print(f"\n📋 INPUTS ENCONTRADOS ({len(inputs)}):")
            
            for i, input_elem in enumerate(inputs):
                try:
                    name = input_elem.get_attribute('name') or 'sin-name'
                    placeholder = input_elem.get_attribute('placeholder') or 'sin-placeholder'
                    input_type = input_elem.get_attribute('type') or 'sin-type'
                    value = input_elem.get_attribute('value') or ''
                    
                    print(f"  {i+1}. name='{name}' | placeholder='{placeholder}' | type='{input_type}' | value='{value}'")
                except:
                    print(f"  {i+1}. Error leyendo input")
            
            # Buscar todos los labels
            labels = self.driver.find_elements(By.TAG_NAME, "label")
            print(f"\n🏷️ LABELS ENCONTRADOS ({len(labels)}):")
            
            for i, label in enumerate(labels):
                try:
                    text = label.text or 'sin-texto'
                    for_attr = label.get_attribute('for') or 'sin-for'
                    print(f"  {i+1}. Texto: '{text}' | for='{for_attr}'")
                except:
                    print(f"  {i+1}. Error leyendo label")
            
            # Buscar específicamente campos de celular
            print(f"\n📱 BUSCANDO CAMPOS DE CELULAR:")
            
            # Buscar por name
            celular_selectors = [
                "input[name='celular']",
                "input[name='celular_2']",
                "input[placeholder*='celular']",
                "input[placeholder*='Celular']"
            ]
            
            for selector in celular_selectors:
                try:
                    elementos = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elementos:
                        print(f"  ✅ Selector '{selector}': {len(elementos)} elementos encontrados")
                        for elem in elementos:
                            name = elem.get_attribute('name') or 'sin-name'
                            placeholder = elem.get_attribute('placeholder') or 'sin-placeholder'
                            print(f"    - name='{name}' | placeholder='{placeholder}'")
                    else:
                        print(f"  ❌ Selector '{selector}': No encontrado")
                except Exception as e:
                    print(f"  ⚠️ Selector '{selector}': Error - {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error inspeccionando formulario: {e}")
            return False
    
    def cerrar_driver(self):
        """Cerrar el driver"""
        if self.driver:
            self.driver.quit()
            print("🔒 Driver cerrado")

def main():
    """Función principal"""
    print("🔍 INSPECCIÓN DEL FORMULARIO - ENCONTRAR SELECTORES CORRECTOS")
    print("=" * 70)
    
    inspector = InspeccionarFormulario()
    
    try:
        # Configurar driver
        if not inspector.configurar_driver():
            return False
        
        # Navegar a COORDIS
        if not inspector.navegar_a_coordis():
            return False
        
        # Hacer clic en "NUEVA COORDINACIÓN"
        if not inspector.hacer_clic_nueva_coordinacion():
            return False
        
        # Inspeccionar formulario
        if not inspector.inspeccionar_formulario():
            return False
        
        print("\n🎉 INSPECCIÓN COMPLETADA")
        print("✅ Formulario inspeccionado")
        print("✅ Selectores identificados")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error en la inspección: {e}")
        return False
    
    finally:
        inspector.cerrar_driver()

if __name__ == "__main__":
    main()


