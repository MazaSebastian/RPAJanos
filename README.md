# RPA Jano's Eventos

Sistema automatizado de transferencia de eventos entre plataformas web utilizando RPA (Robotic Process Automation) con Python, Selenium y Node.js.

## 🎯 ¡NUEVO! Sistema de Producción

**El sistema ha sido completamente refactorizado y está listo para producción.**

👉 **[Ver Sistema de Producción →](production/)**

### 🚀 Características del Sistema de Producción

- **Arquitectura Modular**: Código organizado en componentes reutilizables
- **API REST Completo**: Gestión de coordinaciones con Node.js/Express
- **Logger Profesional**: Sistema de logs estructurados con rotación automática
- **Configuración Centralizada**: Variables de entorno y validaciones
- **Scripts de Deployment**: Inicio/detención automatizada del sistema
- **Documentación Exhaustiva**: 4 guías completas (README, Inicio Rápido, Migración, Resumen)
- **Manejo Robusto de Errores**: Reintentos automáticos y recuperación
- **Backups Automáticos**: Respaldo de datos y CSV

## 📋 Requisitos

- Python 3.8+
- Google Chrome o Microsoft Edge
- Acceso a los dos sistemas web

## 🛠️ Instalación Rápida

### Sistema de Producción (Recomendado)

```bash
cd production
./scripts/start_system.sh
python3 src/main.py
```

**[📖 Ver Guía Completa de Instalación](production/INICIO_RAPIDO.md)**

### Sistema Legacy (Archivos antiguos)

Los archivos originales están disponibles en la raíz del proyecto para referencia.

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno:**
   ```bash
   cp env_example.txt .env
   ```
   Edita el archivo `.env` con tus credenciales reales

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

## 🎯 Sistema de Producción

### Estructura del Proyecto

```
production/
├── src/
│   ├── main.py                    # Script principal
│   ├── rpa/extractor_eventos.py   # Extractor RPA
│   ├── api/server.js              # API Server
│   ├── sync/sincronizador.py      # Sincronizador
│   └── utils/                     # Config + Logger
├── scripts/                       # Scripts de deployment
├── config/                        # Configuración
└── docs/                          # Documentación
```

### Documentación Disponible

- **[README.md](production/README.md)** - Documentación completa del sistema
- **[INICIO_RAPIDO.md](production/INICIO_RAPIDO.md)** - Guía de inicio en 5 minutos
- **[MIGRACION.md](production/MIGRACION.md)** - Guía de migración
- **[RESUMEN_SISTEMA.md](production/RESUMEN_SISTEMA.md)** - Vista ejecutiva

### Inicio Rápido

```bash
# 1. Ir al directorio de producción
cd production

# 2. Configurar credenciales
nano config/production.env

# 3. Iniciar sistema
./scripts/start_system.sh

# 4. Ejecutar RPA
python3 src/main.py
```

## 📄 Licencia

Este proyecto es de uso interno. No distribuir sin autorización.

---

**Desarrollado por:** Sebastian Maza  
**Repositorio:** https://github.com/MazaSebastian/RPAJanos  
**Versión Producción:** 1.0.0


