# 🎯 USO DEL SISTEMA CTF DOCKER LAB

## 🚀 Inicio Rápido

### Iniciar todo el sistema
```bash
./start_all.sh
```

### Detener todo el sistema
```bash
./stop_all.sh
```

---

## 📊 Servicios Disponibles

### 🎓 Dashboard de Estudiantes
- **URL**: http://localhost:5000
- **Descripción**: Interfaz para que los estudiantes vean y completen retos
- **Características**:
  - 15 retos CTF sobre Docker
  - Sistema de flags personalizadas
  - Tracking de progreso
  - Pistas disponibles

### 👨‍🏫 Monitor del Profesor
- **URL**: http://localhost:5001
- **Descripción**: Panel de monitoreo en tiempo real
- **Características**:
  - Visualización de estudiantes activos
  - Tabla de posiciones (leaderboard)
  - Estadísticas globales
  - Eventos en tiempo real vía MQTT
  - Base de datos PostgreSQL

### 🗄️ Adminer (Gestión de BD)
- **URL**: http://localhost:8080
- **Credenciales**:
  - Sistema: PostgreSQL
  - Servidor: ctf_monitor_db
  - Usuario: monitor_user
  - Contraseña: monitor_pass_2024
  - Base de datos: ctf_monitor

---

## 🔧 API Endpoints

### Dashboard de Estudiantes (Puerto 5000)

#### Obtener todos los retos
```bash
curl http://localhost:5000/api/challenges
```

#### Obtener progreso
```bash
curl http://localhost:5000/api/progress
```

#### Enviar una flag
```bash
curl -X POST http://localhost:5000/api/submit \
  -H "Content-Type: application/json" \
  -d '{"flag":"FLAG{...}"}'
```

#### Obtener pista de un reto
```bash
curl http://localhost:5000/api/hint/1
```

### Monitor del Profesor (Puerto 5001)

#### Health check
```bash
curl http://localhost:5001/health
```

#### Lista de estudiantes
```bash
curl http://localhost:5001/api/students
```

#### Tabla de posiciones
```bash
curl http://localhost:5001/api/leaderboard
```

#### Estadísticas globales
```bash
curl http://localhost:5001/api/statistics
```

#### Eliminar estudiante
```bash
curl -X DELETE http://localhost:5001/api/student/<DOCUMENTO>
```

#### Eventos recientes
```bash
curl http://localhost:5001/api/events/recent
```

---

## 🗑️ Eliminar Estudiantes de la Base de Datos

### Eliminar un estudiante específico
```bash
curl -X DELETE http://localhost:5001/api/student/1234567890
```

### Eliminar múltiples estudiantes
```bash
for doc in 1111111111 2222222222 3333333333; do
  curl -X DELETE http://localhost:5001/api/student/$doc
done
```

### Verificar estudiantes registrados
```bash
curl http://localhost:5001/api/students | python3 -m json.tool
```

---

## 🐛 Troubleshooting

### Los retos no se ven en el dashboard
1. **Verificar que el servicio está corriendo**:
   ```bash
   curl http://localhost:5000/api/challenges
   ```

2. **Limpiar caché del navegador**:
   - Presiona `Ctrl + Shift + R` (hard refresh)
   - O abre el navegador en modo incógnito

3. **Reiniciar el dashboard**:
   ```bash
   pkill -f "python3 web_dashboard.py"
   python3 web_dashboard.py &
   ```

### El monitor del profesor no responde
1. **Verificar contenedores Docker**:
   ```bash
   docker ps --filter "name=ctf_monitor"
   ```

2. **Ver logs del monitor**:
   ```bash
   cd mqtt_monitor
   docker-compose logs -f monitor_app
   ```

3. **Reiniciar el monitor**:
   ```bash
   cd mqtt_monitor
   ./deploy.sh
   ```

### Error de conexión a PostgreSQL
1. **Verificar que el contenedor está corriendo**:
   ```bash
   docker ps | grep ctf_monitor_db
   ```

2. **Reiniciar base de datos**:
   ```bash
   cd mqtt_monitor
   docker-compose restart ctf_monitor_db
   ```

---

## 📝 Archivos de Configuración

### Dashboard de Estudiantes
- **Código principal**: `web_dashboard.py`
- **Template HTML**: `templates/index.html`
- **Retos**: `docker_challenge.py`

### Monitor del Profesor
- **Código principal**: `mqtt_monitor/app.py`
- **Base de datos**: `mqtt_monitor/db.py`
- **Configuración Docker**: `mqtt_monitor/docker-compose.yml`
- **Template HTML**: `mqtt_monitor/templates/dashboard.html`
- **Schema SQL**: `mqtt_monitor/init.sql`

---

## 🎓 Para Estudiantes

1. **Abrir dashboard**: http://localhost:5000
2. **Ver retos disponibles**: Los 15 retos aparecen en la página principal
3. **Copiar la flag**: Cada reto muestra su flag única
4. **Completar el reto**: Ejecutar los comandos Docker necesarios
5. **Enviar la flag**: Pegar la flag en el formulario y enviar
6. **Ver progreso**: El sistema actualiza automáticamente los puntos

---

## 👨‍🏫 Para Profesores

1. **Abrir monitor**: http://localhost:5001
2. **Ver estudiantes activos**: En tiempo real
3. **Revisar leaderboard**: Tabla de posiciones ordenada por puntos
4. **Ver estadísticas**: Métricas globales del curso
5. **Eliminar estudiantes**: Usar endpoint DELETE o Adminer
6. **Acceder a BD**: http://localhost:8080 para consultas SQL

---

## 🔐 Seguridad

- Las flags son únicas por estudiante (basadas en documento)
- Los datos se persisten en PostgreSQL
- El monitor del profesor está separado del dashboard de estudiantes
- Los estudiantes solo tienen acceso a su propio progreso

---

## 📚 Documentación Adicional

- **Guía del Profesor**: `GUIA_PROFESOR.md`
- **Taller**: `TALLER.md`
- **Sistema de BD**: `mqtt_monitor/SISTEMA_BD.md`
- **Deploy**: `mqtt_monitor/DEPLOY.md`
- **Inicio Rápido**: `INICIO_RAPIDO.md`
