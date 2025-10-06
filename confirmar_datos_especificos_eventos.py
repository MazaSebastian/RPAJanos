#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para confirmar acceso a datos específicos de cada evento individual:
- Homenajeada/o
- Código de evento
- Tipo de evento
- Fecha del evento
- Salón
- Cliente (clickeable - CELULAR y CELULAR 2)
- Tipo de Pack
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def confirmar_datos_especificos_eventos():
    """Confirmar acceso a datos específicos de cada evento individual"""
    
    print("=== CONFIRMACIÓN DE DATOS ESPECÍFICOS DE EVENTOS ===")
    print("Buscando información específica de cada evento:")
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
        
        # PASO 5: Analizar datos específicos de eventos
        print(f"\n=== PASO 5: ANÁLISIS DE DATOS ESPECÍFICOS ===")
        
        eventos_analizados = []
        
        for i, fecha_coral in enumerate(fechas_coral[:2]):  # Analizar las primeras 2 fechas
            try:
                fecha_texto = fecha_coral.text.strip()
                print(f"\n--- ANÁLISIS FECHA {i+1}: {fecha_texto} ---")
                
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
                        
                        # ANÁLISIS DE DATOS ESPECÍFICOS
                        print(f"    ✓ Analizando datos específicos del evento...")
                        
                        datos_evento = {
                            'fecha': fecha_texto,
                            'codigo': codigo_texto,
                            'homenajeada': None,
                            'tipo_evento': None,
                            'fecha_evento': None,
                            'salon': None,
                            'cliente': None,
                            'celular': None,
                            'celular_2': None,
                            'tipo_pack': None
                        }
                        
                        # 1. BUSCAR HOMENAJEADA/O
                        print(f"    --- BUSCANDO HOMENAJEADA/O ---")
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
                                            print(f"      ✓ Homenajeada/o: {texto}")
                                            break
                                if datos_evento['homenajeada']:
                                    break
                            except:
                                continue
                        
                        # 2. BUSCAR TIPO DE EVENTO
                        print(f"    --- BUSCANDO TIPO DE EVENTO ---")
                        tipo_evento_selectors = [
                            "//*[contains(text(), 'tipo') and contains(text(), 'evento')]",
                            "//*[contains(text(), 'Tipo') and contains(text(), 'Evento')]",
                            "//*[contains(text(), 'TIPO') and contains(text(), 'EVENTO')]"
                        ]
                        
                        for selector in tipo_evento_selectors:
                            try:
                                elementos = driver.find_elements(By.XPATH, selector)
                                for elem in elementos:
                                    if elem.is_displayed() and elem.text.strip():
                                        texto = elem.text.strip()
                                        if len(texto) > 0 and len(texto) < 200:
                                            datos_evento['tipo_evento'] = texto
                                            print(f"      ✓ Tipo de evento: {texto}")
                                            break
                                if datos_evento['tipo_evento']:
                                    break
                            except:
                                continue
                        
                        # 3. BUSCAR FECHA DEL EVENTO
                        print(f"    --- BUSCANDO FECHA DEL EVENTO ---")
                        fecha_selectors = [
                            "//*[contains(text(), 'fecha')]",
                            "//*[contains(text(), 'Fecha')]",
                            "//*[contains(text(), 'FECHA')]"
                        ]
                        
                        for selector in fecha_selectors:
                            try:
                                elementos = driver.find_elements(By.XPATH, selector)
                                for elem in elementos:
                                    if elem.is_displayed() and elem.text.strip():
                                        texto = elem.text.strip()
                                        if len(texto) > 0 and len(texto) < 200:
                                            datos_evento['fecha_evento'] = texto
                                            print(f"      ✓ Fecha del evento: {texto}")
                                            break
                                if datos_evento['fecha_evento']:
                                    break
                            except:
                                continue
                        
                        # 4. BUSCAR SALÓN
                        print(f"    --- BUSCANDO SALÓN ---")
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
                                            print(f"      ✓ Salón: {texto}")
                                            break
                                if datos_evento['salon']:
                                    break
                            except:
                                continue
                        
                        # 5. BUSCAR CLIENTE (CLICKEABLE)
                        print(f"    --- BUSCANDO CLIENTE (CLICKEABLE) ---")
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
                                            print(f"      ✓ Cliente encontrado: {texto}")
                                            
                                            # Intentar hacer clic en el cliente
                                            try:
                                                print(f"      ✓ Intentando hacer clic en cliente...")
                                                elem.click()
                                                time.sleep(3)  # Esperar a que se despliegue la información del cliente
                                                
                                                # BUSCAR CELULAR Y CELULAR 2
                                                print(f"      --- BUSCANDO CELULAR Y CELULAR 2 ---")
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
                                                                            print(f"        ✓ Celular: {cel_texto}")
                                                                        elif not datos_evento['celular_2']:
                                                                            datos_evento['celular_2'] = cel_texto
                                                                            print(f"        ✓ Celular 2: {cel_texto}")
                                                                    break
                                                    except:
                                                        continue
                                                
                                                cliente_encontrado = True
                                                break
                                            except Exception as e:
                                                print(f"      ✗ Error haciendo clic en cliente: {str(e)}")
                                            
                                            if cliente_encontrado:
                                                break
                                if cliente_encontrado:
                                    break
                            except:
                                continue
                        
                        # 6. BUSCAR TIPO DE PACK
                        print(f"    --- BUSCANDO TIPO DE PACK ---")
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
                                            print(f"      ✓ Tipo de Pack: {texto}")
                                            break
                                if datos_evento['tipo_pack']:
                                    break
                            except:
                                continue
                        
                        # 7. MOSTRAR RESUMEN DE DATOS ENCONTRADOS
                        print(f"    --- RESUMEN DE DATOS ENCONTRADOS ---")
                        datos_encontrados = 0
                        for campo, valor in datos_evento.items():
                            if valor and campo not in ['fecha', 'codigo']:
                                datos_encontrados += 1
                                print(f"      ✓ {campo}: {valor}")
                            elif not valor and campo not in ['fecha', 'codigo']:
                                print(f"      ✗ {campo}: No encontrado")
                        
                        print(f"    ✓ Total de datos encontrados: {datos_encontrados}/7")
                        
                        eventos_analizados.append(datos_evento)
                        
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
        print(f"\n=== RESUMEN FINAL DE DATOS ESPECÍFICOS ===")
        print(f"Eventos analizados: {len(eventos_analizados)}")
        
        for i, evento in enumerate(eventos_analizados):
            print(f"\n--- EVENTO {i+1}: Fecha {evento['fecha']}, Código {evento['codigo']} ---")
            print(f"  Homenajeada/o: {evento['homenajeada'] or 'No encontrado'}")
            print(f"  Tipo de evento: {evento['tipo_evento'] or 'No encontrado'}")
            print(f"  Fecha del evento: {evento['fecha_evento'] or 'No encontrado'}")
            print(f"  Salón: {evento['salon'] or 'No encontrado'}")
            print(f"  Cliente: {evento['cliente'] or 'No encontrado'}")
            print(f"  Celular: {evento['celular'] or 'No encontrado'}")
            print(f"  Celular 2: {evento['celular_2'] or 'No encontrado'}")
            print(f"  Tipo de Pack: {evento['tipo_pack'] or 'No encontrado'}")
        
        return len(eventos_analizados) > 0
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
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
            time.sleep(180)  # Mantener abierto por 3 minutos
            driver.quit()

if __name__ == "__main__":
    confirmar_datos_especificos_eventos()


