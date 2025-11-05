#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker CTF Lab - Web Dashboard
Servidor Flask para interfaz web del laboratorio
"""

import subprocess
import json
import re
from flask import Flask, render_template, request, jsonify
from docker_challenge import DockerChallenge

app = Flask(__name__)
challenge = DockerChallenge()

# Mapeo de IDs de retos a textos base para generación de flags UUID
# Debe coincidir exactamente con el usado en docker_challenge.py
FLAG_BASES = {
    1: "primer_contenedor",
    2: "imagen_descargada",
    3: "contenedor_background",
    4: "puerto_mapeado",
    5: "volumen_creado",
    6: "red_creada",
    7: "contenedores_conectados",
    8: "ssh_configurado",
    9: "telnet_activo",
    10: "scada_desplegado",
    11: "vnc_funcionando",
    12: "dockerfile_creado",
    13: "compose_desplegado",
    14: "inspeccion_exitosa",
    15: "limpieza_completa"
}


@app.route('/')
def index():
    """Página principal del dashboard"""
    return render_template('index.html')


@app.route('/test')
def test():
    """Página de prueba para debugging"""
    return render_template('test_challenges.html')


@app.route('/api/debug')
def debug_info():
    """Endpoint de diagnóstico"""
    return jsonify({
        "status": "OK",
        "documento_estudiante": challenge.documento_estudiante,
        "total_retos": len(challenge.retos),
        "retos_ids": [r["id"] for r in challenge.retos],
        "completados": challenge.progress.get("completados", []),
        "puntos": challenge.progress.get("puntos", 0)
    })


@app.route('/api/progress')
def get_progress():
    """
    Endpoint para obtener el progreso del usuario
    
    Returns:
        JSON con progreso completo
    """
    return jsonify({
        "documento": challenge.documento_estudiante,
        "completados": challenge.progress.get("completados", []),
        "puntos": challenge.progress.get("puntos", 0),
        "total_retos": len(challenge.retos),
        "total_puntos": sum(r["puntos"] for r in challenge.retos),
        "fecha_inicio": challenge.progress.get("fecha_inicio", "")
    })


@app.route('/api/challenges')
def get_challenges():
    """
    Endpoint para obtener todos los retos
    
    Returns:
        JSON con lista de retos (incluye flag si está completado)
    """
    challenges_data = []
    
    for reto in challenge.retos:
        completado = reto["id"] in challenge.progress.get("completados", [])
        
        challenge_data = {
            "id": reto["id"],
            "nombre": reto["nombre"],
            "descripcion": reto["descripcion"],
            "pista": reto["pista"],
            "puntos": reto["puntos"],
            "dificultad": reto["dificultad"],
            "categoria": reto["categoria"],
            "completado": completado,
            "fecha_completado": challenge.progress.get(f"reto_{reto['id']}_fecha", "") if completado else None,
            "preguntas": reto.get("preguntas", [])
        }
        
        # Si el reto NO está completado, mostrar la flag para que pueda copiarla
        if not completado:
            flag_personalizada = challenge.generar_flag_personalizada(reto["id"], FLAG_BASES[reto["id"]])
            challenge_data["flag"] = flag_personalizada
        
        challenges_data.append(challenge_data)
    
    return jsonify(challenges_data)


@app.route('/api/verify-flag', methods=['POST'])
def verify_flag():
    """
    Endpoint para verificar una flag y los requisitos Docker antes de enviar.
    Ejecuta 'python3 docker_challenge.py start' en el backend para obtener las flags oficiales.
    
    Body JSON:
        {
            "flag": "FLAG{...}"
        }
    
    Returns:
        JSON con resultado de la verificación
    """
    data = request.get_json()
    
    if not data or 'flag' not in data:
        return jsonify({
            "success": False,
            "message": "❌ Debes proporcionar una flag"
        }), 400
    
    flag = data['flag'].strip()
    
    try:
        # PASO 1: Ejecutar 'python3 docker_challenge.py start' para obtener las flags oficiales
        result = subprocess.run(
            ['python3', 'docker_challenge.py', 'start'],
            capture_output=True,
            text=True,
            timeout=15,
            cwd='/workspaces/ctf_docker_lab'
        )
        
        if result.returncode != 0:
            return jsonify({
                "success": False,
                "message": "❌ Error al verificar el sistema. Asegúrate de haber ejecutado 'python3 docker_challenge.py setup' primero."
            })
        
        # PASO 2: Parsear la salida para encontrar el reto que corresponde a esta flag
        output = result.stdout
        reto_id = None
        
        # Buscar líneas con formato: "🚩 Flag a enviar: uuid"
        # y luego buscar hacia arriba para encontrar "Reto X:"
        lines = output.split('\n')
        for i, line in enumerate(lines):
            if flag in line and "Flag a enviar" in line:
                # Buscar hacia arriba para encontrar "Reto X:"
                for j in range(i-1, max(0, i-10), -1):
                    match = re.search(r'Reto\s+(\d+):', lines[j])
                    if match:
                        reto_id = int(match.group(1))
                        break
                if reto_id:
                    break
        
        if not reto_id:
            return jsonify({
                "success": False,
                "message": "❌ Flag incorrecta o no válida"
            })
        
        # PASO 3: Obtener información del reto
        reto = next((r for r in challenge.retos if r["id"] == reto_id), None)
        if not reto:
            return jsonify({
                "success": False,
                "message": "❌ Reto no encontrado"
            })
        
        # PASO 4: Verificar si ya fue completado
        if reto_id in challenge.progress.get("completados", []):
            return jsonify({
                "success": False,
                "message": f"⚠️  Ya completaste este reto: {reto['nombre']}"
            })
        
        # PASO 5: Verificar requisitos Docker del reto (ejecuta verificación real de Docker)
        verificacion_exitosa = challenge._verificar_reto_especifico(reto_id)
        
        if verificacion_exitosa:
            return jsonify({
                "success": True,
                "message": f"✅ Verificación Docker exitosa para: {reto['nombre']}\n\n🎯 El comando fue ejecutado correctamente. Procediendo a enviar la flag...",
                "reto_id": reto_id,
                "reto_nombre": reto['nombre']
            })
        else:
            return jsonify({
                "success": False,
                "message": f"⚠️  Flag correcta, pero no se detectó la ejecución del comando Docker.\n\n💡 Reto: {reto['nombre']}\n\n📝 Pista: {reto.get('pista', 'Revisa la descripción del reto')}\n\nAsegúrate de ejecutar el comando requerido antes de enviar la flag.",
                "reto_id": reto_id,
                "reto_nombre": reto['nombre'],
                "pista": reto.get('pista', '')
            })
            
    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "message": "❌ Timeout al verificar el sistema. Intenta nuevamente."
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"❌ Error en la verificación: {str(e)}"
        })


@app.route('/api/submit', methods=['POST'])
def submit_flag():
    """
    Endpoint para enviar una flag
    
    Body JSON:
        {
            "flag": "FLAG{...}"
        }
    
    Returns:
        JSON con resultado de la validación
    """
    data = request.get_json()
    
    if not data or 'flag' not in data:
        return jsonify({
            "success": False,
            "message": "❌ Debes proporcionar una flag"
        }), 400
    
    flag = data['flag']
    exito, mensaje, reto_id = challenge.submit_flag(flag)
    
    response = {
        "success": exito,
        "message": mensaje,
        "reto_id": reto_id if exito else None,
        "puntos_totales": challenge.progress.get("puntos", 0),
        "completados": len(challenge.progress.get("completados", [])),
        "total_retos": len(challenge.retos)
    }
    
    # Verificar si completó todos los retos
    if exito and len(challenge.progress["completados"]) == len(challenge.retos):
        response["all_completed"] = True
        response["message"] += "\n\n🏆 ¡FELICIDADES! Has completado TODOS los retos del Docker CTF Lab 🐳"
    
    return jsonify(response)


@app.route('/api/hint/<int:reto_id>')
def get_hint(reto_id):
    """
    Endpoint para obtener la pista de un reto
    
    Args:
        reto_id: ID del reto
    
    Returns:
        JSON con la pista
    """
    reto = next((r for r in challenge.retos if r["id"] == reto_id), None)
    
    if not reto:
        return jsonify({
            "success": False,
            "message": "Reto no encontrado"
        }), 404
    
    return jsonify({
        "success": True,
        "reto_id": reto_id,
        "nombre": reto["nombre"],
        "pista": reto["pista"]
    })


@app.route('/api/flags')
def get_flags():
    """
    Endpoint para obtener las flags de los retos completados
    Simula el comando: python3 docker_challenge.py start
    
    Returns:
        JSON con las flags generadas para el estudiante
    """
    flags_data = []
    completados = challenge.progress.get("completados", [])
    
    for reto in challenge.retos:
        if reto["id"] in completados:
            # Generar flag personalizada usando el texto base correcto
            flag_personalizada = challenge.generar_flag_personalizada(reto["id"], FLAG_BASES[reto["id"]])
            flags_data.append({
                "id": reto["id"],
                "nombre": reto["nombre"],
                "flag": flag_personalizada,
                "puntos": reto["puntos"]
            })
    
    return jsonify({
        "success": True,
        "documento": challenge.documento_estudiante,
        "total_completados": len(completados),
        "flags": flags_data,
        "puntos_totales": challenge.progress.get("puntos", 0)
    })


@app.route('/api/writeup')
def get_writeup():
    """
    Endpoint para obtener el contenido del taller/write-up en formato Markdown
    
    Returns:
        JSON con el contenido del archivo TALLER.md
    """
    try:
        import os
        writeup_path = os.path.join(os.path.dirname(__file__), 'TALLER.md')
        
        with open(writeup_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            "success": True,
            "content": content,
            "title": "🐳 Taller Docker CTF Lab - Write-ups y Soluciones"
        })
    except FileNotFoundError:
        return jsonify({
            "success": False,
            "message": "❌ Archivo de write-up no encontrado"
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"❌ Error al cargar write-up: {str(e)}"
        }), 500


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🐳 DOCKER CTF LAB - Dashboard Web".center(70))
    print("=" * 70)
    print("\n🌐 Iniciando servidor en http://localhost:5000")
    print("📊 Dashboard disponible para tracking de retos")
    print("\n💡 Presiona CTRL+C para detener el servidor\n")
    print("=" * 70 + "\n")
    
    # Ejecutar servidor
    app.run(host='0.0.0.0', port=5000, debug=False)
