# 🐳 Docker CTF Lab - Monitor del Profesor

## 📋 Descripción

Sistema de monitoreo en tiempo real para profesores, utilizando **Docker Compose** con PostgreSQL para persistencia de datos y seguimiento detallado de estudiantes.

## 🏗️ Arquitectura

```
mqtt_monitor/
├── docker-compose.yml      # Orquestación de servicios
├── Dockerfile             # Imagen de la aplicación
├── init.sql               # Schema de base de datos
├── app.py                 # Servidor Flask + MQTT + WebSocket
├── db.py                  # Módulo de base de datos
├── requirements.txt       # Dependencias Python
├── .env.example          # Configuración de ejemplo
└── templates/
    └── dashboard.html     # Interface web
```

### Servicios Docker:

1. **PostgreSQL** (`postgres`): Base de datos para persistencia
2. **Monitor App** (`monitor_app`): Aplicación Flask con MQTT
3. **Adminer** (`adminer`): Interface web para PostgreSQL (opcional)

## 🚀 Inicio Rápido

### 1. Configurar variables de entorno

```bash
cd mqtt_monitor
cp .env.example .env
# Editar .env si es necesario
```

### 2. Iniciar servicios con Docker Compose

```bash
docker-compose up -d
```

Esto iniciará:
- PostgreSQL en puerto `5432`
- Monitor App en puerto `5001`
- Adminer en puerto `8080`

### 3. Verificar que todo está funcionando

```bash
docker-compose ps
docker-compose logs -f monitor_app
```

### 4. Acceder al dashboard

Abrir en el navegador: **http://localhost:5001**

## 📊 Base de Datos PostgreSQL

### Acceso directo con psql

```bash
docker exec -it ctf_monitor_db psql -U monitor_user -d ctf_monitor
```

### Acceso por Adminer (Web UI)

1. Abrir: http://localhost:8080
2. Credenciales:
   - Sistema: **PostgreSQL**
   - Servidor: **postgres**
   - Usuario: **monitor_user**
   - Contraseña: **monitor_pass_2024**
   - Base de datos: **ctf_monitor**

### Tablas Principales

- `estudiantes`: Registro de estudiantes
- `retos`: Catálogo de retos (15 pre-cargados)
- `retos_completados`: Historial de completados
- `eventos_mqtt`: Log de todos los eventos
- `sesiones`: Sesiones de trabajo
- `estadisticas_globales`: Estadísticas agregadas

### Vistas SQL

- `v_leaderboard`: Tabla de posiciones
- `v_progreso_por_reto`: Estadísticas por reto
- `v_actividad_reciente`: Últimos 100 eventos

## 🔌 API REST

### Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Dashboard principal |
| `/health` | GET | Health check |
| `/api/students` | GET | Lista de estudiantes |
| `/api/student/<documento>` | GET | Detalle de estudiante |
| `/api/leaderboard` | GET | Tabla de posiciones |
| `/api/statistics` | GET | Estadísticas globales |
| `/api/retos/progreso` | GET | Progreso por reto |
| `/api/eventos/recientes` | GET | Eventos recientes |
| `/api/actividad/horaria` | GET | Actividad por hora |

### Ejemplos de uso:

```bash
# Ver todos los estudiantes
curl http://localhost:5001/api/students | jq .

# Ver leaderboard
curl http://localhost:5001/api/leaderboard | jq .

# Ver estadísticas
curl http://localhost:5001/api/statistics | jq .

# Ver progreso de retos
curl http://localhost:5001/api/retos/progreso | jq .

# Ver eventos recientes (últimos 20)
curl "http://localhost:5001/api/eventos/recientes?limit=20" | jq .
```

## 📡 Eventos MQTT

El monitor escucha automáticamente en el tópico: `docker_ctf_lab/+/+`

### Tipos de eventos:

1. **Heartbeat** (`docker_ctf_lab/{documento}/heartbeat`)
   - Enviado cada 30 segundos
   - Actualiza status a "online"

2. **Progress** (`docker_ctf_lab/{documento}/progress`)
   - Enviado al completar reto
   - Actualiza estadísticas del estudiante

3. **Flag Submit** (`docker_ctf_lab/{documento}/flag_submit`)
   - Enviado al validar flag
   - Registra reto completado

## 🛠️ Comandos Docker Compose

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
docker-compose logs -f monitor_app
docker-compose logs -f postgres

