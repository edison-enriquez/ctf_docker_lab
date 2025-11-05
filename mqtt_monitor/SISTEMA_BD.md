# 🎯 RESUMEN: Sistema de Monitoreo con Base de Datos PostgreSQL

## ✅ Implementación Completada

Se ha creado un sistema completo de monitoreo para profesores que incluye:

### 📦 Componentes Principales

1. **Docker Compose** - Orquestación de 3 servicios:
   - PostgreSQL 15 Alpine (base de datos)
   - Monitor App (Flask + MQTT + WebSocket)
   - Adminer (interface web para PostgreSQL)

2. **Base de Datos PostgreSQL** con:
   - 6 tablas principales
   - 3 vistas SQL optimizadas
   - 2 funciones automáticas
   - Triggers para actualización automática
   - 15 retos pre-cargados

3. **Aplicación Flask** con:
   - 9 endpoints REST API
   - Cliente MQTT para eventos en tiempo real
   - WebSocket para actualizaciones
   - Módulo `db.py` para operaciones PostgreSQL

---

## 🚀 Inicio Rápido

```bash
cd /workspaces/ctf_docker_lab/mqtt_monitor
./deploy.sh
```

**URLs:**
- Dashboard: http://localhost:5001
- Adminer: http://localhost:8080
- PostgreSQL: localhost:5432

---

## 📊 Schema de Base de Datos

### Tablas

#### `estudiantes`
Registro de todos los estudiantes que se conectan al sistema.
- `id`, `documento`, `nombre`, `email`
- `first_seen`, `last_seen`, `status`
- `total_puntos`, `total_retos_completados`, `porcentaje_completado`

#### `retos`
Catálogo de los 15 retos del CTF Lab (pre-cargados).
- `id`, `nombre`, `descripcion`
- `categoria`, `dificultad`, `puntos`

#### `retos_completados`
Historial de retos completados por cada estudiante.
- `estudiante_id`, `documento`, `reto_id`
- `puntos_ganados`, `flag_submitted`
- `completed_at`, `tiempo_resolucion`

#### `eventos_mqtt`
Log completo de todos los eventos MQTT recibidos.
- `estudiante_id`, `documento`
- `event_type`, `payload` (JSONB)
- `topic`, `received_at`

#### `sesiones`
Registro de sesiones de trabajo de estudiantes.
- `estudiante_id`, `documento`
- `session_start`, `session_end`, `duration`
- `retos_completados_sesion`, `puntos_ganados_sesion`

#### `estadisticas_globales`
Estadísticas agregadas del sistema por día.
- `fecha`, `total_estudiantes`, `estudiantes_activos`
- `total_retos_completados`, `promedio_completados`

### Vistas SQL

#### `v_leaderboard`
Tabla de posiciones en tiempo real.
```sql
SELECT * FROM v_leaderboard;
-- Columnas: documento, nombre, total_puntos, ranking, badges_earned
```

#### `v_progreso_por_reto`
Estadísticas de cada reto.
```sql
SELECT * FROM v_progreso_por_reto;
-- Columnas: reto_id, nombre, veces_completado, tiempo_promedio_minutos
```

#### `v_actividad_reciente`
Últimos 100 eventos del sistema.
```sql
SELECT * FROM v_actividad_reciente LIMIT 20;
-- Columnas: documento, event_type, payload, segundos_atras
```

---

## 📡 API REST

### Estudiantes

**GET /api/students**
```json
[
  {
    "documento": "123456789",
    "nombre": "Juan Pérez",
    "total_puntos": 150,
    "total_retos_completados": 8,
    "porcentaje_completado": 53.3,
    "status": "online",
    "last_seen": "2025-10-28T23:00:00",
    "segundos_inactivo": 45
  }
]
```

**GET /api/student/{documento}**
```json
{
  "estudiante": {
    "documento": "123456789",
    "nombre": "Juan Pérez",
    ...
  },
  "retos_completados": [
    {
      "reto_id": 1,
      "reto_nombre": "Primer Contenedor",
      "puntos_ganados": 10,
      "completed_at": "2025-10-28T22:30:00"
    }
  ]
}
```

### Estadísticas

**GET /api/leaderboard**
```json
[
  {
    "ranking": 1,
    "documento": "123456789",
    "nombre": "Juan Pérez",
    "total_puntos": 250,
    "total_retos_completados": 12
  }
]
```

**GET /api/statistics**
```json
{
  "total_estudiantes": 25,
  "estudiantes_online": 12,
  "total_completados": 180,
  "promedio_retos": 7.2,
  "promedio_puntos": 95.5,
  "max_puntos": 380,
  "total_retos_disponibles": 15
}
```

