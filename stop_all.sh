#!/bin/bash

# ============================================================================
# Docker CTF Lab - Script para Detener Todos los Servicios
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║       🛑 DOCKER CTF LAB - Deteniendo Sistema                       ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# 1. Detener Dashboard de Estudiantes
echo "1️⃣  Deteniendo Dashboard de Estudiantes..."
pkill -f "python3 web_dashboard.py" && echo "   ✅ Dashboard detenido" || echo "   ℹ️  Dashboard no estaba corriendo"

# 2. Detener Monitor del Profesor (Docker Compose)
echo ""
echo "2️⃣  Deteniendo Monitor del Profesor..."
if [ -d "mqtt_monitor" ]; then
    cd mqtt_monitor
    docker-compose down
    cd ..
    echo "   ✅ Monitor detenido"
else
    echo "   ⚠️  Directorio mqtt_monitor no encontrado"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ SISTEMA DETENIDO                             ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