# Detener servicios
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener y eliminar TODO (incluyendo volúmenes)
docker-compose down -v

# Reconstruir imágenes
docker-compose build

# Reconstruir y reiniciar
docker-compose up -d --build

# Ver estado de servicios
docker-compose ps

# Ejecutar comando en contenedor
docker-compose exec monitor_app python -c "from db import get_db; print(get_db().get_health())"
```

## 🔧 Desarrollo Local (sin Docker)

Si prefieres ejecutar sin Docker para desarrollo:

### 1. Instalar PostgreSQL localmente

```bash
sudo apt-get install postgresql postgresql-contrib
```

### 2. Crear base de datos

```bash
sudo -u postgres psql
CREATE DATABASE ctf_monitor;
CREATE USER monitor_user WITH PASSWORD 'monitor_pass_2024';
GRANT ALL PRIVILEGES ON DATABASE ctf_monitor TO monitor_user;
\q
```

### 3. Ejecutar script de inicialización

```bash
psql -U monitor_user -d ctf_monitor -f init.sql
```

### 4. Configurar .env

```bash
DATABASE_URL=postgresql://monitor_user:monitor_pass_2024@localhost:5432/ctf_monitor
```

### 5. Instalar dependencias e iniciar

```bash
pip install -r requirements.txt
python app.py
```

## 📈 Monitoreo y Mantenimiento

### Ver uso de recursos

```bash
docker stats
```

### Backup de base de datos

```bash
docker exec ctf_monitor_db pg_dump -U monitor_user ctf_monitor > backup_$(date +%Y%m%d).sql
```

### Restaurar backup

```bash
cat backup_20241028.sql | docker exec -i ctf_monitor_db psql -U monitor_user -d ctf_monitor
```

### Limpiar eventos antiguos

```sql
-- Eliminar eventos de más de 30 días
DELETE FROM eventos_mqtt WHERE received_at < NOW() - INTERVAL '30 days';
```

O usando la función del sistema:

```bash
docker-compose exec monitor_app python -c "from db import get_db; get_db().cleanup_old_events(30)"
```

## 🐛 Troubleshooting

### PostgreSQL no inicia

```bash
docker-compose logs postgres
docker volume ls
docker volume rm ctf_monitor_postgres_data
docker-compose up -d
```

### Monitor App no se conecta a PostgreSQL

```bash
# Verificar que PostgreSQL está listo
docker-compose exec postgres pg_isready -U monitor_user

# Ver logs del monitor
docker-compose logs monitor_app

# Reiniciar solo el monitor
docker-compose restart monitor_app
```

### MQTT no recibe eventos

```bash
# Verificar conexión MQTT
docker-compose logs monitor_app | grep MQTT

# Probar con mosquitto_sub (si está instalado)
mosquitto_sub -h broker.hivemq.com -t "docker_ctf_lab/#" -v
```

## 🔒 Seguridad en Producción

1. **Cambiar contraseñas**:
   - Editar `docker-compose.yml`: `POSTGRES_PASSWORD`
   - Editar `.env`: `SECRET_KEY`, `DATABASE_URL`

2. **Usar HTTPS**:
   - Configurar reverse proxy (nginx/Caddy)
   - Obtener certificado SSL

3. **Restringir acceso a Adminer**:
   - Comentar servicio `adminer` en `docker-compose.yml`
   - O usar firewall para restringir puerto 8080

4. **Variables de entorno seguras**:
   - No commitear archivo `.env`
   - Usar secrets de Docker Swarm/Kubernetes

## 📝 Notas Importantes

- ✅ **Separación de proyectos**: El monitor del profesor (`mqtt_monitor/`) es independiente del proyecto de estudiantes
- ✅ **No sincronizar**: El directorio `mqtt_monitor/` NO debe compartirse con estudiantes
- ✅ **Persistencia**: Los datos se guardan en volumen Docker `ctf_monitor_postgres_data`
- ✅ **Escalabilidad**: Puede manejar cientos de estudiantes simultáneos
- ✅ **Tiempo real**: WebSocket + MQTT para actualizaciones instantáneas

## 🎯 Próximos Pasos

1. Personalizar `templates/dashboard.html` con tu diseño
2. Configurar alertas automáticas (email/Slack)
3. Agregar exportación de reportes (PDF/Excel)
4. Implementar autenticación de profesores
5. Añadir gráficos y visualizaciones avanzadas

---

**🐳 Docker CTF Lab - Sistema de Monitoreo v2.0**
