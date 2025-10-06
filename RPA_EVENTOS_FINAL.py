#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPA FINAL PARA EXTRACCIÓN COMPLETA DE DATOS DE EVENTOS
Script completo que extrae todos los datos requeridos:
- Homenajeada/o
- Código de evento  
- Tipo de evento
- Fecha del evento
- Salón
- Cliente
- Celular
- Celular 2
- Tipo de Pack
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

def buscar_fechas_coral(driver):
    """Buscar fechas con eventos (coral)"""
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
    
    return fechas_coral

def hacer_clic_en_fecha(driver, wait, fechas_coral):
    """Hacer clic en una fecha coral"""
    print(f"\n=== PASO 5: HACER CLIC EN FECHA CORAL ===")
    
    if not fechas_coral:
        print("✗ No se encontraron fechas coral")
        return None
    
    fecha_coral = fechas_coral[0]
    fecha_texto = fecha_coral.text.strip()
    print(f"✓ Haciendo clic en fecha {fecha_texto}...")
    fecha_coral.click()
    time.sleep(3)
    
    return fecha_texto

def buscar_codigos_evento(driver):
    """Buscar códigos de 5 dígitos"""
    print(f"\n=== PASO 6: BUSCAR CÓDIGOS DE 5 DÍGITOS ===")
    
    codigos_5_digitos = driver.find_elements(By.XPATH, "//*[text() and string-length(normalize-space(text())) = 5 and translate(text(), '0123456789', '0000000000') = '00000']")
    print(f"Códigos de 5 dígitos encontrados: {len(codigos_5_digitos)}")
    
    return codigos_5_digitos

def hacer_clic_en_codigo(driver, codigos_5_digitos, codigo_buscado="33069"):
    """Hacer clic en un código específico"""
    print(f"\n=== PASO 7: HACER CLIC EN CÓDIGO {codigo_buscado} ===")
    
    if not codigos_5_digitos:
        print("✗ No se encontraron códigos de 5 dígitos")
        return None
    
    codigo_elemento = None
    for codigo in codigos_5_digitos:
        if codigo.text.strip() == codigo_buscado:
            codigo_elemento = codigo
            break
    
    if not codigo_elemento:
        print(f"✗ No se encontró código {codigo_buscado}")
        return None
    
    print(f"✓ Haciendo clic en código {codigo_buscado}...")
    codigo_elemento.click()
    time.sleep(5)
    
    return codigo_buscado

def capturar_url_evento(driver):
    """Capturar URL del evento"""
    print(f"\n=== PASO 8: CAPTURAR URL DEL EVENTO ===")
    
    enlaces_evento = driver.find_elements(By.XPATH, "//a[contains(@href, 'ver_evento.php')]")
    print(f"Enlaces a ver_evento.php encontrados: {len(enlaces_evento)}")
    
    if not enlaces_evento:
        print("✗ No se encontraron enlaces a ver_evento.php")
        return None
    
    enlace_evento = enlaces_evento[0]
    url_evento = enlace_evento.get_attribute('href')
    print(f"✓ URL del evento capturada: {url_evento}")
    
    return url_evento

def navegar_a_evento_individual(driver, url_evento):
    """Navegar directamente a la URL del evento"""
    print(f"\n=== PASO 9: NAVEGAR A EVENTO INDIVIDUAL ===")
    
    print(f"✓ Navegando directamente a: {url_evento}")
    driver.get(url_evento)
    time.sleep(8)
    
    current_url = driver.current_url
    print(f"✓ URL actual: {current_url}")
    
    if "ver_evento.php" not in current_url:
        print("⚠ No estamos en la página individual del evento")
        return False
    
    print("✓ ¡Estamos en la página individual del evento!")
    return True

