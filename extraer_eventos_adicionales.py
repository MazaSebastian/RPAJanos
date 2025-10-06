#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extraer eventos de ADICIONALES con filtros específicos
- Salon: DOT
- Zona: CABA  
- Año: 2025
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def extraer_eventos_adicionales():
    """Extraer eventos de ADICIONALES con filtros específicos"""
    
    print("=== EXTRACCIÓN DE EVENTOS DE ADICIONALES ===")
    print("Filtros a aplicar:")
    print("- Salon: DOT")
    print("- Zona: CABA")
    print("- Año: 2025")
    
    driver = None
    eventos_extraidos = []
    
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
        print("Aplicando filtro SALON: DOT")
        try:
            salon_select = Select(driver.find_element(By.ID, "salon"))
            salon_select.select_by_visible_text("DOT")
            print("✓ Filtro SALON aplicado: DOT")
        except Exception as e:
            print(f"✗ Error aplicando filtro SALON: {str(e)}")
            # Intentar buscar por valor o texto parcial
            try:
                salon_select = Select(driver.find_element(By.ID, "salon"))
                for option in salon_select.options:
                    if "DOT" in option.text:
                        salon_select.select_by_visible_text(option.text)
                        print(f"✓ Filtro SALON aplicado: {option.text}")
                        break
            except Exception as e2:
                print(f"✗ Error alternativo con SALON: {str(e2)}")
        
        # Filtro ZONA: CABA
        print("Aplicando filtro ZONA: CABA")
        try:
            zona_select = Select(driver.find_element(By.ID, "cluster"))
            zona_select.select_by_visible_text("CABA")
            print("✓ Filtro ZONA aplicado: CABA")
        except Exception as e:
            print(f"✗ Error aplicando filtro ZONA: {str(e)}")
            # Intentar buscar por valor o texto parcial
            try:
                zona_select = Select(driver.find_element(By.ID, "cluster"))
                for option in zona_select.options:
                    if "CABA" in option.text:
                        zona_select.select_by_visible_text(option.text)
                        print(f"✓ Filtro ZONA aplicado: {option.text}")
                        break
            except Exception as e2:
                print(f"✗ Error alternativo con ZONA: {str(e2)}")
        
        # Filtro AÑO: 2025
        print("Aplicando filtro AÑO: 2025")
        try:
            ano_select = Select(driver.find_element(By.ID, "ano"))
            ano_select.select_by_visible_text("2025")
            print("✓ Filtro AÑO aplicado: 2025")
        except Exception as e:
            print(f"✗ Error aplicando filtro AÑO: {str(e)}")
        
        # PASO 4: Aplicar filtros (hacer clic en FILTRAR)
        print("\n=== PASO 4: APLICANDO FILTROS ===")
        try:
            # Buscar botón FILTRAR
            filtrar_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Filtrar']")
            print("✓ Botón FILTRAR encontrado")
            print("✓ Haciendo clic en FILTRAR...")
            filtrar_button.click()
            time.sleep(5)  # Esperar a que se procesen los filtros
            print("✓ Filtros aplicados")
        except Exception as e:
            print(f"✗ Error aplicando filtros: {str(e)}")
            # Intentar con otros selectores
            try:
                filtrar_buttons = driver.find_elements(By.XPATH, "//input[@value='Filtrar']")
                if filtrar_buttons:
                    filtrar_buttons[0].click()
                    time.sleep(5)
                    print("✓ Filtros aplicados (método alternativo)")
            except Exception as e2:
                print(f"✗ Error alternativo aplicando filtros: {str(e2)}")
        
        # PASO 5: Extraer datos de eventos
        print("\n=== PASO 5: EXTRAYENDO DATOS DE EVENTOS ===")
        
        # Buscar tabla de eventos
        try:
            # Buscar tabla principal
            tablas = driver.find_elements(By.TAG_NAME, "table")
            print(f"Tablas encontradas: {len(tablas)}")
            
            tabla_eventos = None
            for i, tabla in enumerate(tablas):
                print(f"  Tabla {i+1}:")
                print(f"    - filas: {len(tabla.find_elements(By.TAG_NAME, 'tr'))}")
                print(f"    - visible: {tabla.is_displayed()}")
                if tabla.is_displayed() and len(tabla.find_elements(By.TAG_NAME, 'tr')) > 1:
                    tabla_eventos = tabla
                    print(f"    ✓ Tabla de eventos identificada")
                    break
            
            if tabla_eventos:
                # Extraer datos de la tabla
                filas = tabla_eventos.find_elements(By.TAG_NAME, "tr")
                print(f"✓ Filas en tabla de eventos: {len(filas)}")
                
                # Procesar cada fila (saltando encabezados)
                for i, fila in enumerate(filas[1:], 1):  # Saltar primera fila (encabezados)
                    try:
                        celdas = fila.find_elements(By.TAG_NAME, "td")
                        if len(celdas) >= 6:  # Asegurar que tiene suficientes columnas
                            evento_data = {
                                'NOMBRE_CLIENTE': celdas[0].text.strip() if len(celdas) > 0 else '',
                                'TIPO_EVENTO': celdas[1].text.strip() if len(celdas) > 1 else '',
                                'AGASAJADO_A': celdas[2].text.strip() if len(celdas) > 2 else '',
                                'Fecha': celdas[3].text.strip() if len(celdas) > 3 else '',
                                'Horario_Evento': celdas[4].text.strip() if len(celdas) > 4 else '',
                                'SalonAsignado': celdas[5].text.strip() if len(celdas) > 5 else '',
                                'ID_Unico_Origen': f"EVENTO_{i}"
                            }
                            
                            eventos_extraidos.append(evento_data)
                            print(f"✓ Evento {i} extraído: {evento_data['NOMBRE_CLIENTE']}")
                        else:
                            print(f"⚠ Fila {i} no tiene suficientes columnas: {len(celdas)}")
                    except Exception as e:
                        print(f"✗ Error procesando fila {i}: {str(e)}")
            else:
                print("✗ No se encontró tabla de eventos")
                
        except Exception as e:
            print(f"✗ Error extrayendo datos: {str(e)}")
        
        # PASO 6: Mostrar resultados
        print(f"\n=== RESULTADOS DE EXTRACCIÓN ===")
        print(f"Eventos extraídos: {len(eventos_extraidos)}")
        
        if eventos_extraidos:
            # Crear DataFrame
            df_eventos = pd.DataFrame(eventos_extraidos)
            print(f"\nDataFrame creado con {len(df_eventos)} eventos")
            print(f"\nPrimeros 3 eventos:")
            print(df_eventos.head(3).to_string())
            
            # Guardar en archivo CSV
            df_eventos.to_csv('eventos_adicionales.csv', index=False)
            print(f"\n✓ Datos guardados en 'eventos_adicionales.csv'")
        else:
            print("⚠ No se extrajeron eventos")
            
            # Mostrar contenido de la página para diagnóstico
            print(f"\n=== DIAGNÓSTICO ===")
            print(f"URL actual: {driver.current_url}")
            print(f"Título: {driver.title}")
            
            # Buscar mensajes en la página
            mensajes = driver.find_elements(By.XPATH, "//*[contains(text(), 'Seleccione') or contains(text(), 'adicional') or contains(text(), 'evento')]")
            print(f"Mensajes encontrados: {len(mensajes)}")
            for msg in mensajes:
                if msg.text.strip():
                    print(f"  - {msg.text}")
        
        return len(eventos_extraidos) > 0
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación...")
            print("Verifica que los filtros se aplicaron correctamente")
            time.sleep(60)  # Mantener abierto por 1 minuto
            driver.quit()

if __name__ == "__main__":
    extraer_eventos_adicionales()


