#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script corregido para extraer datos específicos del evento con mapeo correcto
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def verificar_sesion_activa(driver):
    """Verificar si la sesión está activa o ha vencido"""
    try:
        sesion_vencida_indicators = [
            "Sesion vencida", "Sesión vencida", "Sesion expirada", "Sesión expirada",
            "Volve a ingresar", "Vuelve a ingresar", "login.php"
        ]
        
        page_source = driver.page_source.lower()
        current_url = driver.current_url.lower()
        
        for indicator in sesion_vencida_indicators:
            if indicator.lower() in page_source or indicator.lower() in current_url:
                print(f"⚠ Sesión vencida detectada: {indicator}")
                return False
        
        if "login.php" in current_url:
            print("⚠ Redirigido a página de login - sesión vencida")
            return False
            
        print("✓ Sesión activa")
        return True
        
    except Exception as e:
        print(f"✗ Error verificando sesión: {str(e)}")
        return False

def reloguear_automaticamente(driver):
    """Reloguear automáticamente cuando la sesión ha vencido"""
    try:
        print("\n=== RELOGUEO AUTOMÁTICO ===")
        driver.get("https://tecnica.janosgroup.com/login.php")
        time.sleep(3)
        
        username_field = driver.find_element(By.NAME, "username")
        username_field.clear()
        username_field.send_keys("sebastian_maza")
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys("Janos2025+!")
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button.button")
        login_button.click()
        
        wait = WebDriverWait(driver, 20)
        wait.until(lambda driver: "login.php" not in driver.current_url)
        print("✓ Relogueo exitoso")
        return True
        
    except Exception as e:
        print(f"✗ Error en relogueo: {str(e)}")
        return False

