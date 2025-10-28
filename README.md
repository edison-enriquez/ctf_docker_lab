# 🐳 Docker CTF Lab - Sistema de Retos Capture The Flag

> **Laboratorio interactivo estilo HackTheBox para aprendizaje de Docker con validación automática de flags personalizadas**

[![Docker](https://img.shields.io/badge/Docker-Requerido-2496ED?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Dashboard-000000?logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Descripción

**Docker CTF Lab** es un sistema de retos progresivos tipo "Capture The Flag" diseñado para aprender Docker de forma práctica e interactiva. Cada estudiante recibe **flags personalizadas** basadas en su documento de identidad, lo que garantiza la integridad académica y facilita el seguimiento del progreso individual.

### 🎯 Características Principales

- ✅ **15 Retos Progresivos**: Desde comandos básicos hasta arquitecturas complejas
- 🔒 **Flags Personalizadas**: Únicas por estudiante usando hash de documento
- 🤖 **Validación Automática**: Verifica contenedores, redes, volúmenes mediante Docker API
- 📊 **Dashboard Web**: Interfaz visual para tracking de progreso
- 🚀 **Auto-configuración**: Setup automático en GitHub Codespaces
- 🏆 **Sistema de Puntos**: 380 puntos totales distribuidos por dificultad

## 🎓 Retos Incluidos

| # | Reto | Categoría | Dificultad | Puntos |
|---|------|-----------|------------|--------|
| 1 | 🐳 Primer Contenedor | Comandos Básicos | Principiante | 10 |
| 2 | 🔍 Inspector de Imágenes | Imágenes | Principiante | 10 |
| 3 | 🚀 Contenedor en Background | Ejecución | Principiante | 15 |
| 4 | 🔌 Mapeo de Puertos | Redes | Intermedio | 15 |
| 5 | 💾 Volúmenes Persistentes | Volúmenes | Intermedio | 20 |
| 6 | 🌐 Red Personalizada | Redes | Intermedio | 20 |
| 7 | 🔗 Conectando Contenedores | Redes | Avanzado | 25 |
| 8 | 🔐 SSH en Contenedor | Servicios | Avanzado | 30 |
| 9 | 📡 Telnet Antiguo | Servicios | Avanzado | 30 |
| 10 | 🏭 SCADA Industrial | Aplicaciones | Experto | 35 |
| 11 | 🖥️ Escritorio Remoto VNC | Aplicaciones | Experto | 35 |
| 12 | 🏗️ Dockerfile Personalizado | Construcción | Avanzado | 30 |
| 13 | 📦 Docker Compose Multi-Servicio | Orquestación | Experto | 40 |
| 14 | 🔍 Inspección Avanzada | Diagnóstico | Intermedio | 25 |
| 15 | 🧹 Limpieza Maestra | Mantenimiento | Intermedio | 20 |

**Total**: 380 puntos disponibles

## 🚀 Inicio Rápido en GitHub Codespaces

### Opción 1: Fork y Codespaces (Recomendado para estudiantes)

1. **Fork este repositorio** a tu cuenta de GitHub
2. **Abre Codespaces**:
   - Click en el botón verde "Code"
   - Selecciona "Codespaces"
   - Click en "Create codespace on main"
3. **Espera la configuración automática** (1-2 minutos)
4. **Ejecuta el script de inicio**:
   ```bash
   ./start.sh
   ```
5. **Configura tu documento** cuando se solicite
6. **¡Comienza a resolver retos!**

### Opción 2: Instalación Local

#### Prerequisitos

- Python 3.8 o superior
- Docker instalado y corriendo
- Git

#### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/edison-enriquez/ctf_docker_lab.git
cd ctf_docker_lab

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Dar permisos de ejecución
chmod +x start.sh verify_system.py

# 4. Verificar sistema
./verify_system.py

# 5. Configurar laboratorio
python3 docker_challenge.py setup

# 6. Iniciar dashboard
python3 web_dashboard.py
```

## 💻 Uso del Sistema

### 🌐 Dashboard Web (Recomendado)

```bash
./start.sh
# Selecciona opción 1: Iniciar Dashboard Web
```

Accede en: **http://localhost:5000**

### 💻 Línea de Comandos (CLI)

```bash
# Ver todos los retos
python3 docker_challenge.py start

# Ver tu progreso
python3 docker_challenge.py status

# Ver pista de un reto
python3 docker_challenge.py hint 1

# Enviar una flag
python3 docker_challenge.py submit FLAG{primer_contenedor_ABC12345}

# Limpiar contenedores de prueba
python3 docker_challenge.py cleanup
```

## 🔒 Sistema de Flags Personalizadas

Cada estudiante recibe flags únicas basadas en su documento de identidad mediante hash SHA-256.

**Ejemplo**:
```
Documento: 1234567890
Reto: #1
Flag: FLAG{primer_contenedor_ABC12345}
```

## 📚 Recursos

- [TALLER.md](TALLER.md) - Write-ups y soluciones detalladas
- [GUIA_PROFESOR.md](GUIA_PROFESOR.md) - Guía para instructores
- [Documentación Docker](https://docs.docker.com/)

## 👨‍💻 Autor

**Edison Enríquez**
- GitHub: [@edison-enriquez](https://github.com/edison-enriquez)

---

**¿Listo para el desafío? 🐳**