#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para investigar por qué los enlaces no navegan a la página individual del evento
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def investigar_navegacion_evento():
    """Investigar por qué los enlaces no navegan a la página individual del evento"""
    
    print("=== INVESTIGACIÓN DE NAVEGACIÓN DEL EVENTO ===")
    print("Proceso a analizar:")
    print("1. Fecha naranja → código clickeable")
    print("2. Código clickeable → información individual")
    print("3. Verificar qué información se despliega")
    
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
        
        # PASO 5: HACER CLIC EN FECHA CORAL Y ANALIZAR
        print(f"\n=== PASO 5: HACER CLIC EN FECHA CORAL ===")
        
        fecha_coral = fechas_coral[0]
        fecha_texto = fecha_coral.text.strip()
        print(f"✓ Haciendo clic en fecha {fecha_texto}...")
        fecha_coral.click()
        time.sleep(3)
        
        # Analizar qué se despliega después del clic
        print(f"\n=== ANÁLISIS POST-CLIC EN FECHA ===")
        current_url = driver.current_url
        print(f"URL actual: {current_url}")
        
        # Buscar códigos de 5 dígitos
        codigos_5_digitos = driver.find_elements(By.XPATH, "//*[text() and string-length(normalize-space(text())) = 5 and translate(text(), '0123456789', '0000000000') = '00000']")
        print(f"Códigos de 5 dígitos encontrados: {len(codigos_5_digitos)}")
        
        if codigos_5_digitos:
            print("Códigos encontrados:")
            for i, codigo in enumerate(codigos_5_digitos[:5]):  # Mostrar solo los primeros 5
                print(f"  {i+1}. {codigo.text.strip()}")
        
        # PASO 6: HACER CLIC EN CÓDIGO 33069 Y ANALIZAR
        print(f"\n=== PASO 6: HACER CLIC EN CÓDIGO 33069 ===")
        
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
        
        # Analizar qué se despliega después del clic en el código
        print(f"\n=== ANÁLISIS POST-CLIC EN CÓDIGO 33069 ===")
        current_url = driver.current_url
        print(f"URL actual: {current_url}")
        
        # Buscar enlaces a ver_evento.php
        enlaces_evento = driver.find_elements(By.XPATH, "//a[contains(@href, 'ver_evento.php')]")
        print(f"Enlaces a ver_evento.php encontrados: {len(enlaces_evento)}")
        
        if enlaces_evento:
            print("Enlaces encontrados:")
            for i, enlace in enumerate(enlaces_evento[:5]):  # Mostrar solo los primeros 5
                href = enlace.get_attribute('href')
                print(f"  {i+1}. {href}")
        
        # PASO 7: HACER CLIC EN ENLACE DEL EVENTO Y ANALIZAR
        print(f"\n=== PASO 7: HACER CLIC EN ENLACE DEL EVENTO ===")
        
        if enlaces_evento:
            enlace_evento = enlaces_evento[0]
            url_evento = enlace_evento.get_attribute('href')
            print(f"✓ URL del evento: {url_evento}")
            
            # Hacer clic en el enlace
            print(f"✓ Haciendo clic en enlace del evento...")
            enlace_evento.click()
            time.sleep(8)  # Esperar más tiempo para que cargue
            
            # Verificar que cambió la URL
            current_url = driver.current_url
            print(f"✓ URL actual: {current_url}")
            
            # Verificar si estamos en la página correcta
            if "ver_evento.php" in current_url:
                print("✓ ¡Estamos en la página individual del evento!")
                
                # Analizar contenido de la página individual
                print(f"\n=== ANÁLISIS DE LA PÁGINA INDIVIDUAL DEL EVENTO ===")
                
                # Buscar todos los elementos con texto
                todos_elementos = driver.find_elements(By.XPATH, "//*[text()]")
                elementos_relevantes = []
                
                for elem in todos_elementos:
                    if elem.is_displayed() and elem.text.strip():
                        texto = elem.text.strip()
                        if len(texto) > 0 and len(texto) < 500:
                            elementos_relevantes.append({
                                'tag': elem.tag_name,
                                'texto': texto,
                                'clase': elem.get_attribute('class'),
                                'id': elem.get_attribute('id'),
                                'elemento': elem
                            })
                
                print(f"Total de elementos con texto: {len(elementos_relevantes)}")
                
                # Mostrar los primeros 30 elementos para análisis
                print(f"\n=== PRIMEROS 30 ELEMENTOS ENCONTRADOS ===")
                for k, elem in enumerate(elementos_relevantes[:30]):
                    print(f"  {k+1}. {elem['tag']}: {elem['texto']}")
                
                # Buscar datos específicos
                print(f"\n=== BÚSQUEDA DE DATOS ESPECÍFICOS ===")
                
                # Buscar HOMENAJEADA/O
                print(f"--- BUSCANDO HOMENAJEADA/O ---")
                homenajeada_encontrada = False
                for elem in elementos_relevantes:
                    if 'homenajeada' in elem['texto'].lower() or 'homenajeado' in elem['texto'].lower():
                        print(f"✓ Encontrado: {elem['texto']}")
                        homenajeada_encontrada = True
                        break
                
                if not homenajeada_encontrada:
                    print("✗ No se encontró homenajeada/o")
                
                # Buscar TIPO DE EVENTO
                print(f"--- BUSCANDO TIPO DE EVENTO ---")
                tipo_evento_encontrado = False
                for elem in elementos_relevantes:
                    if 'tipo' in elem['texto'].lower() and 'evento' in elem['texto'].lower():
                        print(f"✓ Encontrado: {elem['texto']}")
                        tipo_evento_encontrado = True
                        break
                
                if not tipo_evento_encontrado:
                    print("✗ No se encontró tipo de evento")
                
                # Buscar FECHA DEL EVENTO
                print(f"--- BUSCANDO FECHA DEL EVENTO ---")
                fecha_evento_encontrada = False
                for elem in elementos_relevantes:
                    if 'fecha del evento' in elem['texto'].lower():
                        print(f"✓ Encontrado: {elem['texto']}")
                        fecha_evento_encontrada = True
                        break
                
                if not fecha_evento_encontrada:
                    print("✗ No se encontró fecha del evento")
                
                # Buscar SALÓN
                print(f"--- BUSCANDO SALÓN ---")
                salon_encontrado = False
                for elem in elementos_relevantes:
                    if 'salon' in elem['texto'].lower() or 'salón' in elem['texto'].lower():
                        print(f"✓ Encontrado: {elem['texto']}")
                        salon_encontrado = True
                        break
                
                if not salon_encontrado:
                    print("✗ No se encontró salón")
                
                # Buscar CLIENTE
                print(f"--- BUSCANDO CLIENTE ---")
                cliente_encontrado = False
                for elem in elementos_relevantes:
                    if 'cliente' in elem['texto'].lower():
                        print(f"✓ Encontrado: {elem['texto']}")
                        cliente_encontrado = True
                        break
                
                if not cliente_encontrado:
                    print("✗ No se encontró cliente")
                
                # Buscar TIPO DE PACK
                print(f"--- BUSCANDO TIPO DE PACK ---")
                pack_encontrado = False
                for elem in elementos_relevantes:
                    if 'pack' in elem['texto'].lower():
                        print(f"✓ Encontrado: {elem['texto']}")
                        pack_encontrado = True
                        break
                
                if not pack_encontrado:
                    print("✗ No se encontró tipo de pack")
                
                return {
                    'url': current_url,
                    'total_elementos': len(elementos_relevantes),
                    'homenajeada_encontrada': homenajeada_encontrada,
                    'tipo_evento_encontrado': tipo_evento_encontrado,
                    'fecha_evento_encontrada': fecha_evento_encontrada,
                    'salon_encontrado': salon_encontrado,
                    'cliente_encontrado': cliente_encontrado,
                    'pack_encontrado': pack_encontrado
                }
                
            else:
                print("⚠ Aún no estamos en la página individual del evento")
                print(f"URL actual: {current_url}")
                return None
        else:
            print("✗ No se encontraron enlaces a ver_evento.php")
            return None
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return None
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación manual...")
            print("Verifica manualmente el proceso:")
            print("1. Fecha naranja → código clickeable")
            print("2. Código clickeable → información individual")
            print("3. ¿Qué información se despliega?")
            time.sleep(300)  # Mantener abierto por 5 minutos
            driver.quit()

if __name__ == "__main__":
    resultado = investigar_navegacion_evento()
    if resultado:
        print(f"\n=== RESULTADO FINAL DE LA INVESTIGACIÓN ===")
        print(f"URL: {resultado['url']}")
        print(f"Total de elementos: {resultado['total_elementos']}")
        print(f"Homenajeada/o encontrada: {resultado['homenajeada_encontrada']}")
        print(f"Tipo de evento encontrado: {resultado['tipo_evento_encontrado']}")
        print(f"Fecha del evento encontrada: {resultado['fecha_evento_encontrada']}")
        print(f"Salón encontrado: {resultado['salon_encontrado']}")
        print(f"Cliente encontrado: {resultado['cliente_encontrado']}")
        print(f"Tipo de Pack encontrado: {resultado['pack_encontrado']}")
    else:
        print(f"\n=== RESULTADO FINAL DE LA INVESTIGACIÓN ===")
        print(f"No se pudo completar la investigación")


