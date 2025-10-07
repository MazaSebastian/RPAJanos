#!/bin/bash
# ===================================
# Script de inicio del sistema
# RPA Jano's Eventos
# ===================================

set -e  # Salir si hay algún error

echo "=========================================="
echo "🚀 Iniciando RPA Jano's Eventos"
echo "=========================================="

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Directorio base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE_DIR"

echo -e "${YELLOW}📂 Directorio base: $BASE_DIR${NC}"

# Verificar Node.js
echo -e "\n${YELLOW}🔍 Verificando Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js: $(node --version)${NC}"

# Verificar Python
echo -e "\n${YELLOW}🔍 Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python: $(python3 --version)${NC}"

# Crear directorios necesarios
echo -e "\n${YELLOW}📁 Creando directorios...${NC}"
mkdir -p logs data data/backups

# Instalar dependencias Node.js si es necesario
if [ -f "package.json" ]; then
    echo -e "\n${YELLOW}📦 Verificando dependencias Node.js...${NC}"
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Instalando dependencias Node.js...${NC}"
        npm install
        echo -e "${GREEN}✅ Dependencias Node.js instaladas${NC}"
    else
        echo -e "${GREEN}✅ Dependencias Node.js ya instaladas${NC}"
    fi
fi

# Instalar dependencias Python si es necesario
if [ -f "../requirements.txt" ]; then
    echo -e "\n${YELLOW}📦 Verificando dependencias Python...${NC}"
    echo -e "${YELLOW}Instalando/actualizando dependencias Python...${NC}"
    pip3 install -q -r ../requirements.txt
    echo -e "${GREEN}✅ Dependencias Python instaladas${NC}"
fi

# Verificar archivo de configuración
echo -e "\n${YELLOW}⚙️ Verificando configuración...${NC}"
if [ ! -f "config/production.env" ]; then
    echo -e "${RED}❌ Archivo config/production.env no encontrado${NC}"
    echo -e "${YELLOW}Por favor, crea el archivo de configuración${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Archivo de configuración encontrado${NC}"

# Iniciar API Server
echo -e "\n${YELLOW}🌐 Iniciando API Server...${NC}"
if [ -f "src/api/server.js" ]; then
    node src/api/server.js > logs/api_server.log 2>&1 &
    API_PID=$!
    echo $API_PID > logs/api_server.pid
    echo -e "${GREEN}✅ API Server iniciado (PID: $API_PID)${NC}"
    sleep 3
else
    echo -e "${RED}❌ Archivo src/api/server.js no encontrado${NC}"
    exit 1
fi

# Verificar que el API está respondiendo
echo -e "\n${YELLOW}🏥 Verificando salud del API...${NC}"
MAX_RETRIES=5
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:3002/api/health > /dev/null; then
        echo -e "${GREEN}✅ API Server está respondiendo${NC}"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT+1))
    echo -e "${YELLOW}⏳ Esperando al API (intento $RETRY_COUNT/$MAX_RETRIES)...${NC}"
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo -e "${RED}❌ API Server no responde después de $MAX_RETRIES intentos${NC}"
    kill $API_PID 2>/dev/null || true
    exit 1
fi

echo -e "\n=========================================="
echo -e "${GREEN}✅ Sistema iniciado correctamente${NC}"
echo "=========================================="
echo -e "📊 API Server: http://localhost:3002"
echo -e "📝 Logs API: logs/api_server.log"
echo -e "🔧 PID API: $API_PID"
echo ""
echo -e "Para ejecutar el RPA:"
echo -e "  ${YELLOW}python3 src/main.py${NC}"
echo ""
echo -e "Para detener el sistema:"
echo -e "  ${YELLOW}./scripts/stop_system.sh${NC}"
echo "=========================================="

