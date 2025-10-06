#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar el login del sistema origen (Tecnica Dj's)
Identifica los selectores HTML correctos del formulario de login
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

def test_login_tecnica():
    """Probar el login en Tecnica Dj's e identificar selectores"""
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Configurar navegador (modo visible para inspección)
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    try:
        # Inicializar driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 10)
        
        print("=== PROBANDO LOGIN EN TECNICA DJ'S ===")
        print("URL: https://tecnica.janosgroup.com/login.php")
        print("Usuario: sebastian_maza")
        print("Contraseña: [OCULTA]")
        print()
        
        # Navegar al login
        driver.get("https://tecnica.janosgroup.com/login.php")
        print("✓ Navegando a la página de login...")
        
        # Esperar a que cargue la página
        time.sleep(3)
        
        # Intentar diferentes selectores comunes para el campo de usuario
        print("\n=== IDENTIFICANDO SELECTORES ===")
        
        # Buscar campo de usuario
        username_selectors = [
            "input[name='username']",
            "input[name='user']", 
            "input[name='login']",
            "input[name='email']",
            "input[type='text']",
            "input[type='email']",
            "#username",
            "#user",
            "#login",
            "#email",
            ".username",
            ".user",
            ".login"
        ]
        
        username_field = None
        for selector in username_selectors:
            try:
                if selector.startswith("input[") or selector.startswith("#") or selector.startswith("."):
                    username_field = driver.find_element(By.CSS_SELECTOR, selector)
                else:
                    username_field = driver.find_element(By.NAME, selector.split("'")[1])
                print(f"✓ Campo usuario encontrado con selector: {selector}")
                break
            except NoSuchElementException:
                continue
        
        if not username_field:
            print("✗ No se encontró el campo de usuario")
            print("Elementos input disponibles:")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            for i, inp in enumerate(inputs):
                print(f"  {i+1}. type='{inp.get_attribute('type')}', name='{inp.get_attribute('name')}', id='{inp.get_attribute('id')}', class='{inp.get_attribute('class')}'")
            return False
        
        # Buscar campo de contraseña
        password_selectors = [
            "input[name='password']",
            "input[name='pass']",
            "input[name='pwd']",
            "input[type='password']",
            "#password",
            "#pass",
            "#pwd",
            ".password",
            ".pass",
            ".pwd"
        ]
        
        password_field = None
        for selector in password_selectors:
            try:
                if selector.startswith("input[") or selector.startswith("#") or selector.startswith("."):
                    password_field = driver.find_element(By.CSS_SELECTOR, selector)
                else:
                    password_field = driver.find_element(By.NAME, selector.split("'")[1])
                print(f"✓ Campo contraseña encontrado con selector: {selector}")
                break
            except NoSuchElementException:
                continue
        
        if not password_field:
            print("✗ No se encontró el campo de contraseña")
            return False
        
        # Buscar botón de login
        login_selectors = [
            "input[type='submit']",
            "button[type='submit']",
            "button",
            "input[value*='login']",
            "input[value*='ingresar']",
            "input[value*='entrar']",
            "#login",
            "#submit",
            "#btn-login",
            ".login",
            ".submit",
            ".btn-login"
        ]
        
        login_button = None
        for selector in login_selectors:
            try:
                if selector.startswith("input[") or selector.startswith("button["):
                    login_button = driver.find_element(By.CSS_SELECTOR, selector)
                elif selector.startswith("#") or selector.startswith("."):
                    login_button = driver.find_element(By.CSS_SELECTOR, selector)
                else:
                    login_button = driver.find_element(By.ID, selector[1:])
                print(f"✓ Botón login encontrado con selector: {selector}")
                break
            except NoSuchElementException:
                continue
        
        if not login_button:
            print("✗ No se encontró el botón de login")
            print("Botones disponibles:")
            buttons = driver.find_elements(By.TAG_NAME, "button")
            inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='submit']")
            for i, btn in enumerate(buttons + inputs):
                print(f"  {i+1}. tag='{btn.tag_name}', type='{btn.get_attribute('type')}', value='{btn.get_attribute('value')}', text='{btn.text}'")
            return False
        
        # Intentar el login
        print("\n=== INTENTANDO LOGIN ===")
        
        # Limpiar y llenar campos
        username_field.clear()
        username_field.send_keys("sebastian_maza")
        print("✓ Usuario ingresado")
        
        password_field.clear()
        password_field.send_keys("Janos2025+!")
        print("✓ Contraseña ingresada")
        
        # Hacer clic en login
        login_button.click()
        print("✓ Botón de login presionado")
        
        # Esperar resultado del login
        time.sleep(5)
        
        # Verificar si el login fue exitoso
        current_url = driver.current_url
        print(f"\nURL después del login: {current_url}")
        
        if "login.php" not in current_url:
            print("✓ Login exitoso - redirigido a otra página")
            
            # Buscar elementos que indiquen login exitoso
            success_indicators = [
                "dashboard", "menu", "welcome", "logout", "salir", "perfil", "profile"
            ]
            
            for indicator in success_indicators:
                try:
                    element = driver.find_element(By.CSS_SELECTOR, f"*[class*='{indicator}'], *[id*='{indicator}']")
                    print(f"✓ Indicador de login exitoso encontrado: {indicator}")
                    break
                except NoSuchElementException:
                    continue
            
            return True
        else:
            print("✗ Login falló - permanece en página de login")
            
            # Buscar mensajes de error
            error_selectors = [
                ".error", ".alert", ".message", ".warning", ".danger"
            ]
            
            for selector in error_selectors:
                try:
                    error_msg = driver.find_element(By.CSS_SELECTOR, selector)
                    if error_msg.text.strip():
                        print(f"✗ Mensaje de error: {error_msg.text}")
                        break
                except NoSuchElementException:
                    continue
            
            return False
        
    except Exception as e:
        print(f"✗ Error durante la prueba: {str(e)}")
        return False
    
    finally:
        if driver:
            input("\nPresiona Enter para cerrar el navegador...")
            driver.quit()

if __name__ == "__main__":
    test_login_tecnica()


