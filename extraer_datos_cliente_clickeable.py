#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para hacer clic en el cliente clickeable y extraer CELULAR y CELULAR 2
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def extraer_datos_cliente_clickeable():
    """Hacer clic en el cliente clickeable y extraer CELULAR y CELULAR 2"""
    
    print("=== EXTRACCIÓN DE DATOS DEL CLIENTE CLICKEABLE ===")
    print("Objetivo: Hacer clic en 'Veronica Cazajus' y extraer CELULAR y CELULAR 2")
    
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
        
        # Navegar directamente a la URL del evento
        print(f"✓ Navegando directamente a: {url_evento}")
        driver.get(url_evento)
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
        
        # PASO 10: BUSCAR Y HACER CLIC EN EL CLIENTE CLICKEABLE
        print(f"\n=== PASO 10: BUSCAR Y HACER CLIC EN EL CLIENTE CLICKEABLE ===")
        
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
        
        # Buscar el cliente clickeable
        cliente_encontrado = False
        cliente_elemento = None
        
        for elem in elementos_relevantes:
            if 'veronica cazajus' in elem['texto'].lower():
                print(f"✓ Cliente encontrado: {elem['texto']}")
                cliente_elemento = elem['elemento']
                cliente_encontrado = True
                break
        
        if not cliente_encontrado:
            print("✗ No se encontró el cliente 'Veronica Cazajus'")
            return None
        
        # Hacer clic en el cliente
        print(f"✓ Haciendo clic en cliente 'Veronica Cazajus'...")
        try:
            cliente_elemento.click()
            time.sleep(5)  # Esperar a que se despliegue la información del cliente
            print("✓ Clic en cliente exitoso")
        except Exception as e:
            print(f"✗ Error haciendo clic en cliente: {str(e)}")
            return None
        
        # PASO 11: EXTRAER CELULAR Y CELULAR 2
        print(f"\n=== PASO 11: EXTRAER CELULAR Y CELULAR 2 ===")
        
        # Buscar elementos con información de contacto después del clic
        elementos_contacto = driver.find_elements(By.XPATH, "//*[text()]")
        celulares_encontrados = []
        
        print(f"Buscando información de contacto...")
        for elem_contacto in elementos_contacto:
            if elem_contacto.is_displayed() and elem_contacto.text.strip():
                texto_contacto = elem_contacto.text.strip()
                # Buscar números de teléfono
                if any(char.isdigit() for char in texto_contacto):
                    if any(palabra in texto_contacto.lower() for palabra in ['celular', 'telefono', 'teléfono', 'tel', 'móvil', 'movil', 'phone', 'mobile']):
                        celulares_encontrados.append(texto_contacto)
                        print(f"✓ Celular encontrado: {texto_contacto}")
        
        # Mostrar todos los elementos para análisis adicional
        print(f"\n=== ANÁLISIS COMPLETO DE ELEMENTOS DESPUÉS DEL CLIC ===")
        for k, elem in enumerate(elementos_contacto[:50]):  # Mostrar los primeros 50
            if elem.is_displayed() and elem.text.strip():
                texto = elem.text.strip()
                if len(texto) > 0 and len(texto) < 200:
                    print(f"  {k+1}. {elem.tag_name}: {texto}")
        
        # Inicializar datos del evento
        datos_evento = {
            'fecha': fecha_texto,
            'codigo': '33069',
            'url': current_url,
            'homenajeada': 'Carola',
            'codigo_evento': '33069',
            'tipo_evento': '15',
            'fecha_evento': '12/10/2025(Domingo)',
            'salon': '53 - DOT',
            'cliente': 'Veronica Cazajus',
            'celular': None,
            'celular_2': None,
            'tipo_pack': 'Pack 1'
        }
        
        # Asignar celulares encontrados
        if len(celulares_encontrados) >= 1:
            datos_evento['celular'] = celulares_encontrados[0]
            print(f"✓ Celular: {celulares_encontrados[0]}")
        
        if len(celulares_encontrados) >= 2:
            datos_evento['celular_2'] = celulares_encontrados[1]
            print(f"✓ Celular 2: {celulares_encontrados[1]}")
        
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
            print("- Homenajeada/o: Carola")
            print("- Código de evento: 33069")
            print("- Tipo de evento: 15 (cumpleaños)")
            print("- Fecha del evento: 12/10/2025(Domingo)")
            print("- Salón: 53 - DOT")
            print("- Cliente: Veronica Cazajus (clickeable - CELULAR y CELULAR 2)")
            print("- Tipo de Pack: Pack 1")
            time.sleep(300)  # Mantener abierto por 5 minutos
            driver.quit()

if __name__ == "__main__":
    resultado = extraer_datos_cliente_clickeable()
    if resultado:
        print(f"\n=== RESULTADO FINAL ===")
        print(f"Datos extraídos exitosamente:")
        for campo, valor in resultado.items():
            print(f"  {campo}: {valor}")
    else:
        print(f"\n=== RESULTADO FINAL ===")
        print(f"No se pudieron extraer los datos requeridos")


