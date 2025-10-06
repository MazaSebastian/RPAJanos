#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archivo de configuración de selectores HTML
REEMPLAZA TODOS LOS SELECTORES CON LOS DE TUS SISTEMAS REALES
"""

# =============================================================================
# CONFIGURACIÓN DEL SISTEMA ORIGEN (Extracción de eventos)
# =============================================================================

# Selectores para el login del sistema origen
LOGIN_ORIGEN = {
    'username_field': "username",  # ID del campo de usuario
    'password_field': "password",  # ID del campo de contraseña
    'login_button': "//button[@type='submit']",  # XPath del botón de login
    'success_indicator': "dashboard"  # Clase que aparece después del login exitoso
}

# Selectores para la extracción de eventos
EXTRACCION_EVENTOS = {
    'eventos_url': "/eventos",  # Ruta relativa a la URL origen para ver eventos
    'eventos_container': "eventos-lista",  # Clase del contenedor de eventos
    'evento_item': "evento-item",  # Clase de cada evento individual
    'cliente_nombre': "cliente-nombre",  # Clase del nombre del cliente
    'tipo_evento': "tipo-evento",  # Clase del tipo de evento
    'agasajado': "agasajado",  # Clase del agasajado/a
    'fecha_evento': "fecha-evento",  # Clase de la fecha del evento
    'horario_evento': "horario-evento",  # Clase del horario del evento
    'salon': "salon",  # Clase del salón asignado
    'evento_id': "data-id"  # Atributo que contiene el ID único del evento
}

# =============================================================================
# CONFIGURACIÓN DEL SISTEMA DESTINO (Inserción de eventos)
# =============================================================================

# Selectores para el login del sistema destino
LOGIN_DESTINO = {
    'username_field': "usuario",  # ID del campo de usuario
    'password_field': "clave",  # ID del campo de contraseña
    'login_button': "//input[@type='submit']",  # XPath del botón de login
    'success_indicator': "menu-principal"  # Clase que aparece después del login exitoso
}

# Selectores para la inserción de eventos
INSERCION_EVENTOS = {
    'nuevo_evento_url': "/nuevo-evento",  # Ruta relativa para crear nuevo evento
    'formulario': "formulario-evento",  # ID del formulario de evento
    'nombre_cliente': "nombre-cliente",  # ID del campo nombre cliente
    'tipo_evento': "tipo-evento",  # ID del campo tipo evento
    'agasajado': "agasajado",  # ID del campo agasajado/a
    'fecha_evento': "fecha-evento",  # ID del campo fecha
    'horario_evento': "horario-evento",  # ID del campo horario
    'salon_asignado': "salon-asignado",  # ID del campo salón
    'btn_guardar': "btn-guardar",  # ID del botón guardar
    'mensaje_exito': "mensaje-exito"  # Clase que aparece después de guardar exitosamente
}

# =============================================================================
# INSTRUCCIONES DE CONFIGURACIÓN
# =============================================================================

"""
PASOS PARA CONFIGURAR TUS SELECTORES:

1. SISTEMA ORIGEN (Extracción):
   - Abre tu navegador y ve al sistema origen
   - Haz login manualmente
   - Inspecciona los elementos HTML (clic derecho > Inspeccionar elemento)
   - Copia los selectores reales y reemplaza los valores en LOGIN_ORIGEN y EXTRACCION_EVENTOS

2. SISTEMA DESTINO (Inserción):
   - Abre tu navegador y ve al sistema destino
   - Haz login manualmente
   - Ve al formulario de "Nuevo Evento"
   - Inspecciona los elementos HTML
   - Copia los selectores reales y reemplaza los valores en LOGIN_DESTINO e INSERCION_EVENTOS

3. TIPOS DE SELECTORES MÁS COMUNES:
   - Por ID: "mi-id" (usar con By.ID)
   - Por clase: "mi-clase" (usar con By.CLASS_NAME)
   - Por XPath: "//div[@class='mi-clase']" (usar con By.XPATH)
   - Por CSS: "div.mi-clase" (usar con By.CSS_SELECTOR)

4. EJEMPLOS DE SELECTORES REALES:
   - Campo usuario: "input[name='username']" o "//input[@name='username']"
   - Botón login: "button[type='submit']" o "//button[contains(text(),'Login')]"
   - Lista eventos: "div.event-list" o "//div[contains(@class,'event')]"
   - Campo formulario: "input[name='cliente']" o "//input[@name='cliente']"

5. VERIFICACIÓN:
   - Usa las herramientas de desarrollador del navegador
   - Prueba los selectores en la consola: document.querySelector('tu-selector')
   - Asegúrate de que los selectores sean únicos y específicos
"""


