#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar todas las fechas clickeables y buscar información desplegada
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def probar_fechas_clickeables():
    """Probar todas las fechas clickeables y buscar información desplegada"""
    
    print("=== PROBANDO FECHAS CLICKEABLES ===")
    print("Buscando todas las fechas clickeables...")
    print("Probando clic y buscando información desplegada...")
    
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
        
        # PASO 4: Buscar todas las fechas clickeables
        print("\n=== PASO 4: BUSCANDO FECHAS CLICKEABLES ===")
        
        # Buscar todos los divs con clase boton
        todos_botones = driver.find_elements(By.CSS_SELECTOR, "div.boton")
        print(f"Total de divs con clase 'boton': {len(todos_botones)}")
        
        # Filtrar solo los que tienen números (fechas)
        fechas_numericas = []
        for boton in todos_botones:
            if boton.text.strip().isdigit() and boton.is_displayed():
                fechas_numericas.append(boton)
        
        print(f"Fechas numéricas encontradas: {len(fechas_numericas)}")
        
        # Buscar fechas con colores específicos
        fechas_con_color = []
        for boton in fechas_numericas:
            style = boton.get_attribute('style')
            if 'background:' in style and style != 'background:':
                fechas_con_color.append(boton)
        
        print(f"Fechas con color de fondo: {len(fechas_con_color)}")
        
        # Mostrar información de las primeras fechas con color
        print(f"\nPrimeras fechas con color:")
        for i, fecha in enumerate(fechas_con_color[:10]):
            print(f"  {i+1}. Texto: '{fecha.text}', Estilo: '{fecha.get_attribute('style')}'")
        
        # PASO 5: Probar clic en fechas con color
        print(f"\n=== PASO 5: PROBANDO CLIC EN FECHAS CON COLOR ===")
        
        fechas_procesadas = 0
        codigos_encontrados = []
        
        for i, fecha in enumerate(fechas_con_color[:5]):  # Probar con las primeras 5 fechas con color
            try:
                fecha_texto = fecha.text.strip()
                print(f"\n--- Probando fecha {i+1}: {fecha_texto} ---")
                
                # Verificar que es clickeable
                if fecha.is_displayed() and fecha.is_enabled():
                    print(f"✓ Fecha {fecha_texto} es clickeable")
                    print(f"  - Estilo: '{fecha.get_attribute('style')}'")
                    
                    # Hacer clic en la fecha
                    print(f"✓ Haciendo clic en fecha {fecha_texto}...")
                    fecha.click()
                    time.sleep(3)  # Esperar a que se despliegue la información
                    
                    # Buscar información desplegada
                    print(f"✓ Buscando información desplegada...")
                    
                    # Buscar todos los elementos con texto después del clic
                    elementos_con_texto = driver.find_elements(By.XPATH, "//*[text()]")
                    print(f"  - Elementos con texto encontrados: {len(elementos_con_texto)}")
                    
                    # Buscar códigos de 5 dígitos
                    codigos_5_digitos = []
                    for elem in elementos_con_texto:
                        if elem.is_displayed():
                            texto = elem.text.strip()
                            if len(texto) == 5 and texto.isdigit():
                                codigos_5_digitos.append(texto)
                                print(f"    ✓ Código de 5 dígitos encontrado: {texto}")
                    
                    if codigos_5_digitos:
                        codigos_encontrados.extend(codigos_5_digitos)
                        fechas_procesadas += 1
                        print(f"✓ Fecha {fecha_texto} procesada exitosamente")
                    else:
                        print(f"⚠ Fecha {fecha_texto}: No se encontró código de 5 dígitos")
                        
                        # Mostrar texto visible para diagnóstico
                        print(f"  Texto visible después del clic:")
                        for elem in elementos_con_texto[:15]:  # Primeros 15
                            if elem.is_displayed() and elem.text.strip():
                                texto_limpio = elem.text.strip()
                                if len(texto_limpio) > 0:
                                    print(f"    - '{texto_limpio[:100]}...'")
                    
                    # Intentar cerrar información desplegada
                    try:
                        # Hacer clic en otra parte para cerrar
                        driver.find_element(By.TAG_NAME, "body").click()
                        time.sleep(1)
                    except:
                        pass
                    
                else:
                    print(f"✗ Fecha {fecha_texto} no es clickeable")
                    
            except Exception as e:
                print(f"✗ Error procesando fecha {i+1}: {str(e)}")
        
        # PASO 6: Mostrar resultados
        print(f"\n=== RESULTADOS DE LA PRUEBA ===")
        print(f"Fechas con color encontradas: {len(fechas_con_color)}")
        print(f"Fechas procesadas exitosamente: {fechas_procesadas}")
        print(f"Códigos de 5 dígitos encontrados: {len(codigos_encontrados)}")
        
        if codigos_encontrados:
            print(f"\nCódigos encontrados:")
            for codigo in codigos_encontrados:
                print(f"  - {codigo}")
        
        # Mostrar información detallada de las fechas
        print(f"\n=== INFORMACIÓN DETALLADA DE FECHAS ===")
        print(f"Total de fechas numéricas: {len(fechas_numericas)}")
        print(f"Fechas con color: {len(fechas_con_color)}")
        
        # Contar fechas por color
        colores_encontrados = {}
        for fecha in fechas_con_color:
            style = fecha.get_attribute('style')
            if 'background:' in style:
                color = style.split('background:')[1].split(';')[0].strip()
                if color not in colores_encontrados:
                    colores_encontrados[color] = 0
                colores_encontrados[color] += 1
        
        print(f"\nFechas por color:")
        for color, cantidad in colores_encontrados.items():
            print(f"  - {color}: {cantidad} fechas")
        
        return fechas_procesadas > 0
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación manual...")
            print("Verifica manualmente:")
            print("1. Que las fechas con color son clickeables")
            print("2. Que al hacer clic se despliega información")
            print("3. Que aparece un código de 5 dígitos")
            time.sleep(180)  # Mantener abierto por 3 minutos
            driver.quit()

if __name__ == "__main__":
    probar_fechas_clickeables()


