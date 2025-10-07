#!/bin/bash
# ===================================
# Script de detención del sistema
# RPA Jano's Eventos
# ===================================

echo "=========================================="
echo "🛑 Deteniendo RPA Jano's Eventos"
echo "=========================================="

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Directorio base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE_DIR"

# Detener API Server
echo -e "\n${YELLOW}🔧 Deteniendo API Server...${NC}"
if [ -f "logs/api_server.pid" ]; then
    API_PID=$(cat logs/api_server.pid)
    if ps -p $API_PID > /dev/null 2>&1; then
        kill $API_PID
        echo -e "${GREEN}✅ API Server detenido (PID: $API_PID)${NC}"
    else
        echo -e "${YELLOW}⚠️ API Server no estaba corriendo${NC}"
    fi
    rm logs/api_server.pid
else
    echo -e "${YELLOW}⚠️ No se encontró archivo PID del API Server${NC}"
    # Intentar matar por puerto
    API_PID=$(lsof -ti:3002 2>/dev/null)
    if [ ! -z "$API_PID" ]; then
        kill $API_PID
        echo -e "${GREEN}✅ Proceso en puerto 3002 detenido${NC}"
    fi
fi

# Limpiar procesos huérfanos
echo -e "\n${YELLOW}🧹 Limpiando procesos...${NC}"
pkill -f "node.*server.js" 2>/dev/null || true
pkill -f "python.*main.py" 2>/dev/null || true

echo -e "\n=========================================="
echo -e "${GREEN}✅ Sistema detenido${NC}"
echo "=========================================="

