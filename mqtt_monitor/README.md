# 📡 MQTT Monitoring System - Especificaciones para Desarrollo

## 🎯 Objetivo

Crear un sistema de monitoreo en tiempo real para que el **profesor** pueda visualizar el progreso de todos los estudiantes que están realizando el Docker CTF Lab. El sistema debe recibir datos vía MQTT y mostrarlos en un dashboard web profesional estilo hacker.

---

## 📋 Especificaciones Técnicas

### 1. Arquitectura del Sistema

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Estudiantes   │ ────►   │   MQTT Broker    │ ────►   │   Monitor Web   │
│  (docker_ctf)   │ PUBLISH │ (HiveMQ/Mosquitto│ SUBSCRIBE│   (Profesor)    │
└─────────────────┘         └──────────────────┘         └─────────────────┘
```

**Componentes a desarrollar:**

1. **Servidor MQTT Subscriber** (Python)
   - Se conecta al broker MQTT
   - Suscribe a tópicos de eventos
   - Almacena datos en memoria/base de datos

2. **API REST** (Flask/FastAPI)
   - Expone datos recolectados
   - Endpoints para estadísticas
   - WebSocket para actualizaciones en tiempo real

3. **Dashboard Web** (HTML/CSS/JavaScript)
   - Visualización en tiempo real
   - Estilo hacker similar al lab
   - Gráficos y estadísticas

---

## 🔌 Protocolo MQTT

### Broker Configurado

**Por defecto en `docker_challenge.py`:**
- Broker: `broker.hivemq.com`
- Puerto: `1883`
- Protocolo: MQTT v3.1.1
- Sin autenticación (puede configurarse con env vars)

### Tópicos MQTT

El sistema actual publica en estos tópicos:

```
docker_ctf_lab/{documento}/heartbeat
docker_ctf_lab/{documento}/progress
docker_ctf_lab/{documento}/flag_submit
```

**Variables de tópico:**
- `{documento}`: Identificador único del estudiante (ej: "1234567890")

### Estructura de Mensajes

#### 1. **Heartbeat** (Cada 30 segundos)

**Tópico:** `docker_ctf_lab/{documento}/heartbeat`

**Payload (JSON):**
```json
{
  "timestamp": "2024-01-15T14:30:00.123456",
  "documento": "1234567890",
  "status": "online",
  "completados": 5,
  "puntos": 120
}
```

**Descripción:**
- Indica que el estudiante está activo
- Envía resumen rápido de progreso
- Se envía automáticamente desde el dashboard cada 30 segundos

---

#### 2. **Progress Report** (Reporte completo)

**Tópico:** `docker_ctf_lab/{documento}/progress`

**Payload (JSON):**
```json
{
  "timestamp": "2024-01-15T14:30:00.123456",
  "documento": "1234567890",
  "completados": 5,
  "puntos": 120,
  "total_retos": 15,
  "total_puntos": 380,
  "progreso_porcentaje": 33.3,
  "retos_completados": [1, 2, 3, 4, 5],
  "ultimo_reto_completado": {
    "id": 5,
    "nombre": "Reto SSH",
    "puntos": 30,
    "timestamp": "2024-01-15T14:25:00.000000"
  }
}
```

**Descripción:**
- Se envía cuando el estudiante completa un reto
- Incluye estado completo del progreso
- Útil para estadísticas detalladas

---

#### 3. **Flag Submit** (Bandera enviada)

**Tópico:** `docker_ctf_lab/{documento}/flag_submit`

**Payload (JSON):**
```json
{
  "timestamp": "2024-01-15T14:25:00.123456",
  "documento": "1234567890",
  "reto_id": 5,
  "reto_nombre": "Conexión SSH entre contenedores",
  "flag": "FLAG{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}",
  "puntos_ganados": 30,
  "puntos_totales": 120,
  "completados": 5,
  "es_correcto": true
}
```

**Descripción:**
- Se envía cuando el estudiante completa un reto exitosamente
- Incluye detalles del reto completado
- Permite ver actividad en tiempo real

---

## 🛠️ Stack Tecnológico Recomendado

### Backend

**Opción 1: Flask + SocketIO (Recomendado)**
```python
- Flask: API REST
- Flask-SocketIO: WebSocket para tiempo real
- paho-mqtt: Cliente MQTT
- SQLite/JSON: Persistencia de datos (opcional)
```

**Opción 2: FastAPI + WebSockets**
```python
- FastAPI: API REST moderna
- WebSockets nativo
- paho-mqtt: Cliente MQTT
- Redis: Cache en memoria (opcional)
```

### Frontend

```javascript
- HTML5 + CSS3
- JavaScript Vanilla o Vue.js ligero
- Socket.io-client (si usas Flask-SocketIO)
- Chart.js o ApexCharts para gráficos
- Diseño: Estilo hacker similar al lab
```

---

## 📊 Funcionalidades Requeridas

### 1. **Dashboard Principal**

**Vista General:**
- [ ] Lista de estudiantes conectados (online/offline)
- [ ] Última actividad de cada estudiante
- [ ] Progreso visual (barra de progreso)
- [ ] Puntos acumulados
- [ ] Tiempo de sesión activa

**Indicadores visuales:**
```
┌─────────────────────────────────────────────────────┐
│ 📡 MONITORING DASHBOARD - DOCKER CTF LAB            │
├─────────────────────────────────────────────────────┤
│ 🟢 Online: 15 | 🔴 Offline: 3 | 📊 Total: 18        │
└─────────────────────────────────────────────────────┘

┌──────────┬───────────┬──────────┬─────────┬──────────┐
│ STUDENT  │  STATUS   │ PROGRESS │ POINTS  │ LAST SEEN│
├──────────┼───────────┼──────────┼─────────┼──────────┤
│ 1234567  │ 🟢 Online │ ████████ │ 280/380 │ 2s ago   │
│ 9876543  │ 🟢 Online │ ████░░░░ │ 150/380 │ 5s ago   │
│ 5555555  │ 🔴 Offline│ ██░░░░░░ │  60/380 │ 15m ago  │
└──────────┴───────────┴──────────┴─────────┴──────────┘
```

---

### 2. **Vista Detallada por Estudiante**

Al hacer clic en un estudiante:

- [ ] Historial de retos completados con timestamps
- [ ] Gráfico de progreso en el tiempo
- [ ] Banderas capturadas
- [ ] Tiempo promedio por reto
- [ ] Retos pendientes
- [ ] Sesiones activas

---

### 3. **Estadísticas Globales**

- [ ] Total de estudiantes activos/inactivos
- [ ] Promedio de retos completados
- [ ] Distribución de progreso (histograma)
- [ ] Ranking de estudiantes por puntos
- [ ] Retos más difíciles (mayor tiempo promedio)
- [ ] Gráfico de actividad por hora

---

### 4. **Notificaciones en Tiempo Real**

- [ ] Toast notification cuando un estudiante completa un reto
- [ ] Sonido opcional para nuevos eventos
- [ ] Log de actividad reciente
- [ ] Filtros por tipo de evento

Ejemplo de notificación:
```
🎉 [14:25:30] Estudiante 1234567 completó "Conexión SSH" (+30 pts)
```

---

## 🎨 Diseño Visual

### Paleta de Colores (Igual al lab)

```css
:root {
    --bg-primary: #0a0e27;
    --bg-secondary: #111827;
    --bg-tertiary: #1a1f3a;
    --accent-green: #00ff41;
    --accent-cyan: #00d9ff;
    --accent-purple: #9d4edd;
    --accent-red: #ff006e;
    --text-primary: #e0e0e0;
    --text-secondary: #a0a0a0;
}
```

### Tipografía

```css
font-family: 'Fira Code', 'Share Tech Mono', monospace;
```

### Elementos Visuales

- [x] Fondo oscuro con efecto Matrix (opcional)
- [x] Bordes con glow verde neón
- [x] Animaciones sutiles de escaneo
- [x] Fuentes monoespaciadas
- [x] Iconos de estado (🟢🔴⚡🏆)
- [x] Efectos hover con glow

---

## 🔧 Endpoints API Requeridos

### REST API

```
GET  /api/students              → Lista de todos los estudiantes
GET  /api/students/{documento}  → Detalles de un estudiante
GET  /api/students/online       → Solo estudiantes activos
GET  /api/statistics            → Estadísticas globales
GET  /api/events/recent         → Últimos eventos (últimos 100)
GET  /api/leaderboard           → Ranking por puntos
```

### WebSocket Events (Tiempo Real)

```javascript
// Cliente se conecta
socket.on('connect', () => { ... })

// Nuevo heartbeat recibido
socket.on('heartbeat', (data) => { ... })

// Nuevo progreso
socket.on('progress_update', (data) => { ... })

// Nueva flag enviada
socket.on('flag_submitted', (data) => { ... })

// Estudiante se conectó/desconectó
socket.on('student_status', (data) => { ... })
```

---

## 📁 Estructura de Archivos Propuesta

```
mqtt_monitor/
├── README.md                    # Este archivo
├── requirements.txt             # Dependencias Python
├── config.py                    # Configuración
├── app.py                       # Aplicación principal
├── mqtt_client.py               # Cliente MQTT subscriber
├── models.py                    # Modelos de datos
├── database.py                  # Almacenamiento (opcional)
├── api/
│   ├── __init__.py
│   ├── routes.py                # Rutas de la API
│   └── websockets.py            # WebSocket handlers
├── static/
│   ├── css/
│   │   └── dashboard.css        # Estilos del dashboard
│   ├── js/
│   │   ├── dashboard.js         # Lógica principal
│   │   ├── charts.js            # Gráficos
│   │   └── websocket-client.js  # Cliente WebSocket
│   └── img/
│       └── logo.png
├── templates/
│   ├── dashboard.html           # Vista principal
│   └── student_detail.html      # Vista de estudiante
├── docker-compose.yml           # Opcional: despliegue con Docker
└── .env.example                 # Variables de entorno
```

---

## 🚀 Configuración y Variables de Entorno

### `.env` requerido

```bash
# MQTT Configuration
MQTT_BROKER=broker.hivemq.com
MQTT_PORT=1883
MQTT_TOPIC=docker_ctf_lab/+/+
MQTT_USERNAME=                    # Opcional
MQTT_PASSWORD=                    # Opcional

# Flask Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5001
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Database (opcional)
DATABASE_TYPE=sqlite              # sqlite, redis, memory
DATABASE_PATH=./monitor.db

# Features
ENABLE_WEBSOCKET=True
ENABLE_NOTIFICATIONS=True
HEARTBEAT_TIMEOUT=90              # Segundos sin heartbeat = offline
```

---

## 💾 Almacenamiento de Datos

### Opción 1: En Memoria (Simple)

```python
# Estructura de datos en memoria
students = {
    "1234567890": {
        "documento": "1234567890",
        "last_seen": datetime,
        "status": "online",
        "completados": 5,
        "puntos": 120,
        "history": [...]
    }
}
```

**Pros:** Simple, rápido
**Cons:** Se pierde al reiniciar

---

### Opción 2: SQLite (Recomendado)

```sql
CREATE TABLE students (
    documento VARCHAR(20) PRIMARY KEY,
    last_seen TIMESTAMP,
    status VARCHAR(10),
    completados INTEGER,
    puntos INTEGER,
    total_retos INTEGER
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento VARCHAR(20),
    event_type VARCHAR(20),
    timestamp TIMESTAMP,
    payload JSON,
    FOREIGN KEY (documento) REFERENCES students(documento)
);
```

**Pros:** Persistente, consultas SQL
**Cons:** Requiere setup inicial

---

### Opción 3: Redis (Avanzado)

```python
# Para alta concurrencia y tiempo real
redis_client.hset(f"student:{documento}", mapping={
    "last_seen": timestamp,
    "status": "online",
    ...
})
```

**Pros:** Muy rápido, pub/sub integrado
**Cons:** Requiere Redis server

---

## 🧪 Testing y Simulación

### Generar Datos de Prueba

Crear script `mqtt_test_publisher.py` para simular estudiantes:

```python
import paho.mqtt.client as mqtt
import json
import time
import random

broker = "broker.hivemq.com"
documentos = ["1111111", "2222222", "3333333"]

client = mqtt.Client()
client.connect(broker, 1883)

while True:
    for doc in documentos:
        # Simular heartbeat
        payload = {
            "timestamp": datetime.now().isoformat(),
            "documento": doc,
            "status": "online",
            "completados": random.randint(0, 15),
            "puntos": random.randint(0, 380)
        }
        client.publish(f"docker_ctf_lab/{doc}/heartbeat", json.dumps(payload))
    
    time.sleep(5)
```

---

## 📝 Checklist de Desarrollo

### Fase 1: Backend MQTT + API
- [ ] Cliente MQTT conecta al broker
- [ ] Suscripción a tópicos con wildcard (+)
- [ ] Parser de mensajes JSON
- [ ] Almacenamiento de datos
- [ ] Detección de estudiantes offline (timeout)
- [ ] API REST con endpoints básicos
- [ ] CORS configurado correctamente

### Fase 2: Frontend Base
- [ ] HTML con diseño hacker-style
- [ ] CSS con paleta de colores
- [ ] JavaScript para consumir API
- [ ] Tabla de estudiantes
- [ ] Indicadores de estado (online/offline)
- [ ] Auto-refresh cada 5 segundos

### Fase 3: Tiempo Real
- [ ] WebSocket server configurado
- [ ] Cliente WebSocket en frontend
- [ ] Eventos en tiempo real
- [ ] Notificaciones toast
- [ ] Actualización automática sin refresh

### Fase 4: Visualización Avanzada
- [ ] Gráficos de progreso
- [ ] Histograma de distribución
- [ ] Ranking/leaderboard
- [ ] Vista detallada por estudiante
- [ ] Filtros y búsqueda

### Fase 5: Mejoras
- [ ] Sonidos para notificaciones
- [ ] Exportar datos a CSV/JSON
- [ ] Temas claro/oscuro (opcional)
- [ ] Autenticación para profesor
- [ ] Docker deployment ready

---

## 🎯 Resultado Esperado

Un dashboard profesional donde el profesor puede:

1. ✅ Ver todos los estudiantes activos en tiempo real
2. ✅ Monitorear el progreso de cada uno
3. ✅ Recibir notificaciones cuando completan retos
4. ✅ Analizar estadísticas globales
5. ✅ Identificar estudiantes con dificultades
6. ✅ Exportar datos para calificación

---

## 🔗 Referencias

- **Paho MQTT Python:** https://www.eclipse.org/paho/index.php?page=clients/python/index.php
- **Flask-SocketIO:** https://flask-socketio.readthedocs.io/
- **Chart.js:** https://www.chartjs.org/
- **HiveMQ Public Broker:** https://www.hivemq.com/public-mqtt-broker/

---

## 📞 Notas para el Agente Desarrollador

**Prioridades:**
1. **Tiempo real** es crucial - usar WebSockets
2. **Diseño visual** debe ser consistente con el lab
3. **Manejo de offline** - detectar cuando estudiantes se desconectan
4. **Performance** - debe manejar 50+ estudiantes simultáneos
5. **Simplicidad** - código limpio y bien documentado

**Tecnologías obligatorias:**
- Python 3.8+
- paho-mqtt
- Flask o FastAPI
- WebSockets (Flask-SocketIO o nativo)

**Tecnologías opcionales:**
- Redis (si quieres más performance)
- Docker (para deployment)
- Vue.js (si prefieres framework JS)

---

## ✨ Bonus Features (Opcionales)

- [ ] Historial de sesiones por estudiante
- [ ] Alertas cuando un estudiante se estanca
- [ ] Comparación entre estudiantes
- [ ] Exportación de reportes PDF
- [ ] Integración con Google Sheets
- [ ] Modo presentación (proyector)
- [ ] Dark/Light theme toggle
- [ ] Sonidos personalizables
- [ ] Autenticación con contraseña

---

**¡Adelante! El sistema está completamente especificado. Solo necesitas implementarlo siguiendo estas guías.**

🚀 **Good luck, hacker!**
