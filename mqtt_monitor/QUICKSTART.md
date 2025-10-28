# 🚀 Quick Start Guide - MQTT Monitoring System

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- MQTT broker access (default: broker.hivemq.com)

---

## ⚡ Installation

### 1. Navigate to the mqtt_monitor directory

```bash
cd mqtt_monitor
```

### 2. Create virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env with your preferred settings
nano .env
```

---

## 🎯 Running the Monitor

### Development Mode

```bash
python app.py
```

The dashboard will be available at: **http://localhost:5001**

### Production Mode

```bash
# Using gunicorn
pip install gunicorn
gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5001 app:app

# Or using waitress
pip install waitress
waitress-serve --listen=0.0.0.0:5001 app:app
```

---

## 🧪 Testing with Simulated Data

Generate test data to see the dashboard in action:

```bash
python mqtt_test_publisher.py
```

This will simulate multiple students sending events.

---

## 🐳 Docker Deployment (Optional)

### Build and run with Docker

```bash
docker build -t mqtt-monitor .
docker run -p 5001:5001 --env-file .env mqtt-monitor
```

### Using Docker Compose

```bash
docker-compose up -d
```

---

## 📊 Dashboard Features

### Main View

- Real-time student list
- Online/offline status
- Progress bars
- Points and completion percentage
- Last activity timestamp

### Student Detail View

- Click on any student to see:
  - Complete challenge history
  - Timeline of completed challenges
  - Total session time
  - Average time per challenge

### Statistics Panel

- Global completion statistics
- Active vs inactive students
- Leaderboard ranking
- Activity graphs

---

## 🔧 Configuration Options

### MQTT Settings

Edit `.env` to change MQTT broker:

```env
MQTT_BROKER=your-broker.com
MQTT_PORT=1883
MQTT_USERNAME=your-username
MQTT_PASSWORD=your-password
```

### WebSocket Settings

```env
ENABLE_WEBSOCKET=True  # Real-time updates
```

### Timeouts

```env
HEARTBEAT_TIMEOUT=90   # Seconds without heartbeat = offline
SESSION_TIMEOUT=300    # Inactive session timeout
```

---

## 🎨 UI Customization

The dashboard uses the same hacker-style theme as the Docker CTF Lab.

Colors can be customized in `static/css/dashboard.css`:

```css
:root {
    --bg-primary: #0a0e27;
    --accent-green: #00ff41;
    --accent-cyan: #00d9ff;
    /* ... */
}
```

---

## 📡 MQTT Topics

The system subscribes to:

```
docker_ctf_lab/+/heartbeat
docker_ctf_lab/+/progress
docker_ctf_lab/+/flag_submit
```

**Topic structure:** `docker_ctf_lab/{student_id}/{event_type}`

---

## 🔍 Troubleshooting

### Students not appearing

1. Check MQTT broker connection
2. Verify students are sending heartbeats
3. Check firewall/network settings
4. Review console logs for errors

### WebSocket not working

1. Ensure `ENABLE_WEBSOCKET=True` in `.env`
2. Check browser console for errors
3. Verify Flask-SocketIO is installed
4. Try disabling ad blockers

### Database issues

```bash
# Reset database
rm monitor.db
python app.py  # Will recreate on startup
```

---

## 📝 API Endpoints

### REST API

```
GET /api/students              # All students
GET /api/students/online       # Only online students
GET /api/students/{id}         # Specific student
GET /api/statistics            # Global stats
GET /api/leaderboard           # Rankings
GET /api/events/recent         # Recent events
```

### WebSocket Events

```javascript
socket.on('heartbeat', (data) => { ... })
socket.on('progress_update', (data) => { ... })
socket.on('flag_submitted', (data) => { ... })
socket.on('student_status', (data) => { ... })
```

---

## 🛠️ Development

### Project Structure

```
mqtt_monitor/
├── app.py                  # Main application
├── mqtt_client.py          # MQTT subscriber
├── models.py               # Data models
├── database.py             # Database operations
├── api/
│   └── routes.py           # API endpoints
├── static/
│   ├── css/
│   └── js/
└── templates/
    └── dashboard.html
```

### Adding New Features

1. MQTT events: Edit `mqtt_client.py`
2. API endpoints: Add to `api/routes.py`
3. Frontend: Modify `templates/dashboard.html`
4. Styles: Update `static/css/dashboard.css`

---

## 📚 Additional Resources

- [Paho MQTT Documentation](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [HiveMQ Public Broker](https://www.hivemq.com/public-mqtt-broker/)

---

## 🆘 Support

If you encounter issues:

1. Check the console logs
2. Review the `.env` configuration
3. Ensure all dependencies are installed
4. Verify MQTT broker is accessible

---

**Happy Monitoring! 🚀**
