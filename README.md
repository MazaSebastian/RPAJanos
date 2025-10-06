# RPA de Transferencia de Eventos

Este proyecto automatiza la transferencia de eventos entre dos sistemas web que carecen de API, utilizando técnicas de RPA (Robotic Process Automation) con Python y Selenium.

## 🚀 Características

- **Automatización completa**: Login, extracción e inserción de datos
- **Programación semanal**: Ejecución automática los lunes a las 09:00
- **Manejo robusto de errores**: Logging detallado y recuperación de fallos
- **Configuración segura**: Variables de entorno para credenciales
- **Simulación humana**: Navegación que imita comportamiento humano

## 📋 Requisitos

- Python 3.8+
- Google Chrome o Microsoft Edge
- Acceso a los dos sistemas web

## 🛠️ Instalación

1. **Clonar/descargar el proyecto**
2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno:**
   ```bash
   cp env_example.txt .env
   ```
   Edita el archivo `.env` con tus credenciales reales.

4. **Configurar selectores HTML:**
   - Edita `configuracion_selectores.py`
   - Reemplaza todos los selectores con los de tus sistemas reales

## ⚙️ Configuración

### 1. Variables de Entorno (.env)

```env
# Sistema Origen (Extracción)
URL_ORIGEN=https://tu-sistema-origen.com
USER_ORIGEN=tu_usuario_origen
PASS_ORIGEN=tu_contraseña_origen

# Sistema Destino (Inserción)
URL_DESTINO=https://tu-sistema-destino.com
USER_DESTINO=tu_usuario_destino
PASS_DESTINO=tu_contraseña_destino

# Configuración del navegador
HEADLESS_MODE=true
```

### 2. Selectores HTML

Debes reemplazar TODOS los selectores en `configuracion_selectores.py`:

#### Sistema Origen (Login):
- Campo usuario: `username`
- Campo contraseña: `password`
- Botón login: `//button[@type='submit']`

#### Sistema Origen (Extracción):
- Contenedor eventos: `eventos-lista`
- Item evento: `evento-item`
- Campos: `cliente-nombre`, `tipo-evento`, etc.

#### Sistema Destino (Login):
- Campo usuario: `usuario`
- Campo contraseña: `clave`
- Botón login: `//input[@type='submit']`

#### Sistema Destino (Inserción):
- Formulario: `formulario-evento`
- Campos: `nombre-cliente`, `tipo-evento`, etc.
- Botón guardar: `btn-guardar`

## 🚀 Uso

### Ejecución Manual (Pruebas)
```bash
python test_rpa.py
```

### Ejecución Programada
```bash
python rpa_eventos.py
```

### Ejecución Única
```python
from rpa_eventos import RPAEventos

rpa = RPAEventos()
rpa.ejecutar_rpa()
```

## 📊 Datos Extraídos

El script extrae los siguientes campos de cada evento:

- **NOMBRE_CLIENTE**: Nombre del cliente
- **TIPO_EVENTO**: Tipo de evento
- **AGASAJADO_A**: Persona agasajada
- **Fecha**: Fecha del evento (YYYY-MM-DD)
- **Horario_Evento**: Horario del evento
- **SalonAsignado**: Salón asignado
- **ID_Unico_Origen**: ID único del evento

## 📝 Logs

Los logs se guardan en `rpa_eventos.log` con información detallada:
- Inicio y fin de cada paso
- Errores y excepciones
- Número de eventos procesados
- Tiempo de ejecución

## 🔧 Solución de Problemas

### Error: "Variables de entorno faltantes"
- Verifica que el archivo `.env` existe y tiene todas las variables
- Asegúrate de que no hay espacios extra en los valores

### Error: "Timeout durante el login"
- Verifica que las URLs son correctas
- Comprueba que los selectores HTML son correctos
- Aumenta el tiempo de espera si es necesario

### Error: "No se encontraron eventos"
- Verifica que la URL de eventos es correcta
- Comprueba que los selectores de extracción son correctos
- Asegúrate de que hay eventos visibles en el sistema origen

### Error: "Falló la inserción de eventos"
- Verifica que la URL del formulario es correcta
- Comprueba que los selectores del formulario son correctos
- Asegúrate de que el formulario acepta los datos

## 📅 Programación

El script está configurado para ejecutarse:
- **Frecuencia**: Semanal
- **Día**: Lunes
- **Hora**: 09:00 AM

Para cambiar la programación, modifica la línea en `rpa_eventos.py`:
```python
schedule.every().monday.at("09:00").do(rpa.ejecutar_programado)
```

## 🔒 Seguridad

- Las credenciales se almacenan en variables de entorno
- No se codifican contraseñas en el código
- Los logs no incluyen información sensible
- El navegador se ejecuta en modo headless por defecto

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs en `rpa_eventos.log`
2. Verifica la configuración de selectores
3. Prueba el login manual en ambos sistemas
4. Ejecuta `test_rpa.py` para diagnóstico

## 📄 Licencia

Este proyecto es de uso interno. No distribuir sin autorización.


