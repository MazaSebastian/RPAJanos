#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para diagnosticar la estructura real del calendario
y identificar cómo están marcadas las fechas resaltadas
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def diagnosticar_calendario():
    """Diagnosticar la estructura real del calendario"""
    
    print("=== DIAGNÓSTICO DEL CALENDARIO ===")
    print("Inspeccionando HTML real para identificar fechas resaltadas...")
    
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
            return False
        
        # PASO 3: Aplicar filtros
        print("\n=== PASO 3: APLICANDO FILTROS ===")
        
        # Filtro SALON: DOT
        try:
            salon_select = Select(driver.find_element(By.ID, "salon"))
            salon_select.select_by_visible_text("DOT")
            print("✓ Filtro SALON aplicado: DOT")
        except Exception as e:
            print(f"✗ Error aplicando filtro SALON: {str(e)}")
        
        # Filtro ZONA: CABA
        try:
            zona_select = Select(driver.find_element(By.ID, "cluster"))
            zona_select.select_by_visible_text("CABA")
            print("✓ Filtro ZONA aplicado: CABA")
        except Exception as e:
            print(f"✗ Error aplicando filtro ZONA: {str(e)}")
        
        # Filtro AÑO: 2025
        try:
            ano_select = Select(driver.find_element(By.ID, "ano"))
            ano_select.select_by_visible_text("2025")
            print("✓ Filtro AÑO aplicado: 2025")
        except Exception as e:
            print(f"✗ Error aplicando filtro AÑO: {str(e)}")
        
        # Aplicar filtros
        try:
            filtrar_buttons = driver.find_elements(By.XPATH, "//input[@value='Filtrar']")
            if filtrar_buttons:
                filtrar_buttons[0].click()
                time.sleep(5)
                print("✓ Filtros aplicados")
        except Exception as e:
            print(f"✗ Error aplicando filtros: {str(e)}")
        
        # PASO 4: Inspeccionar HTML del calendario
        print("\n=== PASO 4: INSPECCIONANDO HTML DEL CALENDARIO ===")
        
        # Buscar todas las tablas
        tablas = driver.find_elements(By.TAG_NAME, "table")
        print(f"Tablas encontradas: {len(tablas)}")
        
        for i, tabla in enumerate(tablas):
            print(f"\n--- Tabla {i+1} ---")
            print(f"  - visible: {tabla.is_displayed()}")
            print(f"  - filas: {len(tabla.find_elements(By.TAG_NAME, 'tr'))}")
            print(f"  - celdas: {len(tabla.find_elements(By.TAG_NAME, 'td'))}")
            
            # Buscar celdas con estilos específicos
            celdas_con_estilo = tabla.find_elements(By.CSS_SELECTOR, "td[style]")
            print(f"  - celdas con estilo: {len(celdas_con_estilo)}")
            
            for j, celda in enumerate(celdas_con_estilo[:5]):  # Primeras 5
                print(f"    Celda {j+1}:")
                print(f"      - text: '{celda.text}'")
                print(f"      - style: '{celda.get_attribute('style')}'")
                print(f"      - class: '{celda.get_attribute('class')}'")
                print(f"      - bgcolor: '{celda.get_attribute('bgcolor')}'")
        
        # Buscar elementos con colores específicos
        print(f"\n=== BUSCANDO ELEMENTOS CON COLORES ===")
        
        # Buscar por diferentes selectores de color
        selectores_color = [
            "td[style*='orange']",
            "td[style*='background-color: orange']",
            "td[style*='background: orange']",
            "td[bgcolor='orange']",
            "td[class*='orange']",
            "td[style*='#ffa500']",
            "td[style*='rgb(255, 165, 0)']",
            "td[style*='background-color: #ffa500']",
            "td[style*='background: #ffa500']"
        ]
        
        for selector in selectores_color:
            try:
                elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                if elementos:
                    print(f"✓ Encontrados {len(elementos)} elementos con selector '{selector}'")
                    for elem in elementos:
                        print(f"  - text: '{elem.text}', style: '{elem.get_attribute('style')}'")
                else:
                    print(f"✗ No se encontraron elementos con selector '{selector}'")
            except Exception as e:
                print(f"✗ Error con selector '{selector}': {str(e)}")
        
        # Buscar todos los elementos td
        print(f"\n=== TODOS LOS ELEMENTOS TD ===")
        try:
            todas_celdas = driver.find_elements(By.TAG_NAME, "td")
            print(f"Total de celdas td: {len(todas_celdas)}")
            
            celdas_con_texto = [celda for celda in todas_celdas if celda.text.strip() and celda.text.strip().isdigit()]
            print(f"Celdas con números: {len(celdas_con_texto)}")
            
            for i, celda in enumerate(celdas_con_texto[:10]):  # Primeras 10
                print(f"  Celda {i+1}:")
                print(f"    - text: '{celda.text}'")
                print(f"    - style: '{celda.get_attribute('style')}'")
                print(f"    - class: '{celda.get_attribute('class')}'")
                print(f"    - bgcolor: '{celda.get_attribute('bgcolor')}'")
                print(f"    - visible: {celda.is_displayed()}")
                
        except Exception as e:
            print(f"✗ Error analizando celdas: {str(e)}")
        
        # Mostrar HTML completo de una tabla específica
        print(f"\n=== HTML DE UNA TABLA ESPECÍFICA ===")
        try:
            if tablas:
                tabla_ejemplo = tablas[1]  # Segunda tabla (probablemente un mes)
                html_tabla = tabla_ejemplo.get_attribute('outerHTML')
                print(f"HTML de la tabla (primeros 2000 caracteres):")
                print(html_tabla[:2000])
        except Exception as e:
            print(f"✗ Error mostrando HTML: {str(e)}")
        
        print(f"\n=== RESULTADO DEL DIAGNÓSTICO ===")
        print(f"URL actual: {driver.current_url}")
        print(f"Título: {driver.title}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para inspección manual...")
            print("Inspecciona manualmente las fechas resaltadas en naranja")
            time.sleep(180)  # Mantener abierto por 3 minutos
            driver.quit()

if __name__ == "__main__":
    diagnosticar_calendario()


