#!/bin/bash

# ============================================================================
# Docker CTF Lab - Monitor Deployment Script
# Script para iniciar el sistema de monitoreo con Docker Compose
# ============================================================================

set -e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
cat << "EOF"
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║          🐳 Docker CTF Lab - Monitor del Profesor 🐳          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ Error: docker-compose.yml no encontrado${NC}"
    echo -e "${YELLOW}   Por favor ejecuta este script desde mqtt_monitor/${NC}"
    exit 1
fi

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose no está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker y Docker Compose detectados${NC}\n"

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Archivo .env no encontrado, creando desde .env.example...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Archivo .env creado${NC}"
    else
        echo -e "${RED}❌ .env.example no encontrado${NC}"
        exit 1
    fi
fi

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Iniciando servicios con Docker Compose...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# Detener servicios existentes si los hay
if [ "$(docker ps -aq -f name=ctf_monitor)" ]; then
    echo -e "${YELLOW}Deteniendo servicios existentes...${NC}"
    docker-compose down
fi

# Construir e iniciar servicios
echo -e "${GREEN}Construyendo imágenes...${NC}"
docker-compose build

echo -e "\n${GREEN}Iniciando contenedores...${NC}"
docker-compose up -d

# Esperar a que PostgreSQL esté listo
echo -e "\n${YELLOW}Esperando a que PostgreSQL esté listo...${NC}"
for i in {1..30}; do
    if docker-compose exec -T postgres pg_isready -U monitor_user -d ctf_monitor &>/dev/null; then
        echo -e "${GREEN}✅ PostgreSQL está listo${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

# Verificar estado de servicios
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Estado de servicios:${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
docker-compose ps

# Esperar a que la aplicación esté lista
echo -e "\n${YELLOW}Esperando a que la aplicación esté lista...${NC}"
for i in {1..20}; do
    if curl -s http://localhost:5001/health &>/dev/null; then
        echo -e "${GREEN}✅ Aplicación está lista${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

# Resumen
echo -e "\n${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}  ${GREEN}✅ Sistema de Monitoreo Iniciado Correctamente${NC}             ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}\n"

echo -e "${GREEN}📊 URLs Disponibles:${NC}"
echo -e "   ${BLUE}Dashboard:${NC}  http://localhost:5001"
echo -e "   ${BLUE}Adminer:${NC}    http://localhost:8080"
echo -e "   ${BLUE}PostgreSQL:${NC} localhost:5432"

echo -e "\n${GREEN}🔑 Credenciales PostgreSQL:${NC}"
echo -e "   ${BLUE}Usuario:${NC}    monitor_user"
echo -e "   ${BLUE}Password:${NC}   monitor_pass_2024"
echo -e "   ${BLUE}Database:${NC}   ctf_monitor"

echo -e "\n${GREEN}📝 Comandos útiles:${NC}"
echo -e "   ${BLUE}Ver logs:${NC}           docker-compose logs -f"
echo -e "   ${BLUE}Detener:${NC}            docker-compose stop"
echo -e "   ${BLUE}Reiniciar:${NC}          docker-compose restart"
echo -e "   ${BLUE}Eliminar todo:${NC}      docker-compose down -v"

echo -e "\n${GREEN}🎯 El monitor está escuchando eventos MQTT en tiempo real${NC}"
echo -e "${YELLOW}   Los estudiantes deben conectarse a http://localhost:5000${NC}\n"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Preguntar si quiere ver logs
read -p "¿Deseas ver los logs en tiempo real? (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo -e "\n${GREEN}Mostrando logs (Ctrl+C para salir)...${NC}\n"
    docker-compose logs -f
fi
