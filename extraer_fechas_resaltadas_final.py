#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script final para extraer fechas resaltadas en naranja del calendario
- Usa los selectores correctos identificados: div.boton[style*="background:"]
- Navega por todo el calendario anual
- Extrae datos de eventos de fechas resaltadas
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def extraer_fechas_resaltadas_final():
    """Extraer fechas resaltadas en naranja del calendario completo"""
    
    print("=== EXTRACCIÓN FINAL DE FECHAS RESALTADAS ===")
    print("Usando selectores correctos: div.boton[style*='background:']")
    print("Navegando por todo el calendario anual...")
    
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
        actions = ActionChains(driver)
        
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
        
        # Filtro ZONA: CABA
        print("Aplicando filtro ZONA: CABA")
        try:
            zona_select = Select(driver.find_element(By.ID, "cluster"))
            zona_select.select_by_visible_text("CABA")
            print("✓ Filtro ZONA aplicado: CABA")
        except Exception as e:
            print(f"✗ Error aplicando filtro ZONA: {str(e)}")
        
        # Filtro AÑO: 2025
        print("Aplicando filtro AÑO: 2025")
        try:
            ano_select = Select(driver.find_element(By.ID, "ano"))
            ano_select.select_by_visible_text("2025")
            print("✓ Filtro AÑO aplicado: 2025")
        except Exception as e:
            print(f"✗ Error aplicando filtro AÑO: {str(e)}")
        
        # Aplicar filtros
        print("Aplicando filtros...")
        try:
            filtrar_buttons = driver.find_elements(By.XPATH, "//input[@value='Filtrar']")
            if filtrar_buttons:
                filtrar_buttons[0].click()
                time.sleep(5)  # Esperar a que se procesen los filtros
                print("✓ Filtros aplicados")
        except Exception as e:
            print(f"✗ Error aplicando filtros: {str(e)}")
        
        # PASO 4: Extraer fechas resaltadas
        print("\n=== PASO 4: EXTRAYENDO FECHAS RESALTADAS ===")
        
        # Función para extraer fechas resaltadas de un mes específico
        def extraer_fechas_mes(mes_nombre):
            print(f"\n--- Procesando {mes_nombre} ---")
            fechas_mes = []
            
            try:
                # Buscar el mes específico
                mes_element = driver.find_element(By.XPATH, f"//span[contains(text(), '{mes_nombre}')]")
                print(f"✓ Mes {mes_nombre} encontrado")
                
                # Buscar la tabla del mes
                tabla_mes = mes_element.find_element(By.XPATH, "./following-sibling::table")
                print(f"✓ Tabla de {mes_nombre} encontrada")
                
                # Buscar fechas resaltadas usando el selector correcto
                fechas_resaltadas = tabla_mes.find_elements(By.CSS_SELECTOR, "div.boton[style*='background:']")
                
                print(f"✓ Fechas resaltadas en {mes_nombre}: {len(fechas_resaltadas)}")
                
                for fecha_elem in fechas_resaltadas:
                    try:
                        fecha_numero = fecha_elem.text.strip()
                        if fecha_numero.isdigit():
                            # Obtener el color de fondo
                            style = fecha_elem.get_attribute('style')
                            color_fondo = "desconocido"
                            if "background:" in style:
                                color_fondo = style.split("background:")[1].split(";")[0].strip()
                            
                            fecha_completa = f"{fecha_numero}/{mes_nombre}/2025"
                            fechas_mes.append({
                                'fecha': fecha_completa,
                                'numero': fecha_numero,
                                'mes': mes_nombre,
                                'color': color_fondo,
                                'elemento': fecha_elem
                            })
                            print(f"  - Fecha resaltada: {fecha_completa} (color: {color_fondo})")
                    except Exception as e:
                        print(f"✗ Error procesando fecha: {str(e)}")
                
            except Exception as e:
                print(f"✗ Error procesando {mes_nombre}: {str(e)}")
            
            return fechas_mes
        
        # Lista de todos los meses
        meses = [
            "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
            "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
        ]
        
        todas_fechas_eventos = []
        
        # Scroll hacia arriba para ver los primeros meses
        print("Haciendo scroll hacia arriba para ver Enero-Junio...")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        # Procesar primeros 6 meses (Enero-Junio)
        for mes in meses[:6]:
            fechas_mes = extraer_fechas_mes(mes)
            todas_fechas_eventos.extend(fechas_mes)
            
            # Scroll hacia abajo para ver el siguiente mes
            driver.execute_script("window.scrollBy(0, 200);")
            time.sleep(1)
        
        # Scroll hacia abajo para ver los últimos meses
        print("Haciendo scroll hacia abajo para ver Julio-Diciembre...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Procesar últimos 6 meses (Julio-Diciembre)
        for mes in meses[6:]:
            fechas_mes = extraer_fechas_mes(mes)
            todas_fechas_eventos.extend(fechas_mes)
            
            # Scroll hacia arriba para ver el siguiente mes
            driver.execute_script("window.scrollBy(0, -200);")
            time.sleep(1)
        
        # PASO 5: Procesar fechas encontradas
        print(f"\n=== PASO 5: PROCESANDO FECHAS ENCONTRADAS ===")
        print(f"Total de fechas con eventos: {len(todas_fechas_eventos)}")
        
        if todas_fechas_eventos:
            print(f"\nFechas resaltadas encontradas:")
            for i, fecha_data in enumerate(todas_fechas_eventos, 1):
                print(f"  {i}. {fecha_data['fecha']} (color: {fecha_data['color']})")
                
                # Crear entrada de evento para cada fecha
                evento_data = {
                    'NOMBRE_CLIENTE': f'Cliente_{i}',
                    'TIPO_EVENTO': 'Evento Adicional',
                    'AGASAJADO_A': f'Agasajado_{i}',
                    'Fecha': fecha_data['fecha'],
                    'Horario_Evento': 'Por definir',
                    'SalonAsignado': 'DOT',
                    'ID_Unico_Origen': f"EVENTO_{i}_{fecha_data['fecha'].replace('/', '_')}",
                    'Color_Fondo': fecha_data['color']
                }
                
                eventos_extraidos.append(evento_data)
            
            # Crear DataFrame
            df_eventos = pd.DataFrame(eventos_extraidos)
            print(f"\nDataFrame creado con {len(df_eventos)} eventos")
            
            # Mostrar resumen por mes
            print(f"\nResumen por mes:")
            for mes in meses:
                eventos_mes = [e for e in eventos_extraidos if mes in e['Fecha']]
                if eventos_mes:
                    print(f"  {mes}: {len(eventos_mes)} eventos")
                    for evento in eventos_mes:
                        print(f"    - {evento['Fecha']} (color: {evento['Color_Fondo']})")
            
            # Guardar en archivo CSV
            df_eventos.to_csv('eventos_fechas_resaltadas.csv', index=False)
            print(f"\n✓ Datos guardados en 'eventos_fechas_resaltadas.csv'")
        else:
            print("⚠ No se encontraron fechas resaltadas")
            print("Esto puede indicar que:")
            print("  - No hay eventos programados para los filtros aplicados")
            print("  - Los filtros no están mostrando eventos")
            print("  - Las fechas resaltadas tienen un estilo diferente")
            
            # Mostrar diagnóstico adicional
            print(f"\n=== DIAGNÓSTICO ADICIONAL ===")
            
            # Buscar todos los divs con clase boton
            todos_botones = driver.find_elements(By.CSS_SELECTOR, "div.boton")
            print(f"Total de divs con clase 'boton': {len(todos_botones)}")
            
            # Buscar divs con background no vacío
            botones_con_background = driver.find_elements(By.CSS_SELECTOR, "div.boton[style*='background:']")
            print(f"Divs con background no vacío: {len(botones_con_background)}")
            
            # Mostrar algunos ejemplos
            for i, boton in enumerate(botones_con_background[:5]):
                print(f"  Botón {i+1}: text='{boton.text}', style='{boton.get_attribute('style')}'")
        
        # PASO 6: Mostrar resultados finales
        print(f"\n=== RESULTADOS FINALES ===")
        print(f"Eventos extraídos: {len(eventos_extraidos)}")
        print(f"Fechas resaltadas encontradas: {len(todas_fechas_eventos)}")
        
        if eventos_extraidos:
            print(f"\nPrimeros 3 eventos:")
            df_eventos = pd.DataFrame(eventos_extraidos)
            print(df_eventos.head(3).to_string())
        
        return len(eventos_extraidos) > 0
        
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        return False
    
    finally:
        if driver:
            print("\nManteniendo navegador abierto para verificación...")
            print("Verifica que se identificaron las fechas resaltadas correctamente")
            time.sleep(120)  # Mantener abierto por 2 minutos
            driver.quit()

if __name__ == "__main__":
    extraer_fechas_resaltadas_final()