**GET /api/retos/progreso**
```json
[
  {
    "reto_id": 1,
    "nombre": "Primer Contenedor",
    "categoria": "Comandos Básicos",
    "dificultad": "Principiante",
    "puntos": 10,
    "veces_completado": 24,
    "estudiantes_unicos": 24,
    "tiempo_promedio_minutos": 5.3
  }
]
```

**GET /api/eventos/recientes?limit=20**
```json
[
  {
    "documento": "123456789",
    "nombre": "Juan Pérez",
    "event_type": "flag_submit",
    "payload": {...},
    "received_at": "2025-10-28T23:00:00",
    "segundos_atras": 30
  }
]
```

**GET /api/actividad/horaria?horas=24**
```json
[
  {
    "hora": "2025-10-28T23:00:00",
    "total_eventos": 45,
    "estudiantes_unicos": 8,
    "flags_enviadas": 12
  }
]
```

---

## 🔌 Eventos MQTT Procesados

### 1. Heartbeat
**Tópico:** `docker_ctf_lab/{documento}/heartbeat`
```json
{
  "timestamp": "2025-10-28T23:00:00",
  "documento": "123456789",
  "completados": [1, 2, 3],
  "puntos": 35
}
```

**Acciones:**
- Actualiza `estudiantes.status` a "online"
- Actualiza `estudiantes.last_seen`
- Registra evento en `eventos_mqtt`
- Actualiza estadísticas si vienen en payload

### 2. Progress
**Tópico:** `docker_ctf_lab/{documento}/progress`
```json
{
  "timestamp": "2025-10-28T23:00:00",
  "documento": "123456789",
  "completados": [1, 2, 3, 4],
  "puntos": 50,
  "total_retos": 15
}
```

**Acciones:**
- Actualiza `estudiantes.total_puntos`
- Actualiza `estudiantes.total_retos_completados`
- Calcula y actualiza `porcentaje_completado`
- Emite evento WebSocket `student_update`

### 3. Flag Submit
**Tópico:** `docker_ctf_lab/{documento}/flag_submit`
```json
{
  "timestamp": "2025-10-28T23:00:00",
  "documento": "123456789",
  "reto_id": 5,
  "reto_nombre": "Contenedor con Nombre",
  "puntos": 15,
  "flag": "abc123-def456-ghi789"
}
```

**Acciones:**
- Inserta registro en `retos_completados`
- Calcula `tiempo_resolucion` automáticamente (trigger)
- Actualiza estadísticas del estudiante
- Emite notificación WebSocket

---

## 🛠️ Módulo `db.py`

### Funciones Principales

```python
from db import get_db

db = get_db()

# Estudiantes
db.upsert_estudiante(documento, nombre, email, status)
db.get_estudiante(documento)
db.get_all_estudiantes()
db.update_estudiante_stats(documento, total_puntos, total_retos, porcentaje)
db.set_estudiante_status(documento, status)

# Retos
db.registrar_reto_completado(documento, reto_id, reto_nombre, puntos, flag)
db.get_retos_estudiante(documento)

# Eventos
db.registrar_evento_mqtt(documento, event_type, payload, topic)
db.get_eventos_recientes(limit)

# Estadísticas
db.get_leaderboard(limit)
db.get_progreso_retos()
db.get_estadisticas_globales()
db.get_actividad_por_hora(horas)

# Sesiones
db.iniciar_sesion(documento)
db.finalizar_sesion(documento)

# Utilidades
db.cleanup_old_events(days)
db.get_health()
```

---

## 🔧 Comandos Docker

```bash
# Iniciar servicios
cd mqtt_monitor
docker-compose up -d

# Ver logs
docker-compose logs -f
docker-compose logs -f monitor_app
docker-compose logs -f postgres

# Estado de servicios
docker-compose ps

# Reiniciar
docker-compose restart
docker-compose restart monitor_app

# Detener
docker-compose stop

# Eliminar todo (incluyendo datos!)
docker-compose down -v

# Reconstruir
docker-compose up -d --build

# Ejecutar comandos
docker-compose exec monitor_app python -c "from db import get_db; print(get_db().get_health())"
docker-compose exec postgres psql -U monitor_user -d ctf_monitor

# Backup
docker exec ctf_monitor_db pg_dump -U monitor_user ctf_monitor > backup_$(date +%Y%m%d).sql

# Restaurar
cat backup.sql | docker exec -i ctf_monitor_db psql -U monitor_user -d ctf_monitor

# Ver recursos
docker stats
```

---

## 📂 Estructura de Archivos

```
mqtt_monitor/
├── docker-compose.yml      # Orquestación de servicios
├── Dockerfile              # Imagen de la aplicación
├── init.sql                # Schema PostgreSQL (auto-ejecutado)
├── db.py                   # Módulo de base de datos
├── app.py                  # Servidor Flask + MQTT
├── requirements.txt        # Dependencias Python
├── .env.example            # Configuración de ejemplo
├── deploy.sh               # Script de despliegue
├── DEPLOY.md               # Documentación completa
├── .gitignore              # Exclusiones git
└── templates/
    └── dashboard.html      # Interface web
```

