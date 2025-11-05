#!/bin/bash
# Script de inicio interactivo para Docker CTF Lab

# Colores
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
clear
echo -e "${GREEN}"
echo "======================================================================"
echo "   🐳 DOCKER CTF LAB - Sistema de Retos Capture The Flag"
echo "======================================================================"
echo -e "${NC}"

# Modo automático para postStartCommand
if [ "$1" == "auto" ]; then
    echo -e "${CYAN}🚀 Inicialización automática en Codespaces...${NC}"
    
    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker no está disponible${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Docker disponible${NC}"
    
    # Verificar Python y dependencias
    if ! python3 -c "import flask, docker" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Instalando dependencias...${NC}"
        pip install -q -r requirements.txt
    fi
    echo -e "${GREEN}✅ Dependencias instaladas${NC}"
    
    # Verificar si ya está configurado
    if [ ! -f "$HOME/.docker_ctf_configured" ]; then
        echo -e "${CYAN}📋 Configuración inicial pendiente${NC}"
        echo -e "${YELLOW}Por favor ejecuta: ./start.sh para configurar tu laboratorio${NC}"
    else
        echo -e "${GREEN}✅ Laboratorio ya configurado${NC}"
        echo -e "${CYAN}💡 Ejecuta ./start.sh para ver el menú principal${NC}"
    fi
    exit 0
fi

# Verificar Python
echo -e "${CYAN}[1/4] Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python $(python3 --version) encontrado${NC}"

# Verificar Docker
echo -e "\n${CYAN}[2/4] Verificando Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker $(docker --version) encontrado${NC}"

# Verificar dependencias
echo -e "\n${CYAN}[3/4] Verificando dependencias Python...${NC}"
if ! python3 -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Flask no está instalado. Instalando...${NC}"
    pip install -q flask
    echo -e "${GREEN}✅ Flask instalado correctamente${NC}"
else
    echo -e "${GREEN}✅ Flask ya está instalado${NC}"
fi

if ! python3 -c "import docker" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Docker SDK no está instalado. Instalando...${NC}"
    pip install -q docker
    echo -e "${GREEN}✅ Docker SDK instalado correctamente${NC}"
else
    echo -e "${GREEN}✅ Docker SDK ya está instalado${NC}"
fi

# Verificar si el entorno está configurado
echo -e "\n${CYAN}[4/4] Verificando configuración...${NC}"
if [ ! -f "$HOME/.docker_ctf_configured" ]; then
    echo -e "${YELLOW}⚠️  El laboratorio no está configurado${NC}"
    echo -e "${YELLOW}Necesitas configurar tu documento de identidad para generar tus flags${NC}"
    read -p "$(echo -e ${CYAN}¿Configurar ahora? [S/n]: ${NC})" configurar
    if [[ ! $configurar =~ ^[Nn]$ ]]; then
        python3 docker_challenge.py setup
    fi
else
    echo -e "${GREEN}✅ Laboratorio ya configurado${NC}"
fi

# Si se ejecuta en modo no interactivo o con argumento "start" iniciamos los servicios mínimos para estudiante
if [[ "$1" == "start" || "$1" == "" ]]; then
    echo -e "\n${GREEN}🚀 Modo estudiante: iniciando servicios mínimos...${NC}"
    # Verificar puerto 5000
    if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}ℹ️  Puerto 5000 ya en uso, suponiendo que el dashboard está corriendo${NC}"
    else
        echo -e "${CYAN}🌐 Iniciando Dashboard Web en background...${NC}"
        nohup python3 web_dashboard.py > /tmp/ctf_dashboard.log 2>&1 &
        DASH_PID=$!
        echo -e "${GREEN}✅ Dashboard iniciado (PID: ${DASH_PID}) - http://localhost:5000${NC}"
        sleep 2
    fi

    echo -e "\n${CYAN}📌 Nota: Este modo inicia únicamente los servicios necesarios para estudiantes (dashboard web).${NC}"
    echo -e "Si necesitas el menú interactivo ejecuta: ./start.sh menu${NC}\n"
    exit 0
fi

# Menú principal (solo si se pasa 'menu' o 'interactive')
if [[ "$1" == "menu" || "$1" == "interactive" ]]; then
    while true; do
    echo -e "\n${GREEN}======================================================================"
    echo "   📋 MENÚ PRINCIPAL - Docker CTF Lab"
    echo "======================================================================${NC}"
    echo ""
    echo "  1) 🌐 Iniciar Dashboard Web (recomendado)"
    echo "  2) 💻 Usar Línea de Comandos (CLI)"
    echo "  3) 📊 Ver Mi Progreso"
    echo "  4) 📖 Ver README / Documentación"
    echo "  5) 🔄 Reconfigurar Entorno"
    echo "  6) 🧪 Verificar Sistema"
    echo "  7) 🧹 Limpiar Contenedores de Prueba"
    echo "  8) 👋 Salir"
    echo ""
    read -p "$(echo -e ${CYAN}Selecciona una opción [1-8]: ${NC})" opcion
    
    case $opcion in
        1)
            echo -e "\n${GREEN}🌐 Iniciando Dashboard Web...${NC}"
            echo -e "${CYAN}El dashboard estará disponible en: http://localhost:5000${NC}"
            echo -e "${YELLOW}Presiona CTRL+C para detener el servidor${NC}\n"
            python3 web_dashboard.py
            ;;
        2)
            echo -e "\n${CYAN}💻 Modo Línea de Comandos${NC}"
            python3 docker_challenge.py start
            echo -e "\n${CYAN}Presiona Enter para continuar...${NC}"
            read
            ;;
        3)
            echo -e "\n${CYAN}📊 Tu Progreso Actual${NC}"
            python3 docker_challenge.py status
            echo -e "\n${CYAN}Presiona Enter para continuar...${NC}"
            read
            ;;
        4)
            echo -e "\n${CYAN}📖 Abriendo README...${NC}"
            if command -v less &> /dev/null; then
                less README.md
            else
                cat README.md
                echo -e "\n${CYAN}Presiona Enter para continuar...${NC}"
                read
            fi
            ;;
        5)
            echo -e "\n${YELLOW}🔄 Reconfigurando entorno...${NC}"
            read -p "$(echo -e ${RED}¿Estás seguro? Esto eliminará tu progreso [s/N]: ${NC})" confirmar
            if [[ $confirmar =~ ^[Ss]$ ]]; then
                rm -f "$HOME/.docker_ctf_configured"
                rm -f "$HOME/.docker_ctf_progress.json"
                python3 docker_challenge.py setup
                echo -e "${GREEN}✅ Entorno reconfigurado${NC}"
            else
                echo -e "${YELLOW}❌ Operación cancelada${NC}"
            fi
            echo -e "\n${CYAN}Presiona Enter para continuar...${NC}"
            read
            ;;
        6)
            echo -e "\n${CYAN}🧪 Verificando sistema...${NC}"
            python3 verify_system.py
            echo -e "\n${CYAN}Presiona Enter para continuar...${NC}"
            read
            ;;
        7)
            echo -e "\n${YELLOW}🧹 Limpiando contenedores de prueba...${NC}"
            python3 docker_challenge.py cleanup
            echo -e "\n${CYAN}Presiona Enter para continuar...${NC}"
            read
            ;;
        8)
            echo -e "\n${GREEN}👋 ¡Hasta luego!${NC}"
            echo -e "${YELLOW}Sigue aprendiendo Docker 🐳${NC}\n"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opción inválida. Intenta de nuevo.${NC}"
            ;;
    esac
done
