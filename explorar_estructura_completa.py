#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para explorar la estructura completa de la página de eventos
y identificar dónde están los datos específicos requeridos
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def explorar_estructura_completa():
    """Explorar la estructura completa de la página de eventos"""
    
    print("=== EXPLORACIÓN COMPLETA DE ESTRUCTURA ===")
    print("Analizando toda la información disponible en la página...")
    
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
        
        # PASO 4: Buscar fechas coral
        print("\n=== PASO 4: BUSCANDO FECHAS CORAL ===")
        
        # Buscar fechas con color coral
        fechas_coral = driver.find_elements(By.CSS_SELECTOR, "div.boton[style*='background: coral']")
        print(f"Fechas coral encontradas: {len(fechas_coral)}")
        
        if not fechas_coral:
            print("⚠ No se encontraron fechas coral, buscando con otros selectores...")
            # Buscar todas las fechas con color
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
            return False
        
        # PASO 5: Explorar estructura completa
        print(f"\n=== PASO 5: EXPLORACIÓN COMPLETA DE ESTRUCTURA ===")
        
        for i, fecha_coral in enumerate(fechas_coral[:1]):  # Analizar solo la primera fecha
            try:
                fecha_texto = fecha_coral.text.strip()
                print(f"\n--- EXPLORACIÓN FECHA {i+1}: {fecha_texto} ---")
                
                # Hacer clic en la fecha coral
                print(f"✓ Haciendo clic en fecha {fecha_texto}...")
                fecha_coral.click()
                time.sleep(3)  # Esperar a que se despliegue la información
                
                # Buscar códigos de 5 dígitos clickeables
                print(f"✓ Buscando códigos de 5 dígitos...")
                codigos_5_digitos = driver.find_elements(By.XPATH, "//*[text() and string-length(normalize-space(text())) = 5 and translate(text(), '0123456789', '0000000000') = '00000']")
                
                print(f"  - Códigos de 5 dígitos encontrados: {len(codigos_5_digitos)}")
                
                # Analizar cada código
                for j, codigo_elem in enumerate(codigos_5_digitos[:1]):  # Analizar el primer código
                    try:
                        codigo_texto = codigo_elem.text.strip()
                        print(f"\n    === EXPLORACIÓN CÓDIGO {j+1}: {codigo_texto} ===")
                        
                        # Hacer clic en el código
                        print(f"    ✓ Haciendo clic en código {codigo_texto}...")
                        codigo_elem.click()
                        time.sleep(5)  # Esperar a que cargue la información detallada
                        
                        # EXPLORACIÓN COMPLETA DE TODA LA INFORMACIÓN
                        print(f"    ✓ Explorando toda la información disponible...")
                        
                        # 1. ANÁLISIS DE TODOS LOS ELEMENTOS VISIBLES
                        print(f"    --- ANÁLISIS DE TODOS LOS ELEMENTOS VISIBLES ---")
                        
                        # Buscar todos los elementos con texto
                        todos_elementos = driver.find_elements(By.XPATH, "//*[text()]")
                        elementos_relevantes = []
                        
                        for elem in todos_elementos:
                            if elem.is_displayed() and elem.text.strip():
                                texto = elem.text.strip()
                                if len(texto) > 0 and len(texto) < 500:  # Filtrar texto relevante
                                    tag = elem.tag_name
                                    clase = elem.get_attribute('class')
                                    id_elem = elem.get_attribute('id')
                                    
                                    elementos_relevantes.append({
                                        'tag': tag,
                                        'texto': texto,
                                        'clase': clase,
                                        'id': id_elem
                                    })
                        
                        print(f"      Total de elementos con texto: {len(elementos_relevantes)}")
                        
                        # Mostrar los primeros 20 elementos
                        print(f"      Primeros 20 elementos encontrados:")
                        for k, elem in enumerate(elementos_relevantes[:20]):
                            print(f"        {k+1}. {elem['tag']}: {elem['texto'][:100]}...")
                        
                        # 2. BUSCAR PATRONES ESPECÍFICOS
                        print(f"    --- BÚSQUEDA DE PATRONES ESPECÍFICOS ---")
                        
                        patrones_buscados = {
                            'homenajeada': ['homenajeada', 'homenajeado', 'Homenajeada', 'Homenajeado'],
                            'tipo_evento': ['tipo', 'evento', 'Tipo', 'Evento'],
                            'fecha': ['fecha', 'Fecha', 'FECHA'],
                            'salon': ['salon', 'salón', 'Salon', 'Salón'],
                            'cliente': ['cliente', 'Cliente', 'CLIENTE'],
                            'celular': ['celular', 'Celular', 'CELULAR', 'telefono', 'teléfono'],
                            'pack': ['pack', 'Pack', 'PACK']
                        }
                        
                        patrones_encontrados = {}
                        for patron_nombre, palabras in patrones_buscados.items():
                            elementos_patron = []
                            for elem in elementos_relevantes:
                                for palabra in palabras:
                                    if palabra.lower() in elem['texto'].lower():
                                        elementos_patron.append(elem)
                                        break
                            
                            if elementos_patron:
                                patrones_encontrados[patron_nombre] = elementos_patron
                                print(f"      ✓ {patron_nombre}: {len(elementos_patron)} elementos encontrados")
                                for elem in elementos_patron[:3]:  # Mostrar los primeros 3
                                    print(f"        - {elem['tag']}: {elem['texto'][:50]}...")
                            else:
                                print(f"      ✗ {patron_nombre}: No encontrado")
                        
                        # 3. ANÁLISIS DE TABLAS
                        print(f"    --- ANÁLISIS DE TABLAS ---")
                        tablas = driver.find_elements(By.TAG_NAME, "table")
                        print(f"      Total de tablas: {len(tablas)}")
                        
                        for k, tabla in enumerate(tablas):
                            if tabla.is_displayed():
                                filas = tabla.find_elements(By.TAG_NAME, "tr")
                                print(f"      Tabla {k+1}: {len(filas)} filas")
                                
                                # Analizar contenido de la tabla
                                for l, fila in enumerate(filas[:5]):  # Primeras 5 filas
                                    celdas = fila.find_elements(By.TAG_NAME, "td")
                                    if celdas:
                                        contenido_fila = []
                                        for celda in celdas:
                                            if celda.is_displayed() and celda.text.strip():
                                                contenido_fila.append(celda.text.strip())
                                        
                                        if contenido_fila:
                                            print(f"        Fila {l+1}: {contenido_fila}")
                        
                        # 4. ANÁLISIS DE FORMULARIOS
                        print(f"    --- ANÁLISIS DE FORMULARIOS ---")
                        forms = driver.find_elements(By.TAG_NAME, "form")
                        print(f"      Total de formularios: {len(forms)}")
                        
                        for k, form in enumerate(forms):
                            if form.is_displayed():
                                inputs = form.find_elements(By.TAG_NAME, "input")
                                selects = form.find_elements(By.TAG_NAME, "select")
                                textareas = form.find_elements(By.TAG_NAME, "textarea")
                                
                                print(f"      Formulario {k+1}: {len(inputs)} inputs, {len(selects)} selects, {len(textareas)} textareas")
                                
                                # Analizar inputs
                                for input_elem in inputs:
                                    if input_elem.is_displayed():
                                        tipo = input_elem.get_attribute('type')
                                        nombre = input_elem.get_attribute('name')
                                        valor = input_elem.get_attribute('value')
                                        placeholder = input_elem.get_attribute('placeholder')
                                        
                                        if valor or nombre or placeholder:
                                            print(f"        Input: tipo={tipo}, nombre={nombre}, valor={valor}, placeholder={placeholder}")
                        
                        # 5. ANÁLISIS DE ENLACES Y BOTONES
                        print(f"    --- ANÁLISIS DE ENLACES Y BOTONES ---")
                        enlaces = driver.find_elements(By.TAG_NAME, "a")
                        botones = driver.find_elements(By.TAG_NAME, "button")
                        
                        print(f"      Total de enlaces: {len(enlaces)}")
                        print(f"      Total de botones: {len(botones)}")
                        
                        # Analizar enlaces clickeables
                        for enlace in enlaces:
                            if enlace.is_displayed() and enlace.is_enabled() and enlace.text.strip():
                                texto = enlace.text.strip()
                                href = enlace.get_attribute('href')
                                onclick = enlace.get_attribute('onclick')
                                
                                if len(texto) > 0 and len(texto) < 200:
                                    print(f"        Enlace: '{texto}' (href: {href}, onclick: {onclick})")
                        
                        # Analizar botones clickeables
                        for boton in botones:
                            if boton.is_displayed() and boton.is_enabled() and boton.text.strip():
                                texto = boton.text.strip()
                                onclick = boton.get_attribute('onclick')
                                
                                if len(texto) > 0 and len(texto) < 200:
                                    print(f"        Botón: '{texto}' (onclick: {onclick})")
                        
                        # 6. RESUMEN DE INFORMACIÓN DISPONIBLE
                        print(f"    --- RESUMEN DE INFORMACIÓN DISPONIBLE ---")
                        print(f"      Elementos con texto: {len(elementos_relevantes)}")
                        print(f"      Patrones encontrados: {len(patrones_encontrados)}")
                        print(f"      Tablas: {len(tablas)}")
                        print(f"      Formularios: {len(forms)}")
                        print(f"      Enlaces: {len(enlaces)}")
                        print(f"      Botones: {len(botones)}")
                        
                        # Volver atrás
                        try:
                            driver.find_element(By.TAG_NAME, "body").click()
                            time.sleep(1)
                        except:
                            pass
                        
                    except Exception as e:
                        print(f"    ✗ Error explorando código {j+1}: {str(e)}")
                
                # Cerrar información desplegada de la fecha
                try:
                    driver.find_element(By.TAG_NAME, "body").click()
                    time.sleep(1)
                except:
                    pass
                
            except Exception as e:
                print(f"✗ Error explorando fecha {i+1}: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación manual...")
            print("Verifica manualmente la estructura completa de la página")
            print("Y identifica dónde están los datos específicos requeridos:")
            print("- Homenajeada/o")
            print("- Código de evento")
            print("- Tipo de evento")
            print("- Fecha del evento")
            print("- Salón")
            print("- Cliente (clickeable - CELULAR y CELULAR 2)")
            print("- Tipo de Pack")
            time.sleep(300)  # Mantener abierto por 5 minutos
            driver.quit()

if __name__ == "__main__":
    explorar_estructura_completa()


