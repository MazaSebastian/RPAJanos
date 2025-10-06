#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para el RPA de eventos
Ejecuta una prueba sin programación para verificar la configuración
"""

import os
import sys
from dotenv import load_dotenv
from rpa_eventos import RPAEventos

def test_configuracion():
    """Probar que la configuración esté correcta"""
    print("=== VERIFICANDO CONFIGURACIÓN ===")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar variables requeridas
    variables = [
        'URL_ORIGEN', 'USER_ORIGEN', 'PASS_ORIGEN',
        'URL_DESTINO', 'USER_DESTINO', 'PASS_DESTINO'
    ]
    
    print("Variables de entorno configuradas:")
    for var in variables:
        valor = os.environ.get(var)
        if valor:
            # Ocultar contraseñas
            if 'PASS' in var:
                valor = '*' * len(valor)
            print(f"  ✓ {var}: {valor}")
        else:
            print(f"  ✗ {var}: NO CONFIGURADA")
    
    print("\n=== INSTRUCCIONES ===")
    print("1. Copia el archivo 'env_example.txt' a '.env'")
    print("2. Edita '.env' con tus URLs y credenciales reales")
    print("3. Configura los selectores en 'configuracion_selectores.py'")
    print("4. Ejecuta este script nuevamente para probar")

def test_rpa_manual():
    """Ejecutar el RPA manualmente para pruebas"""
    print("\n=== EJECUTANDO RPA MANUAL ===")
    
    try:
        rpa = RPAEventos()
        resultado = rpa.ejecutar_rpa()
        
        if resultado:
            print("✓ RPA ejecutado exitosamente")
        else:
            print("✗ RPA falló en la ejecución")
            print("Revisa los logs en 'rpa_eventos.log'")
        
        return resultado
        
    except Exception as e:
        print(f"✗ Error ejecutando RPA: {str(e)}")
        return False

def main():
    """Función principal de prueba"""
    print("RPA DE EVENTOS - SCRIPT DE PRUEBA")
    print("=" * 50)
    
    # Verificar configuración
    test_configuracion()
    
    # Preguntar si ejecutar el RPA
    respuesta = input("\n¿Deseas ejecutar el RPA ahora? (s/n): ").lower().strip()
    
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        test_rpa_manual()
    else:
        print("RPA no ejecutado. Configura las variables y ejecuta nuevamente.")

if __name__ == "__main__":
    main()