def extraer_datos_corregidos(driver, url_evento):
    """Extraer datos específicos del evento con mapeo correcto"""
    try:
        print(f"\n=== EXTRAYENDO DATOS CORREGIDOS DEL EVENTO ===")
        print(f"URL: {url_evento}")
        
        # Verificar sesión
        if not verificar_sesion_activa(driver):
            if not reloguear_automaticamente(driver):
                return None
        
        # Navegar al evento
        driver.get(url_evento)
        time.sleep(5)
        
        if not verificar_sesion_activa(driver):
            print("⚠ Sesión vencida después de navegar al evento")
            if not reloguear_automaticamente(driver):
                return None
            driver.get(url_evento)
            time.sleep(5)
        
        current_url = driver.current_url
        titulo = driver.title
        print(f"✓ URL actual: {current_url}")
        print(f"✓ Título: {titulo}")
        
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
        
        # Mostrar todos los elementos para análisis
        print(f"\n=== ANÁLISIS COMPLETO DE ELEMENTOS ===")
        for k, elem in enumerate(elementos_relevantes):
            print(f"  {k+1}. {elem['tag']}: {elem['texto']}")
        
        # Inicializar datos del evento
        datos_evento = {
            'url': current_url,
            'titulo': titulo,
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
        
        print(f"\n=== BÚSQUEDA ESPECÍFICA DE DATOS CORREGIDOS ===")
        
        # 1. HOMENAJEADA/O (ya está correcto)
        print(f"--- BUSCANDO HOMENAJEADA/O ---")
        for elem in elementos_relevantes:
            if 'homenajeada' in elem['texto'].lower() or 'homenajeado' in elem['texto'].lower():
                # Buscar el valor siguiente
                indice = elementos_relevantes.index(elem)
                if indice + 1 < len(elementos_relevantes):
                    siguiente_elem = elementos_relevantes[indice + 1]
                    if siguiente_elem['texto'] and len(siguiente_elem['texto']) > 1:
                        datos_evento['homenajeada'] = siguiente_elem['texto']
                        print(f"✓ Homenajeada/o: {siguiente_elem['texto']}")
                        break
        
        # 2. CÓDIGO DE EVENTO (ya está correcto)
        print(f"--- BUSCANDO CÓDIGO DE EVENTO ---")
        for elem in elementos_relevantes:
            if 'codigo' in elem['texto'].lower() and 'evento' in elem['texto'].lower():
                # Buscar el valor siguiente
                indice = elementos_relevantes.index(elem)
                if indice + 1 < len(elementos_relevantes):
                    siguiente_elem = elementos_relevantes[indice + 1]
                    if siguiente_elem['texto'] and siguiente_elem['texto'].isdigit():
                        datos_evento['codigo_evento'] = siguiente_elem['texto']
                        print(f"✓ Código de evento: {siguiente_elem['texto']}")
                        break
        
        # 3. TIPO DE EVENTO (CORREGIR: buscar "15", "cumpleaños", "boda", "corporativo")
        print(f"--- BUSCANDO TIPO DE EVENTO (15, cumpleaños, boda, corporativo) ---")
        for elem in elementos_relevantes:
            if 'tipo' in elem['texto'].lower() and 'evento' in elem['texto'].lower():
                # Buscar el valor siguiente
                indice = elementos_relevantes.index(elem)
                if indice + 1 < len(elementos_relevantes):
                    siguiente_elem = elementos_relevantes[indice + 1]
                    if siguiente_elem['texto']:
                        datos_evento['tipo_evento'] = siguiente_elem['texto']
                        print(f"✓ Tipo de evento: {siguiente_elem['texto']}")
                        break
        
        # 4. FECHA DEL EVENTO (CORREGIR: buscar "Fecha del Evento", no "Fecha de Alta")
        print(f"--- BUSCANDO FECHA DEL EVENTO (no fecha de alta) ---")
        for elem in elementos_relevantes:
            if 'fecha del evento' in elem['texto'].lower():
                # Buscar el valor siguiente
                indice = elementos_relevantes.index(elem)
                if indice + 1 < len(elementos_relevantes):
                    siguiente_elem = elementos_relevantes[indice + 1]
                    if siguiente_elem['texto']:
                        datos_evento['fecha_evento'] = siguiente_elem['texto']
                        print(f"✓ Fecha del evento: {siguiente_elem['texto']}")
                        break
        
        # 5. SALÓN (ya está correcto)
        print(f"--- BUSCANDO SALÓN ---")
        for elem in elementos_relevantes:
            if 'salon' in elem['texto'].lower() or 'salón' in elem['texto'].lower():
                # Buscar el valor siguiente
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
                    time.sleep(3)  # Esperar a que se despliegue la información
                    
                    # Buscar CELULAR y CELULAR 2 en la información desplegada
                    print(f"--- BUSCANDO CELULAR Y CELULAR 2 ---")
                    
                    # Buscar elementos con información de contacto
                    elementos_contacto = driver.find_elements(By.XPATH, "//*[text()]")
                    celulares_encontrados = []
                    
                    for elem_contacto in elementos_contacto:
                        if elem_contacto.is_displayed() and elem_contacto.text.strip():
                            texto_contacto = elem_contacto.text.strip()
                            # Buscar números de teléfono
                            if any(char.isdigit() for char in texto_contacto):
                                if any(palabra in texto_contacto.lower() for palabra in ['celular', 'telefono', 'teléfono', 'tel', 'móvil', 'movil']):
                                    celulares_encontrados.append(texto_contacto)
                                    print(f"  ✓ Celular encontrado: {texto_contacto}")
                    
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
        
        # 7. TIPO DE PACK (CORREGIR: buscar "Pack 1", "Pack 2", etc.)
        print(f"--- BUSCANDO TIPO DE PACK (Pack 1, Pack 2, etc.) ---")
        for elem in elementos_relevantes:
            if 'pack' in elem['texto'].lower():
                datos_evento['tipo_pack'] = elem['texto']
                print(f"✓ Tipo de Pack: {elem['texto']}")
                break
        
        # Mostrar resumen final
        print(f"\n=== RESUMEN FINAL DE DATOS CORREGIDOS ===")
        datos_encontrados = 0
        for campo, valor in datos_evento.items():
            if valor and campo not in ['url', 'titulo']:
                datos_encontrados += 1
                print(f"✓ {campo}: {valor}")
            elif not valor and campo not in ['url', 'titulo']:
                print(f"✗ {campo}: No encontrado")
        
        print(f"\nTotal de datos encontrados: {datos_encontrados}/7")
        
        return datos_evento
        
    except Exception as e:
        print(f"✗ Error extrayendo datos corregidos: {str(e)}")
        return None

def extraer_datos_corregidos_completo():
    """Función principal con extracción corregida"""
    
    print("=== EXTRACCIÓN DE DATOS CORREGIDOS ===")
    print("Correcciones aplicadas:")
    print("- Tipo de evento: 15, cumpleaños, boda, corporativo")
    print("- Fecha del evento: Fecha del Evento (no fecha de alta)")
    print("- Tipo de Pack: Pack 1, Pack 2, etc.")
    print("- Cliente clickeable: CELULAR y CELULAR 2")
    
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
        
        # Login inicial
        print("\n=== LOGIN INICIAL ===")
        driver.get("https://tecnica.janosgroup.com/login.php")
        time.sleep(3)
        
        username_field = driver.find_element(By.NAME, "username")
        username_field.clear()
        username_field.send_keys("sebastian_maza")
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys("Janos2025+!")
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button.button")
        login_button.click()
        
        wait.until(lambda driver: "login.php" not in driver.current_url)
        print("✓ Login exitoso")
        
        # Navegar directamente al evento
        url_evento = "https://janosgroup.com/ver_evento.php?id=33069"
        print(f"\n=== NAVEGACIÓN DIRECTA AL EVENTO ===")
        print(f"URL: {url_evento}")
        
        # Extraer datos corregidos
        datos_evento = extraer_datos_corregidos(driver, url_evento)
        
        if datos_evento:
            print(f"\n=== EXTRACCIÓN CORREGIDA EXITOSA ===")
            return datos_evento
        else:
            print(f"\n=== EXTRACCIÓN CORREGIDA FALLIDA ===")
            return None
        
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
    resultado = extraer_datos_corregidos_completo()
    if resultado:
        print(f"\n=== RESULTADO FINAL CORREGIDO ===")
        print(f"Datos extraídos exitosamente:")
        for campo, valor in resultado.items():
            print(f"  {campo}: {valor}")
    else:
        print(f"\n=== RESULTADO FINAL CORREGIDO ===")
        print(f"No se pudieron extraer los datos requeridos")


