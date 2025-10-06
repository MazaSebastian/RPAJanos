#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPA PARA PROCESAMIENTO DE MÚLTIPLES EVENTOS
Script que procesa todas las fechas coral del calendario y extrae datos de todos los eventos
"""

import time
import re
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_driver():
    """Configurar y retornar el driver de Chrome"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def login(driver, wait):
    """Realizar login en el sistema origen"""
    print("=== PASO 1: LOGIN INICIAL ===")
    driver.get(os.getenv("URL_ORIGEN"))
    time.sleep(3)
    
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username_field.clear()
    username_field.send_keys(os.getenv("USER_ORIGEN"))
    print("✓ Usuario ingresado")
    
    password_field = driver.find_element(By.NAME, "password")
    password_field.clear()
    password_field.send_keys(os.getenv("PASS_ORIGEN"))
    print("✓ Contraseña ingresada")
    
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button")))
    login_button.click()
    print("✓ Botón de login presionado")
    
    wait.until(lambda driver: "login.php" not in driver.current_url)
    print("✓ Login exitoso")

def navegar_a_adicionales(driver, wait):
    """Navegar a la sección ADICIONALES"""
    print("\n=== PASO 2: ACCESO A ADICIONALES ===")
    
    open_nav_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@onclick='openNav()']")))
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
    
    main_frame = wait.until(EC.presence_of_element_located((By.ID, "mainFrame")))
    driver.switch_to.frame(main_frame)
    print("✓ Cambiado al frame principal")

def aplicar_filtros(driver, wait):
    """Aplicar filtros: DOT, CABA, 2025"""
    print("\n=== PASO 3: APLICAR FILTROS ===")
    
    salon_select = Select(wait.until(EC.presence_of_element_located((By.ID, "salon"))))
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

def obtener_todas_fechas_coral(driver):
    """Obtener todas las fechas coral (con eventos)"""
    print("\n=== PASO 4: OBTENER TODAS LAS FECHAS CORAL ===")
    
    # Buscar fechas coral
    fechas_coral = driver.find_elements(By.CSS_SELECTOR, "div.boton[style*='background: coral']")
    print(f"Fechas coral encontradas: {len(fechas_coral)}")
    
    if not fechas_coral:
        # Buscar fechas con cualquier color de fondo
        todas_fechas = driver.find_elements(By.CSS_SELECTOR, "div.boton")
        fechas_con_color = []
        
        for fecha in todas_fechas:
            if fecha.text.strip().isdigit() and fecha.is_displayed():
                style = fecha.get_attribute('style')
                if 'background:' in style and style != 'background:':
                    fechas_con_color.append(fecha)
        
        print(f"Fechas con color encontradas: {len(fechas_con_color)}")
        fechas_coral = fechas_con_color
    
    # Extraer información de las fechas
    fechas_info = []
    for i, fecha in enumerate(fechas_coral):
        fecha_texto = fecha.text.strip()
        fechas_info.append({
            'indice': i,
            'fecha': fecha_texto,
            'elemento': fecha
        })
        print(f"  Fecha {i+1}: {fecha_texto}")
    
    return fechas_info

def procesar_fecha_coral(driver, wait, fecha_info):
    """Procesar una fecha coral específica"""
    fecha_texto = fecha_info['fecha']
    print(f"\n=== PROCESANDO FECHA {fecha_texto} ===")
    
    try:
        # Hacer clic en la fecha
        fecha_elemento = fecha_info['elemento']
        fecha_elemento.click()
        time.sleep(3)
        print(f"✓ Clic en fecha {fecha_texto}")
        
        # Buscar códigos de 5 dígitos
        codigos_5_digitos = driver.find_elements(By.XPATH, "//*[text() and string-length(normalize-space(text())) = 5 and translate(text(), '0123456789', '0000000000') = '00000']")
        print(f"  Códigos de 5 dígitos encontrados: {len(codigos_5_digitos)}")
        
        if not codigos_5_digitos:
            print(f"  ✗ No se encontraron códigos para fecha {fecha_texto}")
            return None
        
        # Obtener el primer código único (todos los demás son repetidos)
        codigo_evento = codigos_5_digitos[0].text.strip()
        print(f"  ✓ Código de evento: {codigo_evento}")
        
        # Hacer clic en el primer código (cualquiera de los repetidos)
        codigos_5_digitos[0].click()
        time.sleep(5)
        print(f"  ✓ Clic en código {codigo_evento}")
        
        # Capturar URL del evento
        enlaces_evento = driver.find_elements(By.XPATH, "//a[contains(@href, 'ver_evento.php')]")
        if not enlaces_evento:
            print(f"  ✗ No se encontraron enlaces para código {codigo_evento}")
            return None
        
        url_evento = enlaces_evento[0].get_attribute('href')
        print(f"  ✓ URL capturada: {url_evento}")
        
        # Navegar al evento individual
        driver.get(url_evento)
        time.sleep(8)
        
        if "ver_evento.php" not in driver.current_url:
            print(f"  ✗ No se pudo acceder al evento {codigo_evento}")
            return None
        
        print(f"  ✓ Acceso exitoso al evento {codigo_evento}")
        
        # Extraer datos del evento
        datos_evento = extraer_datos_evento(driver, fecha_texto, codigo_evento)
        
        # Volver al calendario para procesar la siguiente fecha
        driver.back()
        time.sleep(3)
        
        # Volver al frame principal
        driver.switch_to.frame(driver.find_element(By.ID, "mainFrame"))
        time.sleep(2)
        
        return datos_evento
        
    except Exception as e:
        print(f"  ✗ Error procesando fecha {fecha_texto}: {str(e)}")
        return None