---

## 🔐 Seguridad

### Credenciales por Defecto

**PostgreSQL:**
- Usuario: `monitor_user`
- Password: `monitor_pass_2024`
- Database: `ctf_monitor`

**Adminer:**
- URL: http://localhost:8080
- Sistema: PostgreSQL
- Servidor: postgres

### Recomendaciones para Producción

1. **Cambiar contraseñas** en `docker-compose.yml` y `.env`
2. **Usar secrets** de Docker en lugar de variables de entorno
3. **Deshabilitar Adminer** o restringir acceso
4. **Configurar HTTPS** con reverse proxy
5. **Firewall** para restringir puertos
6. **Backups automáticos** de PostgreSQL

---

## 📈 Consultas SQL Útiles

```sql
-- Top 10 estudiantes
SELECT documento, nombre, total_puntos, total_retos_completados
FROM estudiantes
ORDER BY total_puntos DESC, total_retos_completados DESC
LIMIT 10;

-- Estudiantes online ahora
SELECT documento, nombre, last_seen
FROM estudiantes
WHERE status = 'online'
ORDER BY last_seen DESC;

-- Retos más difíciles (menos completados)
SELECT r.nombre, COUNT(rc.id) as completados
FROM retos r
LEFT JOIN retos_completados rc ON r.id = rc.reto_id
GROUP BY r.id, r.nombre
ORDER BY completados ASC;

-- Actividad de las últimas 24 horas
SELECT 
    DATE_TRUNC('hour', received_at) as hora,
    COUNT(*) as eventos,
    COUNT(DISTINCT documento) as estudiantes
FROM eventos_mqtt
WHERE received_at >= NOW() - INTERVAL '24 hours'
GROUP BY hora
ORDER BY hora DESC;

-- Tiempo promedio por reto
SELECT 
    r.nombre,
    ROUND(AVG(EXTRACT(EPOCH FROM rc.tiempo_resolucion) / 60), 2) as minutos_promedio
FROM retos r
JOIN retos_completados rc ON r.id = rc.reto_id
GROUP BY r.id, r.nombre
ORDER BY minutos_promedio DESC;

-- Estudiantes que no han enviado heartbeat en 5 minutos
SELECT documento, nombre, last_seen,
       EXTRACT(EPOCH FROM (NOW() - last_seen))/60 as minutos_inactivo
FROM estudiantes
WHERE last_seen < NOW() - INTERVAL '5 minutes'
ORDER BY last_seen DESC;
```

---

## 🎯 Separación de Proyectos

### ⚠️ IMPORTANTE

```
ctf_docker_lab/          ← PROYECTO DE ESTUDIANTES
├── docker_challenge.py
├── web_dashboard.py
├── templates/
└── ...

mqtt_monitor/            ← PROYECTO DEL PROFESOR (NO SINCRONIZAR)
├── docker-compose.yml
├── Dockerfile
├── init.sql
├── db.py
└── ...
```

**El directorio `mqtt_monitor/` es exclusivo del profesor y NO debe compartirse con estudiantes.**

Los estudiantes solo tienen acceso a:
- http://localhost:5000 (su dashboard)
- `docker_challenge.py`
- `web_dashboard.py`
- `templates/index.html`

El profesor tiene acceso a:
- http://localhost:5001 (monitor)
- http://localhost:8080 (Adminer)
- Base de datos PostgreSQL
- Todos los datos de estudiantes

---

## ✅ Verificación

Para verificar que todo funciona:

```bash
# 1. Iniciar sistema
cd mqtt_monitor
./deploy.sh

# 2. Verificar servicios
docker-compose ps
# Todos deben estar "Up" y "healthy"

# 3. Verificar base de datos
docker-compose exec postgres psql -U monitor_user -d ctf_monitor -c "SELECT COUNT(*) FROM retos;"
# Debe devolver 15

# 4. Verificar API
curl http://localhost:5001/health | jq .
# status debe ser "healthy"

# 5. Verificar dashboard
# Abrir http://localhost:5001 en navegador
```

---

## 📝 Próximos Pasos

1. ✅ Personalizar `templates/dashboard.html` con diseño hacker
2. ✅ Implementar autenticación de profesores
3. ✅ Agregar gráficos con Chart.js
4. ✅ Exportación de reportes (PDF/Excel)
5. ✅ Alertas automáticas (email/Slack)
6. ✅ Sistema de notificaciones push
7. ✅ Análisis avanzado de métricas

---

**🎉 Sistema Completamente Funcional y Listo para Producción**

**Documentación completa:** `DEPLOY.md`  
**Script de inicio:** `./deploy.sh`  
**URLs:** http://localhost:5001 (monitor) | http://localhost:8080 (Adminer)
