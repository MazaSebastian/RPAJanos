#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analizar completamente el menú lateral y encontrar ADICIONALES
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

def analizar_menu_lateral():
    """Analizar completamente el menú lateral"""
    
    print("=== ANÁLISIS COMPLETO DEL MENÚ LATERAL ===")
    
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
        
        # PASO 2: Abrir menú lateral
        print("\n=== PASO 2: ABRIENDO MENÚ LATERAL ===")
        
        # Hacer clic en el div de navegación
        nav_div = driver.find_element(By.CSS_SELECTOR, "div.navBarDiv")
        print("✓ Haciendo clic en el div de navegación...")
        nav_div.click()
        time.sleep(3)  # Esperar más tiempo para que se despliegue
        
        # PASO 3: Análisis completo del menú lateral
        print("\n=== PASO 3: ANÁLISIS COMPLETO DEL MENÚ ===")
        
        # Buscar todos los elementos del menú lateral
        print("Buscando todos los elementos del menú lateral...")
        
        # Buscar por diferentes selectores de menú lateral
        menu_selectors = [
            "div[class*='menu']",
            "div[class*='nav']",
            "div[class*='sidebar']",
            "div[class*='lateral']",
            "nav",
            ".menu",
            ".sidebar",
            ".nav-lateral"
        ]
        
        menu_lateral = None
        for selector in menu_selectors:
            try:
                elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                if elementos:
                    for elem in elementos:
                        if elem.is_displayed():
                            print(f"✓ Menú lateral encontrado con selector '{selector}'")
                            print(f"  - tag: {elem.tag_name}")
                            print(f"  - class: '{elem.get_attribute('class')}'")
                            print(f"  - text: '{elem.text[:100]}...'")
                            if not menu_lateral:
                                menu_lateral = elem
            except Exception as e:
                print(f"✗ Error con selector '{selector}': {str(e)}")
        
        # Si no encontramos un contenedor específico, buscar todos los elementos visibles
        if not menu_lateral:
            print("Buscando todos los elementos visibles en la página...")
            todos_elementos = driver.find_elements(By.XPATH, "//*")
            elementos_visibles = [elem for elem in todos_elementos if elem.is_displayed()]
            print(f"Elementos visibles encontrados: {len(elementos_visibles)}")
            
            # Buscar elementos que contengan texto del menú
            for elem in elementos_visibles:
                if elem.text and len(elem.text) > 10:  # Elementos con texto significativo
                    print(f"  - tag: {elem.tag_name}, text: '{elem.text[:50]}...', class: '{elem.get_attribute('class')}'")
        
        # Buscar específicamente el texto "ADICIONALES" con diferentes variaciones
        print(f"\n=== BUSCANDO 'ADICIONALES' CON DIFERENTES VARIACIONES ===")
        
        variaciones_adicionales = [
            "ADICIONALES",
            "Adicionales", 
            "adicionales",
            "ADICIONAL",
            "Adicional",
            "adicional",
            ">> Adicionales",
            ">> ADICIONALES",
            ">> adicionales"
        ]
        
        for variacion in variaciones_adicionales:
            try:
                elementos = driver.find_elements(By.XPATH, f"//*[contains(text(), '{variacion}')]")
                if elementos:
                    print(f"✓ Encontrados {len(elementos)} elemento(s) con texto '{variacion}':")
                    for i, elem in enumerate(elementos):
                        print(f"  {i+1}. tag: {elem.tag_name}")
                        print(f"     text: '{elem.text}'")
                        print(f"     visible: {elem.is_displayed()}")
                        print(f"     class: '{elem.get_attribute('class')}'")
                        print(f"     href: '{elem.get_attribute('href')}'")
                        
                        if elem.is_displayed():
                            print(f"     ✓ ¡VISIBLE! Haciendo clic...")
                            elem.click()
                            time.sleep(3)
                            print(f"     - URL después del clic: {driver.current_url}")
                            return True
            except Exception as e:
                print(f"✗ Error buscando '{variacion}': {str(e)}")
        
        # Buscar todos los enlaces visibles
        print(f"\n=== TODOS LOS ENLACES VISIBLES ===")
        try:
            enlaces = driver.find_elements(By.TAG_NAME, "a")
            enlaces_visibles = [enlace for enlace in enlaces if enlace.is_displayed()]
            print(f"Enlaces visibles: {len(enlaces_visibles)}")
            
            for i, enlace in enumerate(enlaces_visibles):
                if enlace.text.strip():
                    print(f"  {i+1}. text: '{enlace.text}'")
                    print(f"     href: '{enlace.get_attribute('href')}'")
                    print(f"     class: '{enlace.get_attribute('class')}'")
        except Exception as e:
            print(f"✗ Error mostrando enlaces: {str(e)}")
        
        # Buscar elementos que contengan ">>" (indicador de submenú)
        print(f"\n=== ELEMENTOS CON '>>' (SUBMENÚS) ===")
        try:
            submenus = driver.find_elements(By.XPATH, "//*[contains(text(), '>>')]")
            print(f"Elementos con '>>': {len(submenus)}")
            
            for i, elem in enumerate(submenus):
                if elem.is_displayed():
                    print(f"  {i+1}. text: '{elem.text}'")
                    print(f"     tag: {elem.tag_name}")
                    print(f"     class: '{elem.get_attribute('class')}'")
                    print(f"     href: '{elem.get_attribute('href')}'")
        except Exception as e:
            print(f"✗ Error buscando submenús: {str(e)}")
        
        # Mostrar el HTML de la página para análisis manual
        print(f"\n=== HTML DE LA PÁGINA (PRIMEROS 2000 CARACTERES) ===")
        html_content = driver.page_source
        print(html_content[:2000])
        
        print(f"\n=== RESULTADO FINAL ===")
        print(f"URL actual: {driver.current_url}")
        print(f"Título: {driver.title}")
        
        return False
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para análisis manual...")
            print("Busca manualmente el enlace 'ADICIONALES' en el menú lateral")
            time.sleep(120)  # Mantener abierto por 2 minutos
            driver.quit()

if __name__ == "__main__":
    analizar_menu_lateral()


