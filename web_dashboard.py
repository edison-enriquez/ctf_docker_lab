#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker CTF Lab - Web Dashboard
Servidor Flask para interfaz web del laboratorio
"""

from flask import Flask, render_template, request, jsonify
from docker_challenge import DockerChallenge

app = Flask(__name__)
challenge = DockerChallenge()


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
            flag_personalizada = challenge.generar_flag_personalizada(reto["id"], reto["flag"])
            challenge_data["flag"] = flag_personalizada
        
        challenges_data.append(challenge_data)
    
    return jsonify(challenges_data)


@app.route('/api/verify-flag', methods=['POST'])
def verify_flag():
    """
    Endpoint para verificar una flag y los requisitos Docker antes de enviar
    
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
    
    # Mapeo de retos a sus textos base de flags
    flag_bases = {
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
    
    # Buscar el reto que corresponde a esta flag
    reto_id = None
    reto = None
    for r in challenge.retos:
        flag_esperada = challenge.generar_flag_personalizada(r["id"], flag_bases[r["id"]])
        if flag_esperada == flag:
            reto_id = r["id"]
            reto = r
            break
    
    if not reto_id:
        return jsonify({
            "success": False,
            "message": "❌ Flag incorrecta o no válida"
        })
    
    # Verificar si ya fue completado
    if reto_id in challenge.progress.get("completados", []):
        return jsonify({
            "success": False,
            "message": f"⚠️  Ya completaste este reto: {reto['nombre']}"
        })
    
    # Verificar requisitos Docker del reto
    verificacion_exitosa = challenge._verificar_reto_especifico(reto_id)
    
    if verificacion_exitosa:
        return jsonify({
            "success": True,
            "message": f"✅ Verificación Docker exitosa para: {reto['nombre']}",
            "reto_id": reto_id,
            "reto_nombre": reto['nombre']
        })
    else:
        return jsonify({
            "success": False,
            "message": f"⚠️  Flag correcta, pero no se detectó la ejecución del comando Docker. Asegúrate de ejecutar el comando requerido para: {reto['nombre']}",
            "reto_id": reto_id,
            "reto_nombre": reto['nombre']
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
            # Generar flag personalizada
            flag_personalizada = challenge.generar_flag_personalizada(reto["id"], reto["flag"])
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
