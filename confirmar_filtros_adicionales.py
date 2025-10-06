#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para confirmar los filtros en la página de ADICIONALES
- Salon
- Zona  
- Año
- Botón FILTRAR
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def confirmar_filtros_adicionales():
    """Confirmar que los filtros están visibles y funcionando"""
    
    print("=== CONFIRMACIÓN DE FILTROS EN ADICIONALES ===")
    print("Buscando: Salon, Zona, Año, Botón FILTRAR")
    
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
        
        # PASO 2: Acceder a ADICIONALES
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
                enlace.click()
                time.sleep(5)  # Esperar a que cargue
                break
        
        # Cambiar al frame principal
        try:
            main_frame = driver.find_element(By.ID, "mainFrame")
            driver.switch_to.frame(main_frame)
            print("✓ Cambiado al frame principal")
        except Exception as e:
            print(f"✗ Error cambiando al frame: {str(e)}")
        
        # PASO 3: Buscar y confirmar filtros
        print("\n=== PASO 3: CONFIRMANDO FILTROS ===")
        
        # Buscar filtro SALON
        print("\n--- FILTRO SALON ---")
        try:
            salon_selectors = [
                "select[name='salon']",
                "select[id='salon']",
                "input[name='salon']",
                "input[id='salon']",
                "[name='salon']",
                "[id='salon']"
            ]
            
            salon_encontrado = None
            for selector in salon_selectors:
                try:
                    elemento = driver.find_element(By.CSS_SELECTOR, selector)
                    if elemento.is_displayed():
                        print(f"✓ Filtro SALON encontrado con selector: {selector}")
                        print(f"  - tag: {elemento.tag_name}")
                        print(f"  - type: {elemento.get_attribute('type')}")
                        print(f"  - visible: {elemento.is_displayed()}")
                        print(f"  - opciones: {len(elemento.find_elements(By.TAG_NAME, 'option'))}")
                        salon_encontrado = elemento
                        break
                except NoSuchElementException:
                    continue
            
            if not salon_encontrado:
                print("✗ Filtro SALON no encontrado")
        except Exception as e:
            print(f"✗ Error buscando filtro SALON: {str(e)}")
        
        # Buscar filtro ZONA
        print("\n--- FILTRO ZONA ---")
        try:
            zona_selectors = [
                "select[name='zona']",
                "select[id='zona']",
                "input[name='zona']",
                "input[id='zona']",
                "[name='zona']",
                "[id='zona']"
            ]
            
            zona_encontrado = None
            for selector in zona_selectors:
                try:
                    elemento = driver.find_element(By.CSS_SELECTOR, selector)
                    if elemento.is_displayed():
                        print(f"✓ Filtro ZONA encontrado con selector: {selector}")
                        print(f"  - tag: {elemento.tag_name}")
                        print(f"  - type: {elemento.get_attribute('type')}")
                        print(f"  - visible: {elemento.is_displayed()}")
                        print(f"  - opciones: {len(elemento.find_elements(By.TAG_NAME, 'option'))}")
                        zona_encontrado = elemento
                        break
                except NoSuchElementException:
                    continue
            
            if not zona_encontrado:
                print("✗ Filtro ZONA no encontrado")
        except Exception as e:
            print(f"✗ Error buscando filtro ZONA: {str(e)}")
        
        # Buscar filtro AÑO
        print("\n--- FILTRO AÑO ---")
        try:
            ano_selectors = [
                "select[name='ano']",
                "select[id='ano']",
                "input[name='ano']",
                "input[id='ano']",
                "[name='ano']",
                "[id='ano']"
            ]
            
            ano_encontrado = None
            for selector in ano_selectors:
                try:
                    elemento = driver.find_element(By.CSS_SELECTOR, selector)
                    if elemento.is_displayed():
                        print(f"✓ Filtro AÑO encontrado con selector: {selector}")
                        print(f"  - tag: {elemento.tag_name}")
                        print(f"  - type: {elemento.get_attribute('type')}")
                        print(f"  - visible: {elemento.is_displayed()}")
                        print(f"  - opciones: {len(elemento.find_elements(By.TAG_NAME, 'option'))}")
                        ano_encontrado = elemento
                        break
                except NoSuchElementException:
                    continue
            
            if not ano_encontrado:
                print("✗ Filtro AÑO no encontrado")
        except Exception as e:
            print(f"✗ Error buscando filtro AÑO: {str(e)}")
        
        # Buscar botón FILTRAR
        print("\n--- BOTÓN FILTRAR ---")
        try:
            filtrar_selectors = [
                "input[type='submit']",
                "button[type='submit']",
                "button",
                "input[value*='Filtrar']",
                "input[value*='filtrar']",
                "input[value*='FILTRAR']",
                "button[onclick*='filtro']",
                "[onclick*='filtro']"
            ]
            
            filtrar_encontrado = None
            for selector in filtrar_selectors:
                try:
                    elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                    for elemento in elementos:
                        if elemento.is_displayed():
                            print(f"✓ Botón FILTRAR encontrado con selector: {selector}")
                            print(f"  - tag: {elemento.tag_name}")
                            print(f"  - type: {elemento.get_attribute('type')}")
                            print(f"  - value: '{elemento.get_attribute('value')}'")
                            print(f"  - text: '{elemento.text}'")
                            print(f"  - onclick: '{elemento.get_attribute('onclick')}'")
                            print(f"  - visible: {elemento.is_displayed()}")
                            filtrar_encontrado = elemento
                            break
                    if filtrar_encontrado:
                        break
                except NoSuchElementException:
                    continue
            
            if not filtrar_encontrado:
                print("✗ Botón FILTRAR no encontrado")
        except Exception as e:
            print(f"✗ Error buscando botón FILTRAR: {str(e)}")
        
        # Mostrar todos los elementos de formulario
        print(f"\n=== TODOS LOS ELEMENTOS DE FORMULARIO ===")
        try:
            # Buscar todos los inputs
            inputs = driver.find_elements(By.TAG_NAME, "input")
            print(f"Inputs encontrados: {len(inputs)}")
            for i, inp in enumerate(inputs):
                if inp.is_displayed():
                    print(f"  {i+1}. type: '{inp.get_attribute('type')}', name: '{inp.get_attribute('name')}', id: '{inp.get_attribute('id')}', value: '{inp.get_attribute('value')}'")
            
            # Buscar todos los selects
            selects = driver.find_elements(By.TAG_NAME, "select")
            print(f"Selects encontrados: {len(selects)}")
            for i, sel in enumerate(selects):
                if sel.is_displayed():
                    print(f"  {i+1}. name: '{sel.get_attribute('name')}', id: '{sel.get_attribute('id')}', opciones: {len(sel.find_elements(By.TAG_NAME, 'option'))}")
            
            # Buscar todos los botones
            botones = driver.find_elements(By.TAG_NAME, "button")
            print(f"Botones encontrados: {len(botones)}")
            for i, btn in enumerate(botones):
                if btn.is_displayed():
                    print(f"  {i+1}. type: '{btn.get_attribute('type')}', text: '{btn.text}', onclick: '{btn.get_attribute('onclick')}'")
                    
        except Exception as e:
            print(f"✗ Error mostrando elementos: {str(e)}")
        
        # Resumen de confirmación
        print(f"\n=== RESUMEN DE CONFIRMACIÓN ===")
        print(f"URL actual: {driver.current_url}")
        print(f"Título: {driver.title}")
        
        # Verificar si estamos en la página correcta
        if "adicionales" in driver.current_url.lower() or "adicionales" in driver.title.lower():
            print("✓ Confirmado: Estamos en la página de ADICIONALES")
        else:
            print("⚠ Advertencia: No se confirma que estemos en ADICIONALES")
        
        return True
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación manual...")
            print("Verifica que los filtros estén visibles:")
            print("- Salon (dropdown/select)")
            print("- Zona (dropdown/select)")  
            print("- Año (dropdown/select)")
            print("- Botón FILTRAR")
            time.sleep(120)  # Mantener abierto por 2 minutos
            driver.quit()

if __name__ == "__main__":
    confirmar_filtros_adicionales()


