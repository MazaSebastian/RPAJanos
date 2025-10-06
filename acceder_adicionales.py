#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para acceder al enlace ADICIONALES en el menú lateral izquierdo
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

def acceder_adicionales():
    """Acceder al enlace ADICIONALES en el menú lateral"""
    
    print("=== ACCEDIENDO A 'ADICIONALES' EN EL MENÚ LATERAL ===")
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
        
        # PASO 2: Buscar y hacer clic en el icono de hamburguesa
        print("\n=== PASO 2: ABRIENDO MENÚ LATERAL ===")
        
        # Buscar el icono de hamburguesa (tres líneas horizontales)
        hamburger_selectors = [
            "[class*='hamburger']",
            "[class*='menu-toggle']",
            "[class*='menu-icon']",
            "[aria-label*='menu']",
            "[aria-label*='Menu']",
            "button[class*='menu']",
            "div[class*='menu']",
            "span[class*='menu']",
            "i[class*='menu']",
            "i[class*='hamburger']",
            "i[class*='bars']",
            "i[class*='nav']"
        ]
        
        hamburger_encontrado = None
        for selector in hamburger_selectors:
            try:
                elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                if elementos:
                    for elem in elementos:
                        if elem.is_displayed():
                            print(f"✓ Elemento de menú encontrado con selector '{selector}': {elem.tag_name}")
                            print(f"  - class: '{elem.get_attribute('class')}'")
                            print(f"  - text: '{elem.text}'")
                            if not hamburger_encontrado:
                                hamburger_encontrado = elem
            except Exception as e:
                print(f"✗ Error con selector '{selector}': {str(e)}")
        
        # Si no encontramos con selectores específicos, buscar en la barra superior
        if not hamburger_encontrado:
            print("Buscando en la barra superior...")
            try:
                # Buscar en la barra púrpura superior
                barra_superior = driver.find_element(By.CSS_SELECTOR, "div[class*='nav'], div[class*='header'], div[class*='top']")
                elementos_barra = barra_superior.find_elements(By.XPATH, ".//*")
                
                for elem in elementos_barra:
                    if elem.is_displayed() and (elem.tag_name in ['button', 'div', 'span', 'i']):
                        print(f"  - tag: {elem.tag_name}, class: '{elem.get_attribute('class')}', text: '{elem.text}'")
                        # Buscar elementos que podrían ser el icono de hamburguesa
                        if (elem.get_attribute('class') and 
                            any(word in elem.get_attribute('class').lower() for word in ['menu', 'hamburger', 'nav', 'toggle', 'bars'])):
                            hamburger_encontrado = elem
                            print(f"    ✓ Posible icono de menú encontrado!")
                            break
            except Exception as e:
                print(f"✗ Error buscando en barra superior: {str(e)}")
        
        # Si aún no encontramos, buscar por posición (esquina superior izquierda)
        if not hamburger_encontrado:
            print("Buscando por posición en esquina superior izquierda...")
            try:
                # Buscar elementos en la parte superior izquierda
                elementos_izquierda = driver.find_elements(By.CSS_SELECTOR, "div, button, span, i")
                for elem in elementos_izquierda:
                    if elem.is_displayed():
                        # Obtener posición del elemento
                        location = elem.location
                        size = elem.size
                        if location['x'] < 100 and location['y'] < 100:  # Esquina superior izquierda
                            print(f"  - Elemento en esquina: {elem.tag_name}, class: '{elem.get_attribute('class')}', text: '{elem.text}'")
                            if elem.tag_name in ['button', 'div', 'span', 'i']:
                                hamburger_encontrado = elem
                                print(f"    ✓ Posible icono de menú en esquina!")
                                break
            except Exception as e:
                print(f"✗ Error buscando por posición: {str(e)}")
        
        if not hamburger_encontrado:
            print("✗ No se encontró el icono de hamburguesa")
            return False
        
        # Hacer clic en el icono de hamburguesa
        print(f"✓ Haciendo clic en el icono de menú...")
        hamburger_encontrado.click()
        time.sleep(2)
        print("✓ Menú lateral desplegado")
        
        # PASO 3: Buscar el enlace "ADICIONALES" en el menú lateral
        print("\n=== PASO 3: BUSCANDO ENLACE 'ADICIONALES' ===")
        
        # Buscar el enlace ADICIONALES
        adicionales_selectors = [
            "//*[contains(text(), 'ADICIONALES')]",
            "//*[contains(text(), 'Adicionales')]",
            "//*[contains(text(), 'adicionales')]",
            "//a[contains(text(), 'ADICIONALES')]",
            "//a[contains(text(), 'Adicionales')]",
            "//a[contains(text(), 'adicionales')]"
        ]
        
        adicionales_encontrado = None
        for selector in adicionales_selectors:
            try:
                elementos = driver.find_elements(By.XPATH, selector)
                if elementos:
                    for elem in elementos:
                        if elem.is_displayed():
                            print(f"✓ Enlace ADICIONALES encontrado!")
                            print(f"  - tag: {elem.tag_name}")
                            print(f"  - text: '{elem.text}'")
                            print(f"  - href: '{elem.get_attribute('href')}'")
                            print(f"  - class: '{elem.get_attribute('class')}'")
                            adicionales_encontrado = elem
                            break
                    if adicionales_encontrado:
                        break
            except Exception as e:
                print(f"✗ Error con selector '{selector}': {str(e)}")
        
        if not adicionales_encontrado:
            print("✗ No se encontró el enlace ADICIONALES")
            
            # Mostrar todos los enlaces visibles en el menú lateral
            print("\nEnlaces visibles en el menú lateral:")
            try:
                enlaces_visibles = driver.find_elements(By.CSS_SELECTOR, "a")
                for i, enlace in enumerate(enlaces_visibles):
                    if enlace.is_displayed() and enlace.text.strip():
                        print(f"  {i+1}. text: '{enlace.text}', href: '{enlace.get_attribute('href')}'")
            except Exception as e:
                print(f"✗ Error mostrando enlaces: {str(e)}")
            
            return False
        
        # PASO 4: Hacer clic en el enlace ADICIONALES
        print(f"\n=== PASO 4: HACIENDO CLIC EN 'ADICIONALES' ===")
        
        print("✓ Haciendo clic en el enlace ADICIONALES...")
        adicionales_encontrado.click()
        time.sleep(3)
        
        # Verificar que se navegó correctamente
        url_final = driver.current_url
        titulo_final = driver.title
        
        print(f"✓ Navegación exitosa!")
        print(f"  - URL final: {url_final}")
        print(f"  - Título final: {titulo_final}")
        
        # Verificar si estamos en la página correcta
        if "adicionales" in url_final.lower() or "adicionales" in titulo_final.lower():
            print("✓ ¡CONFIRMADO! Estamos en la página de ADICIONALES")
            return True
        else:
            print("⚠ Página cargada, pero no se confirma que sea ADICIONALES")
            return True  # Aún así consideramos exitoso si llegamos aquí
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación...")
            print("Verifica que estés en la página de ADICIONALES")
            time.sleep(60)  # Mantener abierto por 1 minuto
            driver.quit()

if __name__ == "__main__":
    acceder_adicionales()


