#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extraer datos específicos del evento con manejo automático de vencimiento de sesión
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
        # Buscar indicadores de sesión vencida
        sesion_vencida_indicators = [
            "Sesion vencida",
            "Sesión vencida", 
            "Sesion expirada",
            "Sesión expirada",
            "Volve a ingresar",
            "Vuelve a ingresar",
            "login.php"
        ]
        
        page_source = driver.page_source.lower()
        current_url = driver.current_url.lower()
        
        for indicator in sesion_vencida_indicators:
            if indicator.lower() in page_source or indicator.lower() in current_url:
                print(f"⚠ Sesión vencida detectada: {indicator}")
                return False
        
        # Verificar que no estamos en página de login
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
        
        # Navegar a página de login
        driver.get("https://tecnica.janosgroup.com/login.php")
        time.sleep(3)
        print("✓ Navegando a página de login...")
        
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
        wait = WebDriverWait(driver, 20)
        wait.until(lambda driver: "login.php" not in driver.current_url)
        print("✓ Relogueo exitoso")
        
        return True
        
    except Exception as e:
        print(f"✗ Error en relogueo: {str(e)}")
        return False

def acceder_adicionales_con_sesion(driver):
    """Acceder a ADICIONALES con verificación de sesión"""
    try:
        print("\n=== ACCEDIENDO A ADICIONALES CON VERIFICACIÓN DE SESIÓN ===")
        
        # Verificar sesión antes de proceder
        if not verificar_sesion_activa(driver):
            if not reloguear_automaticamente(driver):
                return False
        
        # Abrir menú lateral
        open_nav_element = driver.find_element(By.XPATH, "//*[@onclick='openNav()']")
        open_nav_element.click()
        time.sleep(2)
        print("✓ Menú lateral abierto")
        
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
        
        # Aplicar filtros
        print("\n=== APLICANDO FILTROS ===")
        
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
        
        return True
        
    except Exception as e:
        print(f"✗ Error accediendo a ADICIONALES: {str(e)}")
        return False

def extraer_datos_evento_individual(driver, url_evento):
    """Extraer datos específicos del evento individual con manejo de sesión"""
    try:
        print(f"\n=== EXTRAYENDO DATOS DEL EVENTO INDIVIDUAL ===")
        print(f"URL: {url_evento}")
        
        # Verificar sesión antes de navegar
        if not verificar_sesion_activa(driver):
            if not reloguear_automaticamente(driver):
                return None
        
        # Navegar a la página del evento
        driver.get(url_evento)
        time.sleep(5)  # Esperar a que cargue
        
        # Verificar sesión después de navegar
        if not verificar_sesion_activa(driver):
            print("⚠ Sesión vencida después de navegar al evento")
            if not reloguear_automaticamente(driver):
                return None
            # Reintentar navegación
            driver.get(url_evento)
            time.sleep(5)
        
        # Verificar que cargó correctamente
        current_url = driver.current_url
        titulo = driver.title
        print(f"✓ URL actual: {current_url}")
        print(f"✓ Título: {titulo}")
        
        # Analizar contenido de la página
        page_source = driver.page_source
        if "sesion vencida" in page_source.lower() or "sesión vencida" in page_source.lower():
            print("⚠ Sesión vencida detectada en el contenido de la página")
            return None
        
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
                        'id': elem.get_attribute('id')
                    })
        
        print(f"Total de elementos con texto: {len(elementos_relevantes)}")
        
        # Mostrar los primeros 15 elementos para análisis
        print(f"Primeros 15 elementos encontrados:")
        for k, elem in enumerate(elementos_relevantes[:15]):
            print(f"  {k+1}. {elem['tag']}: {elem['texto'][:80]}...")
        
        # Buscar datos específicos
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
        
        # Búsqueda inteligente de datos
        print(f"\n--- BÚSQUEDA INTELIGENTE DE DATOS ---")
        
        # Buscar patrones específicos en todos los elementos
        for elem in elementos_relevantes:
            texto = elem['texto'].lower()
            
            # HOMENAJEADA/O
            if not datos_evento['homenajeada']:
                if any(palabra in texto for palabra in ['homenajeada', 'homenajeado', 'cumpleañero', 'cumpleañera']):
                    datos_evento['homenajeada'] = elem['texto']
                    print(f"✓ Homenajeada/o: {elem['texto']}")
            
            # TIPO DE EVENTO
            if not datos_evento['tipo_evento']:
                if any(palabra in texto for palabra in ['cumpleaños', 'casamiento', 'bautismo', 'comunión', 'quince', 'evento']):
                    datos_evento['tipo_evento'] = elem['texto']
                    print(f"✓ Tipo de evento: {elem['texto']}")
            
            # FECHA DEL EVENTO
            if not datos_evento['fecha_evento']:
                if any(palabra in texto for palabra in ['fecha', 'date', '2025', '2024']):
                    if len(elem['texto']) > 5 and len(elem['texto']) < 50:
                        datos_evento['fecha_evento'] = elem['texto']
                        print(f"✓ Fecha del evento: {elem['texto']}")
            
            # SALÓN
            if not datos_evento['salon']:
                if any(palabra in texto for palabra in ['salón', 'salon', 'sala', 'dot', 'caba']):
                    datos_evento['salon'] = elem['texto']
                    print(f"✓ Salón: {elem['texto']}")
            
            # CLIENTE
            if not datos_evento['cliente']:
                if any(palabra in texto for palabra in ['cliente', 'contacto', 'nombre']):
                    if len(elem['texto']) > 2 and len(elem['texto']) < 100:
                        datos_evento['cliente'] = elem['texto']
                        print(f"✓ Cliente: {elem['texto']}")
            
            # CELULAR
            if not datos_evento['celular']:
                if any(palabra in texto for palabra in ['celular', 'telefono', 'teléfono', 'tel', 'móvil']):
                    if any(char.isdigit() for char in elem['texto']):
                        datos_evento['celular'] = elem['texto']
                        print(f"✓ Celular: {elem['texto']}")
            
            # TIPO DE PACK
            if not datos_evento['tipo_pack']:
                if any(palabra in texto for palabra in ['pack', 'paquete', 'tipo', 'nivel']):
                    datos_evento['tipo_pack'] = elem['texto']
                    print(f"✓ Tipo de Pack: {elem['texto']}")
        
        # Mostrar resumen final
        print(f"\n=== RESUMEN FINAL DE DATOS ENCONTRADOS ===")
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
        print(f"✗ Error extrayendo datos del evento: {str(e)}")
        return None

