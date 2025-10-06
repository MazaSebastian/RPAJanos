#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROBAR CELULAR 2 - ENCONTRAR SELECTOR CORRECTO
=============================================

Script específico para encontrar el selector correcto del campo "Celular 2".

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

class ProbarCelular2:
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
            time.sleep(5)
            
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
    
    def probar_selectores_celular_2(self):
        """Probar diferentes selectores para el campo Celular 2"""
        print("🔍 Probando selectores para Celular 2...")
        
        # Lista de selectores a probar
        selectors_to_test = [
            "input[placeholder='1157526518']",
            "input[placeholder*='1157526518']",
            "input[type='tel'][placeholder='1157526518']",
            "input[type='tel']:nth-of-type(2)",
            "input[type='tel']:nth-child(6)",
            "input[type='tel']:nth-child(7)",
            "input[type='tel']:nth-child(8)",
            "input[type='tel']:nth-child(9)",
            "input[type='tel']:nth-child(10)",
            "input[type='tel']:last-of-type",
            "input[type='tel']:nth-last-of-type(1)",
            "input[type='tel']:nth-last-of-type(2)",
            "input[type='tel']:nth-last-of-type(3)",
            "input[type='tel']:nth-last-of-type(4)",
            "input[type='tel']:nth-last-of-type(5)",
            "input[type='tel']:nth-last-of-type(6)",
            "input[type='tel']:nth-last-of-type(7)",
            "input[type='tel']:nth-last-of-type(8)",
            "input[type='tel']:nth-last-of-type(9)",
            "input[type='tel']:nth-last-of-type(10)"
        ]
        
        for i, selector in enumerate(selectors_to_test, 1):
            try:
                elementos = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elementos:
                    print(f"  ✅ Selector {i}: '{selector}' - {len(elementos)} elementos encontrados")
                    for j, elem in enumerate(elementos):
                        placeholder = elem.get_attribute('placeholder') or 'sin-placeholder'
                        value = elem.get_attribute('value') or ''
                        print(f"    Elemento {j+1}: placeholder='{placeholder}' | value='{value}'")
                        
                        # Intentar llenar el campo
                        try:
                            elem.clear()
                            elem.send_keys("1157526518")
                            print(f"    ✅ Campo llenado exitosamente")
                            return True
                        except Exception as e:
                            print(f"    ❌ Error llenando campo: {e}")
                else:
                    print(f"  ❌ Selector {i}: '{selector}' - No encontrado")
            except Exception as e:
                print(f"  ⚠️ Selector {i}: '{selector}' - Error: {e}")
        
        return False
    
    def cerrar_driver(self):
        """Cerrar el driver"""
        if self.driver:
            self.driver.quit()
            print("🔒 Driver cerrado")

def main():
    """Función principal"""
    print("🔍 PROBAR CELULAR 2 - ENCONTRAR SELECTOR CORRECTO")
    print("=" * 60)
    
    probador = ProbarCelular2()
    
    try:
        # Configurar driver
        if not probador.configurar_driver():
            return False
        
        # Navegar a COORDIS
        if not probador.navegar_a_coordis():
            return False
        
        # Hacer clic en "NUEVA COORDINACIÓN"
        if not probador.hacer_clic_nueva_coordinacion():
            return False
        
        # Probar selectores para Celular 2
        if probador.probar_selectores_celular_2():
            print("\n🎉 CELULAR 2 ENCONTRADO Y LLENADO EXITOSAMENTE")
        else:
            print("\n❌ NO SE PUDO ENCONTRAR EL CAMPO CELULAR 2")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error en la prueba: {e}")
        return False
    
    finally:
        probador.cerrar_driver()

if __name__ == "__main__":
    main()


