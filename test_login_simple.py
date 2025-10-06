#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para probar el login en Tecnica Dj's
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def test_login_simple():
    """Probar el login de forma simple"""
    
    print("=== PROBANDO LOGIN EN TECNICA DJ'S ===")
    print("URL: https://tecnica.janosgroup.com/login.php")
    print("Usuario: sebastian_maza")
    print()
    
    driver = None
    try:
        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Inicializar driver
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Navegar al login
        driver.get("https://tecnica.janosgroup.com/login.php")
        print("✓ Navegando a la página de login...")
        
        # Esperar a que cargue
        time.sleep(3)
        
        # Mostrar información de la página
        print(f"Título de la página: {driver.title}")
        print(f"URL actual: {driver.current_url}")
        
        # Buscar todos los elementos input
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"\nElementos input encontrados: {len(inputs)}")
        
        for i, inp in enumerate(inputs):
            print(f"  {i+1}. type='{inp.get_attribute('type')}', name='{inp.get_attribute('name')}', id='{inp.get_attribute('id')}', class='{inp.get_attribute('class')}'")
        
        # Buscar todos los botones
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"\nBotones encontrados: {len(buttons)}")
        
        for i, btn in enumerate(buttons):
            print(f"  {i+1}. type='{btn.get_attribute('type')}', value='{btn.get_attribute('value')}', text='{btn.text}'")
        
        # Intentar encontrar campos por atributos comunes
        print("\n=== INTENTANDO IDENTIFICAR CAMPOS ===")
        
        # Buscar campo de usuario
        username_field = None
        username_selectors = [
            ("name", "username"),
            ("name", "user"),
            ("name", "login"),
            ("name", "email"),
            ("id", "username"),
            ("id", "user"),
            ("id", "login"),
            ("id", "email")
        ]
        
        for attr, value in username_selectors:
            try:
                if attr == "name":
                    username_field = driver.find_element(By.NAME, value)
                else:
                    username_field = driver.find_element(By.ID, value)
                print(f"✓ Campo usuario encontrado: {attr}='{value}'")
                break
            except NoSuchElementException:
                continue
        
        if not username_field:
            print("✗ No se encontró campo de usuario")
            return False
        
        # Buscar campo de contraseña
        password_field = None
        password_selectors = [
            ("name", "password"),
            ("name", "pass"),
            ("name", "pwd"),
            ("id", "password"),
            ("id", "pass"),
            ("id", "pwd")
        ]
        
        for attr, value in password_selectors:
            try:
                if attr == "name":
                    password_field = driver.find_element(By.NAME, value)
                else:
                    password_field = driver.find_element(By.ID, value)
                print(f"✓ Campo contraseña encontrado: {attr}='{value}'")
                break
            except NoSuchElementException:
                continue
        
        if not password_field:
            print("✗ No se encontró campo de contraseña")
            return False
        
        # Buscar botón de login
        login_button = None
        login_selectors = [
            ("type", "submit"),
            ("value", "login"),
            ("value", "ingresar"),
            ("value", "entrar"),
            ("id", "login"),
            ("id", "submit")
        ]
        
        for attr, value in login_selectors:
            try:
                if attr == "type":
                    login_button = driver.find_element(By.CSS_SELECTOR, f"input[type='{value}']")
                elif attr == "value":
                    login_button = driver.find_element(By.CSS_SELECTOR, f"input[value*='{value}']")
                else:
                    login_button = driver.find_element(By.ID, value)
                print(f"✓ Botón login encontrado: {attr}='{value}'")
                break
            except NoSuchElementException:
                continue
        
        if not login_button:
            print("✗ No se encontró botón de login")
            return False
        
        # Intentar el login
        print("\n=== INTENTANDO LOGIN ===")
        
        username_field.clear()
        username_field.send_keys("sebastian_maza")
        print("✓ Usuario ingresado")
        
        password_field.clear()
        password_field.send_keys("Janos2025+!")
        print("✓ Contraseña ingresada")
        
        login_button.click()
        print("✓ Botón de login presionado")
        
        # Esperar resultado
        time.sleep(5)
        
        # Verificar resultado
        current_url = driver.current_url
        print(f"\nURL después del login: {current_url}")
        
        if "login.php" not in current_url:
            print("✓ LOGIN EXITOSO - Redirigido a otra página")
            return True
        else:
            print("✗ LOGIN FALLÓ - Permanece en página de login")
            return False
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False
    
    finally:
        if driver:
            input("\nPresiona Enter para cerrar el navegador...")
            driver.quit()

if __name__ == "__main__":
    test_login_simple()


