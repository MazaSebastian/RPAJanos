#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para salir del iframe, hacer clic en el código 33069 y extraer todos los datos específicos del evento
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def extraer_datos_evento_fuera_iframe():
    """Salir del iframe, hacer clic en código 33069 y extraer datos específicos del evento"""
    
    print("=== EXTRACCIÓN DE DATOS DEL EVENTO FUERA DEL IFRAME ===")
    print("Proceso:")
    print("1. Acceder al calendario")
    print("2. Salir del iframe")
    print("3. Hacer clic en código 33069")
    print("4. Extraer todos los datos específicos del evento")
    
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
        
        # PASO 8: BUSCAR ENLACES A ver_evento.php
        print(f"\n=== PASO 8: BUSCAR ENLACES A ver_evento.php ===")
        
        enlaces_evento = driver.find_elements(By.XPATH, "//a[contains(@href, 'ver_evento.php')]")
        print(f"Enlaces a ver_evento.php encontrados: {len(enlaces_evento)}")
        
        if not enlaces_evento:
            print("✗ No se encontraron enlaces a ver_evento.php")
            return None
        
        # PASO 9: SALIR DEL IFRAME Y HACER CLIC EN ENLACE
        print(f"\n=== PASO 9: SALIR DEL IFRAME Y HACER CLIC EN ENLACE ===")
        
        # Salir del iframe
        driver.switch_to.default_content()
        print("✓ Salido del iframe")
        
        # Buscar el enlace del evento en el contexto principal
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
        else:
            print("⚠ Aún no estamos en la página individual del evento")
            return None
        
        # PASO 10: EXTRAER DATOS ESPECÍFICOS
        print(f"\n=== PASO 10: EXTRAER DATOS ESPECÍFICOS ===")
        
        # Analizar todos los elementos de la página
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
        
        # Inicializar datos del evento
        datos_evento = {
            'fecha': fecha_texto,
            'codigo': '33069',
            'url': current_url,
            'homenajeada': None,
            'codigo_evento': None,
            'tipo_evento': None,
            'fecha_evento': None,
            'salon': None,
            'cliente': None,
            'celular': None,
            'celular_2': None,
            'tipo_pack': None
        }
        
        # BÚSQUEDA ESPECÍFICA DE DATOS
        print(f"\n=== BÚSQUEDA ESPECÍFICA DE DATOS ===")
        
        # 1. HOMENAJEADA/O
        print(f"--- BUSCANDO HOMENAJEADA/O ---")
        for elem in elementos_relevantes:
            if 'homenajeada' in elem['texto'].lower() or 'homenajeado' in elem['texto'].lower():
                indice = elementos_relevantes.index(elem)
                if indice + 1 < len(elementos_relevantes):
                    siguiente_elem = elementos_relevantes[indice + 1]
                    if siguiente_elem['texto'] and len(siguiente_elem['texto']) > 1:
                        datos_evento['homenajeada'] = siguiente_elem['texto']
                        print(f"✓ Homenajeada/o: {siguiente_elem['texto']}")
                        break
        
        # 2. CÓDIGO DE EVENTO
        print(f"--- BUSCANDO CÓDIGO DE EVENTO ---")
        for elem in elementos_relevantes:
            if 'codigo' in elem['texto'].lower() and 'evento' in elem['texto'].lower():
                indice = elementos_relevantes.index(elem)
                if indice + 1 < len(elementos_relevantes):
                    siguiente_elem = elementos_relevantes[indice + 1]
                    if siguiente_elem['texto'] and siguiente_elem['texto'].isdigit():
                        datos_evento['codigo_evento'] = siguiente_elem['texto']
                        print(f"✓ Código de evento: {siguiente_elem['texto']}")
                        break
        
        # 3. TIPO DE EVENTO (15, cumpleaños, boda, corporativo)
        print(f"--- BUSCANDO TIPO DE EVENTO (15, cumpleaños, boda, corporativo) ---")
        for elem in elementos_relevantes:
            if 'tipo' in elem['texto'].lower() and 'evento' in elem['texto'].lower():
                indice = elementos_relevantes.index(elem)
                if indice + 1 < len(elementos_relevantes):
                    siguiente_elem = elementos_relevantes[indice + 1]
                    if siguiente_elem['texto']:
                        datos_evento['tipo_evento'] = siguiente_elem['texto']
                        print(f"✓ Tipo de evento: {siguiente_elem['texto']}")
                        break
        
        # 4. FECHA DEL EVENTO (no fecha de alta)
        print(f"--- BUSCANDO FECHA DEL EVENTO (no fecha de alta) ---")
        for elem in elementos_relevantes:
            if 'fecha del evento' in elem['texto'].lower():
                indice = elementos_relevantes.index(elem)
                if indice + 1 < len(elementos_relevantes):
                    siguiente_elem = elementos_relevantes[indice + 1]
                    if siguiente_elem['texto']:
                        datos_evento['fecha_evento'] = siguiente_elem['texto']
                        print(f"✓ Fecha del evento: {siguiente_elem['texto']}")
                        break
        
        # 5. SALÓN
        print(f"--- BUSCANDO SALÓN ---")
        for elem in elementos_relevantes:
            if 'salon' in elem['texto'].lower() or 'salón' in elem['texto'].lower():
                indice = elementos_relevantes.index(elem)
                if indice + 1 < len(elementos_relevantes):
                    siguiente_elem = elementos_relevantes[indice + 1]
                    if siguiente_elem['texto']:
                        datos_evento['salon'] = siguiente_elem['texto']
                        print(f"✓ Salón: {siguiente_elem['texto']}")
                        break
        
        # 6. CLIENTE (CLICKEABLE) - Hacer clic y extraer CELULAR y CELULAR 2
        print(f"--- BUSCANDO CLIENTE (CLICKEABLE) ---")
        cliente_encontrado = False
        for elem in elementos_relevantes:
            if 'cliente' in elem['texto'].lower() and elem['elemento'].tag_name in ['a', 'button']:
                try:
                    cliente_texto = elem['texto']
                    print(f"✓ Cliente encontrado: {cliente_texto}")
                    datos_evento['cliente'] = cliente_texto
                    
                    # Hacer clic en el cliente
                    print(f"✓ Haciendo clic en cliente...")
                    elem['elemento'].click()
                    time.sleep(3)
                    
                    # Buscar CELULAR y CELULAR 2
                    print(f"--- BUSCANDO CELULAR Y CELULAR 2 ---")
                    
                    elementos_contacto = driver.find_elements(By.XPATH, "//*[text()]")
                    celulares_encontrados = []
                    
                    for elem_contacto in elementos_contacto:
                        if elem_contacto.is_displayed() and elem_contacto.text.strip():
                            texto_contacto = elem_contacto.text.strip()
                            if any(char.isdigit() for char in texto_contacto):
                                if any(palabra in texto_contacto.lower() for palabra in ['celular', 'telefono', 'teléfono', 'tel', 'móvil', 'movil']):
                                    celulares_encontrados.append(texto_contacto)
                                    print(f"✓ Celular encontrado: {texto_contacto}")
                    
                    # Asignar celulares
                    if len(celulares_encontrados) >= 1:
                        datos_evento['celular'] = celulares_encontrados[0]
                        print(f"✓ Celular: {celulares_encontrados[0]}")
                    
                    if len(celulares_encontrados) >= 2:
                        datos_evento['celular_2'] = celulares_encontrados[1]
                        print(f"✓ Celular 2: {celulares_encontrados[1]}")
                    
                    cliente_encontrado = True
                    break
                    
                except Exception as e:
                    print(f"✗ Error haciendo clic en cliente: {str(e)}")
                    continue
        
        if not cliente_encontrado:
            print("✗ No se encontró cliente clickeable")
        
        # 7. TIPO DE PACK (Pack 1, Pack 2, etc.)
        print(f"--- BUSCANDO TIPO DE PACK (Pack 1, Pack 2, etc.) ---")
        for elem in elementos_relevantes:
            if 'pack' in elem['texto'].lower():
                datos_evento['tipo_pack'] = elem['texto']
                print(f"✓ Tipo de Pack: {elem['texto']}")
                break
        
        # Mostrar resumen final
        print(f"\n=== RESUMEN FINAL DE DATOS ENCONTRADOS ===")
        datos_encontrados = 0
        for campo, valor in datos_evento.items():
            if valor and campo not in ['fecha', 'codigo', 'url']:
                datos_encontrados += 1
                print(f"✓ {campo}: {valor}")
            elif not valor and campo not in ['fecha', 'codigo', 'url']:
                print(f"✗ {campo}: No encontrado")
        
        print(f"\nTotal de datos encontrados: {datos_encontrados}/7")
        
        return datos_evento
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return None
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación manual...")
            print("Verifica que se pueden acceder a todos los datos específicos:")
            print("- Homenajeada/o")
            print("- Código de evento")
            print("- Tipo de evento (15, cumpleaños, boda, corporativo)")
            print("- Fecha del evento (no fecha de alta)")
            print("- Salón")
            print("- Cliente (clickeable - CELULAR y CELULAR 2)")
            print("- Tipo de Pack (Pack 1, Pack 2, etc.)")
            time.sleep(300)  # Mantener abierto por 5 minutos
            driver.quit()

if __name__ == "__main__":
    resultado = extraer_datos_evento_fuera_iframe()
    if resultado:
        print(f"\n=== RESULTADO FINAL ===")
        print(f"Datos extraídos exitosamente:")
        for campo, valor in resultado.items():
            print(f"  {campo}: {valor}")
    else:
        print(f"\n=== RESULTADO FINAL ===")
        print(f"No se pudieron extraer los datos requeridos")


