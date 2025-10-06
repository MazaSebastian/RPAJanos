#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para buscar el enlace "ADICIONALES" en el menú desplegable
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

def buscar_adicionales():
    """Buscar el enlace ADICIONALES en el menú desplegable"""
    
    print("=== BUSCANDO ENLACE 'ADICIONALES' ===")
    print("Nota: Cada ejecución inicia sesión desde cero para evitar cierre automático")
    
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
        
        # PASO 2: Buscar menú desplegable en parte superior izquierda
        print("\n=== PASO 2: BUSCANDO MENÚ DESPLEGABLE ===")
        
        # Buscar elementos en la parte superior izquierda
        print("Buscando elementos en la parte superior izquierda...")
        
        # Buscar diferentes tipos de menús desplegables
        menu_selectors = [
            "nav",
            ".menu",
            ".navbar", 
            ".nav",
            ".dropdown",
            ".menu-toggle",
            ".hamburger",
            "[class*='menu']",
            "[class*='nav']",
            "[class*='dropdown']",
            "select",
            "ul",
            "div[role='menu']",
            "div[role='navigation']"
        ]
        
        menu_encontrado = None
        for selector in menu_selectors:
            try:
                elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                if elementos:
                    print(f"✓ Encontrados {len(elementos)} elemento(s) con selector '{selector}'")
                    for elem in elementos:
                        if elem.is_displayed():
                            print(f"    - tag: {elem.tag_name}, text: '{elem.text[:50]}...', class: '{elem.get_attribute('class')}'")
                            if not menu_encontrado:
                                menu_encontrado = elem
            except Exception as e:
                print(f"✗ Error con selector '{selector}': {str(e)}")
        
        # Buscar específicamente el texto "ADICIONALES"
        print(f"\n=== PASO 3: BUSCANDO TEXTO 'ADICIONALES' ===")
        
        # Buscar por XPath que contenga "ADICIONALES"
        try:
            adicionales_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'ADICIONALES') or contains(text(), 'Adicionales') or contains(text(), 'adicionales')]")
            print(f"Elementos con texto 'ADICIONALES' encontrados: {len(adicionales_elements)}")
            
            for i, elem in enumerate(adicionales_elements):
                print(f"  {i+1}. tag: {elem.tag_name}, text: '{elem.text}', class: '{elem.get_attribute('class')}', id: '{elem.get_attribute('id')}'")
                print(f"      visible: {elem.is_displayed()}, enabled: {elem.is_enabled()}")
                
                # Si es un enlace, mostrar el href
                if elem.tag_name == 'a':
                    print(f"      href: '{elem.get_attribute('href')}'")
        except Exception as e:
            print(f"✗ Error buscando 'ADICIONALES': {str(e)}")
        
        # Buscar enlaces en general
        print(f"\n=== PASO 4: BUSCANDO TODOS LOS ENLACES ===")
        try:
            enlaces = driver.find_elements(By.TAG_NAME, "a")
            print(f"Enlaces encontrados: {len(enlaces)}")
            
            for i, enlace in enumerate(enlaces[:20]):  # Mostrar solo los primeros 20
                if enlace.is_displayed() and enlace.text.strip():
                    print(f"  {i+1}. text: '{enlace.text}', href: '{enlace.get_attribute('href')}', class: '{enlace.get_attribute('class')}'")
        except Exception as e:
            print(f"✗ Error buscando enlaces: {str(e)}")
        
        # Buscar elementos clickeables que puedan ser menús
        print(f"\n=== PASO 5: BUSCANDO ELEMENTOS CLICKEABLES ===")
        try:
            clickeables = driver.find_elements(By.CSS_SELECTOR, "button, a, [onclick], [role='button'], [role='menuitem']")
            print(f"Elementos clickeables encontrados: {len(clickeables)}")
            
            for i, elem in enumerate(clickeables[:15]):  # Mostrar solo los primeros 15
                if elem.is_displayed() and elem.text.strip():
                    print(f"  {i+1}. tag: {elem.tag_name}, text: '{elem.text}', class: '{elem.get_attribute('class')}'")
        except Exception as e:
            print(f"✗ Error buscando clickeables: {str(e)}")
        
        # Mostrar información de la página actual
        print(f"\n=== INFORMACIÓN DE LA PÁGINA ===")
        print(f"URL actual: {driver.current_url}")
        print(f"Título: {driver.title}")
        
        # Buscar si hay algún menú hamburguesa o botón de menú
        print(f"\n=== BUSCANDO BOTONES DE MENÚ ===")
        menu_buttons = driver.find_elements(By.CSS_SELECTOR, "[class*='hamburger'], [class*='menu'], [class*='toggle'], [aria-label*='menu'], [aria-label*='Menu']")
        print(f"Botones de menú encontrados: {len(menu_buttons)}")
        for i, btn in enumerate(menu_buttons):
            print(f"  {i+1}. tag: {btn.tag_name}, class: '{btn.get_attribute('class')}', aria-label: '{btn.get_attribute('aria-label')}'")
        
        # Intentar hacer clic en elementos que podrían abrir el menú
        print(f"\n=== INTENTANDO ABRIR MENÚS ===")
        for i, btn in enumerate(menu_buttons[:3]):  # Intentar con los primeros 3
            try:
                print(f"Intentando hacer clic en botón {i+1}...")
                btn.click()
                time.sleep(2)
                
                # Buscar "ADICIONALES" después del clic
                adicionales_despues = driver.find_elements(By.XPATH, "//*[contains(text(), 'ADICIONALES')]")
                if adicionales_despues:
                    print(f"✓ ¡ADICIONALES encontrado después del clic!")
                    for elem in adicionales_despues:
                        print(f"    - text: '{elem.text}', class: '{elem.get_attribute('class')}'")
                        if elem.is_displayed():
                            print(f"    - ¡VISIBLE! Intentando hacer clic...")
                            elem.click()
                            time.sleep(3)
                            print(f"    - URL después del clic: {driver.current_url}")
                            break
                else:
                    print(f"✗ No se encontró ADICIONALES después del clic")
            except Exception as e:
                print(f"✗ Error haciendo clic en botón {i+1}: {str(e)}")
        
        print(f"\n=== RESULTADO FINAL ===")
        print(f"URL final: {driver.current_url}")
        print(f"Título final: {driver.title}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para inspección manual...")
            print("Busca manualmente el enlace 'ADICIONALES' en el menú desplegable")
            time.sleep(60)  # Mantener abierto por 1 minuto
            driver.quit()

if __name__ == "__main__":
    buscar_adicionales()


