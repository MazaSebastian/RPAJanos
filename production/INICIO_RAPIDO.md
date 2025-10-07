# 🚀 Inicio Rápido - RPA Jano's Eventos

## ⚡ 5 Minutos para Estar Corriendo

### Paso 1: Configurar Credenciales (2 min)

```bash
cd production
nano config/production.env
```

Editar solo estas líneas:
```env
USER_ORIGEN=tu_usuario_janos
PASS_ORIGEN=tu_contraseña_janos
```

Guardar: `Ctrl+O` → `Enter` → `Ctrl+X`

### Paso 2: Instalar Dependencias (2 min)

```bash
# Python
pip3 install -r ../requirements.txt

# Node.js
npm install
```

### Paso 3: Iniciar Sistema (1 min)

```bash
# Dar permisos a scripts
chmod +x scripts/*.sh

# Iniciar
./scripts/start_system.sh
```

---

## 🎯 Ejecutar el RPA

### Opción 1: Flujo Completo (Recomendado)
```bash
python3 src/main.py
```
Esto hará:
1. ✅ Extracción de eventos desde Janos
2. ✅ Guardado en CSV
3. ✅ Sincronización con API
4. ✅ Generación de script para COORDIS

### Opción 2: Solo Extracción
```bash
python3 src/main.py --extract
```

### Opción 3: Solo Sincronización
```bash
python3 src/main.py --sync
```

---

## 📊 Verificar que Todo Funcione

```bash
# Verificar salud del sistema
python3 src/main.py --health

# Verificar API
curl http://localhost:3002/api/health

# Ver logs en tiempo real
tail -f logs/rpa_janos.log
```

---

## 🛑 Detener el Sistema

```bash
./scripts/stop_system.sh
```

---

## 📋 Comandos Útiles

```bash
# Ver últimos 50 logs
tail -n 50 logs/rpa_janos.log

# Ver solo errores
tail -f logs/rpa_janos_errors.log

# Limpiar logs antiguos
find logs/ -name "*.log.*" -mtime +30 -delete

# Backup manual
cp -r data/ "backup_$(date +%Y%m%d)/"
```

---

## ❓ Problemas Comunes

### "API no accesible"
```bash
./scripts/stop_system.sh
./scripts/start_system.sh
```

### "Timeout en login"
1. Verificar credenciales en `config/production.env`
2. Cambiar `HEADLESS_MODE=false` para ver el navegador

### "No se encontraron eventos"
- Verificar que hay eventos en el sistema Janos
- Revisar logs: `tail -f logs/rpa_janos.log`

---

## 📞 Ayuda

Ver documentación completa: `README.md`

**¡Listo! El sistema está funcionando en producción! 🎉**

