#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico detallado del login en Tecnica Dj's
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def diagnostico_login():
    """Diagnóstico completo del login"""
    
    print("=== DIAGNÓSTICO DEL LOGIN TECNICA DJ'S ===")
    
    driver = None
    try:
        # Configurar Chrome con más opciones
        chrome_options = Options()
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Inicializar driver
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Ejecutar script para ocultar automatización
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Navegar al login
        driver.get("https://tecnica.janosgroup.com/login.php")
        print("✓ Navegando a la página de login...")
        
        # Esperar a que cargue completamente
        time.sleep(5)
        
        # Información de la página
        print(f"\n=== INFORMACIÓN DE LA PÁGINA ===")
        print(f"Título: {driver.title}")
        print(f"URL: {driver.current_url}")
        print(f"HTML completo (primeros 1000 chars):")
        print(driver.page_source[:1000])
        
        # Buscar formulario
        forms = driver.find_elements(By.TAG_NAME, "form")
        print(f"\nFormularios encontrados: {len(forms)}")
        
        for i, form in enumerate(forms):
            print(f"  Formulario {i+1}:")
            print(f"    action: {form.get_attribute('action')}")
            print(f"    method: {form.get_attribute('method')}")
            print(f"    id: {form.get_attribute('id')}")
            print(f"    class: {form.get_attribute('class')}")
        
        # Buscar campos específicos
        print(f"\n=== CAMPOS DEL FORMULARIO ===")
        
        # Campo usuario
        try:
            username_field = driver.find_element(By.NAME, "username")
            print(f"✓ Campo usuario (name='username'):")
            print(f"    type: {username_field.get_attribute('type')}")
            print(f"    id: {username_field.get_attribute('id')}")
            print(f"    class: {username_field.get_attribute('class')}")
            print(f"    required: {username_field.get_attribute('required')}")
            print(f"    placeholder: {username_field.get_attribute('placeholder')}")
        except NoSuchElementException:
            print("✗ Campo usuario no encontrado")
        
        # Campo contraseña
        try:
            password_field = driver.find_element(By.NAME, "password")
            print(f"✓ Campo contraseña (name='password'):")
            print(f"    type: {password_field.get_attribute('type')}")
            print(f"    id: {password_field.get_attribute('id')}")
            print(f"    class: {password_field.get_attribute('class')}")
            print(f"    required: {password_field.get_attribute('required')}")
            print(f"    placeholder: {password_field.get_attribute('placeholder')}")
        except NoSuchElementException:
            print("✗ Campo contraseña no encontrado")
        
        # Botón de login
        try:
            login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            print(f"✓ Botón login:")
            print(f"    type: {login_button.get_attribute('type')}")
            print(f"    value: {login_button.get_attribute('value')}")
            print(f"    id: {login_button.get_attribute('id')}")
            print(f"    class: {login_button.get_attribute('class')}")
        except NoSuchElementException:
            print("✗ Botón login no encontrado")
        
        # Buscar campos ocultos o adicionales
        hidden_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='hidden']")
        print(f"\nCampos ocultos encontrados: {len(hidden_inputs)}")
        for i, hidden in enumerate(hidden_inputs):
            print(f"  {i+1}. name='{hidden.get_attribute('name')}', value='{hidden.get_attribute('value')}'")
        
        # Buscar JavaScript en la página
        scripts = driver.find_elements(By.TAG_NAME, "script")
        print(f"\nScripts JavaScript encontrados: {len(scripts)}")
        
        # Intentar el login paso a paso
        print(f"\n=== INTENTANDO LOGIN PASO A PASO ===")
        
        # Limpiar y llenar usuario
        username_field = driver.find_element(By.NAME, "username")
        username_field.clear()
        username_field.send_keys("sebastian_maza")
        print("✓ Usuario ingresado")
        
        # Limpiar y llenar contraseña
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys("Janos2025+!")
        print("✓ Contraseña ingresada")
        
        # Esperar un momento antes de enviar
        time.sleep(2)
        
        # Hacer clic en el botón
        login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        print("✓ Presionando botón de login...")
        login_button.click()
        
        # Esperar respuesta
        time.sleep(5)
        
        # Verificar resultado
        print(f"\n=== RESULTADO DEL LOGIN ===")
        print(f"URL después del login: {driver.current_url}")
        print(f"Título después del login: {driver.title}")
        
        # Buscar mensajes de error
        error_elements = driver.find_elements(By.CSS_SELECTOR, ".error, .alert, .message, .warning, .danger, [class*='error'], [class*='alert']")
        if error_elements:
            print("Mensajes de error encontrados:")
            for error in error_elements:
                if error.text.strip():
                    print(f"  - {error.text}")
        
        # Verificar si hay redirección
        if "login.php" not in driver.current_url:
            print("✓ LOGIN EXITOSO - Redirigido")
            return True
        else:
            print("✗ LOGIN FALLÓ - Permanece en login")
            
            # Mostrar el HTML de la página después del fallo
            print("\nHTML después del fallo (primeros 500 chars):")
            print(driver.page_source[:500])
            
            return False
        
    except Exception as e:
        print(f"✗ Error durante el diagnóstico: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo el navegador abierto para inspección manual...")
            print("Cierra el navegador manualmente cuando termines.")
            time.sleep(30)  # Mantener abierto por 30 segundos
            driver.quit()

if __name__ == "__main__":
    diagnostico_login()


