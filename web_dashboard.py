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
        JSON con lista de retos
    """
    challenges_data = []
    
    for reto in challenge.retos:
        completado = reto["id"] in challenge.progress.get("completados", [])
        
        # Generar la flag personalizada
        flag_base = reto["flag"].split("{")[1].split("}")[0]
        flag_personalizada = challenge.generar_flag_personalizada(reto["id"], flag_base)
        
        challenges_data.append({
            "id": reto["id"],
            "nombre": reto["nombre"],
            "descripcion": reto["descripcion"],
            "pista": reto["pista"],
            "puntos": reto["puntos"],
            "dificultad": reto["dificultad"],
            "categoria": reto["categoria"],
            "completado": completado,
            "flag": flag_personalizada if not completado else None,
            "fecha_completado": challenge.progress.get(f"reto_{reto['id']}_fecha", "") if completado else None
        })
    
    return jsonify(challenges_data)


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
