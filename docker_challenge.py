#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker CTF Lab - Sistema de Retos Capture The Flag
Sistema principal de gestión de retos para aprendizaje de Docker
"""

import os
import sys
import json
import hashlib
import docker
import subprocess
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# MQTT (opcional - se instala si está disponible)
try:
    import paho.mqtt.client as mqtt
    MQTT_AVAILABLE = True
except ImportError:
    MQTT_AVAILABLE = False
    mqtt = None


class DockerChallengeError(Exception):
    """Excepción personalizada para errores del laboratorio"""
    pass


class DockerChallenge:
    """
    Clase principal que gestiona el sistema de retos de Docker.
    Maneja la configuración, verificación de retos y progreso del usuario.
    """

    def __init__(self):
        """Inicializa la configuración del sistema de retos"""
        self.home_dir = Path.home()
        self.progress_file = self.home_dir / ".docker_ctf_progress.json"
        self.config_file = self.home_dir / ".docker_ctf_configured"
        
        # Cargar progreso existente
        self.progress = self._cargar_progreso()
        self.documento_estudiante = self.progress.get("documento_estudiante", "")
        
        # Inicializar cliente Docker
        try:
            self.docker_client = docker.from_env()
        except Exception as e:
            print(f"⚠️  Advertencia: No se pudo conectar a Docker: {e}")
            self.docker_client = None
        
        # Configuración MQTT (configurable)
        self.mqtt_config = {
            "enabled": os.getenv("MQTT_ENABLED", "false").lower() == "true",
            "broker": os.getenv("MQTT_BROKER", "broker.hivemq.com"),
            "port": int(os.getenv("MQTT_PORT", "1883")),
            "topic_base": os.getenv("MQTT_TOPIC", "docker_ctf_lab"),
            "username": os.getenv("MQTT_USERNAME", ""),
            "password": os.getenv("MQTT_PASSWORD", "")
        }
        
        # Cliente MQTT
        self.mqtt_client = None
        if MQTT_AVAILABLE and self.mqtt_config["enabled"]:
            self._init_mqtt()
        
        # Definir retos
        self.retos = [
            {
                "id": 1,
                "nombre": "🐳 Primer Contenedor",
                "descripcion": "Ejecuta tu primer contenedor usando la imagen 'hello-world'",
                "pista": "Usa 'docker run hello-world'. El sistema verificará que el contenedor se haya ejecutado.",
                "flag": "FLAG{primer_contenedor}",
                "puntos": 10,
                "dificultad": "Principiante",
                "categoria": "Comandos Básicos"
            },
            {
                "id": 2,
                "nombre": "🔍 Inspector de Imágenes",
                "descripcion": "Descarga la imagen 'nginx:alpine' y encuentra su tamaño",
                "pista": "Usa 'docker pull nginx:alpine' y luego 'docker images' para ver el tamaño.",
                "flag": "FLAG{imagen_descargada}",
                "puntos": 10,
                "dificultad": "Principiante",
                "categoria": "Imágenes"
            },
            {
                "id": 3,
                "nombre": "🚀 Contenedor en Background",
                "descripcion": "Ejecuta un contenedor nginx en modo detached (background) con nombre 'webserver'",
                "pista": "Usa 'docker run -d --name webserver nginx:alpine'. Verifica con 'docker ps'.",
                "flag": "FLAG{contenedor_background}",
                "puntos": 15,
                "dificultad": "Principiante",
                "categoria": "Ejecución"
            },
            {
                "id": 4,
                "nombre": "🔌 Mapeo de Puertos",
                "descripcion": "Ejecuta un contenedor nginx mapeando el puerto 8080 del host al puerto 80 del contenedor con nombre 'webserver-port'",
                "pista": "Usa 'docker run -d -p 8080:80 --name webserver-port nginx:alpine'",
                "flag": "FLAG{puerto_mapeado}",
                "puntos": 15,
                "dificultad": "Intermedio",
                "categoria": "Redes"
            },
            {
                "id": 5,
                "nombre": "💾 Volúmenes Persistentes",
                "descripcion": "Crea un volumen llamado 'datos_importantes' y úsalo en un contenedor",
                "pista": "Usa 'docker volume create datos_importantes' y luego móntalo con -v en un contenedor",
                "flag": "FLAG{volumen_creado}",
                "puntos": 20,
                "dificultad": "Intermedio",
                "categoria": "Volúmenes"
            },
            {
                "id": 6,
                "nombre": "🌐 Red Personalizada",
                "descripcion": "Crea una red bridge personalizada llamada 'mi_red_ctf'",
                "pista": "Usa 'docker network create --driver bridge mi_red_ctf'",
                "flag": "FLAG{red_creada}",
                "puntos": 20,
                "dificultad": "Intermedio",
                "categoria": "Redes"
            },
            {
                "id": 7,
                "nombre": "🔗 Conectando Contenedores",
                "descripcion": "Crea dos contenedores (alpine) en la red 'mi_red_ctf' con nombres 'contenedor1' y 'contenedor2' que puedan comunicarse",
                "pista": "Usa --network mi_red_ctf al crear los contenedores. Prueba la conexión con ping.",
                "flag": "FLAG{contenedores_conectados}",
                "puntos": 25,
                "dificultad": "Avanzado",
                "categoria": "Redes"
            },
            {
                "id": 8,
                "nombre": "🔐 SSH en Contenedor",
                "descripcion": "Despliega un contenedor con SSH habilitado (usa una imagen apropiada y configura el puerto 2222)",
                "pista": "Puedes usar imágenes como 'linuxserver/openssh-server' o crear tu propio Dockerfile",
                "flag": "FLAG{ssh_configurado}",
                "puntos": 30,
                "dificultad": "Avanzado",
                "categoria": "Servicios"
            },
            {
                "id": 9,
                "nombre": "📡 Telnet Antiguo",
                "descripcion": "Despliega un contenedor con servicio Telnet en el puerto 2323",
                "pista": "Busca imágenes con telnet o crea un Dockerfile basado en ubuntu/alpine con telnetd instalado",
                "flag": "FLAG{telnet_activo}",
                "puntos": 30,
                "dificultad": "Avanzado",
                "categoria": "Servicios"
            },
            {
                "id": 10,
                "nombre": "🏭 SCADA Industrial",
                "descripcion": "Despliega un contenedor con OpenPLC o similar sistema SCADA en el puerto 8000",
                "pista": "Usa 'docker run -d -p 8000:8080 --name scada-server openplc/openplc:latest' o similar",
                "flag": "FLAG{scada_desplegado}",
                "puntos": 35,
                "dificultad": "Experto",
                "categoria": "Aplicaciones"
            },
            {
                "id": 11,
                "nombre": "🖥️ Escritorio Remoto VNC",
                "descripcion": "Despliega un contenedor con escritorio gráfico accesible por VNC en puerto 5900",
                "pista": "Usa imágenes como 'dorowu/ubuntu-desktop-lxde-vnc' en puerto 5900 o 6080 para web",
                "flag": "FLAG{vnc_funcionando}",
                "puntos": 35,
                "dificultad": "Experto",
                "categoria": "Aplicaciones"
            },
            {
                "id": 12,
                "nombre": "🏗️ Dockerfile Personalizado",
                "descripcion": "Crea un Dockerfile que instale python3 y flask, construye la imagen como 'mi-app:v1'",
                "pista": "FROM python:3.11-slim, RUN pip install flask, luego 'docker build -t mi-app:v1 .'",
                "flag": "FLAG{dockerfile_creado}",
                "puntos": 30,
                "dificultad": "Avanzado",
                "categoria": "Construcción"
            },
            {
                "id": 13,
                "nombre": "📦 Docker Compose Multi-Servicio",
                "descripcion": "Crea un docker-compose.yml con al menos 2 servicios (nginx y redis) y levántalos",
                "pista": "Define services con nginx y redis, luego ejecuta 'docker-compose up -d'",
                "flag": "FLAG{compose_desplegado}",
                "puntos": 40,
                "dificultad": "Experto",
                "categoria": "Orquestación"
            },
            {
                "id": 14,
                "nombre": "🔍 Inspección Avanzada",
                "descripcion": "Inspecciona un contenedor y encuentra su dirección IP interna",
                "pista": "Usa 'docker inspect <contenedor>' y busca el campo NetworkSettings.IPAddress",
                "flag": "FLAG{inspeccion_exitosa}",
                "puntos": 25,
                "dificultad": "Intermedio",
                "categoria": "Diagnóstico"
            },
            {
                "id": 15,
                "nombre": "🧹 Limpieza Maestra",
                "descripcion": "Limpia todos los contenedores detenidos, imágenes sin usar y volúmenes no utilizados",
                "pista": "Usa 'docker system prune -a --volumes' con cuidado",
                "flag": "FLAG{limpieza_completa}",
                "puntos": 20,
                "dificultad": "Intermedio",
                "categoria": "Mantenimiento"
            }
        ]

    def _cargar_progreso(self) -> Dict:
        """Carga el progreso sin inicializar self.progress (usado en __init__)"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "completados": [],
            "puntos": 0,
            "documento_estudiante": "",
            "fecha_inicio": datetime.now().isoformat()
        }

    def solicitar_documento_estudiante(self) -> str:
        """
        Solicita el documento de identidad al usuario.
        
        Returns:
            Documento de estudiante ingresado
        """
        print("\n" + "=" * 70)
        print("🎓 CONFIGURACIÓN PERSONALIZADA".center(70))
        print("=" * 70)
        print("\n📝 Para personalizar tus retos, necesitamos tu documento de identidad.")
        print("   Este documento se usará para generar FLAGS únicas para ti.")
        print("   Puede ser: Cédula, Pasaporte, Código Estudiantil, etc.\n")
        print("   ⚠️  IMPORTANTE: Usa tu documento real, lo necesitarás para validar las flags.\n")
        
        while True:
            documento = input("👤 Ingresa tu documento de identidad: ").strip()
            
            if len(documento) < 4:
                print("❌ El documento debe tener al menos 4 caracteres. Intenta de nuevo.\n")
                continue
            
            print(f"\n✅ Documento registrado: {documento}")
            confirmacion = input("¿Es correcto? (s/n): ").strip().lower()
            
            if confirmacion in ['s', 'si', 'yes', 'y']:
                return documento
            else:
                print("\n🔄 Intenta de nuevo...\n")

    def generar_flag_personalizada(self, reto_id: int, texto_base: str) -> str:
        """
        Genera una flag personalizada en formato UUID basada en el documento del estudiante.
        
        Args:
            reto_id: ID del reto
            texto_base: Texto base de la flag (ej: "primer_contenedor")
            
        Returns:
            UUID directo (sin prefijo FLAG{}): xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        """
        if not self.documento_estudiante:
            # UUID aleatorio si no hay documento
            return str(uuid.uuid4())
        
        # Generar UUID determinístico basado en documento + reto
        # Usamos namespace UUID5 con SHA1
        namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')  # Namespace estándar
        datos = f"{self.documento_estudiante}_{reto_id}_{texto_base}"
        flag_uuid = uuid.uuid5(namespace, datos)
        
        return str(flag_uuid)

    def setup_environment(self) -> bool:
        """
        Configura el entorno del laboratorio.
        """
        try:
            print("🚀 Configurando el entorno de Docker CTF Lab...")
            print("=" * 60)
            
            # Solicitar documento si no existe
            if not self.documento_estudiante:
                self.documento_estudiante = self.solicitar_documento_estudiante()
                self.progress["documento_estudiante"] = self.documento_estudiante
                self.save_progress()
                print(f"\n✅ Tu documento '{self.documento_estudiante}' ha sido guardado.")
                print("   Tus FLAGS serán únicas y personalizadas.\n")
            else:
                print(f"\n👤 Documento registrado: {self.documento_estudiante}")
                print("   Tus FLAGS están personalizadas para tu documento.\n")
            
            # Verificar Docker
            if not self.docker_client:
                print("⚠️  Docker no está disponible. Algunas funciones no trabajarán.")
            else:
                print("✅ Docker está disponible y funcionando")
                
                # Verificar que Docker funciona
                try:
                    self.docker_client.ping()
                    print("✅ Conexión a Docker daemon exitosa")
                except Exception as e:
                    print(f"⚠️  Error al conectar con Docker: {e}")
            
            # Marcar como configurado
            self.config_file.touch()
            
            print("\n" + "=" * 60)
            print("✅ ¡Entorno configurado exitosamente!")
            print(f"👤 Documento de estudiante: {self.documento_estudiante}")
            print(f"🎯 Total de retos: {len(self.retos)}")
            print(f"🏆 Puntos totales disponibles: {sum(r['puntos'] for r in self.retos)}")
            
            print(f"\n🔒 Tus FLAGS son personalizadas y únicas para tu documento.")
            print("\n💡 Usa './start.sh' para ver el menú principal")
            print("💡 Usa 'python3 web_dashboard.py' para abrir el dashboard web")
            
            return True
            
        except Exception as e:
            print(f"❌ Error configurando el entorno: {e}")
            return False

    def save_progress(self) -> None:
        """Guarda el progreso del usuario en el archivo JSON"""
        try:
            with open(self.progress_file, 'w') as f:
                json.dump(self.progress, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error guardando progreso: {e}")

    def submit_flag(self, flag: str) -> Tuple[bool, str, int]:
        """
        Verifica y registra una flag enviada por el usuario.
        
        Args:
            flag: La flag a verificar
            
        Returns:
            Tupla (éxito, mensaje, id_reto)
        """
        flag = flag.strip()
        
        # Verificar que el estudiante esté registrado
        if not self.documento_estudiante:
            return False, "❌ Error: No hay documento registrado. Ejecuta 'setup' primero.", 0
        
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
        
        # Buscar qué reto corresponde a la flag
        for reto in self.retos:
            flag_esperada = self.generar_flag_personalizada(reto["id"], flag_bases[reto["id"]])
            
            if flag_esperada == flag:
                reto_id = reto["id"]
                
                # Verificar si ya fue completado
                if reto_id in self.progress["completados"]:
                    return False, f"❌ Este reto ya fue completado anteriormente", reto_id
                
                # Verificación adicional según el reto
                verificacion_exitosa = self._verificar_reto_especifico(reto_id)
                
                if not verificacion_exitosa:
                    return False, f"⚠️  Flag correcta, pero no cumples los requisitos del reto. Verifica tu configuración.", reto_id
                
                # Registrar completado
                self.progress["completados"].append(reto_id)
                self.progress["puntos"] += reto["puntos"]
                self.progress[f"reto_{reto_id}_fecha"] = datetime.now().isoformat()
                self.save_progress()
                
                # Publicar en MQTT
                self._publish_mqtt("flag_submit", {
                    "reto_id": reto_id,
                    "reto_nombre": reto["nombre"],
                    "puntos": reto["puntos"],
                    "total_puntos": self.progress["puntos"],
                    "completados": len(self.progress["completados"])
                })
                
                mensaje = (
                    "\n🎉 ¡CORRECTO! 🎉\n"
                    f"Reto {reto_id}: {reto['nombre']}\n"
                    f"+{reto['puntos']} puntos\n"
                    f"Total: {self.progress['puntos']} puntos\n"
                    f"Completados: {len(self.progress['completados'])}/{len(self.retos)}\n"
                )
                return True, mensaje, reto_id
        
        return False, "❌ Flag incorrecta. Verifica que hayas completado el reto correctamente.", 0

    def _verificar_reto_especifico(self, reto_id: int) -> bool:
        """
        Verifica requisitos específicos del reto usando Docker API
        
        Args:
            reto_id: ID del reto a verificar
            
        Returns:
            True si cumple los requisitos, False si no
        """
        if not self.docker_client:
            # Si Docker no está disponible, aceptar la flag (modo desarrollo)
            return True
        
        try:
            if reto_id == 1:
                # Verificar que hello-world se haya ejecutado
                containers = self.docker_client.containers.list(all=True, filters={"ancestor": "hello-world"})
                return len(containers) > 0
            
            elif reto_id == 2:
                # Verificar que nginx:alpine existe
                try:
                    self.docker_client.images.get("nginx:alpine")
                    return True
                except:
                    return False
            
            elif reto_id == 3:
                # Verificar contenedor 'webserver' en ejecución
                try:
                    container = self.docker_client.containers.get("webserver")
                    return container.status == "running"
                except:
                    return False
            
            elif reto_id == 4:
                # Verificar contenedor con puerto 8080 mapeado
                try:
                    container = self.docker_client.containers.get("webserver-port")
                    ports = container.attrs['NetworkSettings']['Ports']
                    return '80/tcp' in ports and any('8080' in str(p) for p in ports['80/tcp'] or [])
                except:
                    return False
            
            elif reto_id == 5:
                # Verificar volumen 'datos_importantes'
                volumes = self.docker_client.volumes.list(filters={"name": "datos_importantes"})
                return len(volumes) > 0
            
            elif reto_id == 6:
                # Verificar red 'mi_red_ctf'
                networks = self.docker_client.networks.list(names=["mi_red_ctf"])
                return len(networks) > 0
            
            elif reto_id == 7:
                # Verificar dos contenedores en mi_red_ctf
                try:
                    c1 = self.docker_client.containers.get("contenedor1")
                    c2 = self.docker_client.containers.get("contenedor2")
                    
                    # Verificar que ambos están en la red
                    net1 = 'mi_red_ctf' in c1.attrs['NetworkSettings']['Networks']
                    net2 = 'mi_red_ctf' in c2.attrs['NetworkSettings']['Networks']
                    
                    return net1 and net2 and c1.status == "running" and c2.status == "running"
                except:
                    return False
            
            elif reto_id == 8:
                # Verificar contenedor con SSH (puerto 2222)
                containers = self.docker_client.containers.list()
                for container in containers:
                    ports = container.attrs['NetworkSettings']['Ports']
                    if any('2222' in str(p) for port_list in (ports.values() or []) for p in (port_list or [])):
                        return True
                return False
            
            elif reto_id == 9:
                # Verificar contenedor con Telnet (puerto 2323)
                containers = self.docker_client.containers.list()
                for container in containers:
                    ports = container.attrs['NetworkSettings']['Ports']
                    if any('2323' in str(p) for port_list in (ports.values() or []) for p in (port_list or [])):
                        return True
                return False
            
            elif reto_id == 10:
                # Verificar contenedor SCADA en puerto 8000
                containers = self.docker_client.containers.list()
                for container in containers:
                    ports = container.attrs['NetworkSettings']['Ports']
                    if any('8000' in str(p) for port_list in (ports.values() or []) for p in (port_list or [])):
                        return True
                return False
            
            elif reto_id == 11:
                # Verificar contenedor VNC en puerto 5900 o 6080
                containers = self.docker_client.containers.list()
                for container in containers:
                    ports = container.attrs['NetworkSettings']['Ports']
                    if any(p in str(ports) for p in ['5900', '6080']):
                        return True
                return False
            
            elif reto_id == 12:
                # Verificar imagen mi-app:v1
                try:
                    self.docker_client.images.get("mi-app:v1")
                    return True
                except:
                    return False
            
            elif reto_id == 13:
                # Verificar docker-compose con nginx y redis
                containers = self.docker_client.containers.list()
                nginx_found = any('nginx' in c.image.tags[0] if c.image.tags else '' for c in containers)
                redis_found = any('redis' in c.image.tags[0] if c.image.tags else '' for c in containers)
                return nginx_found and redis_found
            
            elif reto_id == 14:
                # Verificar que hay al menos un contenedor para inspeccionar
                containers = self.docker_client.containers.list()
                return len(containers) > 0
            
            elif reto_id == 15:
                # Verificación simbólica de limpieza (difícil de verificar)
                return True
            
            return True
            
        except Exception as e:
            print(f"⚠️  Error en verificación: {e}")
            return False

    def mostrar_retos(self) -> None:
        """Muestra todos los retos disponibles con su estado"""
        print("\n" + "=" * 80)
        print("🎯 DOCKER CTF LAB - RETOS DISPONIBLES".center(80))
        print("=" * 80)
        print(f"\n👤 Estudiante: {self.documento_estudiante}")
        print(f"📊 Progreso: {len(self.progress['completados'])}/{len(self.retos)} retos completados")
        print(f"🏆 Puntos: {self.progress['puntos']}/{sum(r['puntos'] for r in self.retos)}")
        print("\n" + "-" * 80)
        
        for reto in self.retos:
            completado = reto["id"] in self.progress["completados"]
            estado = "✅" if completado else "❌"
            
            print(f"\n{estado} Reto {reto['id']}: {reto['nombre']}")
            print(f"   📝 {reto['descripcion']}")
            print(f"   🎯 Dificultad: {reto['dificultad']} | Puntos: {reto['puntos']} | Categoría: {reto['categoria']}")
            
            if completado:
                fecha = self.progress.get(f"reto_{reto['id']}_fecha", "")
                if fecha:
                    print(f"   🕐 Completado: {fecha[:19]}")
            else:
                flag_generada = self.generar_flag_personalizada(reto["id"], reto["flag"].split("{")[1].split("}")[0])
                print(f"   🚩 Flag a enviar: {flag_generada}")
            
            print("   " + "-" * 76)
        
        print("\n" + "=" * 80)
        print("💡 Usa 'python3 docker_challenge.py hint <numero>' para ver pistas")
        print("💡 Usa 'python3 docker_challenge.py submit <flag>' para enviar una flag")
        print("=" * 80 + "\n")

    def mostrar_hint(self, reto_id: int) -> None:
        """Muestra la pista de un reto específico"""
        reto = next((r for r in self.retos if r["id"] == reto_id), None)
        
        if not reto:
            print(f"❌ Reto {reto_id} no encontrado")
            return
        
        print(f"\n💡 PISTA - Reto {reto_id}: {reto['nombre']}")
        print("=" * 60)
        print(f"\n{reto['pista']}\n")
        print("=" * 60 + "\n")

    def mostrar_estado(self) -> None:
        """Muestra el estado actual del progreso"""
        print("\n" + "=" * 60)
        print("📊 TU PROGRESO".center(60))
        print("=" * 60)
        print(f"\n👤 Estudiante: {self.documento_estudiante}")
        print(f"📅 Fecha inicio: {self.progress.get('fecha_inicio', '')[:19]}")
        print(f"\n🎯 Retos completados: {len(self.progress['completados'])}/{len(self.retos)}")
        print(f"🏆 Puntos totales: {self.progress['puntos']}/{sum(r['puntos'] for r in self.retos)}")
        
        # Estadísticas por categoría
        categorias = {}
        for reto in self.retos:
            cat = reto['categoria']
            if cat not in categorias:
                categorias[cat] = {"total": 0, "completados": 0}
            categorias[cat]["total"] += 1
            if reto["id"] in self.progress["completados"]:
                categorias[cat]["completados"] += 1
        
        print("\n📈 Por Categoría:")
        for cat, stats in categorias.items():
            print(f"   {cat}: {stats['completados']}/{stats['total']}")
        
        if len(self.progress['completados']) == len(self.retos):
            print("\n" + "🏆" * 20)
            print("¡FELICITACIONES! Has completado TODOS los retos".center(60))
            print("🏆" * 20)
        
        print("\n" + "=" * 60 + "\n")

    def cleanup_containers(self) -> None:
        """Limpia contenedores de prueba del CTF"""
        if not self.docker_client:
            print("❌ Docker no está disponible")
            return
        
        print("\n🧹 Limpiando contenedores de prueba...")
        
        nombres_ctf = [
            "webserver", "webserver-port", "contenedor1", "contenedor2",
            "scada-server", "vnc-desktop", "ssh-server", "telnet-server"
        ]
        
        cleaned = 0
        for nombre in nombres_ctf:
            try:
                container = self.docker_client.containers.get(nombre)
                container.stop()
                container.remove()
                print(f"   ✅ Eliminado: {nombre}")
                cleaned += 1
            except:
                pass
        
        print(f"\n✅ Limpieza completada: {cleaned} contenedores eliminados\n")

    def _init_mqtt(self) -> None:
        """Inicializa el cliente MQTT"""
        try:
            self.mqtt_client = mqtt.Client(client_id=f"docker_ctf_{self.documento_estudiante or 'unknown'}")
            
            # Configurar credenciales si existen
            if self.mqtt_config["username"]:
                self.mqtt_client.username_pw_set(
                    self.mqtt_config["username"],
                    self.mqtt_config["password"]
                )
            
            # Conectar
            self.mqtt_client.connect(
                self.mqtt_config["broker"],
                self.mqtt_config["port"],
                60
            )
            
            # Iniciar loop en background
            self.mqtt_client.loop_start()
            
            print(f"✅ MQTT conectado a {self.mqtt_config['broker']}")
            
        except Exception as e:
            print(f"⚠️  Error conectando MQTT: {e}")
            self.mqtt_client = None

    def _publish_mqtt(self, event_type: str, data: dict) -> None:
        """
        Publica evento en MQTT
        
        Args:
            event_type: Tipo de evento (progress, connection, flag_submit)
            data: Datos del evento
        """
        if not self.mqtt_client or not self.mqtt_config["enabled"]:
            return
        
        try:
            topic = f"{self.mqtt_config['topic_base']}/{self.documento_estudiante}/{event_type}"
            
            payload = {
                "timestamp": datetime.now().isoformat(),
                "documento": self.documento_estudiante,
                "event": event_type,
                **data
            }
            
            self.mqtt_client.publish(topic, json.dumps(payload), qos=1)
            
        except Exception as e:
            print(f"⚠️  Error publicando MQTT: {e}")

    def send_heartbeat(self) -> None:
        """Envía heartbeat para indicar que el estudiante está activo"""
        self._publish_mqtt("heartbeat", {
            "status": "online",
            "completados": len(self.progress.get("completados", [])),
            "puntos": self.progress.get("puntos", 0)
        })

    def send_progress_report(self) -> None:
        """Envía reporte completo de progreso via MQTT"""
        self._publish_mqtt("progress", {
            "completados": self.progress.get("completados", []),
            "puntos": self.progress.get("puntos", 0),
            "total_retos": len(self.retos),
            "fecha_inicio": self.progress.get("fecha_inicio", ""),
            "retos_detalle": [
                {
                    "id": reto_id,
                    "fecha": self.progress.get(f"reto_{reto_id}_fecha", "")
                }
                for reto_id in self.progress.get("completados", [])
            ]
        })


def main():
    """Función principal del CLI"""
    challenge = DockerChallenge()
    
    if len(sys.argv) < 2:
        mensaje_ayuda = (
            "\n🐳 Docker CTF Lab - Sistema de Retos Capture The Flag\n\n"
            "Uso:\n"
            "    python3 docker_challenge.py setup              - Configurar entorno\n"
            "    python3 docker_challenge.py start              - Ver todos los retos\n"
            "    python3 docker_challenge.py submit <flag>      - Enviar una flag\n"
            "    python3 docker_challenge.py status             - Ver tu progreso\n"
            "    python3 docker_challenge.py hint <numero>      - Ver pista de un reto\n"
            "    python3 docker_challenge.py cleanup            - Limpiar contenedores\n\n"
            "Ejemplos:\n"
            "    python3 docker_challenge.py submit FLAG{primer_contenedor_ABC12345}\n"
            "    python3 docker_challenge.py hint 1\n"
        )
        print(mensaje_ayuda)
        sys.exit(1)
    
    comando = sys.argv[1].lower()
    
    if comando == "setup":
        challenge.setup_environment()
    
    elif comando == "start":
        challenge.mostrar_retos()
    
    elif comando == "submit":
        if len(sys.argv) < 3:
            print("❌ Debes proporcionar una flag")
            print("Uso: python3 docker_challenge.py submit FLAG{...}")
            sys.exit(1)
        
        flag = sys.argv[2]
        exito, mensaje, reto_id = challenge.submit_flag(flag)
        print(mensaje)
        
        if exito and len(challenge.progress["completados"]) == len(challenge.retos):
            print("\n" + "=" * 70)
            print("🏆 ¡FELICIDADES! 🏆".center(70))
            print("=" * 70)
            print("\n   Has completado todos los retos del Docker CTF Lab")
            print(f"   Puntuación final: {challenge.progress['puntos']}/{sum(r['puntos'] for r in challenge.retos)} puntos")
            print("\n   ¡Eres un verdadero maestro de Docker! 🐳🎉\n")
            print("=" * 70 + "\n")
    
    elif comando == "status":
        challenge.mostrar_estado()
    
    elif comando == "hint":
        if len(sys.argv) < 3:
            print("❌ Debes proporcionar el número del reto")
            print("Uso: python3 docker_challenge.py hint <numero>")
            sys.exit(1)
        
        try:
            reto_id = int(sys.argv[2])
            challenge.mostrar_hint(reto_id)
        except ValueError:
            print("❌ El número de reto debe ser un número entero")
    
    elif comando == "cleanup":
        challenge.cleanup_containers()
    
    else:
        print(f"❌ Comando desconocido: {comando}")
        print("Usa 'python3 docker_challenge.py' sin argumentos para ver la ayuda")
        sys.exit(1)


if __name__ == "__main__":
    main()