def extraer_datos_evento(driver, fecha_texto, codigo_evento):
    """Extraer datos de un evento específico"""
    print(f"  --- EXTRAYENDO DATOS DEL EVENTO {codigo_evento} ---")
    
    # Inicializar diccionario de datos
    datos_evento = {
        'fecha': fecha_texto,
        'codigo_evento': codigo_evento,
        'url': driver.current_url,
        'homenajeada': None,
        'tipo_evento': None,
        'fecha_evento': None,
        'salon': None,
        'cliente': None,
        'celular': None,
        'celular_2': None,
        'tipo_pack': None,
    }
    
    # Obtener todos los elementos de texto de la página
    todos_elementos = driver.find_elements(By.XPATH, "//*[text()]")
    elementos_relevantes = []
    
    for elem in todos_elementos:
        if elem.is_displayed() and elem.text.strip():
            texto = elem.text.strip()
            if len(texto) > 0 and len(texto) < 500:
                elementos_relevantes.append({
                    'tag': elem.tag_name,
                    'texto': texto,
                    'elemento': elem
                })
    
    # 1. HOMENAJEADA/O
    for i, elem in enumerate(elementos_relevantes):
        if "Homenajeada/o/os:" in elem['texto']:
            if i + 1 < len(elementos_relevantes):
                siguiente_elem = elementos_relevantes[i + 1]
                if siguiente_elem['texto'] and siguiente_elem['tag'] == 'td':
                    datos_evento['homenajeada'] = siguiente_elem['texto']
                    break
    
    # 2. TIPO DE EVENTO
    for i, elem in enumerate(elementos_relevantes):
        if "Tipo de Evento" in elem['texto']:
            if i + 1 < len(elementos_relevantes):
                siguiente_elem = elementos_relevantes[i + 1]
                if siguiente_elem['texto'] and siguiente_elem['tag'] == 'td':
                    datos_evento['tipo_evento'] = siguiente_elem['texto']
                    break
    
    # 3. FECHA DEL EVENTO
    for i, elem in enumerate(elementos_relevantes):
        if "Fecha del Evento" in elem['texto']:
            if i + 1 < len(elementos_relevantes):
                siguiente_elem = elementos_relevantes[i + 1]
                if siguiente_elem['texto'] and siguiente_elem['tag'] == 'td':
                    datos_evento['fecha_evento'] = siguiente_elem['texto']
                    break
    
    # 4. SALÓN
    for i, elem in enumerate(elementos_relevantes):
        if "Salon" in elem['texto'] and elem['tag'] == 'td':
            if i + 1 < len(elementos_relevantes):
                siguiente_elem = elementos_relevantes[i + 1]
                if siguiente_elem['texto'] and siguiente_elem['tag'] == 'td':
                    datos_evento['salon'] = siguiente_elem['texto']
                    break
    
    # 5. CLIENTE
    for i, elem in enumerate(elementos_relevantes):
        if "Cliente" in elem['texto'] and elem['tag'] == 'td':
            if i + 1 < len(elementos_relevantes):
                siguiente_elem = elementos_relevantes[i + 1]
                if siguiente_elem['texto'] and siguiente_elem['tag'] == 'td':
                    datos_evento['cliente'] = siguiente_elem['texto']
                    break
    
    # 6. CELULAR Y CELULAR 2
    page_html = driver.page_source
    patrones_busqueda = [
        r'5411\d{8}',
        r'54\s*11\s*\d{8}',
        r'\+54\s*11\s*\d{8}',
        r'011\s*\d{8}',
        r'11\s*\d{8}',
        r'\d{10,11}'
    ]
    
    numeros_encontrados = []
    for patron in patrones_busqueda:
        matches = re.findall(patron, page_html)
        for match in matches:
            numero_limpio = re.sub(r'[^\d+]', '', match)
            if len(numero_limpio) >= 10 and numero_limpio not in numeros_encontrados:
                numeros_encontrados.append(numero_limpio)
    
    if len(numeros_encontrados) >= 1:
        datos_evento['celular'] = numeros_encontrados[0]
    if len(numeros_encontrados) >= 2:
        datos_evento['celular_2'] = numeros_encontrados[1]
    elif len(numeros_encontrados) == 1:
        datos_evento['celular_2'] = numeros_encontrados[0]
    
    # 7. TIPO DE PACK
    for i, elem in enumerate(elementos_relevantes):
        if "Pack 1" in elem['texto'] and elem['tag'] == 'td':
            datos_evento['tipo_pack'] = elem['texto']
            break
        elif "Pack 2" in elem['texto'] and elem['tag'] == 'td':
            datos_evento['tipo_pack'] = elem['texto']
            break
    
    # Mostrar datos extraídos
    print(f"    ✓ Homenajeada/o: {datos_evento['homenajeada']}")
    print(f"    ✓ Tipo evento: {datos_evento['tipo_evento']}")
    print(f"    ✓ Fecha evento: {datos_evento['fecha_evento']}")
    print(f"    ✓ Salón: {datos_evento['salon']}")
    print(f"    ✓ Cliente: {datos_evento['cliente']}")
    print(f"    ✓ Celular: {datos_evento['celular']}")
    print(f"    ✓ Celular 2: {datos_evento['celular_2']}")
    print(f"    ✓ Tipo Pack: {datos_evento['tipo_pack']}")
    
    return datos_evento

