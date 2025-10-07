# 📦 Guía de Migración a Producción

## 🎯 Objetivo

Migrar del sistema actual (archivos experimentales dispersos) al sistema de producción organizado y profesional.

---

## 📊 Comparación: Antes vs Después

### Antes (Sistema Actual)
```
RPA JANOS FIX V1/
├── RPA_MULTIPLES_EVENTOS.py
├── sincronizar_coordis_final.py
├── api-server-inteligente.js
├── control_sistema_api.py
├── cargador_masivo_csv.py
├── ... (60+ archivos experimentales)
└── todos_los_eventos_extraidos.csv
```

### Después (Sistema de Producción)
```
production/
├── src/
│   ├── main.py                    ← Script principal
│   ├── rpa/extractor_eventos.py   ← RPA consolidado
│   ├── api/server.js              ← API mejorado
│   ├── sync/sincronizador.py      ← Sincronización
│   └── utils/                     ← Config + Logger
├── config/production.env          ← Configuración centralizada
├── scripts/                       ← Scripts de deployment
└── logs/                          ← Logs organizados
```

---

## 🚀 Pasos de Migración

### Fase 1: Preparación (5 min)

1. **Backup del sistema actual**
```bash
cd "/Users/sebamaza/Desktop/RPA JANOS FIX V1"
cp -r . "../RPA_JANOS_BACKUP_$(date +%Y%m%d)"
```

2. **Verificar que production/ existe**
```bash
ls -la production/
```

### Fase 2: Configuración (10 min)

1. **Copiar credenciales del .env actual (si existe)**
```bash
# Si tienes un .env en la raíz
cat .env
```

2. **Configurar production.env**
```bash
cd production
nano config/production.env
```

Completar con tus credenciales reales:
```env
USER_ORIGEN=sebastian_maza
PASS_ORIGEN=tu_contraseña_real
```

3. **Instalar dependencias**
```bash
# Python
pip3 install -r ../requirements.txt

# Node.js
npm install
```

### Fase 3: Prueba del Sistema Nuevo (15 min)

1. **Iniciar el sistema**
```bash
chmod +x scripts/*.sh
./scripts/start_system.sh
```

2. **Verificar salud**
```bash
python3 src/main.py --health
```

Debería mostrar:
```
✅ Configuración válida
✅ Directorios verificados
✅ API accesible
```

3. **Prueba de extracción (sin headless para ver)**
```bash
# Editar temporalmente
nano config/production.env
# Cambiar: HEADLESS_MODE=false
```

```bash
python3 src/main.py --extract
```

4. **Verificar resultados**
```bash
# Ver logs
tail -f logs/rpa_janos.log

# Ver CSV generado
ls -lh data/eventos_extraidos.csv
head data/eventos_extraidos.csv
```

5. **Prueba de sincronización**
```bash
python3 src/main.py --sync
```

### Fase 4: Flujo Completo (5 min)

```bash
# Volver a modo headless
nano config/production.env
# Cambiar: HEADLESS_MODE=true
```

```bash
# Ejecutar flujo completo
python3 src/main.py
```

Esto ejecutará:
1. ✅ Extracción de Janos
2. ✅ Guardado en CSV
3. ✅ Carga al API
4. ✅ Generación de script de sincronización

### Fase 5: Validación (10 min)

1. **Verificar logs**
```bash
tail -n 100 logs/rpa_janos.log
```

Buscar:
- ✅ "Login exitoso"
- ✅ "Extraídos X eventos"
- ✅ "CSV guardado"
- ✅ "Sincronización completada"

2. **Verificar API**
```bash
curl http://localhost:3002/api/health
curl http://localhost:3002/api/coordinations | jq
```

3. **Verificar archivos generados**
```bash
ls -lh data/
ls -lh logs/
ls -lh data/backups/
```

---

## 🔄 Mapeo de Archivos

### De Archivos Antiguos → Nuevos

| Archivo Antiguo | Archivo Nuevo | Notas |
|----------------|---------------|-------|
| `RPA_MULTIPLES_EVENTOS.py` | `src/rpa/extractor_eventos.py` | Refactorizado y mejorado |
| `sincronizar_coordis_final.py` | `src/sync/sincronizador.py` | Con mejor manejo de errores |
| `api-server-inteligente.js` | `src/api/server.js` | Con persistencia en archivo |
| `control_sistema_api.py` | `src/main.py` | Orquestación completa |
| `cargador_masivo_csv.py` | `src/sync/sincronizador.py` | Integrado en sincronizador |
| Variables dispersas | `config/production.env` | Centralizado |
| Logs dispersos | `logs/*.log` | Organizados con rotación |

### Funcionalidades Nuevas

