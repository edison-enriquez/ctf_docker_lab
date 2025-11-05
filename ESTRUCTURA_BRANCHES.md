# 🐳 Docker CTF Lab - Estructura del Repositorio

## 📂 Organización por Branches

Este repositorio está organizado en **dos branches principales**:

### 🎓 Branch `main` - Para Estudiantes

Contiene **solo lo necesario** para que los estudiantes realicen los retos:

```
ctf_docker_lab/
├── docker_challenge.py          # Sistema de retos (15 challenges)
├── web_dashboard.py             # Dashboard web (puerto 5000)
├── start.sh                     # Script de inicio simplificado
├── templates/
│   └── index.html              # UI del dashboard con quiz
├── requirements.txt            # Dependencias Python
├── README_ESTUDIANTES.md       # Documentación para estudiantes
├── QUIZ_QUICKSTART.md          # Guía rápida del sistema de quiz
├── COMO_OBTENER_FLAGS.md       # Explicación del sistema de flags
└── SISTEMA_QUIZ.md             # Documentación completa del quiz
```

**Características:**
- ✅ Sistema de 15 retos Docker progresivos
- ✅ Dashboard web interactivo con tema hacker
- ✅ Sistema de quiz educativo (30 preguntas)
- ✅ Flags personalizadas (UUID-based)
- ✅ Inicio simple con `./start.sh`

**Uso:**
```bash
git clone https://github.com/edison-enriquez/ctf_docker_lab.git
cd ctf_docker_lab
./start.sh
# Abre http://localhost:5000
```

---

### 👨‍🏫 Branch `profesor` - Para Instructores

Contiene **todo lo del branch main** + herramientas de monitoreo:

```
ctf_docker_lab/
├── [Todo lo del branch main]
├── mqtt_monitor/                # Sistema de monitoreo
│   ├── app.py                  # Monitor Flask + MQTT
│   ├── db.py                   # Interfaz PostgreSQL
│   ├── docker-compose.yml      # Servicios (PostgreSQL, Adminer)
│   ├── Dockerfile              # Imagen del monitor
│   ├── init.sql                # Esquema de base de datos
│   ├── deploy.sh               # Script de despliegue
│   └── templates/
│       └── dashboard.html      # UI del monitor del profesor
├── start_all.sh                # Inicia sistema completo
├── stop_all.sh                 # Detiene todos los servicios
├── README_PROFESOR.md          # Documentación para profesores
└── USO_SISTEMA.md              # Manual completo del sistema
```

**Características adicionales:**
- ✅ Monitor MQTT en tiempo real (puerto 5001)
- ✅ Base de datos PostgreSQL con 6 tablas
- ✅ Dashboard del profesor con leaderboard
- ✅ Adminer para gestión de BD (puerto 8080)
- ✅ API REST para consultas
- ✅ WebSockets para actualizaciones en vivo
- ✅ Scripts de inicio/parada completos

**Uso:**
```bash
git clone -b profesor https://github.com/edison-enriquez/ctf_docker_lab.git
cd ctf_docker_lab
./start_all.sh
# Estudiantes: http://localhost:5000
# Profesor: http://localhost:5001
# Adminer: http://localhost:8080
```

---

## 🔄 Comparación de Branches

| Característica | Branch `main` | Branch `profesor` |
|---------------|---------------|-------------------|
| Dashboard Estudiantes (5000) | ✅ | ✅ |
| Sistema de Retos (15) | ✅ | ✅ |
| Quiz Educativo (30 preguntas) | ✅ | ✅ |
| Flags Personalizadas | ✅ | ✅ |
| Start Script (`./start.sh`) | ✅ | ✅ |
| **Monitor del Profesor (5001)** | ❌ | ✅ |
| **PostgreSQL Database** | ❌ | ✅ |
| **MQTT Real-time Tracking** | ❌ | ✅ |
| **Adminer (8080)** | ❌ | ✅ |
| **API REST** | ❌ | ✅ |
| **WebSockets** | ❌ | ✅ |
| **Scripts avanzados** | ❌ | ✅ |

---

## 🎯 ¿Qué Branch Usar?

### Para Estudiantes → `main`

Si eres estudiante y solo quieres hacer los retos:

```bash
git clone https://github.com/edison-enriquez/ctf_docker_lab.git
```

### Para Profesores/Instructores → `profesor`

Si eres profesor y necesitas monitorear a los estudiantes:

```bash
git clone -b profesor https://github.com/edison-enriquez/ctf_docker_lab.git
```

---

## 📊 Arquitectura del Sistema Completo (Branch Profesor)

