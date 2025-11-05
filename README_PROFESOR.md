# 🎓 Docker CTF Lab - Guía del Profesor

## 📋 Descripción

Este branch `profesor` contiene **herramientas adicionales de monitoreo y gestión** para instructores. Incluye todo lo del branch `main` (estudiantes) más:

- ✅ **Monitor MQTT** en tiempo real (puerto 5001)
- ✅ **Base de datos PostgreSQL** con tracking completo
- ✅ **Dashboard del profesor** con estadísticas y leaderboard
- ✅ **Adminer** para gestión de base de datos (puerto 8080)
- ✅ **Scripts de inicio/parada** completos (`start_all.sh`, `stop_all.sh`)
- ✅ **API REST** para consultar progreso de estudiantes
- ✅ **WebSockets** para actualizaciones en tiempo real

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    ESTUDIANTES                              │
│  Dashboard Web (puerto 5000)                                │
│  - 15 retos Docker                                          │
│  - Sistema de quiz                                          │
│  - Flags personalizadas                                     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ MQTT Publish
                 │ (heartbeat, progress, flags)
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              BROKER MQTT (HiveMQ Cloud)                     │
│         Topic: docker_ctf_lab/{documento}/{tipo}            │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ MQTT Subscribe
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  SISTEMA DEL PROFESOR                       │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │  Monitor MQTT (puerto 5001)                       │    │
│  │  - Flask + MQTT + WebSocket                       │    │
│  │  - Dashboard en tiempo real                       │    │
│  └───────────────┬───────────────────────────────────┘    │
│                  │                                         │
│                  ▼                                         │
│  ┌───────────────────────────────────────────────────┐    │
│  │  PostgreSQL Database (puerto 5432)                │    │
│  │  - 6 tablas (estudiantes, retos, eventos, etc.)  │    │
│  │  - 3 vistas (ranking, estadísticas, leaderboard) │    │
│  │  - Triggers y funciones                          │    │
│  └───────────────┬───────────────────────────────────┘    │
│                  │                                         │
│                  ▼                                         │
│  ┌───────────────────────────────────────────────────┐    │
│  │  Adminer (puerto 8080)                            │    │
│  │  - Gestión visual de BD                           │    │
│  └───────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Inicio Rápido (Profesor)

### 1. Clonar el branch profesor

```bash
git clone -b profesor https://github.com/edison-enriquez/ctf_docker_lab.git
cd ctf_docker_lab
```

### 2. Iniciar sistema completo

```bash
./start_all.sh
```

Esto inicia:
- ✅ Dashboard estudiantes (puerto 5000)
- ✅ Monitor del profesor (puerto 5001)
- ✅ PostgreSQL (puerto 5432)
- ✅ Adminer (puerto 8080)

### 3. Acceder a los servicios

- **Dashboard Estudiantes**: http://localhost:5000
- **Monitor Profesor**: http://localhost:5001
- **Adminer (BD)**: http://localhost:8080

---

## 📊 Características del Sistema de Monitoreo

### Dashboard del Profesor (Puerto 5001)

#### Vista Principal

- **Estudiantes Activos**: Lista en tiempo real con documentos
- **Leaderboard**: Ranking por puntos
- **Estadísticas Globales**:
  - Total estudiantes registrados
  - Total retos completados
  - Promedio de puntos
  - Retos más difíciles

#### Eventos en Tiempo Real (WebSocket)

- Heartbeat de estudiantes (cada 30s)
- Progreso de retos
- Flags enviadas
- Retos completados

### Base de Datos PostgreSQL

#### Tablas Principales

1. **estudiantes**
   - documento (PK)
   - nombre
   - fecha_registro
   - ultimo_heartbeat

2. **retos**
   - id (PK)
   - nombre
   - categoria
   - dificultad
   - puntos

3. **retos_completados**
   - id (PK)
   - documento_estudiante (FK)
   - reto_id (FK)
   - fecha_completado
   - flag_enviada

4. **eventos_mqtt**
   - id (PK)
   - tipo_evento
   - documento_estudiante
   - datos_json
   - timestamp

5. **sesiones**
   - id (PK)
   - documento_estudiante (FK)
   - fecha_inicio
   - fecha_fin
   - duracion_minutos

6. **estadisticas_globales**
   - fecha
   - total_estudiantes
   - total_retos_completados
   - promedio_puntos

#### Vistas Útiles

1. **v_ranking_estudiantes**
   ```sql
   SELECT documento, nombre, total_puntos, retos_completados, ranking
   FROM v_ranking_estudiantes
   ORDER BY ranking;
   ```

