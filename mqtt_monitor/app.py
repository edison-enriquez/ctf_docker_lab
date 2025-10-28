"""
Plantilla básica para app.py - MQTT Monitor

Este archivo proporciona una estructura inicial para el servidor de monitoreo.
El agente desarrollador debe expandir esta plantilla con la implementación completa.

Características que debe incluir:
- Cliente MQTT subscriber
- API REST con Flask
- WebSocket para tiempo real con Flask-SocketIO
- Almacenamiento de datos (SQLite/memoria)
- Detección de estudiantes offline
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
MQTT_BROKER = os.getenv('MQTT_BROKER', 'broker.hivemq.com')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'docker_ctf_lab/+/+')
HEARTBEAT_TIMEOUT = int(os.getenv('HEARTBEAT_TIMEOUT', 90))

# Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*")

# Almacenamiento en memoria (implementar persistencia según especificaciones)
students_data = {}
recent_events = []


# ============================================================================
# MQTT CLIENT
# ============================================================================

def on_mqtt_connect(client, userdata, flags, rc):
    """Callback cuando se conecta al broker MQTT"""
    if rc == 0:
        print(f"✅ Conectado a MQTT broker {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Suscrito a tópico: {MQTT_TOPIC}")
    else:
        print(f"❌ Error de conexión MQTT: {rc}")


def on_mqtt_message(client, userdata, msg):
    """Callback cuando llega un mensaje MQTT"""
    try:
        topic_parts = msg.topic.split('/')
        documento = topic_parts[1]
        event_type = topic_parts[2]
        
        payload = json.loads(msg.payload.decode())
        
        # Agregar a eventos recientes
        event = {
            'timestamp': datetime.now().isoformat(),
            'documento': documento,
            'type': event_type,
            'data': payload
        }
        recent_events.insert(0, event)
        
        # Mantener solo los últimos 100 eventos
        if len(recent_events) > 100:
            recent_events.pop()
        
        # Procesar según tipo de evento
        if event_type == 'heartbeat':
            handle_heartbeat(documento, payload)
        elif event_type == 'progress':
            handle_progress(documento, payload)
        elif event_type == 'flag_submit':
            handle_flag_submit(documento, payload)
        
        # Emitir evento via WebSocket
        socketio.emit(event_type, event, broadcast=True)
        
    except Exception as e:
        print(f"❌ Error procesando mensaje MQTT: {e}")


def handle_heartbeat(documento, payload):
    """Procesa un evento de heartbeat"""
    # TODO: Implementar lógica de heartbeat
    # - Actualizar last_seen
    # - Marcar como online
    # - Actualizar progreso básico
    
    if documento not in students_data:
        students_data[documento] = {
            'documento': documento,
            'first_seen': datetime.now().isoformat(),
            'completados': [],
            'events': []
        }
    
    students_data[documento].update({
        'last_seen': datetime.now().isoformat(),
        'status': 'online',
        'completados_count': payload.get('completados', 0),
        'puntos': payload.get('puntos', 0)
    })
    
    print(f"💓 Heartbeat de {documento}: {payload.get('completados', 0)} retos, {payload.get('puntos', 0)} pts")


def handle_progress(documento, payload):
    """Procesa un evento de progreso completo"""
    # TODO: Implementar lógica de progreso
    # - Actualizar retos completados
    # - Calcular estadísticas
    # - Guardar en base de datos
    
    if documento in students_data:
        students_data[documento].update({
            'last_progress': datetime.now().isoformat(),
            'completados': payload.get('retos_completados', []),
            'progreso_porcentaje': payload.get('progreso_porcentaje', 0)
        })
    
    print(f"📊 Progreso de {documento}: {payload.get('progreso_porcentaje', 0)}%")


def handle_flag_submit(documento, payload):
    """Procesa un evento de flag enviada"""
    # TODO: Implementar lógica de flag submit
    # - Registrar reto completado
    # - Actualizar estadísticas
    # - Emitir notificación
    
    reto_nombre = payload.get('reto_nombre', 'Unknown')
    puntos = payload.get('puntos_ganados', 0)
    
    # Emitir notificación
    notification = {
        'type': 'flag_submitted',
        'documento': documento,
        'reto': reto_nombre,
        'puntos': puntos,
        'timestamp': datetime.now().isoformat()
    }
    socketio.emit('notification', notification, broadcast=True)
    
    print(f"🎯 {documento} completó '{reto_nombre}' (+{puntos} pts)")


# Inicializar cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_mqtt_connect
mqtt_client.on_message = on_mqtt_message


# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/')
def index():
    """Página principal del dashboard"""
    return render_template('dashboard.html')


@app.route('/api/students')
def get_students():
    """Obtener lista de todos los estudiantes"""
    # TODO: Implementar lógica completa
    # - Calcular estado online/offline
    # - Ordenar por actividad reciente
    # - Incluir estadísticas
    
    students = []
    now = datetime.now()
    
    for doc, data in students_data.items():
        last_seen = datetime.fromisoformat(data.get('last_seen', datetime.now().isoformat()))
        is_online = (now - last_seen).total_seconds() < HEARTBEAT_TIMEOUT
        
        students.append({
            'documento': doc,
            'status': 'online' if is_online else 'offline',
            'completados': data.get('completados_count', 0),
            'puntos': data.get('puntos', 0),
            'last_seen': data.get('last_seen'),
            'progreso_porcentaje': data.get('progreso_porcentaje', 0)
        })
    
    return jsonify(students)


@app.route('/api/students/online')
def get_online_students():
    """Obtener solo estudiantes activos"""
    # TODO: Filtrar solo estudiantes online
    students = get_students().json
    online = [s for s in students if s['status'] == 'online']
    return jsonify(online)


@app.route('/api/students/<documento>')
def get_student_detail(documento):
    """Obtener detalles de un estudiante específico"""
    # TODO: Implementar vista detallada
    # - Historial de retos
    # - Gráficos de progreso
    # - Tiempos promedio
    
    if documento not in students_data:
        return jsonify({'error': 'Student not found'}), 404
    
    return jsonify(students_data[documento])


@app.route('/api/statistics')
def get_statistics():
    """Obtener estadísticas globales"""
    # TODO: Implementar cálculo de estadísticas
    # - Total de estudiantes
    # - Promedio de progreso
    # - Distribución de completados
    
    total = len(students_data)
    online = sum(1 for s in students_data.values() 
                 if (datetime.now() - datetime.fromisoformat(s.get('last_seen', datetime.now().isoformat()))).total_seconds() < HEARTBEAT_TIMEOUT)
    
    stats = {
        'total_students': total,
        'online_students': online,
        'offline_students': total - online,
        'avg_progress': sum(s.get('progreso_porcentaje', 0) for s in students_data.values()) / total if total > 0 else 0,
        'total_events': len(recent_events)
    }
    
    return jsonify(stats)


@app.route('/api/leaderboard')
def get_leaderboard():
    """Obtener ranking de estudiantes por puntos"""
    # TODO: Implementar ranking
    students = list(students_data.values())
    students.sort(key=lambda x: x.get('puntos', 0), reverse=True)
    
    leaderboard = [
        {
            'rank': i + 1,
            'documento': s['documento'],
            'puntos': s.get('puntos', 0),
            'completados': s.get('completados_count', 0)
        }
        for i, s in enumerate(students)
    ]
    
    return jsonify(leaderboard)


@app.route('/api/events/recent')
def get_recent_events():
    """Obtener eventos recientes"""
    limit = request.args.get('limit', 50, type=int)
    return jsonify(recent_events[:limit])


# ============================================================================
# WEBSOCKET EVENTS
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Cliente WebSocket conectado"""
    print(f"🔌 Cliente WebSocket conectado: {request.sid}")
    emit('connected', {'status': 'success'})


@socketio.on('disconnect')
def handle_disconnect():
    """Cliente WebSocket desconectado"""
    print(f"🔌 Cliente WebSocket desconectado: {request.sid}")


# ============================================================================
# MAIN
# ============================================================================

def start_mqtt():
    """Iniciar cliente MQTT en background"""
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        print(f"🚀 Cliente MQTT iniciado")
    except Exception as e:
        print(f"❌ Error iniciando MQTT: {e}")


if __name__ == '__main__':
    print("="*60)
    print("🚀 MQTT Monitoring Dashboard - Docker CTF Lab")
    print("="*60)
    print(f"📡 MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"🌐 Web Server: http://0.0.0.0:{os.getenv('FLASK_PORT', 5001)}")
    print("="*60)
    
    # Iniciar MQTT
    start_mqtt()
    
    # Iniciar Flask con SocketIO
    socketio.run(
        app,
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5001)),
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    )
