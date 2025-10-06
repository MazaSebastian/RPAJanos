#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para acceder a la información individual de cada evento
- Hacer clic en fechas coral
- Hacer clic en códigos de 5 dígitos
- Acceder a información detallada de cada evento
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def acceder_info_individual_eventos():
    """Acceder a la información individual de cada evento"""
    
    print("=== ACCEDIENDO A INFORMACIÓN INDIVIDUAL DE EVENTOS ===")
    print("1. Hacer clic en fechas coral")
    print("2. Hacer clic en códigos de 5 dígitos")
    print("3. Acceder a información detallada de cada evento")
    
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
            print("✗ No se encontraron fechas coral")
            return False
        
        # PASO 5: Probar acceso a información individual
        print(f"\n=== PASO 5: ACCEDIENDO A INFORMACIÓN INDIVIDUAL ===")
        
        eventos_procesados = 0
        informacion_extraida = []
        
        for i, fecha_coral in enumerate(fechas_coral[:3]):  # Probar con las primeras 3 fechas
            try:
                fecha_texto = fecha_coral.text.strip()
                print(f"\n--- Procesando fecha {i+1}: {fecha_texto} ---")
                
                # Hacer clic en la fecha coral
                print(f"✓ Haciendo clic en fecha {fecha_texto}...")
                fecha_coral.click()
                time.sleep(3)  # Esperar a que se despliegue la información
                
                # Buscar códigos de 5 dígitos clickeables
                print(f"✓ Buscando códigos de 5 dígitos clickeables...")
                codigos_5_digitos = driver.find_elements(By.XPATH, "//*[text() and string-length(normalize-space(text())) = 5 and translate(text(), '0123456789', '0000000000') = '00000']")
                
                print(f"  - Códigos de 5 dígitos encontrados: {len(codigos_5_digitos)}")
                
                # Probar hacer clic en cada código
                for j, codigo_elem in enumerate(codigos_5_digitos[:2]):  # Probar con los primeros 2 códigos
                    try:
                        codigo_texto = codigo_elem.text.strip()
                        print(f"\n    --- Probando código {j+1}: {codigo_texto} ---")
                        
                        # Verificar que es clickeable
                        if codigo_elem.is_displayed() and codigo_elem.is_enabled():
                            print(f"    ✓ Código {codigo_texto} es clickeable")
                            
                            # Hacer clic en el código
                            print(f"    ✓ Haciendo clic en código {codigo_texto}...")
                            codigo_elem.click()
                            time.sleep(5)  # Esperar a que cargue la página individual
                            
                            # Verificar si cambió la URL o apareció nueva información
                            current_url = driver.current_url
                            print(f"    ✓ URL actual: {current_url}")
                            
                            # Buscar información detallada del evento
                            print(f"    ✓ Buscando información detallada del evento...")
                            
                            # Buscar campos comunes de información de evento
                            campos_buscados = [
                                "nombre", "cliente", "evento", "fecha", "hora", "salon", "zona",
                                "tipo", "agasajado", "contacto", "telefono", "email", "direccion",
                                "observaciones", "notas", "descripcion", "detalles"
                            ]
                            
                            informacion_encontrada = {}
                            
                            for campo in campos_buscados:
                                # Buscar por texto que contenga la palabra
                                elementos_campo = driver.find_elements(By.XPATH, f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{campo}')]")
                                
                                if elementos_campo:
                                    for elem in elementos_campo:
                                        if elem.is_displayed() and elem.text.strip():
                                            texto_limpio = elem.text.strip()
                                            if len(texto_limpio) > 0 and len(texto_limpio) < 200:
                                                informacion_encontrada[campo] = texto_limpio
                                                print(f"      ✓ {campo}: {texto_limpio[:50]}...")
                                                break
                            
                            # Buscar también en inputs y textareas
                            inputs = driver.find_elements(By.TAG_NAME, "input")
                            textareas = driver.find_elements(By.TAG_NAME, "textarea")
                            
                            for input_elem in inputs:
                                if input_elem.is_displayed():
                                    valor = input_elem.get_attribute('value')
                                    if valor and len(valor.strip()) > 0:
                                        print(f"      ✓ Input: {valor[:50]}...")
                                        informacion_encontrada['input'] = valor
                            
                            for textarea_elem in textareas:
                                if textarea_elem.is_displayed():
                                    valor = textarea_elem.get_attribute('value')
                                    if valor and len(valor.strip()) > 0:
                                        print(f"      ✓ Textarea: {valor[:50]}...")
                                        informacion_encontrada['textarea'] = valor
                            
                            # Mostrar resumen de información encontrada
                            print(f"    ✓ Información encontrada para código {codigo_texto}:")
                            for campo, valor in informacion_encontrada.items():
                                print(f"      - {campo}: {valor[:100]}...")
                            
                            if informacion_encontrada:
                                eventos_procesados += 1
                                informacion_extraida.append({
                                    'fecha': fecha_texto,
                                    'codigo': codigo_texto,
                                    'informacion': informacion_encontrada
                                })
                                print(f"    ✓ Evento {codigo_texto} procesado exitosamente")
                            else:
                                print(f"    ⚠ Evento {codigo_texto}: No se encontró información detallada")
                            
                            # Volver atrás o cerrar la información
                            try:
                                # Buscar botón de cerrar o volver
                                botones_cerrar = driver.find_elements(By.XPATH, "//*[contains(text(), 'cerrar') or contains(text(), 'volver') or contains(text(), 'atrás') or contains(text(), 'close') or contains(text(), 'back')]")
                                if botones_cerrar:
                                    botones_cerrar[0].click()
                                    time.sleep(2)
                                else:
                                    # Hacer clic en otra parte para cerrar
                                    driver.find_element(By.TAG_NAME, "body").click()
                                    time.sleep(1)
                            except:
                                pass
                            
                        else:
                            print(f"    ✗ Código {codigo_texto} no es clickeable")
                            
                    except Exception as e:
                        print(f"    ✗ Error procesando código {j+1}: {str(e)}")
                
                # Cerrar información desplegada de la fecha
                try:
                    driver.find_element(By.TAG_NAME, "body").click()
                    time.sleep(1)
                except:
                    pass
                
            except Exception as e:
                print(f"✗ Error procesando fecha {i+1}: {str(e)}")
        
        # PASO 6: Mostrar resultados
        print(f"\n=== RESULTADOS DE ACCESO A INFORMACIÓN INDIVIDUAL ===")
        print(f"Fechas coral procesadas: {len(fechas_coral[:3])}")
        print(f"Eventos con información accesible: {eventos_procesados}")
        print(f"Total de eventos con información: {len(informacion_extraida)}")
        
        if informacion_extraida:
            print(f"\nInformación extraída:")
            for evento in informacion_extraida:
                print(f"  - Fecha: {evento['fecha']}, Código: {evento['codigo']}")
                print(f"    Información: {len(evento['informacion'])} campos encontrados")
                for campo, valor in evento['informacion'].items():
                    print(f"      {campo}: {valor[:50]}...")
        
        return eventos_procesados > 0
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación manual...")
            print("Verifica manualmente:")
            print("1. Que las fechas coral son clickeables")
            print("2. Que los códigos de 5 dígitos son clickeables")
            print("3. Que se accede a información detallada de cada evento")
            time.sleep(180)  # Mantener abierto por 3 minutos
            driver.quit()

if __name__ == "__main__":
    acceder_info_individual_eventos()


