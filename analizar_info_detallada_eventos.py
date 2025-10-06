#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analizar detalladamente la información individual de cada evento
- Hacer clic en fechas coral
- Hacer clic en códigos de 5 dígitos
- Analizar exhaustivamente toda la información disponible
"""

import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def analizar_info_detallada_eventos():
    """Analizar detalladamente la información individual de cada evento"""
    
    print("=== ANÁLISIS DETALLADO DE INFORMACIÓN DE EVENTOS ===")
    print("Analizando exhaustivamente toda la información disponible...")
    
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
        
        # PASO 5: Analizar información detallada de eventos
        print(f"\n=== PASO 5: ANÁLISIS DETALLADO DE INFORMACIÓN ===")
        
        eventos_analizados = []
        
        for i, fecha_coral in enumerate(fechas_coral[:2]):  # Analizar las primeras 2 fechas
            try:
                fecha_texto = fecha_coral.text.strip()
                print(f"\n--- ANÁLISIS DETALLADO FECHA {i+1}: {fecha_texto} ---")
                
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
                        print(f"\n    === ANÁLISIS CÓDIGO {j+1}: {codigo_texto} ===")
                        
                        # Hacer clic en el código
                        print(f"    ✓ Haciendo clic en código {codigo_texto}...")
                        codigo_elem.click()
                        time.sleep(5)  # Esperar a que cargue la información detallada
                        
                        # ANÁLISIS EXHAUSTIVO DE INFORMACIÓN
                        print(f"    ✓ Analizando información detallada...")
                        
                        informacion_evento = {
                            'fecha': fecha_texto,
                            'codigo': codigo_texto,
                            'campos_encontrados': {},
                            'estructura_html': {},
                            'datos_especificos': {}
                        }
                        
                        # 1. ANÁLISIS DE INPUTS
                        print(f"    --- ANÁLISIS DE INPUTS ---")
                        inputs = driver.find_elements(By.TAG_NAME, "input")
                        inputs_info = []
                        for input_elem in inputs:
                            if input_elem.is_displayed():
                                tipo = input_elem.get_attribute('type')
                                nombre = input_elem.get_attribute('name')
                                valor = input_elem.get_attribute('value')
                                placeholder = input_elem.get_attribute('placeholder')
                                id_elem = input_elem.get_attribute('id')
                                
                                if valor or nombre or placeholder:
                                    input_data = {
                                        'tipo': tipo,
                                        'nombre': nombre,
                                        'valor': valor,
                                        'placeholder': placeholder,
                                        'id': id_elem
                                    }
                                    inputs_info.append(input_data)
                                    print(f"      ✓ Input: {input_data}")
                        
                        informacion_evento['campos_encontrados']['inputs'] = inputs_info
                        
                        # 2. ANÁLISIS DE TEXTAREAS
                        print(f"    --- ANÁLISIS DE TEXTAREAS ---")
                        textareas = driver.find_elements(By.TAG_NAME, "textarea")
                        textareas_info = []
                        for textarea_elem in textareas:
                            if textarea_elem.is_displayed():
                                nombre = textarea_elem.get_attribute('name')
                                valor = textarea_elem.get_attribute('value')
                                placeholder = textarea_elem.get_attribute('placeholder')
                                id_elem = textarea_elem.get_attribute('id')
                                
                                if valor or nombre or placeholder:
                                    textarea_data = {
                                        'nombre': nombre,
                                        'valor': valor,
                                        'placeholder': placeholder,
                                        'id': id_elem
                                    }
                                    textareas_info.append(textarea_data)
                                    print(f"      ✓ Textarea: {textarea_data}")
                        
                        informacion_evento['campos_encontrados']['textareas'] = textareas_info
                        
                        # 3. ANÁLISIS DE SELECTS
                        print(f"    --- ANÁLISIS DE SELECTS ---")
                        selects = driver.find_elements(By.TAG_NAME, "select")
                        selects_info = []
                        for select_elem in selects:
                            if select_elem.is_displayed():
                                nombre = select_elem.get_attribute('name')
                                id_elem = select_elem.get_attribute('id')
                                opciones = []
                                
                                try:
                                    opciones_elem = select_elem.find_elements(By.TAG_NAME, "option")
                                    for opcion in opciones_elem:
                                        if opcion.is_displayed():
                                            opciones.append({
                                                'texto': opcion.text,
                                                'valor': opcion.get_attribute('value'),
                                                'seleccionado': opcion.is_selected()
                                            })
                                except:
                                    pass
                                
                                select_data = {
                                    'nombre': nombre,
                                    'id': id_elem,
                                    'opciones': opciones
                                }
                                selects_info.append(select_data)
                                print(f"      ✓ Select: {select_data}")
                        
                        informacion_evento['campos_encontrados']['selects'] = selects_info
                        
                        # 4. ANÁLISIS DE DIVS CON INFORMACIÓN
                        print(f"    --- ANÁLISIS DE DIVS CON INFORMACIÓN ---")
                        divs_info = []
                        divs = driver.find_elements(By.TAG_NAME, "div")
                        for div in divs:
                            if div.is_displayed() and div.text.strip():
                                texto = div.text.strip()
                                if len(texto) > 0 and len(texto) < 500:  # Filtrar texto relevante
                                    clase = div.get_attribute('class')
                                    id_elem = div.get_attribute('id')
                                    
                                    # Buscar patrones específicos de información
                                    if any(palabra in texto.lower() for palabra in ['cliente', 'evento', 'fecha', 'hora', 'salon', 'zona', 'tipo', 'agasajado', 'contacto', 'telefono', 'email', 'direccion', 'observaciones', 'notas', 'descripcion', 'detalles']):
                                        div_data = {
                                            'texto': texto,
                                            'clase': clase,
                                            'id': id_elem
                                        }
                                        divs_info.append(div_data)
                                        print(f"      ✓ Div relevante: {texto[:100]}...")
                        
                        informacion_evento['campos_encontrados']['divs'] = divs_info
                        
                        # 5. ANÁLISIS DE TABLAS
                        print(f"    --- ANÁLISIS DE TABLAS ---")
                        tablas = driver.find_elements(By.TAG_NAME, "table")
                        tablas_info = []
                        for tabla in tablas:
                            if tabla.is_displayed():
                                filas = tabla.find_elements(By.TAG_NAME, "tr")
                                tabla_data = {
                                    'filas': len(filas),
                                    'contenido': []
                                }
                                
                                for fila in filas:
                                    celdas = fila.find_elements(By.TAG_NAME, "td")
                                    fila_data = []
                                    for celda in celdas:
                                        if celda.is_displayed() and celda.text.strip():
                                            fila_data.append(celda.text.strip())
                                    
                                    if fila_data:
                                        tabla_data['contenido'].append(fila_data)
                                
                                if tabla_data['contenido']:
                                    tablas_info.append(tabla_data)
                                    print(f"      ✓ Tabla: {len(tabla_data['contenido'])} filas con datos")
                        
                        informacion_evento['campos_encontrados']['tablas'] = tablas_info
                        
                        # 6. ANÁLISIS DE SPANS Y LABELS
                        print(f"    --- ANÁLISIS DE SPANS Y LABELS ---")
                        spans = driver.find_elements(By.TAG_NAME, "span")
                        labels = driver.find_elements(By.TAG_NAME, "label")
                        
                        elementos_texto = []
                        for elem in spans + labels:
                            if elem.is_displayed() and elem.text.strip():
                                texto = elem.text.strip()
                                if len(texto) > 0 and len(texto) < 200:
                                    elementos_texto.append({
                                        'tag': elem.tag_name,
                                        'texto': texto,
                                        'clase': elem.get_attribute('class'),
                                        'id': elem.get_attribute('id')
                                    })
                                    print(f"      ✓ {elem.tag_name}: {texto[:50]}...")
                        
                        informacion_evento['campos_encontrados']['elementos_texto'] = elementos_texto
                        
                        # 7. BÚSQUEDA DE PATRONES ESPECÍFICOS
                        print(f"    --- BÚSQUEDA DE PATRONES ESPECÍFICOS ---")
                        patrones_buscados = {
                            'fecha': r'\d{1,2}/\d{1,2}/\d{4}',
                            'hora': r'\d{1,2}:\d{2}',
                            'telefono': r'\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}',
                            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                            'codigo': r'\d{5}',
                            'precio': r'\$\d+',
                            'numero': r'\d+'
                        }
                        
                        patrones_encontrados = {}
                        for patron_nombre, patron_regex in patrones_buscados.items():
                            elementos_con_patron = driver.find_elements(By.XPATH, f"//*[text()[matches(., '{patron_regex}')]]")
                            if elementos_con_patron:
                                patrones_encontrados[patron_nombre] = [elem.text for elem in elementos_con_patron if elem.is_displayed()]
                                print(f"      ✓ {patron_nombre}: {patrones_encontrados[patron_nombre]}")
                        
                        informacion_evento['patrones_encontrados'] = patrones_encontrados
                        
                        # 8. RESUMEN DE INFORMACIÓN DISPONIBLE
                        print(f"    --- RESUMEN DE INFORMACIÓN DISPONIBLE ---")
                        total_campos = (
                            len(inputs_info) + 
                            len(textareas_info) + 
                            len(selects_info) + 
                            len(divs_info) + 
                            len(tablas_info) + 
                            len(elementos_texto)
                        )
                        
                        print(f"    ✓ Total de campos encontrados: {total_campos}")
                        print(f"    ✓ Inputs: {len(inputs_info)}")
                        print(f"    ✓ Textareas: {len(textareas_info)}")
                        print(f"    ✓ Selects: {len(selects_info)}")
                        print(f"    ✓ Divs relevantes: {len(divs_info)}")
                        print(f"    ✓ Tablas: {len(tablas_info)}")
                        print(f"    ✓ Elementos de texto: {len(elementos_texto)}")
                        print(f"    ✓ Patrones encontrados: {len(patrones_encontrados)}")
                        
                        informacion_evento['resumen'] = {
                            'total_campos': total_campos,
                            'inputs': len(inputs_info),
                            'textareas': len(textareas_info),
                            'selects': len(selects_info),
                            'divs': len(divs_info),
                            'tablas': len(tablas_info),
                            'elementos_texto': len(elementos_texto),
                            'patrones': len(patrones_encontrados)
                        }
                        
                        eventos_analizados.append(informacion_evento)
                        
                        # Volver atrás
                        try:
                            driver.find_element(By.TAG_NAME, "body").click()
                            time.sleep(1)
                        except:
                            pass
                        
                    except Exception as e:
                        print(f"    ✗ Error analizando código {j+1}: {str(e)}")
                
                # Cerrar información desplegada de la fecha
                try:
                    driver.find_element(By.TAG_NAME, "body").click()
                    time.sleep(1)
                except:
                    pass
                
            except Exception as e:
                print(f"✗ Error analizando fecha {i+1}: {str(e)}")
        
        # PASO 6: Mostrar resumen final
        print(f"\n=== RESUMEN FINAL DE INFORMACIÓN DISPONIBLE ===")
        print(f"Eventos analizados: {len(eventos_analizados)}")
        
        for i, evento in enumerate(eventos_analizados):
            print(f"\n--- EVENTO {i+1}: Fecha {evento['fecha']}, Código {evento['codigo']} ---")
            resumen = evento['resumen']
            print(f"  Total de campos: {resumen['total_campos']}")
            print(f"  Inputs: {resumen['inputs']}")
            print(f"  Textareas: {resumen['textareas']}")
            print(f"  Selects: {resumen['selects']}")
            print(f"  Divs relevantes: {resumen['divs']}")
            print(f"  Tablas: {resumen['tablas']}")
            print(f"  Elementos de texto: {resumen['elementos_texto']}")
            print(f"  Patrones encontrados: {resumen['patrones']}")
            
            # Mostrar algunos ejemplos de información
            if evento['campos_encontrados']['divs']:
                print(f"  Ejemplos de divs:")
                for div in evento['campos_encontrados']['divs'][:3]:
                    print(f"    - {div['texto'][:100]}...")
            
            if evento['patrones_encontrados']:
                print(f"  Patrones específicos:")
                for patron, valores in evento['patrones_encontrados'].items():
                    print(f"    - {patron}: {valores}")
        
        return len(eventos_analizados) > 0
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación manual...")
            print("Verifica manualmente la información detallada disponible")
            time.sleep(180)  # Mantener abierto por 3 minutos
            driver.quit()

if __name__ == "__main__":
    analizar_info_detallada_eventos()


