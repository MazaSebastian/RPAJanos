#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analizar la estructura de la página de ADICIONALES
y identificar los datos de eventos
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def analizar_adicionales():
    """Analizar la estructura de la página de ADICIONALES"""
    
    print("=== ANÁLISIS DE LA PÁGINA DE ADICIONALES ===")
    print("Identificando estructura de datos de eventos...")
    
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
        
        # PASO 2: Abrir menú lateral y acceder a ADICIONALES
        print("\n=== PASO 2: ACCEDIENDO A ADICIONALES ===")
        
        # Abrir menú lateral
        open_nav_element = driver.find_element(By.XPATH, "//*[@onclick='openNav()']")
        open_nav_element.click()
        time.sleep(2)
        
        # Buscar y hacer clic en ADICIONALES
        side_menu = driver.find_element(By.ID, "sideMenu")
        enlaces_menu = side_menu.find_elements(By.TAG_NAME, "a")
        
        for enlace in enlaces_menu:
            if "adicionales" in enlace.text.lower():
                print("✓ Encontrado enlace ADICIONALES")
                print(f"  - text: '{enlace.text}'")
                print(f"  - href: '{enlace.get_attribute('href')}'")
                print(f"  - onclick: '{enlace.get_attribute('onclick')}'")
                
                print("✓ Haciendo clic en ADICIONALES...")
                enlace.click()
                time.sleep(5)  # Esperar a que cargue la página
                break
        
        # PASO 3: Analizar la página de ADICIONALES
        print("\n=== PASO 3: ANÁLISIS DE LA PÁGINA ADICIONALES ===")
        
        # Información básica de la página
        print(f"URL actual: {driver.current_url}")
        print(f"Título: {driver.title}")
        
        # Buscar iframe o frame principal
        print("\n=== BUSCANDO FRAMES/IFRAMES ===")
        try:
            frames = driver.find_elements(By.TAG_NAME, "iframe")
            print(f"IFrames encontrados: {len(frames)}")
            
            for i, frame in enumerate(frames):
                print(f"  {i+1}. src: '{frame.get_attribute('src')}'")
                print(f"     id: '{frame.get_attribute('id')}'")
                print(f"     name: '{frame.get_attribute('name')}'")
                print(f"     visible: {frame.is_displayed()}")
                
                # Si hay un frame principal, cambiar a él
                if "mainFrame" in frame.get_attribute('id') or "main" in frame.get_attribute('id').lower():
                    print(f"     ✓ Cambiando al frame principal...")
                    driver.switch_to.frame(frame)
                    time.sleep(2)
                    break
        except Exception as e:
            print(f"✗ Error con frames: {str(e)}")
        
        # Analizar contenido de la página
        print(f"\n=== CONTENIDO DE LA PÁGINA ===")
        
        # Buscar tablas
        print("\n--- TABLAS ---")
        try:
            tablas = driver.find_elements(By.TAG_NAME, "table")
            print(f"Tablas encontradas: {len(tablas)}")
            
            for i, tabla in enumerate(tablas):
                print(f"  Tabla {i+1}:")
                print(f"    - class: '{tabla.get_attribute('class')}'")
                print(f"    - id: '{tabla.get_attribute('id')}'")
                print(f"    - visible: {tabla.is_displayed()}")
                
                # Analizar filas de la tabla
                filas = tabla.find_elements(By.TAG_NAME, "tr")
                print(f"    - filas: {len(filas)}")
                
                for j, fila in enumerate(filas[:5]):  # Primeras 5 filas
                    celdas = fila.find_elements(By.TAG_NAME, "td")
                    if celdas:
                        print(f"      Fila {j+1}: {len(celdas)} celdas")
                        for k, celda in enumerate(celdas[:3]):  # Primeras 3 celdas
                            print(f"        Celda {k+1}: '{celda.text[:50]}...'")
                            
        except Exception as e:
            print(f"✗ Error analizando tablas: {str(e)}")
        
        # Buscar listas
        print("\n--- LISTAS ---")
        try:
            listas = driver.find_elements(By.TAG_NAME, "ul")
            print(f"Listas encontradas: {len(listas)}")
            
            for i, lista in enumerate(listas):
                print(f"  Lista {i+1}:")
                print(f"    - class: '{lista.get_attribute('class')}'")
                print(f"    - id: '{lista.get_attribute('id')}'")
                print(f"    - visible: {lista.is_displayed()}")
                
                items = lista.find_elements(By.TAG_NAME, "li")
                print(f"    - items: {len(items)}")
                
                for j, item in enumerate(items[:3]):  # Primeros 3 items
                    print(f"      Item {j+1}: '{item.text[:50]}...'")
                    
        except Exception as e:
            print(f"✗ Error analizando listas: {str(e)}")
        
        # Buscar divs con datos
        print("\n--- DIVS CON DATOS ---")
        try:
            divs = driver.find_elements(By.TAG_NAME, "div")
            divs_con_datos = [div for div in divs if div.text.strip() and len(div.text) > 10]
            print(f"Divs con datos: {len(divs_con_datos)}")
            
            for i, div in enumerate(divs_con_datos[:10]):  # Primeros 10
                print(f"  Div {i+1}:")
                print(f"    - class: '{div.get_attribute('class')}'")
                print(f"    - id: '{div.get_attribute('id')}'")
                print(f"    - text: '{div.text[:100]}...'")
                
        except Exception as e:
            print(f"✗ Error analizando divs: {str(e)}")
        
        # Buscar elementos con clases específicas de eventos
        print("\n--- ELEMENTOS DE EVENTOS ---")
        clases_eventos = [
            "evento", "event", "calendar", "calendario", 
            "item", "card", "row", "entry", "registro"
        ]
        
        for clase in clases_eventos:
            try:
                elementos = driver.find_elements(By.CSS_SELECTOR, f"[class*='{clase}']")
                if elementos:
                    print(f"Elementos con clase '{clase}': {len(elementos)}")
                    for i, elem in enumerate(elementos[:3]):  # Primeros 3
                        print(f"  {i+1}. text: '{elem.text[:50]}...', class: '{elem.get_attribute('class')}'")
            except Exception as e:
                print(f"✗ Error con clase '{clase}': {str(e)}")
        
        # Buscar campos específicos que necesitamos
        print(f"\n=== BUSCANDO CAMPOS ESPECÍFICOS ===")
        campos_requeridos = [
            "cliente", "client", "nombre", "name",
            "tipo", "type", "evento", "event",
            "agasajado", "fecha", "date", "horario", "time",
            "salon", "salón", "sala"
        ]
        
        for campo in campos_requeridos:
            try:
                elementos = driver.find_elements(By.XPATH, f"//*[contains(text(), '{campo}') or contains(@class, '{campo}') or contains(@id, '{campo}')]")
                if elementos:
                    print(f"Elementos relacionados con '{campo}': {len(elementos)}")
                    for i, elem in enumerate(elementos[:2]):  # Primeros 2
                        print(f"  {i+1}. tag: {elem.tag_name}, text: '{elem.text[:30]}...'")
            except Exception as e:
                print(f"✗ Error buscando '{campo}': {str(e)}")
        
        # Mostrar HTML completo para análisis manual
        print(f"\n=== HTML COMPLETO (PRIMEROS 3000 CARACTERES) ===")
        html_content = driver.page_source
        print(html_content[:3000])
        
        print(f"\n=== RESULTADO DEL ANÁLISIS ===")
        print(f"URL final: {driver.current_url}")
        print(f"Título final: {driver.title}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para análisis manual...")
            print("Analiza manualmente la estructura de datos en la página")
            time.sleep(180)  # Mantener abierto por 3 minutos
            driver.quit()

if __name__ == "__main__":
    analizar_adicionales()


