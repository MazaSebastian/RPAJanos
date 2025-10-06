#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script final para encontrar y acceder a ADICIONALES
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

def encontrar_adicionales_final():
    """Encontrar y acceder a ADICIONALES de forma definitiva"""
    
    print("=== BÚSQUEDA FINAL DE 'ADICIONALES' ===")
    
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
        wait = WebDriverWait(driver, 20)
        
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
        
        # PASO 2: Abrir menú lateral correctamente
        print("\n=== PASO 2: ABRIENDO MENÚ LATERAL ===")
        
        # Buscar el elemento con onclick="openNav()"
        try:
            open_nav_element = driver.find_element(By.XPATH, "//*[@onclick='openNav()']")
            print("✓ Encontrado elemento con onclick='openNav()'")
            print(f"  - tag: {open_nav_element.tag_name}")
            print(f"  - text: '{open_nav_element.text}'")
            print(f"  - class: '{open_nav_element.get_attribute('class')}'")
            
            # Hacer clic para abrir el menú
            print("✓ Haciendo clic para abrir menú lateral...")
            open_nav_element.click()
            time.sleep(3)  # Esperar a que se cargue el menú
            
        except NoSuchElementException:
            print("✗ No se encontró elemento con onclick='openNav()'")
            # Intentar con el div de navegación como fallback
            nav_div = driver.find_element(By.CSS_SELECTOR, "div.navBarDiv")
            print("✓ Usando div de navegación como fallback...")
            nav_div.click()
            time.sleep(3)
        
        # PASO 3: Buscar el menú lateral (sideMenu)
        print("\n=== PASO 3: BUSCANDO MENÚ LATERAL ===")
        
        try:
            # Esperar a que aparezca el menú lateral
            side_menu = wait.until(EC.presence_of_element_located((By.ID, "sideMenu")))
            print("✓ Menú lateral (sideMenu) encontrado")
            print(f"  - visible: {side_menu.is_displayed()}")
            print(f"  - text: '{side_menu.text[:100]}...'")
            
            # Buscar todos los enlaces dentro del menú lateral
            enlaces_menu = side_menu.find_elements(By.TAG_NAME, "a")
            print(f"✓ Enlaces en el menú lateral: {len(enlaces_menu)}")
            
            for i, enlace in enumerate(enlaces_menu):
                print(f"  {i+1}. text: '{enlace.text}'")
                print(f"     href: '{enlace.get_attribute('href')}'")
                print(f"     visible: {enlace.is_displayed()}")
                print(f"     onclick: '{enlace.get_attribute('onclick')}'")
                
                # Buscar específicamente "ADICIONALES"
                if "adicionales" in enlace.text.lower() or "adicional" in enlace.text.lower():
                    print(f"     ✓ ¡ENLACE ADICIONALES ENCONTRADO!")
                    if enlace.is_displayed():
                        print(f"     ✓ ¡VISIBLE! Haciendo clic...")
                        enlace.click()
                        time.sleep(3)
                        print(f"     - URL después del clic: {driver.current_url}")
                        return True
                    else:
                        print(f"     ✗ No visible")
            
        except TimeoutException:
            print("✗ Timeout esperando el menú lateral")
        except Exception as e:
            print(f"✗ Error buscando menú lateral: {str(e)}")
        
        # PASO 4: Buscar ADICIONALES en toda la página
        print(f"\n=== PASO 4: BÚSQUEDA GLOBAL DE 'ADICIONALES' ===")
        
        # Buscar con diferentes variaciones
        variaciones = ["ADICIONALES", "Adicionales", "adicionales", "ADICIONAL", "Adicional", "adicional"]
        
        for variacion in variaciones:
            try:
                elementos = driver.find_elements(By.XPATH, f"//*[contains(text(), '{variacion}')]")
                print(f"Buscando '{variacion}': {len(elementos)} elementos encontrados")
                
                for i, elem in enumerate(elementos):
                    print(f"  {i+1}. tag: {elem.tag_name}")
                    print(f"     text: '{elem.text}'")
                    print(f"     visible: {elem.is_displayed()}")
                    print(f"     href: '{elem.get_attribute('href')}'")
                    print(f"     onclick: '{elem.get_attribute('onclick')}'")
                    
                    if elem.is_displayed() and elem.tag_name == 'a':
                        print(f"     ✓ ¡ENLACE ADICIONALES VISIBLE! Haciendo clic...")
                        elem.click()
                        time.sleep(3)
                        print(f"     - URL después del clic: {driver.current_url}")
                        return True
                        
            except Exception as e:
                print(f"✗ Error buscando '{variacion}': {str(e)}")
        
        # PASO 5: Mostrar todo el contenido del menú lateral
        print(f"\n=== PASO 5: CONTENIDO COMPLETO DEL MENÚ LATERAL ===")
        try:
            side_menu = driver.find_element(By.ID, "sideMenu")
            print(f"Contenido completo del menú lateral:")
            print(f"'{side_menu.text}'")
            
            # Buscar todos los elementos dentro del menú
            todos_elementos = side_menu.find_elements(By.XPATH, ".//*")
            print(f"\nTodos los elementos del menú ({len(todos_elementos)}):")
            for i, elem in enumerate(todos_elementos):
                if elem.text.strip():
                    print(f"  {i+1}. tag: {elem.tag_name}, text: '{elem.text}', visible: {elem.is_displayed()}")
                    
        except Exception as e:
            print(f"✗ Error mostrando contenido del menú: {str(e)}")
        
        print(f"\n=== RESULTADO FINAL ===")
        print(f"URL actual: {driver.current_url}")
        print(f"Título: {driver.title}")
        
        return False
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación final...")
            print("Busca manualmente el enlace 'ADICIONALES' en el menú lateral")
            time.sleep(180)  # Mantener abierto por 3 minutos
            driver.quit()

if __name__ == "__main__":
    encontrar_adicionales_final()


