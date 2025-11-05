#!/bin/bash

# ============================================================================
# Docker CTF Lab - Script de Inicio Completo
# Inicia tanto el dashboard de estudiantes como el monitor del profesor
# ============================================================================

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║       🐳 DOCKER CTF LAB - Iniciando Sistema Completo              ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "docker_challenge.py" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Función para verificar si un puerto está en uso
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 0
    else
        return 1
    fi
}

# 1. Iniciar Monitor del Profesor (Docker Compose)
echo "1️⃣  Iniciando Monitor del Profesor (Puerto 5001)..."
cd mqtt_monitor
if ! docker ps | grep -q "ctf_monitor_app"; then
    ./deploy.sh
else
    echo "   ℹ️  Monitor ya está corriendo"
fi
cd ..

# 2. Iniciar Dashboard de Estudiantes
echo ""
echo "2️⃣  Iniciando Dashboard de Estudiantes (Puerto 5000)..."
if check_port 5000; then
    echo "   ℹ️  Dashboard ya está corriendo en puerto 5000"
else
    nohup python3 web_dashboard.py > /tmp/ctf_dashboard.log 2>&1 &
    DASHBOARD_PID=$!
    echo "   ✅ Dashboard iniciado (PID: $DASHBOARD_PID)"
    sleep 2
fi

# 3. Verificar servicios
echo ""
echo "3️⃣  Verificando servicios..."
sleep 2

if curl -s http://localhost:5000/api/challenges > /dev/null 2>&1; then
    CHALLENGES=$(curl -s http://localhost:5000/api/challenges | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
    echo "   ✅ Dashboard Estudiante: OK ($CHALLENGES retos)"
else
    echo "   ❌ Dashboard Estudiante: ERROR"
fi

if curl -s http://localhost:5001/health > /dev/null 2>&1; then
    echo "   ✅ Monitor Profesor: OK"
else
    echo "   ❌ Monitor Profesor: ERROR"
fi

if docker ps | grep -q "ctf_monitor_db"; then
    echo "   ✅ PostgreSQL Database: OK"
else
    echo "   ❌ PostgreSQL Database: ERROR"
fi

# 4. Mostrar URLs
echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    🚀 SISTEMA INICIADO                             ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Servicios disponibles:"
echo ""
echo "   🎓 Dashboard Estudiantes:"
echo "      http://localhost:5000"
echo ""
echo "   👨‍🏫 Monitor Profesor:"
echo "      http://localhost:5001"
echo ""
echo "   🗄️  Adminer (PostgreSQL):"
echo "      http://localhost:8080"
echo "      Usuario: monitor_user"
echo "      Contraseña: monitor_pass_2024"
echo "      Base de datos: ctf_monitor"
echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║  💡 Para detener: ./stop_all.sh                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