2. **v_retos_mas_dificiles**
   ```sql
   SELECT nombre, intentos, completados, tasa_exito
   FROM v_retos_mas_dificiles
   ORDER BY tasa_exito ASC;
   ```

3. **v_estadisticas_por_estudiante**
   ```sql
   SELECT documento, retos_completados, total_puntos, promedio_por_reto
   FROM v_estadisticas_por_estudiante;
   ```

---

## 🔧 Configuración

### Variables de Entorno (`mqtt_monitor/.env`)

```env
# PostgreSQL
POSTGRES_USER=monitor_user
POSTGRES_PASSWORD=monitor_pass_2024
POSTGRES_DB=ctf_monitor

# MQTT
MQTT_BROKER=broker.hivemq.com
MQTT_PORT=1883
MQTT_TOPIC=docker_ctf_lab/#

# Flask
FLASK_ENV=development
FLASK_PORT=5001
```

### Docker Compose

Los servicios se gestionan con Docker Compose en `mqtt_monitor/docker-compose.yml`:

```yaml
services:
  postgres:    # Base de datos
  mqtt_monitor: # Monitor Flask + MQTT
  adminer:     # Interfaz web BD
```

---

## 📡 API REST del Monitor

### Endpoints Disponibles

#### GET `/health`
Verificar estado del servicio
```bash
curl http://localhost:5001/health
```

#### GET `/api/students`
Obtener lista de estudiantes
```bash
curl http://localhost:5001/api/students
```

#### GET `/api/leaderboard`
Obtener ranking de estudiantes
```bash
curl http://localhost:5001/api/leaderboard
```

#### GET `/api/statistics`
Obtener estadísticas globales
```bash
curl http://localhost:5001/api/statistics
```

#### DELETE `/api/student/<documento>`
Eliminar estudiante (con cascade)
```bash
curl -X DELETE http://localhost:5001/api/student/1086104202
```

---

## 🛠️ Comandos Útiles

### Iniciar Sistema Completo

```bash
./start_all.sh
```

### Detener Sistema

```bash
./stop_all.sh
```

### Ver Logs

```bash
# Dashboard estudiantes
tail -f /tmp/ctf_dashboard.log

# Monitor MQTT (dentro del contenedor)
docker logs -f ctf_monitor_app

# PostgreSQL
docker logs -f ctf_monitor_db
```

### Acceder a PostgreSQL

```bash
# Via Adminer (GUI)
http://localhost:8080

# Via psql (CLI)
docker exec -it ctf_monitor_db psql -U monitor_user -d ctf_monitor
```

### Consultas SQL Útiles

```sql
-- Ver todos los estudiantes
SELECT * FROM estudiantes;

-- Ver ranking
SELECT * FROM v_ranking_estudiantes;

-- Ver retos completados por estudiante
SELECT e.nombre, r.nombre as reto, rc.fecha_completado
FROM retos_completados rc
JOIN estudiantes e ON rc.documento_estudiante = e.documento
JOIN retos r ON rc.reto_id = r.id
WHERE e.documento = '1086104202';

-- Estadísticas por categoría
SELECT 
    r.categoria,
    COUNT(*) as total_completados,
    AVG(r.puntos) as promedio_puntos
FROM retos_completados rc
JOIN retos r ON rc.reto_id = r.id
GROUP BY r.categoria;
```

---

## 🎯 Flujo de Datos MQTT

### Topics

```
docker_ctf_lab/{documento}/heartbeat    # Ping cada 30s
docker_ctf_lab/{documento}/progress     # Progreso general
docker_ctf_lab/{documento}/flag         # Flag enviada
docker_ctf_lab/{documento}/challenge    # Reto completado
```

### Ejemplo de Mensaje (Heartbeat)

```json
{
  "tipo": "heartbeat",
  "documento": "1086104202",
  "timestamp": "2025-11-05T01:30:00Z",
  "completados": [1, 2, 3],
  "puntos": 35
}
```

### Ejemplo de Mensaje (Challenge Completed)

```json
{
  "tipo": "challenge_completed",
  "documento": "1086104202",
  "reto_id": 4,
  "reto_nombre": "🔌 Mapeo de Puertos",
  "puntos": 15,
  "timestamp": "2025-11-05T01:45:00Z"
}
```

---

## 📈 Análisis y Reporting

### Exportar Datos

```bash
# Exportar ranking a CSV
docker exec -it ctf_monitor_db psql -U monitor_user -d ctf_monitor \
  -c "COPY (SELECT * FROM v_ranking_estudiantes) TO STDOUT WITH CSV HEADER" \
  > ranking.csv

# Exportar todos los retos completados
docker exec -it ctf_monitor_db psql -U monitor_user -d ctf_monitor \
  -c "COPY (SELECT * FROM retos_completados) TO STDOUT WITH CSV HEADER" \
  > retos_completados.csv
```