✅ Sistema de configuración centralizado  
✅ Logger profesional con colores y rotación  
✅ Manejo robusto de errores con reintentos  
✅ Backups automáticos  
✅ Health checks  
✅ Scripts de deployment  
✅ Documentación completa  
✅ Estructura modular  

---

## 📝 Checklist de Migración

### Pre-Migración
- [ ] Backup del sistema actual
- [ ] Verificar Python 3.8+
- [ ] Verificar Node.js 14+
- [ ] Verificar Chrome instalado

### Configuración
- [ ] Copiar credenciales a production.env
- [ ] Instalar dependencias Python
- [ ] Instalar dependencias Node.js
- [ ] Dar permisos a scripts

### Pruebas
- [ ] Verificar salud del sistema
- [ ] Probar extracción (modo visible)
- [ ] Verificar CSV generado
- [ ] Probar sincronización
- [ ] Verificar API respondiendo
- [ ] Ejecutar flujo completo

### Validación
- [ ] Revisar logs sin errores
- [ ] Verificar datos en API
- [ ] Confirmar backups creados
- [ ] Probar detener/iniciar sistema

### Post-Migración
- [ ] Ejecutar flujo completo en modo headless
- [ ] Configurar ejecución programada (opcional)
- [ ] Documentar procedimientos específicos
- [ ] Capacitar equipo (si aplica)

---

## ⚠️ Consideraciones Importantes

### 1. Credenciales
- ⚠️ **NUNCA** commitear `production.env` con credenciales reales
- ✅ Usar `production.env` solo en local
- ✅ El archivo ya está en `.gitignore`

### 2. Selectores HTML
- ⚠️ Los selectores en `extractor_eventos.py` son genéricos
- ✅ Debes adaptarlos a tu HTML real del sistema Janos
- ✅ Ver líneas 200-250 en `extractor_eventos.py`

### 3. Logs
- ⚠️ Los logs crecen con el tiempo
- ✅ Hay rotación automática configurada
- ✅ Limpiar logs antiguos cada 30 días

### 4. Backups
- ⚠️ Los backups se acumulan en `data/backups/`
- ✅ Limpiar backups antiguos manualmente o con cron

---

## 🔧 Personalización Post-Migración

### 1. Ajustar Selectores HTML

Editar `src/rpa/extractor_eventos.py`:
```python
# Línea ~200
def _extraer_datos_evento(self, elemento, fecha: str):
    # Ajustar estos selectores según tu HTML real
    datos['cliente'] = elemento.find_element(
        By.CSS_SELECTOR, 
        ".cliente"  # ← Cambiar por selector real
    ).text.strip()
```

### 2. Configurar Filtros Personalizados

Editar `src/rpa/extractor_eventos.py`:
```python
# Línea ~150
def _aplicar_filtros(
    self, 
    salon: str = "DOT",     # ← Cambiar salón
    zona: str = "CABA",     # ← Cambiar zona
    ano: str = "2025"       # ← Cambiar año
):
```

### 3. Ajustar Timeouts

Editar `config/production.env`:
```env
BROWSER_TIMEOUT=30      # Aumentar si la página es lenta
IMPLICIT_WAIT=10        # Tiempo de espera por elementos
```

---

## 📞 Soporte Durante la Migración

### Si algo falla:

1. **Revisar logs**
```bash
tail -f logs/rpa_janos.log
tail -f logs/rpa_janos_errors.log
```

2. **Verificar configuración**
```bash
python3 src/main.py --health
```

3. **Ejecutar en modo visible**
```env
HEADLESS_MODE=false
DEBUG=true
LOG_LEVEL=DEBUG
```

4. **Volver al sistema anterior**
```bash
cd ../RPA_JANOS_BACKUP_YYYYMMDD
# Seguir usando el sistema antiguo hasta resolver
```

---

## ✅ Éxito de la Migración

Sabrás que la migración fue exitosa cuando:

1. ✅ `python3 src/main.py --health` muestra todo OK
2. ✅ El flujo completo se ejecuta sin errores
3. ✅ Los eventos se extraen correctamente
4. ✅ El CSV se genera en `data/`
5. ✅ El API responde en `http://localhost:3002`
6. ✅ La sincronización genera el script JS
7. ✅ Los logs muestran proceso completo
8. ✅ Los backups se crean automáticamente

---

## 🎉 Próximos Pasos Post-Migración

1. **Configurar ejecución programada**
   - Usar cron (Linux/Mac)
   - Usar Task Scheduler (Windows)

2. **Monitoreo continuo**
   - Revisar logs diariamente
   - Verificar salud del sistema

3. **Optimizaciones**
   - Ajustar selectores según sea necesario
   - Afinar timeouts
   - Configurar notificaciones

4. **Expandir funcionalidades**
   - Agregar más salones
   - Integrar con más sistemas
   - Crear dashboard web

---

**¡Bienvenido al sistema de producción! 🚀**

