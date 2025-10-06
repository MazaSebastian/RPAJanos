#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para encontrar el botón de login correcto
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def encontrar_boton_login():
    """Encontrar el botón de login correcto"""
    
    print("=== ENCONTRANDO BOTÓN DE LOGIN ===")
    
    driver = None
    try:
        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Navegar al login
        driver.get("https://tecnica.janosgroup.com/login.php")
        print("✓ Navegando a la página de login...")
        
        time.sleep(3)
        
        # Buscar TODOS los elementos clickeables
        print("\n=== BUSCANDO TODOS LOS ELEMENTOS CLICKEABLES ===")
        
        # Todos los botones
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"Botones encontrados: {len(buttons)}")
        for i, btn in enumerate(buttons):
            print(f"  {i+1}. tag='{btn.tag_name}', type='{btn.get_attribute('type')}', text='{btn.text}', class='{btn.get_attribute('class')}', id='{btn.get_attribute('id')}'")
        
        # Todos los inputs
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"\nInputs encontrados: {len(inputs)}")
        for i, inp in enumerate(inputs):
            print(f"  {i+1}. type='{inp.get_attribute('type')}', value='{inp.get_attribute('value')}', text='{inp.text}', class='{inp.get_attribute('class')}', id='{inp.get_attribute('id')}'")
        
        # Todos los elementos con onclick
        onclick_elements = driver.find_elements(By.CSS_SELECTOR, "[onclick]")
        print(f"\nElementos con onclick: {len(onclick_elements)}")
        for i, elem in enumerate(onclick_elements):
            print(f"  {i+1}. tag='{elem.tag_name}', onclick='{elem.get_attribute('onclick')}', text='{elem.text}', class='{elem.get_attribute('class')}'")
        
        # Buscar por texto "Ingresar"
        ingresar_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Ingresar')]")
        print(f"\nElementos con texto 'Ingresar': {len(ingresar_elements)}")
        for i, elem in enumerate(ingresar_elements):
            print(f"  {i+1}. tag='{elem.tag_name}', text='{elem.text}', class='{elem.get_attribute('class')}', id='{elem.get_attribute('id')}'")
        
        # Buscar elementos con clases comunes de botones
        button_classes = driver.find_elements(By.CSS_SELECTOR, "[class*='btn'], [class*='button'], [class*='submit'], [class*='login']")
        print(f"\nElementos con clases de botón: {len(button_classes)}")
        for i, elem in enumerate(button_classes):
            print(f"  {i+1}. tag='{elem.tag_name}', class='{elem.get_attribute('class')}', text='{elem.text}', id='{elem.get_attribute('id')}'")
        
        # Intentar diferentes selectores para el botón
        print(f"\n=== PROBANDO DIFERENTES SELECTORES ===")
        
        selectores_boton = [
            "button",
            "input[type='button']",
            "input[type='submit']",
            "input[value*='Ingresar']",
            "input[value*='ingresar']",
            "input[value*='Login']",
            "input[value*='login']",
            "[onclick]",
            ".btn",
            ".button",
            ".submit",
            ".login",
            "#login",
            "#submit",
            "#btn-login",
            "a[href*='login']",
            "a[href*='submit']"
        ]
        
        boton_encontrado = None
        for selector in selectores_boton:
            try:
                elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                if elementos:
                    print(f"✓ Selector '{selector}' encontró {len(elementos)} elemento(s)")
                    for elem in elementos:
                        if elem.text.strip() or elem.get_attribute('value'):
                            print(f"    - text='{elem.text}', value='{elem.get_attribute('value')}', class='{elem.get_attribute('class')}'")
                            if not boton_encontrado:
                                boton_encontrado = elem
                else:
                    print(f"✗ Selector '{selector}' no encontró elementos")
            except Exception as e:
                print(f"✗ Error con selector '{selector}': {str(e)}")
        
        if boton_encontrado:
            print(f"\n✓ BOTÓN ENCONTRADO:")
            print(f"    tag: {boton_encontrado.tag_name}")
            print(f"    text: '{boton_encontrado.text}'")
            print(f"    value: '{boton_encontrado.get_attribute('value')}'")
            print(f"    class: '{boton_encontrado.get_attribute('class')}'")
            print(f"    id: '{boton_encontrado.get_attribute('id')}'")
            print(f"    type: '{boton_encontrado.get_attribute('type')}'")
            
            # Intentar hacer clic
            print(f"\n=== INTENTANDO LOGIN CON BOTÓN ENCONTRADO ===")
            
            # Llenar campos
            username_field = driver.find_element(By.NAME, "username")
            username_field.clear()
            username_field.send_keys("sebastian_maza")
            print("✓ Usuario ingresado")
            
            password_field = driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys("Janos2025+!")
            print("✓ Contraseña ingresada")
            
            # Hacer clic en el botón encontrado
            print("✓ Haciendo clic en el botón...")
            boton_encontrado.click()
            
            # Esperar resultado
            time.sleep(5)
            
            print(f"URL después del clic: {driver.current_url}")
            if "login.php" not in driver.current_url:
                print("✓ LOGIN EXITOSO!")
                return True
            else:
                print("✗ Login falló")
                return False
        else:
            print("✗ No se encontró ningún botón de login")
            return False
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para inspección...")
            time.sleep(30)
            driver.quit()

if __name__ == "__main__":
    encontrar_boton_login()