def main():
    """Función principal del RPA para múltiples eventos"""
    print("=== RPA PARA PROCESAMIENTO DE MÚLTIPLES EVENTOS ===")
    print("Objetivo: Procesar todas las fechas coral y extraer datos de todos los eventos")
    
    driver = None
    todos_eventos = []
    
    try:
        # Configurar driver
        driver = get_driver()
        wait = WebDriverWait(driver, 20)
        
        # PASO 1: LOGIN
        login(driver, wait)
        
        # PASO 2: NAVEGAR A ADICIONALES
        navegar_a_adicionales(driver, wait)
        
        # PASO 3: APLICAR FILTROS
        aplicar_filtros(driver, wait)
        
        # PASO 4: OBTENER TODAS LAS FECHAS CORAL
        fechas_info = obtener_todas_fechas_coral(driver)
        
        if not fechas_info:
            print("✗ No se encontraron fechas coral")
            return None
        
        # PASO 5: PROCESAR CADA FECHA CORAL
        print(f"\n=== PASO 5: PROCESANDO {len(fechas_info)} FECHAS CORAL ===")
        
        for i, fecha_info in enumerate(fechas_info):
            print(f"\n--- PROCESANDO FECHA {i+1}/{len(fechas_info)} ---")
            
            datos_evento = procesar_fecha_coral(driver, wait, fecha_info)
            
            if datos_evento:
                todos_eventos.append(datos_evento)
                print(f"✓ Evento procesado exitosamente")
            else:
                print(f"✗ Error procesando evento")
            
            # Pausa entre eventos para evitar sobrecarga
            time.sleep(2)
        
        # Mostrar resumen final
        print(f"\n=== RESUMEN FINAL ===")
        print(f"Total de fechas coral encontradas: {len(fechas_info)}")
        print(f"Total de eventos procesados exitosamente: {len(todos_eventos)}")
        print(f"Eventos con errores: {len(fechas_info) - len(todos_eventos)}")
        
        if todos_eventos:
            # Crear DataFrame con todos los eventos
            df = pd.DataFrame(todos_eventos)
            print(f"\n=== DATAFRAME CON TODOS LOS EVENTOS ===")
            print(df.to_string())
            
            # Guardar en CSV
            df.to_csv('todos_los_eventos_extraidos.csv', index=False)
            print(f"\n✓ Todos los eventos guardados en 'todos_los_eventos_extraidos.csv'")
            
            # Mostrar estadísticas
            print(f"\n=== ESTADÍSTICAS ===")
            print(f"Eventos únicos: {len(todos_eventos)}")
            print(f"Fechas diferentes: {len(set([e['fecha'] for e in todos_eventos]))}")
            print(f"Códigos únicos: {len(set([e['codigo_evento'] for e in todos_eventos]))}")
            
            return todos_eventos
        else:
            print("✗ No se procesaron eventos exitosamente")
            return None
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return None
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación manual...")
            time.sleep(300)  # Mantener abierto por 5 minutos
            driver.quit()

if __name__ == "__main__":
    resultado = main()
    if resultado:
        print(f"\n=== RESULTADO FINAL ===")
        print(f"Total de eventos procesados: {len(resultado)}")
        for i, evento in enumerate(resultado):
            print(f"  Evento {i+1}: {evento['codigo_evento']} - {evento['fecha']} - {evento['cliente']}")
    else:
        print(f"\n=== RESULTADO FINAL ===")
        print(f"No se pudieron procesar los eventos")


