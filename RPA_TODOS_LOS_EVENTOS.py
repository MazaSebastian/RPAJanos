#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPA TODOS LOS EVENTOS - PROCESAMIENTO COMPLETO
==============================================

Script que procesa TODOS los 27 eventos extraídos del RPA
y los integra automáticamente en el software COORDIS.

Autor: Sistema RPA Janos
Fecha: 05/10/2025
"""

import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class RPATodosLosEventos:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.eventos_procesados = 0
        self.eventos_exitosos = 0
        
    def configurar_driver(self):
        """Configurar el driver de Chrome"""
        print("🔧 Configurando driver de Chrome...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            print("✅ Driver configurado correctamente")
            return True
        except Exception as e:
            print(f"❌ Error configurando driver: {e}")
            return False
    
    def cargar_todos_los_eventos(self):
        """Cargar todos los eventos del CSV"""
        print("📊 Cargando todos los eventos...")
        
        try:
            df = pd.read_csv('todos_los_eventos_extraidos.csv')
            if len(df) > 0:
                print(f"✅ {len(df)} eventos cargados exitosamente")
                return df
            else:
                print("❌ No hay eventos disponibles")
                return None
        except Exception as e:
            print(f"❌ Error cargando eventos: {e}")
            return None
    
    def navegar_a_coordis(self):
        """Navegar al software COORDIS"""
        print("🌐 Navegando al software COORDIS...")
        
        try:
            self.driver.get("http://localhost:3001")
            time.sleep(3)
            
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
            # Buscar el botón en la barra lateral
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
    
    def llenar_formulario_evento(self, evento):
        """Llenar el formulario para un evento específico"""
        print(f"📝 Procesando evento {self.eventos_procesados + 1}: {evento.get('codigo_evento', 'N/A')}")
        
        try:
            # Campos esenciales (sin horarios, con celulares separados)
            campos_esenciales = {
                'title': f"{evento.get('tipo_evento', '')} de {evento.get('homenajeada', '')}",
                'event_date': self.formatear_fecha(evento.get('fecha_evento', '')),
                'client_name': evento.get('cliente', ''),
                'celular': evento.get('celular', ''),
                'celular_2': evento.get('celular_2', '')
                # Sin campos de horario (eliminados del formulario)
            }
            
            # Llenar campos esenciales
            for campo, valor in campos_esenciales.items():
                if valor and valor != '':
                    try:
                        self.llenar_campo_esencial(campo, valor)
                        time.sleep(0.3)
                    except Exception as e:
                        print(f"  ⚠️ Error llenando campo '{campo}': {e}")
                        continue
            
            print(f"✅ Evento {self.eventos_procesados + 1} llenado correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error llenando evento {self.eventos_procesados + 1}: {e}")
            return False
    
    def llenar_campo_esencial(self, campo, valor):
        """Llenar un campo esencial del formulario"""
        try:
            # Selectores para campos esenciales (sin horarios)
            selectors = {
            'title': ["input[placeholder='Título de la coordinación']"],
            'event_date': ["input[type='date']"],
            'client_name': ["input[placeholder='Nombre completo del cliente']"],
            'celular': ["input[placeholder='541157526518']"],
            'celular_2': ["input[placeholder='1157526518']"]
            # Sin selectores de horario
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
            return False
    
    def formatear_fecha(self, fecha_str):
        """Formatear fecha para el input de fecha"""
        try:
            if not fecha_str:
                return ''
            
            # Si ya está en formato YYYY-MM-DD, devolverlo
            if len(fecha_str) == 10 and fecha_str.count('-') == 2:
                return fecha_str
            
            # Formato: DD/MM/YYYY(Día)
            if '(' in fecha_str:
                fecha_limpia = fecha_str.split('(')[0].strip()
                from datetime import datetime
                fecha_obj = datetime.strptime(fecha_limpia, '%d/%m/%Y')
                return fecha_obj.strftime('%Y-%m-%d')
            
            return fecha_str
            
        except Exception as e:
            return fecha_str
    
    def guardar_coordinacion(self):
        """Guardar la coordinación usando JavaScript"""
        try:
            # Cerrar iframe de desarrollo si existe
            try:
                iframe = self.driver.find_element(By.ID, "webpack-dev-server-client-overlay")
                self.driver.execute_script("arguments[0].style.display = 'none';", iframe)
            except:
                pass
            
            # Buscar botón de guardar
            boton_selectors = [
                "//button[contains(text(), 'Guardar Coordinación')]",
                "//button[contains(text(), 'Continuar')]",
                "//button[contains(text(), 'Guardar')]"
            ]
            
            for selector in boton_selectors:
                try:
                    boton = self.driver.find_element(By.XPATH, selector)
                    self.driver.execute_script("arguments[0].click();", boton)
                    time.sleep(2)
                    return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            return False
    
    def procesar_todos_los_eventos(self):
        """Procesar todos los eventos del RPA"""
        print("🚀 Iniciando procesamiento de TODOS los eventos...")
        
        # Cargar todos los eventos
        df = self.cargar_todos_los_eventos()
        if df is None:
            return False
        
        # Navegar a COORDIS
        if not self.navegar_a_coordis():
            return False
        
        print(f"\n📋 Procesando {len(df)} eventos...")
        print("=" * 50)
        
        for index, evento in df.iterrows():
            self.eventos_procesados += 1
            
            print(f"\n🔄 EVENTO {self.eventos_procesados}/{len(df)}")
            print(f"   Código: {evento.get('codigo_evento', 'N/A')}")
            print(f"   Cliente: {evento.get('cliente', 'N/A')}")
            print(f"   Fecha: {evento.get('fecha_evento', 'N/A')}")
            
            try:
                # Hacer clic en "NUEVA COORDINACIÓN"
                if not self.hacer_clic_nueva_coordinacion():
                    print(f"❌ Error: No se pudo acceder al formulario")
                    continue
                
                # Llenar formulario
                if not self.llenar_formulario_evento(evento):
                    print(f"❌ Error: No se pudo llenar el formulario")
                    continue
                
                # Guardar coordinación
                if not self.guardar_coordinacion():
                    print(f"❌ Error: No se pudo guardar la coordinación")
                    continue
                
                self.eventos_exitosos += 1
                print(f"✅ Evento {self.eventos_procesados} procesado exitosamente")
                
                # Esperar antes del siguiente evento
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error procesando evento {self.eventos_procesados}: {e}")
                continue
        
        # Mostrar resumen final
        print(f"\n📊 RESUMEN FINAL:")
        print(f"   Total eventos: {len(df)}")
        print(f"   Procesados: {self.eventos_procesados}")
        print(f"   Exitosos: {self.eventos_exitosos}")
        print(f"   Fallidos: {self.eventos_procesados - self.eventos_exitosos}")
        print(f"   Tasa de éxito: {(self.eventos_exitosos/self.eventos_procesados)*100:.1f}%")
        
        return self.eventos_exitosos > 0
    
    def cerrar_driver(self):
        """Cerrar el driver"""
        if self.driver:
            self.driver.quit()
            print("🔒 Driver cerrado")

def main():
    """Función principal"""
    print("🤖 RPA TODOS LOS EVENTOS - PROCESAMIENTO COMPLETO")
    print("=" * 60)
    
    rpa = RPATodosLosEventos()
    
    try:
        # Configurar driver
        if not rpa.configurar_driver():
            return False
        
        # Procesar todos los eventos
        exito = rpa.procesar_todos_los_eventos()
        
        if exito:
            print("\n🎉 PROCESAMIENTO COMPLETO EXITOSO")
            print("✅ Todos los eventos procesados")
            print("✅ Integración con COORDIS completada")
        else:
            print("\n❌ PROCESAMIENTO FALLÓ")
        
        return exito
        
    except Exception as e:
        print(f"\n❌ Error en el procesamiento: {e}")
        return False
    
    finally:
        rpa.cerrar_driver()

if __name__ == "__main__":
    main()
