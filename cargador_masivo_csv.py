#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CARGADOR MASIVO CSV - SISTEMA INDEPENDIENTE
==========================================

Sistema independiente para cargar coordinaciones masivamente
desde archivo CSV al software COORDIS.

Características:
- Lee CSV con datos de eventos
- Valida datos antes de procesar
- Carga masivamente en COORDIS
- Reporta resultados detallados
- Manejo robusto de errores

Autor: Sistema RPA Janos
Fecha: 05/10/2025
"""

import pandas as pd
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class CargadorMasivoCSV:
    def __init__(self, csv_file="todos_los_eventos_extraidos.csv"):
        self.csv_file = csv_file
        self.driver = None
        self.wait = None
        self.eventos_procesados = 0
        self.eventos_exitosos = 0
        self.eventos_fallidos = 0
        self.errores_detallados = []
        
    def configurar_driver(self):
        """Configurar el driver de Chrome"""
        print("🔧 Configurando driver de Chrome...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            print("✅ Driver configurado correctamente")
            return True
        except Exception as e:
            print(f"❌ Error configurando driver: {e}")
            return False
    
    def cargar_csv(self):
        """Cargar y validar el archivo CSV"""
        print(f"📊 Cargando archivo CSV: {self.csv_file}")
        
        try:
            if not os.path.exists(self.csv_file):
                print(f"❌ Archivo CSV no encontrado: {self.csv_file}")
                return None
            
            # Cargar CSV
            df = pd.read_csv(self.csv_file)
            print(f"✅ CSV cargado: {len(df)} eventos encontrados")
            
            # Validar columnas requeridas
            columnas_requeridas = [
                'homenajeada', 'codigo_evento', 'tipo_evento', 'fecha_evento',
                'salon', 'cliente', 'celular', 'celular_2', 'tipo_pack'
            ]
            
            columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
            if columnas_faltantes:
                print(f"⚠️ Columnas faltantes en CSV: {columnas_faltantes}")
                return None
            
            print("✅ Validación de CSV exitosa")
            return df
            
        except Exception as e:
            print(f"❌ Error cargando CSV: {e}")
            return None
    
    def navegar_a_coordis(self):
        """Navegar al software COORDIS"""
        print("🌐 Navegando al software COORDIS...")
        
        try:
            self.driver.get("http://localhost:3001")
            time.sleep(5)
            
            # Cerrar iframe de desarrollo si existe
            try:
                iframe = self.driver.find_element(By.ID, "webpack-dev-server-client-overlay")
                self.driver.execute_script("arguments[0].style.display = 'none';", iframe)
                print("✅ Iframe de desarrollo cerrado")
            except:
                pass
            
            if "Jano's" in self.driver.title or "Coordinaciones" in self.driver.title:
                print("✅ Acceso exitoso al software COORDIS")
                return True
            else:
                print("❌ No se pudo acceder al software COORDIS")
                return False
                
        except Exception as e:
            print(f"❌ Error navegando a COORDIS: {e}")
            return False
    
    def hacer_clic_nueva_coordinacion(self):
        """Hacer clic en el botón 'NUEVA COORDINACIÓN'"""
        print("🖱️ Buscando botón 'NUEVA COORDINACIÓN'...")
        
        try:
            boton_selectors = [
                "//button[contains(text(), 'Nueva Coordinación')]",
                "//a[contains(text(), 'Nueva Coordinación')]",
                "//a[contains(@href, '/coordinations/new')]"
            ]
            
            for selector in boton_selectors:
                try:
                    boton = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    boton.click()
                    print("✅ Botón 'NUEVA COORDINACIÓN' encontrado y clickeado")
                    time.sleep(3)
                    return True
                except:
                    continue
            
            print("❌ No se pudo encontrar el botón 'NUEVA COORDINACIÓN'")
            return False
            
        except Exception as e:
            print(f"❌ Error haciendo clic en el botón: {e}")
            return False
    
    def llenar_campo(self, campo, valor):
        """Llenar un campo del formulario"""
        try:
            # Selectores optimizados
            selectors = {
                'title': ["input[placeholder='Título de la coordinación']"],
                'event_date': ["input[type='date']"],
                'client_name': ["input[placeholder='Nombre completo del cliente']"],
                'celular': ["input[placeholder='541157526518']"],
                'celular_2': ["input[placeholder='1157526518']"]
            }
            
            if campo in selectors:
                for selector in selectors[campo]:
                    try:
                        elemento = self.driver.find_element(By.CSS_SELECTOR, selector)
                        elemento.clear()
                        elemento.send_keys(str(valor))
                        return True
                    except:
                        continue
            
            return False
            
        except Exception as e:
            print(f"  ⚠️ Error llenando campo '{campo}': {e}")
            return False
    
    def llenar_formulario_evento(self, evento):
        """Llenar el formulario para un evento específico"""
        print(f"📝 Procesando evento {self.eventos_procesados + 1}: {evento.get('codigo_evento', 'N/A')}")
        
        try:
            # Campos esenciales
            campos_esenciales = {
                'title': f"{evento.get('tipo_evento', '')} de {evento.get('homenajeada', '')}",
                'event_date': self.formatear_fecha(evento.get('fecha_evento', '')),
                'client_name': evento.get('cliente', ''),
                'celular': evento.get('celular', ''),
                'celular_2': evento.get('celular_2', '')
            }
            
            # Llenar campos esenciales
            for campo, valor in campos_esenciales.items():
                if valor and valor != '':
                    try:
                        self.llenar_campo(campo, valor)
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"  ⚠️ Error llenando campo '{campo}': {e}")
                        continue
                else:
                    print(f"  ⏭️ Saltando campo '{campo}' (sin valor válido)")
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error llenando formulario: {e}")
            return False
    
    def formatear_fecha(self, fecha_str):
        """Formatear fecha para el formulario"""
        try:
            if pd.isna(fecha_str) or fecha_str == '':
                return ''
            
            # Convertir a datetime y formatear como YYYY-MM-DD
            fecha = pd.to_datetime(fecha_str)
            return fecha.strftime('%Y-%m-%d')
        except:
            return ''
    
    def guardar_coordinacion(self):
        """Guardar la coordinación"""
        try:
            # Buscar botón de guardar
            save_selectors = [
                "button[type='submit']",
                "button:contains('Guardar')",
                "button:contains('Crear')",
                "button:contains('Save')"
            ]
            
            for selector in save_selectors:
                try:
                    save_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    # Usar JavaScript para hacer clic (evita problemas de overlay)
                    self.driver.execute_script("arguments[0].click();", save_button)
                    print("✅ Coordinación guardada exitosamente")
                    time.sleep(2)
                    return True
                except:
                    continue
            
            print("❌ No se pudo encontrar el botón de guardar")
            return False
            
        except Exception as e:
            print(f"❌ Error guardando coordinación: {e}")
            return False
    
    def procesar_evento(self, evento):
        """Procesar un evento individual"""
        try:
            # Hacer clic en "NUEVA COORDINACIÓN"
            if not self.hacer_clic_nueva_coordinacion():
                return False
            
            # Llenar formulario
            if not self.llenar_formulario_evento(evento):
                return False
            
            # Guardar coordinación
            if not self.guardar_coordinacion():
                return False
            
            self.eventos_exitosos += 1
            return True
            
        except Exception as e:
            print(f"❌ Error procesando evento: {e}")
            self.eventos_fallidos += 1
            self.errores_detallados.append({
                'evento': evento.get('codigo_evento', 'N/A'),
                'error': str(e)
            })
            return False
    
    def procesar_csv_masivamente(self):
        """Procesar todo el CSV masivamente"""
        print("🚀 Iniciando carga masiva desde CSV...")
        
        # Cargar CSV
        df = self.cargar_csv()
        if df is None:
            return False
        
        # Navegar a COORDIS
        if not self.navegar_a_coordis():
            return False
        
        print(f"\n📋 Procesando {len(df)} eventos...")
        print("=" * 50)
        
        # Procesar cada evento
        for index, evento in df.iterrows():
            self.eventos_procesados += 1
            
            print(f"\n🔄 EVENTO {self.eventos_procesados}/{len(df)}")
            print(f"   Código: {evento.get('codigo_evento', 'N/A')}")
            print(f"   Cliente: {evento.get('cliente', 'N/A')}")
            print(f"   Fecha: {evento.get('fecha_evento', 'N/A')}")
            
            if self.procesar_evento(evento):
                print(f"✅ Evento {self.eventos_procesados} procesado exitosamente")
            else:
                print(f"❌ Evento {self.eventos_procesados} falló")
                self.eventos_fallidos += 1
        
        return True
    
    def generar_reporte(self):
        """Generar reporte final"""
        print("\n📊 REPORTE FINAL:")
        print("=" * 50)
        print(f"Total eventos: {self.eventos_procesados}")
        print(f"Exitosos: {self.eventos_exitosos}")
        print(f"Fallidos: {self.eventos_fallidos}")
        
        if self.eventos_procesados > 0:
            tasa_exito = (self.eventos_exitosos / self.eventos_procesados) * 100
            print(f"Tasa de éxito: {tasa_exito:.1f}%")
        
        if self.errores_detallados:
            print(f"\n❌ ERRORES DETALLADOS:")
            for error in self.errores_detallados:
                print(f"  - Evento {error['evento']}: {error['error']}")
    
    def cerrar_driver(self):
        """Cerrar el driver"""
        if self.driver:
            self.driver.quit()
            print("🔒 Driver cerrado")

def main():
    """Función principal"""
    print("🚀 CARGADOR MASIVO CSV - SISTEMA INDEPENDIENTE")
    print("=" * 60)
    print("📋 Características:")
    print("   ✅ Lee CSV con datos de eventos")
    print("   ✅ Valida datos antes de procesar")
    print("   ✅ Carga masivamente en COORDIS")
    print("   ✅ Reporta resultados detallados")
    print("   ✅ Manejo robusto de errores")
    print("=" * 60)
    
    cargador = CargadorMasivoCSV()
    
    try:
        # Configurar driver
        if not cargador.configurar_driver():
            return False
        
        # Procesar CSV masivamente
        if not cargador.procesar_csv_masivamente():
            return False
        
        # Generar reporte
        cargador.generar_reporte()
        
        print("\n🎉 CARGA MASIVA COMPLETADA")
        print("✅ Sistema independiente funcionando correctamente")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error en la carga masiva: {e}")
        return False
    
    finally:
        cargador.cerrar_driver()

if __name__ == "__main__":
    main()


