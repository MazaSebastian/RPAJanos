# RPA Jano's Eventos - Sistema de Producción

## 📋 Descripción

Sistema automatizado de transferencia de eventos entre plataformas web utilizando RPA (Robotic Process Automation) con Python, Selenium y Node.js. Optimiza procesos de gestión de eventos mediante extracción e inserción inteligente de datos.

**Versión:** 1.0.0 (Producción)  
**Ambiente:** Producción  
**Última actualización:** Octubre 2025

---

## 🏗️ Arquitectura del Sistema

El sistema consta de 4 componentes principales:

### 1. **Extractor RPA** (`src/rpa/`)
- Extrae eventos del sistema Janos usando Selenium
- Navegación automatizada con simulación humana
- Manejo robusto de errores y reintentos
- Genera CSV con datos extraídos

### 2. **API Server** (`src/api/`)
- Servidor Node.js/Express
- Gestiona coordinaciones en memoria y archivo JSON
- Endpoints REST completos
- Detección de duplicados y cambios

### 3. **Sincronizador** (`src/sync/`)
- Sincroniza datos entre API y frontend COORDIS
- Transformación de formatos
- Genera scripts de inyección para localStorage

### 4. **Utilidades** (`src/utils/`)
- Sistema de configuración centralizado
- Logger profesional con rotación
- Validaciones y helpers

---

## 📁 Estructura de Directorios

```
production/
├── config/               # Configuraciones
│   └── production.env   # Variables de entorno
├── src/                 # Código fuente
│   ├── api/            # API Server (Node.js)
│   │   └── server.js
│   ├── rpa/            # Módulos RPA (Python)
│   │   └── extractor_eventos.py
│   ├── sync/           # Sincronización
│   │   └── sincronizador.py
│   ├── utils/          # Utilidades
│   │   ├── config.py
│   │   └── logger.py
│   └── main.py         # Script principal
├── scripts/            # Scripts de deployment
│   ├── start_system.sh
│   └── stop_system.sh
├── logs/               # Logs del sistema
├── data/               # Datos (CSV, JSON)
│   └── backups/       # Backups automáticos
├── tests/             # Tests (futuro)
├── docs/              # Documentación adicional
├── package.json       # Dependencias Node.js
└── README.md          # Este archivo
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- **Python 3.8+**
- **Node.js 14+**
- **Google Chrome** (para Selenium)
- **Git** (para control de versiones)

### Paso 1: Instalar Dependencias

#### Dependencias Python
```bash
cd production
pip3 install -r ../requirements.txt
```

Dependencias principales:
- selenium
- pandas
- requests
- python-dotenv
- flask
- flask-cors

#### Dependencias Node.js
```bash
cd production
npm install
```

Dependencias principales:
- express
- body-parser
- cors

### Paso 2: Configurar Variables de Entorno

1. Editar el archivo `config/production.env`:

```bash
nano config/production.env
```

2. Configurar las credenciales y URLs:

```env
# Sistema Origen (JANOS)
URL_ORIGEN=https://tecnica.janosgroup.com/login.php
USER_ORIGEN=tu_usuario
PASS_ORIGEN=tu_contraseña

# Sistema Destino (COORDIS)
URL_COORDIS=http://localhost:3001
API_COORDIS=http://localhost:3002

# Configuración de Ejecución
HEADLESS_MODE=true
LOG_LEVEL=INFO
BACKUP_ENABLED=true
```

3. **IMPORTANTE:** Nunca commitear este archivo con credenciales reales.

### Paso 3: Verificar Configuración

```bash
cd production
python3 src/main.py --health
```

Este comando verifica:
- ✅ Configuración válida
- ✅ Directorios creados
- ✅ API accesible
- ✅ Sistema listo

---

## 🎮 Uso del Sistema

### Iniciar el Sistema

```bash
./scripts/start_system.sh
```

Esto iniciará:
- ✅ API Server en puerto 3002
- ✅ Verificación de salud
- ✅ Creación de directorios

### Ejecutar el RPA

#### Flujo Completo (Extracción + Sincronización)
```bash
python3 src/main.py
```

#### Solo Extracción
```bash
python3 src/main.py --extract
```

#### Solo Sincronización
```bash
python3 src/main.py --sync
```

#### Verificar Salud del Sistema
```bash
python3 src/main.py --health
```

### Detener el Sistema

```bash
./scripts/stop_system.sh
```

---

## 📊 API Endpoints

### Health Check
```bash
GET http://localhost:3002/api/health
```

### Obtener Coordinaciones
```bash
# Todas
GET http://localhost:3002/api/coordinations

# Con filtros
GET http://localhost:3002/api/coordinations?status=pendiente
GET http://localhost:3002/api/coordinations?salon=DOT
```

### Crear/Actualizar Coordinación
```bash
POST http://localhost:3002/api/coordinations
Content-Type: application/json

{
  "title": "Cumpleaños 15",
  "client_name": "María García",
  "celular": "1234567890",
  "event_date": "2025-12-15",
  "honoree_name": "María",
  "codigo_evento": "EVT001",
  "salon": "DOT",
  "event_type": "15años"
}
```

### Carga Masiva
```bash
POST http://localhost:3002/api/coordinations/bulk
Content-Type: application/json

{
  "coordinations": [
    { ... },
    { ... }
  ]
}
```

---

## 📝 Logs

### Ubicación de Logs

- **RPA General:** `logs/rpa_janos.log`
- **Errores:** `logs/rpa_janos_errors.log`
- **Logs Diarios:** `logs/rpa_janos_daily.log`
- **API Server:** `logs/api_server.log`

### Ver Logs en Tiempo Real

```bash
# Logs generales
tail -f logs/rpa_janos.log

