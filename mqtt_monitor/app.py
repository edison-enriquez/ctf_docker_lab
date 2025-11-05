#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker CTF Lab - MQTT Monitoring Dashboard
Monitor en tiempo real con PostgreSQL y Docker
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging
from db import get_db

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración
MQTT_BROKER = os.getenv('MQTT_BROKER', 'broker.hivemq.com')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'docker_ctf_lab/+/+')
HEARTBEAT_TIMEOUT = int(os.getenv('HEARTBEAT_TIMEOUT', 90))
PORT = int(os.getenv('PORT', 5001))
HOST = os.getenv('HOST', '0.0.0.0')

# Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*")

# Database
db = None

# ============================================================================
# MQTT CLIENT
# ============================================================================

def on_mqtt_connect(client, userdata, flags, rc):
    """Callback cuando se conecta al broker MQTT"""
    if rc == 0:
        logger.info(f"✅ Conectado a MQTT broker {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
        logger.info(f"📡 Suscrito a tópico: {MQTT_TOPIC}")
    else:
        logger.error(f"❌ Error de conexión MQTT: {rc}")


def on_mqtt_message(client, userdata, msg):
    """Callback cuando llega un mensaje MQTT"""
    try:
        topic_parts = msg.topic.split('/')
        if len(topic_parts) < 3:
            return
        
        documento = topic_parts[1]
        event_type = topic_parts[2]
        
        payload = json.loads(msg.payload.decode())
        
        # Registrar evento en base de datos
        db.registrar_evento_mqtt(
            documento=documento,
            event_type=event_type,
            payload=payload,
            topic=msg.topic
        )
        
        # Procesar según tipo de evento
        if event_type == 'heartbeat':
            handle_heartbeat(documento, payload)
        elif event_type == 'progress':
            handle_progress(documento, payload)
        elif event_type == 'flag_submit':
            handle_flag_submit(documento, payload)
        
        # Emitir evento via WebSocket
        event = {
            'timestamp': datetime.now().isoformat(),
            'documento': documento,
            'type': event_type,
            'data': payload
        }
        socketio.emit(event_type, event)
        
    except Exception as e:
        logger.error(f"❌ Error procesando mensaje MQTT: {e}")


def handle_heartbeat(documento, payload):
    """Procesa un evento de heartbeat"""
    try:
        # Actualizar estudiante como online
        db.upsert_estudiante(
            documento=documento,
            status='online'
        )
        
        # Actualizar estadísticas si vienen en el payload
        if 'completados' in payload and 'puntos' in payload:
            completados_data = payload.get('completados', [])
            # Si completados es un entero, usar directamente; si es lista, contar elementos
            completados = completados_data if isinstance(completados_data, int) else len(completados_data)
            puntos = payload.get('puntos', 0)
            porcentaje = (completados / 15) * 100  # 15 retos totales
            
            db.update_estudiante_stats(
                documento=documento,
                total_puntos=puntos,
                total_retos=completados,
                porcentaje=porcentaje
            )
        
        logger.info(f"💓 Heartbeat de {documento}: {payload.get('completados', 0)} retos, {payload.get('puntos', 0)} pts")
        
    except Exception as e:
        logger.error(f"Error en handle_heartbeat: {e}")


def handle_progress(documento, payload):
    """Procesa un evento de progreso"""
    try:
        completados_data = payload.get('completados', [])
        completados = completados_data if isinstance(completados_data, int) else len(completados_data)
        puntos = payload.get('puntos', 0)
        porcentaje = (completados / 15) * 100
        
        db.update_estudiante_stats(
            documento=documento,
            total_puntos=puntos,
            total_retos=completados,
            porcentaje=porcentaje
        )
        
        logger.info(f"📊 Progreso de {documento}: {porcentaje}%")
        
        # Emitir actualización específica
        socketio.emit('student_update', {
            'documento': documento,
            'completados': completados,
            'puntos': puntos,
            'porcentaje': porcentaje
        })
        
    except Exception as e:
        logger.error(f"Error en handle_progress: {e}")


def handle_flag_submit(documento, payload):
    """Procesa un evento de flag enviada"""
    try:
        reto_id = payload.get('reto_id')
        reto_nombre = payload.get('reto_nombre', f'Reto #{reto_id}')
        puntos = payload.get('puntos', 0)
        flag = payload.get('flag')
        
        # Registrar reto completado
        registro_id = db.registrar_reto_completado(
            documento=documento,
            reto_id=reto_id,
            reto_nombre=reto_nombre,
            puntos=puntos,
            flag=flag
        )
        
        if registro_id:
            logger.info(f"🎯 {documento} completó '{reto_nombre}' (+{puntos} pts)")
            
            # Emitir notificación
            socketio.emit('notification', {
                'type': 'flag_submitted',
                'documento': documento,
                'reto': reto_nombre,
                'puntos': puntos,
                'timestamp': datetime.now().isoformat()
            })
        
    except Exception as e:
        logger.error(f"Error en handle_flag_submit: {e}")


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


@app.route('/health')
def health():
    """Health check endpoint"""
    db_health = db.get_health() if db else {'status': 'not_initialized'}
    
    return jsonify({
        'status': 'healthy' if db_health['status'] == 'healthy' else 'degraded',
        'database': db_health,
        'mqtt': 'connected' if mqtt_client.is_connected() else 'disconnected',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/students')
def get_students():
    """Obtener lista de todos los estudiantes"""
    try:
        estudiantes = db.get_all_estudiantes()
        
        # Convertir a formato JSON serializable
        result = []
        for est in estudiantes:
            result.append({
                'documento': est['documento'],
                'nombre': est['nombre'],
                'email': est['email'],
                'status': est['status'],
                'total_puntos': int(est['puntos_totales']) if est['puntos_totales'] else 0,
                'total_retos_completados': int(est['retos_completados']) if est['retos_completados'] else 0,
                'porcentaje_completado': float(est['porcentaje_completado']) if est['porcentaje_completado'] else 0.0,
                'last_seen': est['last_seen'].isoformat() if est['last_seen'] else None,
                'segundos_inactivo': int(est['segundos_inactivo']) if est['segundos_inactivo'] else 0,
                'first_seen': est['first_seen'].isoformat() if est['first_seen'] else None
            })
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error en get_students: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/student/<documento>', methods=['DELETE'])
def delete_student(documento):
    """Eliminar estudiante por documento"""
    try:
        deleted = db.delete_estudiante(documento)
        
        if deleted:
            # Emitir evento WebSocket para actualizar dashboards
            socketio.emit('student_deleted', {
                'documento': documento,
                'timestamp': datetime.now().isoformat()
            })
            
            return jsonify({
                'success': True,
                'message': f'Estudiante {documento} eliminado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Estudiante no encontrado'
            }), 404
    
    except Exception as e:
        logger.error(f"Error eliminando estudiante {documento}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/student/<documento>')
def get_student_detail(documento):
    """Obtener detalles de un estudiante específico"""
    try:
        estudiante = db.get_estudiante(documento)
        if not estudiante:
            return jsonify({'error': 'Estudiante no encontrado'}), 404
        
        retos = db.get_retos_estudiante(documento)
        
        return jsonify({
            'estudiante': dict(estudiante),
            'retos_completados': [dict(r) for r in retos]
        })
    
    except Exception as e:
        logger.error(f"Error en get_student_detail: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/leaderboard')
def get_leaderboard():
    """Obtener tabla de posiciones"""
    try:
        leaderboard = db.get_leaderboard(limit=50)
        
        result = []
        for entry in leaderboard:
            result.append({
                'ranking': int(entry['ranking']),
                'documento': entry['documento'],
                'nombre': entry['nombre'],
                'total_puntos': int(entry['total_puntos']) if entry['total_puntos'] else 0,
                'total_retos_completados': int(entry['total_retos_completados']) if entry['total_retos_completados'] else 0,
                'porcentaje_completado': float(entry['porcentaje_completado']) if entry['porcentaje_completado'] else 0.0,
                'status': entry['status'],
                'last_seen': entry['last_seen'].isoformat() if entry['last_seen'] else None
            })
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error en get_leaderboard: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics')
def get_statistics():
    """Obtener estadísticas globales"""
    try:
        stats = db.get_estadisticas_globales()
        
        return jsonify({
            'total_estudiantes': int(stats['total_estudiantes']) if stats['total_estudiantes'] else 0,
            'estudiantes_online': int(stats['estudiantes_online']) if stats['estudiantes_online'] else 0,
            'total_completados': int(stats['total_completados']) if stats['total_completados'] else 0,
            'promedio_retos': float(stats['promedio_retos']) if stats['promedio_retos'] else 0.0,
            'promedio_puntos': float(stats['promedio_puntos']) if stats['promedio_puntos'] else 0.0,
            'max_puntos': int(stats['max_puntos']) if stats['max_puntos'] else 0,
            'total_retos_disponibles': int(stats['total_retos_disponibles']) if stats['total_retos_disponibles'] else 15
        })
    
    except Exception as e:
        logger.error(f"Error en get_statistics: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/retos/progreso')
def get_retos_progreso():
    """Obtener progreso por cada reto"""
    try:
        progreso = db.get_progreso_retos()
        
        result = []
        for reto in progreso:
            result.append({
                'reto_id': reto['reto_id'],
                'nombre': reto['nombre'],
                'categoria': reto['categoria'],
                'dificultad': reto['dificultad'],
                'puntos': reto['puntos'],
                'veces_completado': int(reto['veces_completado']) if reto['veces_completado'] else 0,
                'estudiantes_unicos': int(reto['estudiantes_unicos']) if reto['estudiantes_unicos'] else 0,
                'tiempo_promedio_minutos': float(reto['tiempo_promedio_minutos']) if reto['tiempo_promedio_minutos'] else 0.0
            })
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error en get_retos_progreso: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/eventos/recientes')
def get_recent_events():
    """Obtener eventos recientes"""
    try:
        limit = request.args.get('limit', 50, type=int)
        eventos = db.get_eventos_recientes(limit=limit)
        
        result = []
        for evento in eventos:
            result.append({
                'documento': evento['documento'],
                'nombre': evento['nombre'],
                'event_type': evento['event_type'],
                'payload': evento['payload'],
                'received_at': evento['received_at'].isoformat() if evento['received_at'] else None,
                'segundos_atras': float(evento['segundos_atras']) if evento['segundos_atras'] else 0
            })
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error en get_recent_events: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/actividad/horaria')
def get_hourly_activity():
    """Obtener actividad por hora"""
    try:
        horas = request.args.get('horas', 24, type=int)
        actividad = db.get_actividad_por_hora(horas=horas)
        
        result = []
        for hora in actividad:
            result.append({
                'hora': hora['hora'].isoformat() if hora['hora'] else None,
                'total_eventos': int(hora['total_eventos']) if hora['total_eventos'] else 0,
                'estudiantes_unicos': int(hora['estudiantes_unicos']) if hora['estudiantes_unicos'] else 0,
                'flags_enviadas': int(hora['flags_enviadas']) if hora['flags_enviadas'] else 0
            })
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error en get_hourly_activity: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# WEBSOCKET EVENTS
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Cliente WebSocket conectado"""
    logger.info(f"🔌 Cliente WebSocket conectado: {request.sid}")
    emit('connected', {'message': 'Conectado al servidor de monitoreo'})


@socketio.on('disconnect')
def handle_disconnect():
    """Cliente WebSocket desconectado"""
    logger.info(f"🔌 Cliente WebSocket desconectado: {request.sid}")


# ============================================================================
# INICIALIZACIÓN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 MQTT Monitoring Dashboard - Docker CTF Lab")
    print("=" * 60)
    print(f"\n📡 MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"🌐 Web Server: http://{HOST}:{PORT}")
    print("=" * 60)
    
    # Inicializar base de datos
    try:
        db = get_db()
        logger.info("✅ Base de datos inicializada")
    except Exception as e:
        logger.error(f"❌ Error inicializando base de datos: {e}")
        logger.info("⚠️  Continuando sin base de datos...")
    
    # Conectar a MQTT
    try:
        logger.info("🚀 Cliente MQTT iniciado")
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
    except Exception as e:
        logger.error(f"❌ Error conectando a MQTT: {e}")
    
    # Ejecutar servidor Flask con SocketIO
    socketio.run(app, host=HOST, port=PORT, debug=os.getenv('FLASK_ENV') == 'development')