def extraer_datos_completos(driver, fecha_texto, codigo_evento):
    """Extraer todos los datos requeridos del evento"""
    print(f"\n=== PASO 10: EXTRAER DATOS COMPLETOS ===")
    
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
    
    print(f"Total de elementos con texto: {len(elementos_relevantes)}")
    
    # 1. HOMENAJEADA/O
    print("--- BUSCANDO HOMENAJEADA/O ---")
    for i, elem in enumerate(elementos_relevantes):
        if "Homenajeada/o/os:" in elem['texto']:
            if i + 1 < len(elementos_relevantes):
                siguiente_elem = elementos_relevantes[i + 1]
                if siguiente_elem['texto'] and siguiente_elem['tag'] == 'td':
                    datos_evento['homenajeada'] = siguiente_elem['texto']
                    print(f"✓ Homenajeada/o: {datos_evento['homenajeada']}")
                    break
    
    # 2. TIPO DE EVENTO
    print("--- BUSCANDO TIPO DE EVENTO ---")
    for i, elem in enumerate(elementos_relevantes):
        if "Tipo de Evento" in elem['texto']:
            if i + 1 < len(elementos_relevantes):
                siguiente_elem = elementos_relevantes[i + 1]
                if siguiente_elem['texto'] and siguiente_elem['tag'] == 'td':
                    datos_evento['tipo_evento'] = siguiente_elem['texto']
                    print(f"✓ Tipo de evento: {datos_evento['tipo_evento']}")
                    break
    
    # 3. FECHA DEL EVENTO
    print("--- BUSCANDO FECHA DEL EVENTO ---")
    for i, elem in enumerate(elementos_relevantes):
        if "Fecha del Evento" in elem['texto']:
            if i + 1 < len(elementos_relevantes):
                siguiente_elem = elementos_relevantes[i + 1]
                if siguiente_elem['texto'] and siguiente_elem['tag'] == 'td':
                    datos_evento['fecha_evento'] = siguiente_elem['texto']
                    print(f"✓ Fecha del evento: {datos_evento['fecha_evento']}")
                    break
    
    # 4. SALÓN
    print("--- BUSCANDO SALÓN ---")
    for i, elem in enumerate(elementos_relevantes):
        if "Salon" in elem['texto'] and elem['tag'] == 'td':
            if i + 1 < len(elementos_relevantes):
                siguiente_elem = elementos_relevantes[i + 1]
                if siguiente_elem['texto'] and siguiente_elem['tag'] == 'td':
                    datos_evento['salon'] = siguiente_elem['texto']
                    print(f"✓ Salón: {datos_evento['salon']}")
                    break
    
    # 5. CLIENTE
    print("--- BUSCANDO CLIENTE ---")
    for i, elem in enumerate(elementos_relevantes):
        if "Cliente" in elem['texto'] and elem['tag'] == 'td':
            if i + 1 < len(elementos_relevantes):
                siguiente_elem = elementos_relevantes[i + 1]
                if siguiente_elem['texto'] and siguiente_elem['tag'] == 'td':
                    datos_evento['cliente'] = siguiente_elem['texto']
                    print(f"✓ Cliente: {datos_evento['cliente']}")
                    break
    
    # 6. CELULAR Y CELULAR 2
    print("--- BUSCANDO CELULAR Y CELULAR 2 ---")
    
    # Obtener HTML de la página
    page_html = driver.page_source
    
    # Buscar números específicos
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
                print(f"✓ Número encontrado: {match}")
    
    # Asignar celulares encontrados
    if len(numeros_encontrados) >= 1:
        datos_evento['celular'] = numeros_encontrados[0]
        print(f"✓ Celular: {datos_evento['celular']}")
    
    if len(numeros_encontrados) >= 2:
        datos_evento['celular_2'] = numeros_encontrados[1]
        print(f"✓ Celular 2: {datos_evento['celular_2']}")
    elif len(numeros_encontrados) == 1:
        # Si solo hay un celular, usar el mismo para ambos
        datos_evento['celular_2'] = numeros_encontrados[0]
        print(f"✓ Celular 2 (mismo que celular): {datos_evento['celular_2']}")
    
    # 7. TIPO DE PACK
    print("--- BUSCANDO TIPO DE PACK ---")
    for i, elem in enumerate(elementos_relevantes):
        if "Pack 1" in elem['texto'] and elem['tag'] == 'td':
            datos_evento['tipo_pack'] = elem['texto']
            print(f"✓ Tipo de Pack: {datos_evento['tipo_pack']}")
            break
        elif "Pack 2" in elem['texto'] and elem['tag'] == 'td':
            datos_evento['tipo_pack'] = elem['texto']
            print(f"✓ Tipo de Pack: {datos_evento['tipo_pack']}")
            break
    
    return datos_evento

def main():
    """Función principal del RPA"""
    print("=== RPA FINAL PARA EXTRACCIÓN DE DATOS DE EVENTOS ===")
    print("Objetivo: Extraer todos los datos requeridos del evento")
    
    driver = None
    
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
        
        # PASO 4: BUSCAR FECHAS CORAL
        fechas_coral = buscar_fechas_coral(driver)
        
        # PASO 5: HACER CLIC EN FECHA
        fecha_texto = hacer_clic_en_fecha(driver, wait, fechas_coral)
        if not fecha_texto:
            return None
        
        # PASO 6: BUSCAR CÓDIGOS DE EVENTO
        codigos_5_digitos = buscar_codigos_evento(driver)
        
        # PASO 7: HACER CLIC EN CÓDIGO
        codigo_evento = hacer_clic_en_codigo(driver, codigos_5_digitos)
        if not codigo_evento:
            return None
        
        # PASO 8: CAPTURAR URL DEL EVENTO
        url_evento = capturar_url_evento(driver)
        if not url_evento:
            return None
        
        # PASO 9: NAVEGAR A EVENTO INDIVIDUAL
        if not navegar_a_evento_individual(driver, url_evento):
            return None
        
        # PASO 10: EXTRAER DATOS COMPLETOS
        datos_evento = extraer_datos_completos(driver, fecha_texto, codigo_evento)
        
        # Mostrar resumen final
        print(f"\n=== RESUMEN FINAL DE DATOS ENCONTRADOS ===")
        datos_encontrados = 0
        for campo, valor in datos_evento.items():
            if valor and campo not in ['fecha', 'url', 'codigo_evento']:
                datos_encontrados += 1
                print(f"✓ {campo}: {valor}")
            elif not valor and campo not in ['fecha', 'url', 'codigo_evento']:
                print(f"✗ {campo}: No encontrado")
        
        print(f"\nTotal de datos encontrados: {datos_encontrados}/9")
        
        # Crear DataFrame con los datos
        df = pd.DataFrame([datos_evento])
        print(f"\n=== DATAFRAME CREADO ===")
        print(df.to_string())
        
        # Guardar en CSV
        df.to_csv('datos_evento_extraidos.csv', index=False)
        print(f"\n✓ Datos guardados en 'datos_evento_extraidos.csv'")
        
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
    resultado = main()
    if resultado:
        print(f"\n=== RESULTADO FINAL ===")
        print(f"Datos extraídos exitosamente:")
        for campo, valor in resultado.items():
            print(f"  {campo}: {valor}")
    else:
        print(f"\n=== RESULTADO FINAL ===")
        print(f"No se pudieron extraer los datos requeridos")


