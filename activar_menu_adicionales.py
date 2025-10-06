#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para activar el menú desplegable y encontrar ADICIONALES
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def activar_menu_adicionales():
    """Activar el menú desplegable y encontrar ADICIONALES"""
    
    print("=== ACTIVANDO MENÚ PARA ENCONTRAR 'ADICIONALES' ===")
    
    driver = None
    try:
        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 15)
        actions = ActionChains(driver)
        
        # Ejecutar script para ocultar automatización
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # PASO 1: Login completo
        print("\n=== PASO 1: LOGIN INICIAL ===")
        driver.get("https://tecnica.janosgroup.com/login.php")
        print("✓ Navegando a página de login...")
        
        time.sleep(3)
        
        # Llenar credenciales
        username_field = driver.find_element(By.NAME, "username")
        username_field.clear()
        username_field.send_keys("sebastian_maza")
        print("✓ Usuario ingresado")
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys("Janos2025+!")
        print("✓ Contraseña ingresada")
        
        # Hacer login
        login_button = driver.find_element(By.CSS_SELECTOR, "button.button")
        login_button.click()
        print("✓ Botón de login presionado")
        
        # Esperar redirección
        wait.until(lambda driver: "login.php" not in driver.current_url)
        print("✓ Login exitoso - redirigido a página principal")
        
        # PASO 2: Buscar el elemento que activa el menú
        print("\n=== PASO 2: BUSCANDO ELEMENTO ACTIVADOR DEL MENÚ ===")
        
        # Buscar el div de navegación que vimos antes
        try:
            nav_div = driver.find_element(By.CSS_SELECTOR, "div.navBarDiv")
            print(f"✓ Encontrado div de navegación: '{nav_div.text[:50]}...'")
            print(f"  - class: '{nav_div.get_attribute('class')}'")
            print(f"  - visible: {nav_div.is_displayed()}")
            
            # Buscar elementos dentro del nav_div
            elementos_nav = nav_div.find_elements(By.XPATH, ".//*")
            print(f"  - Elementos dentro del nav: {len(elementos_nav)}")
            
            for i, elem in enumerate(elementos_nav[:10]):  # Primeros 10
                if elem.text.strip():
                    print(f"    {i+1}. tag: {elem.tag_name}, text: '{elem.text[:30]}...', class: '{elem.get_attribute('class')}'")
            
            # Intentar hacer clic en el nav_div
            print(f"\n=== INTENTANDO ACTIVAR MENÚ ===")
            print("Haciendo clic en el div de navegación...")
            nav_div.click()
            time.sleep(2)
            
            # Buscar ADICIONALES después del clic
            adicionales_visibles = driver.find_elements(By.XPATH, "//*[contains(text(), 'ADICIONALES') and not(@style='display: none')]")
            print(f"ADICIONALES visibles después del clic: {len(adicionales_visibles)}")
            
            for elem in adicionales_visibles:
                print(f"  - text: '{elem.text}', visible: {elem.is_displayed()}, class: '{elem.get_attribute('class')}'")
                if elem.is_displayed():
                    print(f"  - ¡ADICIONALES VISIBLE! Haciendo clic...")
                    elem.click()
                    time.sleep(3)
                    print(f"  - URL después del clic: {driver.current_url}")
                    return True
            
        except Exception as e:
            print(f"✗ Error con nav_div: {str(e)}")
        
        # PASO 3: Buscar otros elementos que puedan activar el menú
        print(f"\n=== PASO 3: BUSCANDO OTROS ACTIVADORES ===")
        
        # Buscar elementos con hover o click
        hover_elements = driver.find_elements(By.CSS_SELECTOR, "[onmouseover], [onmouseenter], [onclick], [class*='hover'], [class*='menu']")
        print(f"Elementos con eventos de mouse: {len(hover_elements)}")
        
        for i, elem in enumerate(hover_elements[:5]):  # Primeros 5
            try:
                print(f"Probando elemento {i+1}: {elem.tag_name}, class: '{elem.get_attribute('class')}'")
                
                # Hacer hover
                actions.move_to_element(elem).perform()
                time.sleep(1)
                
                # Buscar ADICIONALES después del hover
                adicionales_hover = driver.find_elements(By.XPATH, "//*[contains(text(), 'ADICIONALES')]")
                if adicionales_hover:
                    for adic in adicionales_hover:
                        if adic.is_displayed():
                            print(f"✓ ¡ADICIONALES encontrado con hover!")
                            print(f"  - text: '{adic.text}', class: '{adic.get_attribute('class')}'")
                            adic.click()
                            time.sleep(3)
                            print(f"  - URL después del clic: {driver.current_url}")
                            return True
                
                # Hacer clic
                elem.click()
                time.sleep(1)
                
                # Buscar ADICIONALES después del clic
                adicionales_click = driver.find_elements(By.XPATH, "//*[contains(text(), 'ADICIONALES')]")
                if adicionales_click:
                    for adic in adicionales_click:
                        if adic.is_displayed():
                            print(f"✓ ¡ADICIONALES encontrado con clic!")
                            print(f"  - text: '{adic.text}', class: '{adic.get_attribute('class')}'")
                            adic.click()
                            time.sleep(3)
                            print(f"  - URL después del clic: {driver.current_url}")
                            return True
                            
            except Exception as e:
                print(f"✗ Error con elemento {i+1}: {str(e)}")
        
        # PASO 4: Buscar en el HTML completo
        print(f"\n=== PASO 4: ANÁLISIS COMPLETO DEL HTML ===")
        
        # Obtener todo el HTML y buscar patrones
        html_content = driver.page_source
        if "ADICIONALES" in html_content:
            print("✓ 'ADICIONALES' encontrado en el HTML")
            
            # Buscar el contexto alrededor de ADICIONALES
            import re
            pattern = r'.{0,100}ADICIONALES.{0,100}'
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                print(f"  Contexto: {match}")
        else:
            print("✗ 'ADICIONALES' no encontrado en el HTML")
        
        # Buscar elementos que podrían ser menús desplegables
        dropdown_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='dropdown'], [class*='menu'], [class*='nav'], [role='menu'], [aria-haspopup='true']")
        print(f"Elementos de menú desplegable: {len(dropdown_elements)}")
        
        for i, elem in enumerate(dropdown_elements):
            print(f"  {i+1}. tag: {elem.tag_name}, class: '{elem.get_attribute('class')}', role: '{elem.get_attribute('role')}'")
            print(f"      text: '{elem.text[:50]}...'")
            
            # Intentar activar este elemento
            try:
                print(f"      Intentando activar elemento {i+1}...")
                elem.click()
                time.sleep(2)
                
                # Buscar ADICIONALES
                adicionales_activo = driver.find_elements(By.XPATH, "//*[contains(text(), 'ADICIONALES')]")
                for adic in adicionales_activo:
                    if adic.is_displayed():
                        print(f"      ✓ ¡ADICIONALES activo! Haciendo clic...")
                        adic.click()
                        time.sleep(3)
                        print(f"      - URL final: {driver.current_url}")
                        return True
                        
            except Exception as e:
                print(f"      ✗ Error activando elemento {i+1}: {str(e)}")
        
        print(f"\n=== RESULTADO FINAL ===")
        print(f"URL final: {driver.current_url}")
        print(f"Título final: {driver.title}")
        
        return False
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para inspección manual...")
            print("Busca manualmente el menú desplegable y el enlace 'ADICIONALES'")
            time.sleep(120)  # Mantener abierto por 2 minutos
            driver.quit()

if __name__ == "__main__":
    activar_menu_adicionales()


