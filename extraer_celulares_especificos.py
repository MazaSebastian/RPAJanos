#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script específico para extraer los números de celular exactos: 541157526518
"""

import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def extraer_celulares_especificos():
    """Extraer los números de celular específicos: 541157526518"""
    
    print("=== EXTRACCIÓN DE CELULARES ESPECÍFICOS ===")
    print("Objetivo: Extraer 541157526518 (Celular y Celular 2)")
    
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
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # PASO 1: LOGIN INICIAL
        print("\n=== PASO 1: LOGIN INICIAL ===")
        driver.get("https://tecnica.janosgroup.com/login.php")
        time.sleep(3)
        
        username_field = driver.find_element(By.NAME, "username")
        username_field.clear()
        username_field.send_keys("sebastian_maza")
        print("✓ Usuario ingresado")
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys("Janos2025+!")
        print("✓ Contraseña ingresada")
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button.button")
        login_button.click()
        print("✓ Botón de login presionado")
        
        wait.until(lambda driver: "login.php" not in driver.current_url)
        print("✓ Login exitoso")
        
        # PASO 2: ACCESO A ADICIONALES
        print("\n=== PASO 2: ACCESO A ADICIONALES ===")
        
        open_nav_element = driver.find_element(By.XPATH, "//*[@onclick='openNav()']")
        open_nav_element.click()
        time.sleep(2)
        print("✓ Menú lateral abierto")
        
        side_menu = driver.find_element(By.ID, "sideMenu")
        enlaces_menu = side_menu.find_elements(By.TAG_NAME, "a")
        
        for enlace in enlaces_menu:
            if "adicionales" in enlace.text.lower():
                print("✓ Encontrado enlace ADICIONALES")
                enlace.click()
                time.sleep(5)
                break
        
        main_frame = driver.find_element(By.ID, "mainFrame")
        driver.switch_to.frame(main_frame)
        print("✓ Cambiado al frame principal")
        
        # PASO 3: APLICAR FILTROS
        print("\n=== PASO 3: APLICAR FILTROS ===")
        
        salon_select = Select(driver.find_element(By.ID, "salon"))
        salon_select.select_by_visible_text("DOT")
        print("✓ Filtro SALON aplicado: DOT")
        
        zona_select = Select(driver.find_element(By.ID, "cluster"))
        zona_select.select_by_visible_text("CABA")
        print("✓ Filtro ZONA aplicado: CABA")
        
        ano_select = Select(driver.find_element(By.ID, "ano"))
        ano_select.select_by_visible_text("2025")
        print("✓ Filtro AÑO aplicado: 2025")
        
        filtrar_buttons = driver.find_elements(By.XPATH, "//input[@value='Filtrar']")
        if filtrar_buttons:
            filtrar_buttons[0].click()
            time.sleep(5)
            print("✓ Filtros aplicados")
        
        # PASO 4: BUSCAR FECHAS CORAL
        print("\n=== PASO 4: BUSCAR FECHAS CORAL ===")
        
        fechas_coral = driver.find_elements(By.CSS_SELECTOR, "div.boton[style*='background: coral']")
        print(f"Fechas coral encontradas: {len(fechas_coral)}")
        
        if not fechas_coral:
            todas_fechas = driver.find_elements(By.CSS_SELECTOR, "div.boton")
            fechas_con_color = []
            
            for fecha in todas_fechas:
                if fecha.text.strip().isdigit() and fecha.is_displayed():
                    style = fecha.get_attribute('style')
                    if 'background:' in style and style != 'background:':
                        fechas_con_color.append(fecha)
            
            print(f"Fechas con color encontradas: {len(fechas_con_color)}")
            fechas_coral = fechas_con_color
        
        if not fechas_coral:
            print("✗ No se encontraron fechas coral")
            return None
        
        # PASO 5: HACER CLIC EN FECHA CORAL
        print(f"\n=== PASO 5: HACER CLIC EN FECHA CORAL ===")
        
        fecha_coral = fechas_coral[0]
        fecha_texto = fecha_coral.text.strip()
        print(f"✓ Haciendo clic en fecha {fecha_texto}...")
        fecha_coral.click()
        time.sleep(3)
        
        # PASO 6: BUSCAR CÓDIGOS DE 5 DÍGITOS
        print(f"\n=== PASO 6: BUSCAR CÓDIGOS DE 5 DÍGITOS ===")
        
        codigos_5_digitos = driver.find_elements(By.XPATH, "//*[text() and string-length(normalize-space(text())) = 5 and translate(text(), '0123456789', '0000000000') = '00000']")
        print(f"Códigos de 5 dígitos encontrados: {len(codigos_5_digitos)}")
        
        if not codigos_5_digitos:
            print("✗ No se encontraron códigos de 5 dígitos")
            return None
        
        # PASO 7: HACER CLIC EN CÓDIGO 33069
        print(f"\n=== PASO 7: HACER CLIC EN CÓDIGO 33069 ===")
        
        codigo_33069 = None
        for codigo in codigos_5_digitos:
            if codigo.text.strip() == "33069":
                codigo_33069 = codigo
                break
        
        if not codigo_33069:
            print("✗ No se encontró código 33069")
            return None
        
        print(f"✓ Haciendo clic en código 33069...")
        codigo_33069.click()
        time.sleep(5)
        
        # PASO 8: BUSCAR ENLACES A ver_evento.php Y CAPTURAR URL
        print(f"\n=== PASO 8: BUSCAR ENLACES A ver_evento.php Y CAPTURAR URL ===")
        
        enlaces_evento = driver.find_elements(By.XPATH, "//a[contains(@href, 'ver_evento.php')]")
        print(f"Enlaces a ver_evento.php encontrados: {len(enlaces_evento)}")
        
        if not enlaces_evento:
            print("✗ No se encontraron enlaces a ver_evento.php")
            return None
        
        # Capturar la URL del enlace dentro del iframe
        enlace_evento = enlaces_evento[0]
        url_evento = enlace_evento.get_attribute('href')
        print(f"✓ URL del evento capturada: {url_evento}")
        
        # PASO 9: NAVEGAR DIRECTAMENTE A LA URL DEL EVENTO
        print(f"\n=== PASO 9: NAVEGAR DIRECTAMENTE A LA URL DEL EVENTO ===")
        
        print(f"✓ Navegando directamente a: {url_evento}")
        driver.get(url_evento)
        time.sleep(8)
        
        current_url = driver.current_url
        print(f"✓ URL actual: {current_url}")
        
        if "ver_evento.php" not in current_url:
            print("⚠ No estamos en la página individual del evento")
            return None
        
        print("✓ ¡Estamos en la página individual del evento!")
        
        # PASO 10: BUSCAR NÚMEROS DE CELULAR ESPECÍFICOS
        print(f"\n=== PASO 10: BUSCAR NÚMEROS DE CELULAR ESPECÍFICOS ===")
        
        # Obtener todo el HTML de la página
        page_html = driver.page_source
        print(f"HTML de la página obtenido: {len(page_html)} caracteres")
        
        # Buscar el número específico 541157526518
        numero_especifico = "541157526518"
        
        # Buscar en el HTML
        if numero_especifico in page_html:
            print(f"✓ Número {numero_especifico} encontrado en el HTML")
        else:
            print(f"✗ Número {numero_especifico} NO encontrado en el HTML")
        
        # Buscar patrones similares
        patrones_busqueda = [
            r'541157526518',
            r'5411\d{8}',
            r'54\s*11\s*57526518',
            r'\+54\s*11\s*57526518',
            r'011\s*57526518',
            r'11\s*57526518',
            r'57526518'
        ]
        
        numeros_encontrados = []
        for patron in patrones_busqueda:
            matches = re.findall(patron, page_html)
            for match in matches:
                if match not in numeros_encontrados:
                    numeros_encontrados.append(match)
                    print(f"✓ Número encontrado con patrón {patron}: {match}")
        
        # Buscar en elementos específicos
        print(f"\n=== BÚSQUEDA EN ELEMENTOS ESPECÍFICOS ===")
        
        # Buscar elementos que contengan "Celular"
        elementos_celular = driver.find_elements(By.XPATH, "//*[contains(text(), 'Celular')]")
        print(f"Elementos con 'Celular' encontrados: {len(elementos_celular)}")
        
        for elem in elementos_celular:
            texto = elem.text.strip()
            print(f"Elemento Celular: {texto}")
            
            # Buscar números en el texto
            for patron in patrones_busqueda:
                matches = re.findall(patron, texto)
                for match in matches:
                    if match not in numeros_encontrados:
                        numeros_encontrados.append(match)
                        print(f"✓ Número encontrado en elemento: {match}")
        
        # Buscar en todas las celdas de tabla
        print(f"\n=== BÚSQUEDA EN TABLAS ===")
        celdas_tabla = driver.find_elements(By.TAG_NAME, "td")
        print(f"Celdas de tabla encontradas: {len(celdas_tabla)}")
        
        for i, celda in enumerate(celdas_tabla):
            texto_celda = celda.text.strip()
            if texto_celda and any(char.isdigit() for char in texto_celda):
                # Buscar números en el texto de la celda
                for patron in patrones_busqueda:
                    matches = re.findall(patron, texto_celda)
                    for match in matches:
                        if match not in numeros_encontrados:
                            numeros_encontrados.append(match)
                            print(f"✓ Número encontrado en celda {i}: {match}")
                            print(f"  Texto de la celda: {texto_celda}")
        
        # Resultado final
        print(f"\n=== RESULTADO FINAL ===")
        if numeros_encontrados:
            print(f"Total de números encontrados: {len(numeros_encontrados)}")
            for i, num in enumerate(numeros_encontrados):
                print(f"  Número {i+1}: {num}")
        else:
            print("✗ No se encontraron números de celular")
        
        return {
            'numeros': numeros_encontrados,
            'total': len(numeros_encontrados)
        }
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return None
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación manual...")
            time.sleep(300)  # Mantener abierto por 5 minutos
            driver.quit()

if __name__ == "__main__":
    resultado = extraer_celulares_especificos()
    if resultado:
        print(f"\n=== RESULTADO FINAL ===")
        print(f"Números encontrados: {resultado['numeros']}")
        print(f"Total: {resultado['total']}")
    else:
        print(f"\n=== RESULTADO FINAL ===")
        print(f"No se pudieron extraer los números de celular")


