#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para confirmar que las fechas resaltadas en coral son clickeables
y que despliegan información con código de evento de 5 cifras
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def confirmar_fechas_clickeables():
    """Confirmar que las fechas coral son clickeables y muestran información"""
    
    print("=== CONFIRMACIÓN DE FECHAS CLICKEABLES ===")
    print("Verificando que las fechas coral son clickeables...")
    print("Buscando códigos de evento de 5 cifras...")
    
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
        
        # PASO 4: Buscar fechas resaltadas en coral
        print("\n=== PASO 4: BUSCANDO FECHAS CORAL CLICKEABLES ===")
        
        # Buscar fechas con color coral
        fechas_coral = driver.find_elements(By.CSS_SELECTOR, "div.boton[style*='background: coral']")
        print(f"Fechas con color coral encontradas: {len(fechas_coral)}")
        
        if not fechas_coral:
            print("⚠ No se encontraron fechas coral, buscando con otros selectores...")
            # Buscar con otros selectores de color
            selectores_alternativos = [
                "div.boton[style*='coral']",
                "div.boton[style*='orange']",
                "div.boton[style*='#ff7f50']",
                "div.boton[style*='background-color: coral']",
                "div.boton[style*='background-color: orange']"
            ]
            
            for selector in selectores_alternativos:
                fechas_alt = driver.find_elements(By.CSS_SELECTOR, selector)
                if fechas_alt:
                    print(f"✓ Fechas encontradas con selector '{selector}': {len(fechas_alt)}")
                    fechas_coral = fechas_alt
                    break
        
        if not fechas_coral:
            print("✗ No se encontraron fechas coral clickeables")
            return False
        
        # PASO 5: Probar clic en fechas coral
        print(f"\n=== PASO 5: PROBANDO CLIC EN FECHAS CORAL ===")
        
        fechas_procesadas = 0
        codigos_encontrados = []
        
        for i, fecha_coral in enumerate(fechas_coral[:5]):  # Probar con las primeras 5 fechas
            try:
                fecha_texto = fecha_coral.text.strip()
                print(f"\n--- Probando fecha {i+1}: {fecha_texto} ---")
                
                # Verificar que es clickeable
                if fecha_coral.is_displayed() and fecha_coral.is_enabled():
                    print(f"✓ Fecha {fecha_texto} es clickeable")
                    
                    # Hacer clic en la fecha
                    print(f"✓ Haciendo clic en fecha {fecha_texto}...")
                    fecha_coral.click()
                    time.sleep(3)  # Esperar a que se despliegue la información
                    
                    # Buscar información desplegada
                    print(f"✓ Buscando información desplegada...")
                    
                    # Buscar códigos de 5 cifras
                    codigos_5_cifras = driver.find_elements(By.XPATH, "//*[contains(text(), '') and string-length(normalize-space(text())) = 5 and translate(text(), '0123456789', '0000000000') = '00000']")
                    
                    # Buscar también en elementos con texto que contenga números
                    elementos_con_numeros = driver.find_elements(By.XPATH, "//*[contains(text(), '') and translate(text(), '0123456789', '0000000000') != text()]")
                    
                    print(f"  - Elementos con números encontrados: {len(elementos_con_numeros)}")
                    
                    # Buscar específicamente códigos de 5 dígitos
                    codigos_encontrados_mes = []
                    for elem in elementos_con_numeros:
                        texto = elem.text.strip()
                        if len(texto) == 5 and texto.isdigit():
                            codigos_encontrados_mes.append(texto)
                            print(f"    ✓ Código de 5 cifras encontrado: {texto}")
                    
                    if codigos_encontrados_mes:
                        codigos_encontrados.extend(codigos_encontrados_mes)
                        fechas_procesadas += 1
                        print(f"✓ Fecha {fecha_texto} procesada exitosamente")
                    else:
                        print(f"⚠ Fecha {fecha_texto}: No se encontró código de 5 cifras")
                        
                        # Mostrar todo el texto visible para diagnóstico
                        print(f"  Texto visible en la página:")
                        elementos_visibles = driver.find_elements(By.XPATH, "//*[text()]")
                        for elem in elementos_visibles[:10]:  # Primeros 10
                            if elem.is_displayed() and elem.text.strip():
                                print(f"    - {elem.text[:50]}...")
                    
                    # Cerrar información desplegada (si es necesario)
                    try:
                        # Buscar botón de cerrar o hacer clic en otra parte
                        driver.find_element(By.TAG_NAME, "body").click()
                        time.sleep(1)
                    except:
                        pass
                    
                else:
                    print(f"✗ Fecha {fecha_texto} no es clickeable")
                    
            except Exception as e:
                print(f"✗ Error procesando fecha {i+1}: {str(e)}")
        
        # PASO 6: Mostrar resultados
        print(f"\n=== RESULTADOS DE LA CONFIRMACIÓN ===")
        print(f"Fechas coral encontradas: {len(fechas_coral)}")
        print(f"Fechas procesadas exitosamente: {fechas_procesadas}")
        print(f"Códigos de 5 cifras encontrados: {len(codigos_encontrados)}")
        
        if codigos_encontrados:
            print(f"\nCódigos encontrados:")
            for codigo in codigos_encontrados:
                print(f"  - {codigo}")
        
        # Verificar si las fechas son realmente clickeables
        print(f"\n=== VERIFICACIÓN DE CLICKEABILIDAD ===")
        for i, fecha in enumerate(fechas_coral[:3]):  # Verificar las primeras 3
            print(f"Fecha {i+1}:")
            print(f"  - Texto: '{fecha.text}'")
            print(f"  - Visible: {fecha.is_displayed()}")
            print(f"  - Habilitado: {fecha.is_enabled()}")
            print(f"  - Estilo: '{fecha.get_attribute('style')}'")
            print(f"  - Clase: '{fecha.get_attribute('class')}'")
            print(f"  - Tag: {fecha.tag_name}")
        
        return fechas_procesadas > 0
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación manual...")
            print("Verifica manualmente que las fechas coral son clickeables")
            print("Y que despliegan información con códigos de 5 cifras")
            time.sleep(120)  # Mantener abierto por 2 minutos
            driver.quit()

if __name__ == "__main__":
    confirmar_fechas_clickeables()