def extraer_datos_con_manejo_sesion():
    """Función principal con manejo automático de vencimiento de sesión"""
    
    print("=== EXTRACCIÓN DE DATOS CON MANEJO AUTOMÁTICO DE SESIÓN ===")
    print("Características:")
    print("- Detección automática de sesión vencida")
    print("- Relogueo automático sin intervención manual")
    print("- Extracción de datos específicos del evento")
    
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
        
        # PASO 1: Login inicial
        print("\n=== PASO 1: LOGIN INICIAL ===")
        driver.get("https://tecnica.janosgroup.com/login.php")
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
        print("✓ Login exitoso")
        
        # PASO 2: Acceder a ADICIONALES con verificación de sesión
        if not acceder_adicionales_con_sesion(driver):
            print("✗ Error accediendo a ADICIONALES")
            return False
        
        # PASO 3: Navegar directamente a evento individual
        url_evento = "https://janosgroup.com/ver_evento.php?id=33069"
        print(f"\n=== PASO 3: NAVEGACIÓN DIRECTA AL EVENTO ===")
        print(f"URL del evento: {url_evento}")
        
        # Extraer datos del evento individual
        datos_evento = extraer_datos_evento_individual(driver, url_evento)
        
        if datos_evento:
            print(f"\n=== EXTRACCIÓN EXITOSA ===")
            return datos_evento
        else:
            print(f"\n=== EXTRACCIÓN FALLIDA ===")
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
            print("- Tipo de evento")
            print("- Fecha del evento")
            print("- Salón")
            print("- Cliente (clickeable - CELULAR y CELULAR 2)")
            print("- Tipo de Pack")
            time.sleep(300)  # Mantener abierto por 5 minutos
            driver.quit()

if __name__ == "__main__":
    resultado = extraer_datos_con_manejo_sesion()
    if resultado:
        print(f"\n=== RESULTADO FINAL ===")
        print(f"Datos extraídos exitosamente:")
        for campo, valor in resultado.items():
            print(f"  {campo}: {valor}")
    else:
        print(f"\n=== RESULTADO FINAL ===")
        print(f"No se pudieron extraer los datos requeridos")