### Generar Reporte de Sesión

```bash
# Ver duración de sesiones
docker exec -it ctf_monitor_db psql -U monitor_user -d ctf_monitor \
  -c "SELECT documento_estudiante, fecha_inicio, duracion_minutos 
      FROM sesiones 
      ORDER BY duracion_minutos DESC;"
```

---

## 🐛 Solución de Problemas

### Los contenedores no inician

```bash
# Ver logs de Docker Compose
cd mqtt_monitor
docker-compose logs

# Reiniciar servicios
./stop_all.sh
./start_all.sh
```

### Puerto ocupado

```bash
# Verificar puertos
lsof -i :5000  # Dashboard estudiantes
lsof -i :5001  # Monitor profesor
lsof -i :5432  # PostgreSQL
lsof -i :8080  # Adminer

# Matar procesos si es necesario
pkill -f web_dashboard.py
docker-compose down
```

### Base de datos corrupta

```bash
# Eliminar volúmenes y recrear
cd mqtt_monitor
docker-compose down -v
docker-compose up -d
```

### MQTT no recibe mensajes

```bash
# Verificar conectividad
curl http://broker.hivemq.com

# Ver logs del monitor
docker logs -f ctf_monitor_app

# Probar manualmente con mosquitto
mosquitto_sub -h broker.hivemq.com -t "docker_ctf_lab/#" -v
```

---

## 📚 Documentación Adicional

- **[SISTEMA_BD.md](mqtt_monitor/SISTEMA_BD.md)** - Esquema completo de base de datos
- **[DEPLOY.md](mqtt_monitor/DEPLOY.md)** - Guía de despliegue detallada
- **[USO_SISTEMA.md](USO_SISTEMA.md)** - Manual de uso completo

---

## 🔐 Seguridad

### Cambiar Credenciales

Edita `mqtt_monitor/.env`:

```env
POSTGRES_PASSWORD=tu_password_seguro
```

Luego reinicia:

```bash
cd mqtt_monitor
docker-compose down -v
docker-compose up -d
```

### Restringir Acceso

En producción, configura firewall para:
- Puerto 5001: Solo red interna
- Puerto 5432: Solo localhost
- Puerto 8080: Solo red interna

---

## 🎓 Gestión de Estudiantes

### Añadir Estudiante Manualmente

```sql
INSERT INTO estudiantes (documento, nombre)
VALUES ('1086104202', 'Juan Pérez');
```

### Eliminar Estudiante (con todo su progreso)

```bash
curl -X DELETE http://localhost:5001/api/student/1086104202
```

O por SQL:

```sql
DELETE FROM estudiantes WHERE documento = '1086104202';
-- Cascade elimina automáticamente retos_completados, eventos, etc.
```

### Resetear Progreso de Estudiante

```sql
DELETE FROM retos_completados WHERE documento_estudiante = '1086104202';
DELETE FROM eventos_mqtt WHERE documento_estudiante = '1086104202';
UPDATE estudiantes SET ultimo_heartbeat = NULL WHERE documento = '1086104202';
```

---

## 📊 Mejores Prácticas

1. **Monitoreo Regular**: Revisar dashboard cada 15-30 minutos durante sesiones
2. **Backup de BD**: Exportar datos al final de cada sesión
3. **Logs**: Revisar logs si estudiantes reportan problemas
4. **Performance**: Con >50 estudiantes, considerar escalar PostgreSQL
5. **Networking**: Asegurar que MQTT broker sea accesible desde todas las máquinas

---

## 🚀 Próximos Pasos

1. Configurar alertas (email/Slack) para eventos importantes
2. Añadir grafanas para visualización avanzada
3. Implementar autenticación para dashboard del profesor
4. Exportación automática de reportes (PDF)
5. Integración con LMS (Moodle, Canvas)

---

## 📞 Soporte

Para problemas técnicos:
1. Revisa logs en `/tmp/` y `docker logs`
2. Consulta documentación en `mqtt_monitor/`
3. Verifica conectividad MQTT y PostgreSQL

---

## 🎉 ¡Éxito en tu Clase!

Este sistema está diseñado para facilitar la enseñanza de Docker de forma práctica y gamificada. ¡Que tus estudiantes disfruten aprendiendo! 🐳✨

---

**Branch**: `profesor` (sistema completo)  
**Branch estudiantes**: `main` (solo dashboard y retos)  
**Versión**: 2.0 con Sistema de Monitoreo PostgreSQL + MQTT  
**Última actualización**: Noviembre 2025
