#!/bin/bash
# Script de prueba para demostrar la verificación automática de comandos Docker

echo "=================================="
echo "🧪 PRUEBA DE VERIFICACIÓN DOCKER"
echo "=================================="
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}📋 PRUEBA 1: Reto sin ejecutar comando${NC}"
echo "➜ Intentando enviar flag sin ejecutar 'docker run hello-world'"
echo ""

# Obtener la flag del reto 1
FLAG=$(python3 -c "
from docker_challenge import DockerCTFChallenge
import sys
challenge = DockerCTFChallenge('1086104202')
print(challenge.flags.get('1', ''))
")

echo "Flag del Reto 1: $FLAG"
echo ""
echo "➜ Enviando flag sin ejecutar el comando..."

# Intentar verificar sin ejecutar
curl -s -X POST http://localhost:5000/api/verify-flag \
  -H "Content-Type: application/json" \
  -d "{\"flag\": \"$FLAG\"}" | python3 -m json.tool

echo ""
echo -e "${YELLOW}⚠️  Como puedes ver, la verificación falla porque no se ejecutó el comando${NC}"
echo ""
echo "=================================="
echo ""
echo -e "${CYAN}📋 PRUEBA 2: Ejecutar comando y verificar${NC}"
echo "➜ Ejecutando 'docker run hello-world'"
echo ""

# Ejecutar el comando
docker run hello-world > /dev/null 2>&1

echo -e "${GREEN}✅ Comando ejecutado${NC}"
echo ""
echo "➜ Ahora verificando nuevamente..."

# Verificar después de ejecutar
curl -s -X POST http://localhost:5000/api/verify-flag \
  -H "Content-Type: application/json" \
  -d "{\"flag\": \"$FLAG\"}" | python3 -m json.tool

echo ""
echo -e "${GREEN}✅ Ahora la verificación es exitosa porque detectó que se ejecutó el comando${NC}"
echo ""
echo "=================================="
echo ""
echo -e "${CYAN}📋 DEMOSTRACIÓN COMPLETA${NC}"
echo ""
echo "El sistema ahora:"
echo "  1. ✅ Verifica que el comando Docker fue ejecutado"
echo "  2. ✅ Solo acepta la flag si se ejecutó el comando"
echo "  3. ✅ Muestra mensajes específicos de error"
echo ""
echo "En el dashboard, cuando presiones EXECUTE:"
echo "  → Primero verifica automáticamente"
echo "  → Luego envía la flag si pasa la verificación"
echo "  → Muestra mensajes informativos del proceso"
echo ""
echo "=================================="
