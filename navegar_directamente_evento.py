#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para navegar directamente a la página individual del evento
y extraer todos los datos específicos requeridos
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def navegar_directamente_evento():
    """Navegar directamente a la página individual del evento"""
    
    print("=== NAVEGACIÓN DIRECTA A PÁGINA INDIVIDUAL DEL EVENTO ===")
    print("Extrayendo datos específicos:")
    print("- Homenajeada/o")
    print("- Código de evento")
    print("- Tipo de evento")
    print("- Fecha del evento")
    print("- Salón")
    print("- Cliente (clickeable - CELULAR y CELULAR 2)")
    print("- Tipo de Pack")
    
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
        
        # PASO 2: Navegar directamente a la página del evento
        print("\n=== PASO 2: NAVEGACIÓN DIRECTA AL EVENTO ===")
        
        # URL del evento que encontramos anteriormente
        url_evento = "https://janosgroup.com/ver_evento.php?id=33069"
        print(f"✓ Navegando directamente a: {url_evento}")
        
        driver.get(url_evento)
        time.sleep(5)  # Esperar a que cargue la página
        
        # Verificar que cargó correctamente
        current_url = driver.current_url
        titulo = driver.title
        print(f"✓ URL actual: {current_url}")
        print(f"✓ Título de la página: {titulo}")
        
        # PASO 3: Análisis completo de la página del evento
        print(f"\n=== PASO 3: ANÁLISIS COMPLETO DE LA PÁGINA DEL EVENTO ===")
        
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
        
        # 1. ANÁLISIS DE TODOS LOS ELEMENTOS VISIBLES
        print(f"--- ANÁLISIS DE TODOS LOS ELEMENTOS VISIBLES ---")
        
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
        
        print(f"Total de elementos con texto: {len(elementos_relevantes)}")
        
        # Mostrar los primeros 20 elementos
        print(f"Primeros 20 elementos encontrados:")
        for k, elem in enumerate(elementos_relevantes[:20]):
            print(f"  {k+1}. {elem['tag']}: {elem['texto'][:100]}...")
        
        # 2. BUSCAR DATOS ESPECÍFICOS
        print(f"\n--- BÚSQUEDA DE DATOS ESPECÍFICOS ---")
        
        # BUSCAR HOMENAJEADA/O
        print(f"--- BUSCANDO HOMENAJEADA/O ---")
        homenajeada_selectors = [
            "//*[contains(text(), 'homenajeada') or contains(text(), 'homenajeado')]",
            "//*[contains(text(), 'Homenajeada') or contains(text(), 'Homenajeado')]",
            "//*[contains(text(), 'HOMENAJEADA') or contains(text(), 'HOMENAJEADO')]"
        ]
        
        for selector in homenajeada_selectors:
            try:
                elementos = driver.find_elements(By.XPATH, selector)
                for elem in elementos:
                    if elem.is_displayed() and elem.text.strip():
                        texto = elem.text.strip()
                        if len(texto) > 0 and len(texto) < 200:
                            datos_evento['homenajeada'] = texto
                            print(f"✓ Homenajeada/o: {texto}")
                            break
                if datos_evento['homenajeada']:
                    break
            except:
                continue
        
        # BUSCAR TIPO DE EVENTO
        print(f"--- BUSCANDO TIPO DE EVENTO ---")
        tipo_evento_selectors = [
            "//*[contains(text(), 'tipo') and contains(text(), 'evento')]",
            "//*[contains(text(), 'Tipo') and contains(text(), 'Evento')]",
            "//*[contains(text(), 'TIPO') and contains(text(), 'EVENTO')]",
            "//*[contains(text(), 'Evento')]"
        ]
        
        for selector in tipo_evento_selectors:
            try:
                elementos = driver.find_elements(By.XPATH, selector)
                for elem in elementos:
                    if elem.is_displayed() and elem.text.strip():
                        texto = elem.text.strip()
                        if len(texto) > 0 and len(texto) < 200:
                            datos_evento['tipo_evento'] = texto
                            print(f"✓ Tipo de evento: {texto}")
                            break
                if datos_evento['tipo_evento']:
                    break
            except:
                continue
        
        # BUSCAR FECHA DEL EVENTO
        print(f"--- BUSCANDO FECHA DEL EVENTO ---")
        fecha_selectors = [
            "//*[contains(text(), 'fecha')]",
            "//*[contains(text(), 'Fecha')]",
            "//*[contains(text(), 'FECHA')]",
            "//*[contains(text(), 'Date')]"
        ]
        
        for selector in fecha_selectors:
            try:
                elementos = driver.find_elements(By.XPATH, selector)
                for elem in elementos:
                    if elem.is_displayed() and elem.text.strip():
                        texto = elem.text.strip()
                        if len(texto) > 0 and len(texto) < 200:
                            datos_evento['fecha_evento'] = texto
                            print(f"✓ Fecha del evento: {texto}")
                            break
                if datos_evento['fecha_evento']:
                    break
            except:
                continue
        
        # BUSCAR SALÓN
        print(f"--- BUSCANDO SALÓN ---")
        salon_selectors = [
            "//*[contains(text(), 'salon') or contains(text(), 'salón')]",
            "//*[contains(text(), 'Salon') or contains(text(), 'Salón')]",
            "//*[contains(text(), 'SALON') or contains(text(), 'SALÓN')]"
        ]
        
        for selector in salon_selectors:
            try:
                elementos = driver.find_elements(By.XPATH, selector)
                for elem in elementos:
                    if elem.is_displayed() and elem.text.strip():
                        texto = elem.text.strip()
                        if len(texto) > 0 and len(texto) < 200:
                            datos_evento['salon'] = texto
                            print(f"✓ Salón: {texto}")
                            break
                if datos_evento['salon']:
                    break
            except:
                continue
        
        # BUSCAR CLIENTE (CLICKEABLE)
        print(f"--- BUSCANDO CLIENTE (CLICKEABLE) ---")
        cliente_selectors = [
            "//*[contains(text(), 'cliente') or contains(text(), 'Cliente')]",
            "//*[contains(text(), 'CLIENTE')]",
            "//a[contains(text(), 'cliente') or contains(text(), 'Cliente')]",
            "//button[contains(text(), 'cliente') or contains(text(), 'Cliente')]"
        ]
        
        cliente_encontrado = False
        for selector in cliente_selectors:
            try:
                elementos = driver.find_elements(By.XPATH, selector)
                for elem in elementos:
                    if elem.is_displayed() and elem.is_enabled():
                        texto = elem.text.strip()
                        if len(texto) > 0 and len(texto) < 200:
                            datos_evento['cliente'] = texto
                            print(f"✓ Cliente encontrado: {texto}")
                            
                            # Intentar hacer clic en el cliente
                            try:
                                print(f"✓ Intentando hacer clic en cliente...")
                                elem.click()
                                time.sleep(3)  # Esperar a que se despliegue la información del cliente
                                
                                # BUSCAR CELULAR Y CELULAR 2
                                print(f"--- BUSCANDO CELULAR Y CELULAR 2 ---")
                                celular_selectors = [
                                    "//*[contains(text(), 'celular') or contains(text(), 'Celular')]",
                                    "//*[contains(text(), 'CELULAR')]",
                                    "//*[contains(text(), 'telefono') or contains(text(), 'teléfono')]",
                                    "//*[contains(text(), 'Teléfono') or contains(text(), 'Telefono')]"
                                ]
                                
                                for cel_selector in celular_selectors:
                                    try:
                                        cel_elementos = driver.find_elements(By.XPATH, cel_selector)
                                        for cel_elem in cel_elementos:
                                            if cel_elem.is_displayed() and cel_elem.text.strip():
                                                cel_texto = cel_elem.text.strip()
                                                if len(cel_texto) > 0 and len(cel_texto) < 200:
                                                    if 'celular' in cel_texto.lower() or 'telefono' in cel_texto.lower():
                                                        if not datos_evento['celular']:
                                                            datos_evento['celular'] = cel_texto
                                                            print(f"✓ Celular: {cel_texto}")
                                                        elif not datos_evento['celular_2']:
                                                            datos_evento['celular_2'] = cel_texto
                                                            print(f"✓ Celular 2: {cel_texto}")
                                                    break
                                    except:
                                        continue
                                
                                cliente_encontrado = True
                                break
                            except Exception as e:
                                print(f"✗ Error haciendo clic en cliente: {str(e)}")
                            
                            if cliente_encontrado:
                                break
                if cliente_encontrado:
                    break
            except:
                continue
        
        # BUSCAR TIPO DE PACK
        print(f"--- BUSCANDO TIPO DE PACK ---")
        pack_selectors = [
            "//*[contains(text(), 'pack') or contains(text(), 'Pack')]",
            "//*[contains(text(), 'PACK')]",
            "//*[contains(text(), 'tipo') and contains(text(), 'pack')]",
            "//*[contains(text(), 'Tipo') and contains(text(), 'Pack')]"
        ]
        
        for selector in pack_selectors:
            try:
                elementos = driver.find_elements(By.XPATH, selector)
                for elem in elementos:
                    if elem.is_displayed() and elem.text.strip():
                        texto = elem.text.strip()
                        if len(texto) > 0 and len(texto) < 200:
                            datos_evento['tipo_pack'] = texto
                            print(f"✓ Tipo de Pack: {texto}")
                            break
                if datos_evento['tipo_pack']:
                    break
            except:
                continue
        
        # 3. ANÁLISIS DE FORMULARIOS Y INPUTS
        print(f"\n--- ANÁLISIS DE FORMULARIOS E INPUTS ---")
        
        # Buscar inputs
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"Total de inputs: {len(inputs)}")
        
        for input_elem in inputs:
            if input_elem.is_displayed():
                tipo = input_elem.get_attribute('type')
                nombre = input_elem.get_attribute('name')
                valor = input_elem.get_attribute('value')
                placeholder = input_elem.get_attribute('placeholder')
                
                if valor or nombre or placeholder:
                    print(f"  Input: tipo={tipo}, nombre={nombre}, valor={valor}, placeholder={placeholder}")
        
        # Buscar selects
        selects = driver.find_elements(By.TAG_NAME, "select")
        print(f"Total de selects: {len(selects)}")
        
        for select_elem in selects:
            if select_elem.is_displayed():
                nombre = select_elem.get_attribute('name')
                id_elem = select_elem.get_attribute('id')
                print(f"  Select: nombre={nombre}, id={id_elem}")
        
        # Buscar textareas
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        print(f"Total de textareas: {len(textareas)}")
        
        for textarea_elem in textareas:
            if textarea_elem.is_displayed():
                nombre = textarea_elem.get_attribute('name')
                valor = textarea_elem.get_attribute('value')
                placeholder = textarea_elem.get_attribute('placeholder')
                
                if valor or nombre or placeholder:
                    print(f"  Textarea: nombre={nombre}, valor={valor}, placeholder={placeholder}")
        
        # 4. MOSTRAR RESUMEN FINAL
        print(f"\n=== RESUMEN FINAL DE DATOS ENCONTRADOS ===")
        datos_encontrados = 0
        for campo, valor in datos_evento.items():
            if valor and campo not in ['url', 'titulo']:
                datos_encontrados += 1
                print(f"✓ {campo}: {valor}")
            elif not valor and campo not in ['url', 'titulo']:
                print(f"✗ {campo}: No encontrado")
        
        print(f"\nTotal de datos encontrados: {datos_encontrados}/7")
        print(f"URL: {datos_evento['url']}")
        print(f"Título: {datos_evento['titulo']}")
        
        return datos_evento
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return None
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación manual...")
            print("Verifica manualmente que se pueden acceder a todos los datos específicos:")
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
    resultado = navegar_directamente_evento()
    if resultado:
        print(f"\n=== RESULTADO FINAL ===")
        print(f"Datos extraídos exitosamente:")
        for campo, valor in resultado.items():
            print(f"  {campo}: {valor}")
    else:
        print(f"\n=== RESULTADO FINAL ===")
        print(f"No se pudieron extraer los datos requeridos")