# Solo errores
tail -f logs/rpa_janos_errors.log

# API Server
tail -f logs/api_server.log
```

### Formato de Logs

```
2025-10-07 14:30:45 | INFO     | rpa_janos | extractor_eventos:login:125 | ✅ Login exitoso
2025-10-07 14:31:12 | INFO     | rpa_janos | extractor_eventos:extraer:287 | 📊 Extraídos 15 eventos desde Sistema Janos
```

---

## 🔧 Configuración Avanzada

### Modo Headless

Para ver el navegador durante la ejecución (útil para debugging):

```env
HEADLESS_MODE=false
```

### Nivel de Logs

Niveles disponibles: DEBUG, INFO, WARNING, ERROR, CRITICAL

```env
LOG_LEVEL=DEBUG  # Para más detalle
```

### Backups Automáticos

```env
BACKUP_ENABLED=true
BACKUP_DIR=./production/data/backups
```

### Reintentos

```env
MAX_RETRIES=3        # Número de reintentos
RETRY_DELAY=5        # Segundos entre reintentos
```

### Sincronización Automática

```env
AUTO_SYNC_ENABLED=true
AUTO_SYNC_INTERVAL=3600  # Cada 1 hora
```

---

## 🐛 Solución de Problemas

### Error: "Configuración inválida"

**Solución:**
```bash
python3 src/main.py --health
```
Verificar qué variables faltan y completarlas en `config/production.env`

### Error: "API no accesible"

**Solución:**
```bash
# Verificar si el API está corriendo
curl http://localhost:3002/api/health

# Si no responde, reiniciar
./scripts/stop_system.sh
./scripts/start_system.sh
```

### Error: "Timeout durante el login"

**Causas posibles:**
- Credenciales incorrectas
- URL incorrecta
- Selectores HTML cambiaron

**Solución:**
1. Verificar credenciales en `config/production.env`
2. Ejecutar en modo no-headless para ver el navegador:
```env
HEADLESS_MODE=false
```

### Error: "No se encontraron eventos"

**Solución:**
- Verificar que los filtros sean correctos (DOT, CABA, 2025)
- Verificar que haya eventos en el sistema origen
- Revisar logs para más detalles

### Logs muy grandes

Los logs rotan automáticamente, pero puedes limpiarlos manualmente:

```bash
# Limpiar logs antiguos (más de 30 días)
python3 -c "from src.utils.logger import logger; logger.clear_old_logs(30)"
```

---

## 📈 Monitoreo y Mantenimiento

### Verificación Diaria

```bash
# Verificar salud del sistema
python3 src/main.py --health

# Ver últimos logs
tail -n 50 logs/rpa_janos.log
```

### Backup Manual

```bash
# Backup de datos
cp -r data/ "backup_$(date +%Y%m%d_%H%M%S)/"

# Backup de logs
cp -r logs/ "logs_backup_$(date +%Y%m%d_%H%M%S)/"
```

### Limpieza de Archivos Temporales

```bash
# Limpiar CSVs antiguos (mantener últimos 7 días)
find data/ -name "*.csv" -mtime +7 -delete

# Limpiar logs antiguos
find logs/ -name "*.log.*" -mtime +30 -delete
```

---

## 🔒 Seguridad

### Buenas Prácticas

1. ✅ **Nunca** commitear archivos `.env` con credenciales reales
2. ✅ Usar variables de entorno para credenciales
3. ✅ Mantener logs fuera del repositorio
4. ✅ Rotar credenciales periódicamente
5. ✅ Ejecutar con permisos mínimos necesarios
6. ✅ Revisar logs de errores regularmente

### Archivo .gitignore

Asegurar que estos archivos estén ignorados:
```
config/production.env
logs/
data/
*.log
*.csv
node_modules/
__pycache__/
```

---

## 📞 Soporte

### Información de Contacto

- **Desarrollador:** Sebastian Maza
- **Email:** [tu-email]
- **Repositorio:** https://github.com/MazaSebastian/RPAJanos

### Reportar Problemas

1. Revisar logs
2. Verificar configuración con `--health`
3. Intentar soluciones en sección "Solución de Problemas"
4. Si persiste, crear issue en GitHub con:
   - Descripción del problema
   - Logs relevantes
   - Pasos para reproducir

---

## 🗺️ Roadmap

### Próximas Funcionalidades

- [ ] Dashboard web de monitoreo
- [ ] Notificaciones por email
- [ ] Scheduler integrado (cron jobs)
- [ ] Tests automatizados
- [ ] Métricas y analytics
- [ ] API de webhooks
- [ ] Multi-salón simultáneo
- [ ] Histórico de ejecuciones

---

## 📄 Licencia

Este proyecto es de uso interno de Jano's Group. No distribuir sin autorización.

---

## 🎯 Notas de Versión

### v1.0.0 - Sistema de Producción (Octubre 2025)

**Características principales:**
- ✅ Extracción automatizada de eventos
- ✅ API REST completo
- ✅ Sincronización con COORDIS
- ✅ Sistema de logging profesional
- ✅ Configuración centralizada
- ✅ Backups automáticos
- ✅ Manejo robusto de errores
- ✅ Scripts de deployment
- ✅ Documentación completa

**Mejoras respecto a versiones anteriores:**
- 🔄 Refactorización completa del código
- 📦 Estructura modular organizada
- 🛡️ Mayor seguridad y validaciones
- 📊 Logs estructurados y detallados
- ⚡ Mejor rendimiento
- 🔧 Configuración más flexible

---

**¡Sistema listo para producción! 🚀**

