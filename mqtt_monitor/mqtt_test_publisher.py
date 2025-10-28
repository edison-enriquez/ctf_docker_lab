"""
MQTT Test Publisher - Simula estudiantes enviando eventos

Este script genera datos de prueba para el sistema de monitoreo MQTT.
Simula múltiples estudiantes completando retos y enviando heartbeats.

Uso:
    python mqtt_test_publisher.py

Configuración:
    - Edita la lista STUDENTS para agregar más estudiantes
    - Modifica BROKER y PORT si usas un broker diferente
    - Ajusta HEARTBEAT_INTERVAL para cambiar frecuencia
"""

import paho.mqtt.client as mqtt
import json
import time
import random
import uuid
from datetime import datetime

# Configuración
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_BASE = "docker_ctf_lab"
HEARTBEAT_INTERVAL = 10  # segundos

# Estudiantes simulados
STUDENTS = [
    {"documento": "1111111111", "nombre": "Ana García"},
    {"documento": "2222222222", "nombre": "Carlos López"},
    {"documento": "3333333333", "nombre": "María Rodríguez"},
    {"documento": "4444444444", "nombre": "Juan Pérez"},
    {"documento": "5555555555", "nombre": "Laura Martínez"},
]

# Retos disponibles (IDs del 1 al 15)
RETOS = [
    {"id": 1, "nombre": "Primer contenedor", "puntos": 10},
    {"id": 2, "nombre": "Contenedor con nombre", "puntos": 15},
    {"id": 3, "nombre": "Contenedor interactivo", "puntos": 20},
    {"id": 4, "nombre": "Red Docker", "puntos": 25},
    {"id": 5, "nombre": "Conexión SSH", "puntos": 30},
    {"id": 6, "nombre": "Conexión Telnet", "puntos": 30},
    {"id": 7, "nombre": "SCADA System", "puntos": 40},
    {"id": 8, "nombre": "VNC Desktop", "puntos": 35},
    {"id": 9, "nombre": "Docker Compose", "puntos": 40},
    {"id": 10, "nombre": "Volúmenes persistentes", "puntos": 25},
]

# Estado de cada estudiante (retos completados)
student_progress = {student["documento"]: [] for student in STUDENTS}


def on_connect(client, userdata, flags, rc):
    """Callback cuando se conecta al broker"""
    if rc == 0:
        print(f"✅ Conectado al broker {BROKER}:{PORT}")
    else:
        print(f"❌ Error de conexión: {rc}")


def send_heartbeat(client, documento):
    """Envía un heartbeat de un estudiante"""
    completados = student_progress[documento]
    puntos = sum(reto["puntos"] for reto in RETOS if reto["id"] in completados)
    
    payload = {
        "timestamp": datetime.now().isoformat(),
        "documento": documento,
        "status": "online",
        "completados": len(completados),
        "puntos": puntos
    }
    
    topic = f"{TOPIC_BASE}/{documento}/heartbeat"
    client.publish(topic, json.dumps(payload))
    print(f"💓 Heartbeat: {documento} ({len(completados)} retos, {puntos} pts)")


def send_flag_submit(client, documento, reto):
    """Simula que un estudiante completó un reto"""
    if reto["id"] in student_progress[documento]:
        return  # Ya completado
    
    student_progress[documento].append(reto["id"])
    completados = student_progress[documento]
    puntos = sum(r["puntos"] for r in RETOS if r["id"] in completados)
    
    payload = {
        "timestamp": datetime.now().isoformat(),
        "documento": documento,
        "reto_id": reto["id"],
        "reto_nombre": reto["nombre"],
        "flag": f"{uuid.uuid4()}",  # UUID directo sin FLAG{}
        "puntos_ganados": reto["puntos"],
        "puntos_totales": puntos,
        "completados": len(completados),
        "es_correcto": True
    }
    
    topic = f"{TOPIC_BASE}/{documento}/flag_submit"
    client.publish(topic, json.dumps(payload))
    print(f"🎯 Flag submitted: {documento} completó '{reto['nombre']}' (+{reto['puntos']} pts)")


def send_progress_report(client, documento):
    """Envía un reporte completo de progreso"""
    completados = student_progress[documento]
    puntos = sum(reto["puntos"] for reto in RETOS if reto["id"] in completados)
    total_puntos = sum(reto["puntos"] for reto in RETOS)
    
    payload = {
        "timestamp": datetime.now().isoformat(),
        "documento": documento,
        "completados": len(completados),
        "puntos": puntos,
        "total_retos": len(RETOS),
        "total_puntos": total_puntos,
        "progreso_porcentaje": round(len(completados) / len(RETOS) * 100, 1),
        "retos_completados": completados
    }
    
    if completados:
        ultimo_id = completados[-1]
        ultimo_reto = next(r for r in RETOS if r["id"] == ultimo_id)
        payload["ultimo_reto_completado"] = {
            "id": ultimo_id,
            "nombre": ultimo_reto["nombre"],
            "puntos": ultimo_reto["puntos"],
            "timestamp": datetime.now().isoformat()
        }
    
    topic = f"{TOPIC_BASE}/{documento}/progress"
    client.publish(topic, json.dumps(payload))
    print(f"📊 Progress report: {documento}")


def simulate_activity(client):
    """Simula actividad aleatoria de estudiantes"""
    print("\n🎮 Iniciando simulación de actividad...\n")
    
    iteration = 0
    while True:
        iteration += 1
        print(f"\n{'='*60}")
        print(f"Iteración {iteration}")
        print(f"{'='*60}\n")
        
        # Cada estudiante envía heartbeat
        for student in STUDENTS:
            send_heartbeat(client, student["documento"])
            time.sleep(0.5)
        
        # Aleatoriamente, algunos estudiantes completan retos
        for student in STUDENTS:
            documento = student["documento"]
            
            # 30% de probabilidad de completar un reto
            if random.random() < 0.3:
                # Buscar retos no completados
                pendientes = [r for r in RETOS if r["id"] not in student_progress[documento]]
                
                if pendientes:
                    # Completar el siguiente reto en orden
                    reto = pendientes[0]
                    send_flag_submit(client, documento, reto)
                    time.sleep(0.5)
                    send_progress_report(client, documento)
                    time.sleep(0.5)
        
        # Esperar antes de la siguiente iteración
        print(f"\n⏳ Esperando {HEARTBEAT_INTERVAL} segundos...\n")
        time.sleep(HEARTBEAT_INTERVAL)


def main():
    """Función principal"""
    print("="*60)
    print("🚀 MQTT Test Publisher - Docker CTF Lab")
    print("="*60)
    print(f"\n📡 Conectando a {BROKER}:{PORT}...")
    print(f"📝 Simulando {len(STUDENTS)} estudiantes")
    print(f"🎯 {len(RETOS)} retos disponibles")
    print(f"⏰ Heartbeat cada {HEARTBEAT_INTERVAL} segundos\n")
    
    # Crear cliente MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    
    try:
        client.connect(BROKER, PORT, 60)
        client.loop_start()
        
        # Esperar conexión
        time.sleep(2)
        
        # Iniciar simulación
        simulate_activity(client)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo simulación...")
        client.loop_stop()
        client.disconnect()
        print("✅ Desconectado. ¡Hasta pronto!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