```
┌──────────────────────────────────────────────────────────┐
│                    ESTUDIANTES                           │
│         Dashboard Web (puerto 5000)                      │
│         - Retos, Quiz, Flags                             │
└─────────────────┬────────────────────────────────────────┘
                  │
                  │ Publica eventos MQTT
                  ▼
┌──────────────────────────────────────────────────────────┐
│              Broker MQTT (HiveMQ Cloud)                  │
│         Topic: docker_ctf_lab/{documento}/*              │
└─────────────────┬────────────────────────────────────────┘
                  │
                  │ Suscrito a eventos
                  ▼
┌──────────────────────────────────────────────────────────┐
│                SISTEMA DEL PROFESOR                      │
│  ┌────────────────────────────────────────────────┐     │
│  │  Monitor MQTT (puerto 5001)                    │     │
│  │  - Dashboard en tiempo real                    │     │
│  │  - Leaderboard                                 │     │
│  │  - Estadísticas                                │     │
│  └──────────────┬─────────────────────────────────┘     │
│                 │                                        │
│                 ▼                                        │
│  ┌────────────────────────────────────────────────┐     │
│  │  PostgreSQL (puerto 5432)                      │     │
│  │  - 6 tablas (estudiantes, retos, eventos...)  │     │
│  │  - 3 vistas (ranking, estadísticas...)        │     │
│  └──────────────┬─────────────────────────────────┘     │
│                 │                                        │
│                 ▼                                        │
│  ┌────────────────────────────────────────────────┐     │
│  │  Adminer (puerto 8080)                         │     │
│  │  - GUI para gestionar PostgreSQL              │     │
│  └────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start por Rol

### Estudiante

```bash
# 1. Clonar repositorio
git clone https://github.com/edison-enriquez/ctf_docker_lab.git
cd ctf_docker_lab

# 2. Iniciar sistema
./start.sh

# 3. Abrir navegador
# http://localhost:5000

# 4. Configurar documento (primera vez)
python3 docker_challenge.py setup

# 5. ¡Empezar a hackear! 🚀
```

### Profesor

```bash
# 1. Clonar branch profesor
git clone -b profesor https://github.com/edison-enriquez/ctf_docker_lab.git
cd ctf_docker_lab

# 2. Iniciar sistema completo
./start_all.sh

# 3. Acceder a servicios
# Dashboard estudiantes: http://localhost:5000
# Monitor profesor: http://localhost:5001
# Adminer (BD): http://localhost:8080

# 4. Ver estadísticas en tiempo real
# Leaderboard, progreso, eventos MQTT
```

---

## 📚 Documentación

### Branch `main` (Estudiantes)

- **README_ESTUDIANTES.md** - Guía completa para estudiantes
- **QUIZ_QUICKSTART.md** - Guía del sistema de quiz
- **COMO_OBTENER_FLAGS.md** - Explicación de flags
- **SISTEMA_QUIZ.md** - Documentación técnica del quiz

### Branch `profesor` (Profesores)

- **README_PROFESOR.md** - Guía completa para instructores
- **mqtt_monitor/DEPLOY.md** - Despliegue del sistema de monitoreo
- **mqtt_monitor/SISTEMA_BD.md** - Esquema de base de datos
- **USO_SISTEMA.md** - Manual de uso del sistema completo

---

## 🔄 Sincronización de Branches

### Flujo de Desarrollo

```
main (estudiantes)
  │
  │ Merge ───────────────────────────────────┐
  │                                          │
  ▼                                          ▼
profesor (main + herramientas de monitoreo)
```

### Actualizar Branch Profesor

Si hay cambios en `main` que deben ir a `profesor`:

```bash
git checkout profesor
git merge main
git push origin profesor
```

---

## 🎓 Casos de Uso

### Caso 1: Clase Presencial

**Branch**: `profesor`

El profesor despliega el sistema completo en su máquina:
- Estudiantes acceden a `http://<ip-profesor>:5000`
- Profesor monitorea en `http://localhost:5001`

### Caso 2: Laboratorio Individual

**Branch**: `main`

Cada estudiante clona el repositorio en su máquina:
- Trabaja localmente con `./start.sh`
- No necesita servidor centralizado

### Caso 3: Clase Virtual

**Branch**: `profesor` + deploy en servidor

Profesor despliega en servidor cloud:
- Estudiantes acceden remotamente al dashboard
- Profesor monitorea desde cualquier lugar

---

## 🛠️ Mantenimiento

### Actualizar el Sistema

```bash
# Estudiantes (branch main)
git pull origin main
./start.sh

# Profesores (branch profesor)
git pull origin profesor
./stop_all.sh
./start_all.sh
```

### Limpiar y Reiniciar

```bash
# Matar procesos
pkill -f web_dashboard.py

# Limpiar Docker (profesor)
cd mqtt_monitor
docker-compose down -v

# Reiniciar
./start_all.sh  # o ./start.sh si es main
```

---

## 📞 Soporte

### Problemas en Branch Main
1. Revisar logs en `/tmp/ctf_dashboard.log`
2. Verificar Docker: `docker ps`
3. Consultar `README_ESTUDIANTES.md`

### Problemas en Branch Profesor
1. Revisar logs: `docker logs ctf_monitor_app`
2. Verificar BD: `docker logs ctf_monitor_db`
3. Consultar `README_PROFESOR.md`

---

## 🎉 Conclusión

Este repositorio está diseñado para **facilitar el aprendizaje de Docker** de forma práctica:

- **Estudiantes** obtienen un entorno limpio y fácil de usar (`main`)
- **Profesores** obtienen herramientas completas de monitoreo (`profesor`)
- Ambos branches se mantienen **sincronizados** y **documentados**

**¡Feliz aprendizaje de Docker!** 🐳✨

---

**Última actualización**: Noviembre 2025  
**Versión**: 2.0 con Sistema de Quiz Educativo + Monitoreo PostgreSQL
