#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación del sistema Docker CTF Lab
Verifica que todos los componentes estén correctamente instalados
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Imprime un encabezado formateado"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def check_python():
    """Verifica la versión de Python"""
    print("\n🐍 Verificando Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Se requiere Python 3.8 o superior (tienes {version.major}.{version.minor})")
        return False


def check_docker():
    """Verifica Docker"""
    print("\n🐳 Verificando Docker...")
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   ✅ {version}")
            
            # Verificar que Docker daemon está corriendo
            result = subprocess.run(['docker', 'ps'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("   ✅ Docker daemon está corriendo")
                return True
            else:
                print("   ❌ Docker daemon no está corriendo")
                return False
        else:
            print("   ❌ Docker no está instalado")
            return False
    except FileNotFoundError:
        print("   ❌ Docker no está instalado")
        return False
    except subprocess.TimeoutExpired:
        print("   ❌ Timeout al verificar Docker")
        return False


def check_dependencies():
    """Verifica las dependencias Python"""
    print("\n📦 Verificando dependencias Python...")
    dependencies = {
        'flask': 'Flask',
        'docker': 'Docker SDK'
    }
    
    all_installed = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} no está instalado")
            all_installed = False
    
    return all_installed


def check_files():
    """Verifica que existan los archivos necesarios"""
    print("\n📄 Verificando archivos del sistema...")
    required_files = {
        'docker_challenge.py': 'Sistema principal de retos',
        'web_dashboard.py': 'Servidor web',
        'templates/index.html': 'Dashboard HTML',
        'requirements.txt': 'Dependencias',
        'start.sh': 'Script de inicio'
    }
    
    all_exist = True
    for file, description in required_files.items():
        path = Path(file)
        if path.exists():
            size = path.stat().st_size
            print(f"   ✅ {file} ({size} bytes) - {description}")
        else:
            print(f"   ❌ {file} - {description}")
            all_exist = False
    
    return all_exist


def check_permissions():
    """Verifica permisos de archivos ejecutables"""
    print("\n🔐 Verificando permisos...")
    executable_files = ['start.sh', 'docker_challenge.py', 'web_dashboard.py']
    
    all_ok = True
    for file in executable_files:
        path = Path(file)
        if path.exists():
            if os.access(path, os.X_OK):
                print(f"   ✅ {file} tiene permisos de ejecución")
            else:
                print(f"   ⚠️  {file} no tiene permisos de ejecución")
                print(f"      Ejecuta: chmod +x {file}")
                all_ok = False
        else:
            print(f"   ❌ {file} no existe")
            all_ok = False
    
    return all_ok


def check_configuration():
    """Verifica si el laboratorio está configurado"""
    print("\n🔧 Verificando configuración del laboratorio...")
    home_dir = Path.home()
    config_file = home_dir / ".docker_ctf_configured"
    progress_file = home_dir / ".docker_ctf_progress.json"
    
    if config_file.exists():
        print("   ✅ Laboratorio configurado")
        
        if progress_file.exists():
            import json
            try:
                with open(progress_file, 'r') as f:
                    progress = json.load(f)
                completados = len(progress.get('completados', []))
                puntos = progress.get('puntos', 0)
                documento = progress.get('documento_estudiante', 'No configurado')
                
                print(f"\n   📊 Progreso actual:")
                print(f"      • Estudiante: {documento}")
                print(f"      • Retos completados: {completados}/15")
                print(f"      • Puntos: {puntos}/380")
            except:
                print(f"   ⚠️  Archivo de progreso corrupto")
        else:
            print(f"\n   ℹ️  No hay progreso guardado aún")
        
        return True
    else:
        print("   ℹ️  Laboratorio no configurado")
        print("   💡 Ejecuta: python3 docker_challenge.py setup")
        return True  # No es crítico


def check_ports():
    """Verifica disponibilidad del puerto 5000"""
    print("\n🔌 Verificando puertos...")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5000))
        sock.close()
        
        if result == 0:
            print("   ⚠️  Puerto 5000 está en uso")
            print("   💡 Puede que el dashboard ya esté corriendo")
        else:
            print("   ✅ Puerto 5000 disponible para el dashboard")
        
        return True
    except:
        print("   ⚠️  No se pudo verificar el puerto")
        return True


def print_summary(results):
    """Imprime un resumen de los resultados"""
    print_header("📋 RESUMEN DE VERIFICACIÓN")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    
    print(f"\n   Verificaciones completadas: {passed}/{total}")
    print(f"   Estado: ", end="")
    
    if passed == total:
        print("✅ SISTEMA COMPLETAMENTE FUNCIONAL")
        print("\n   🚀 Todo está listo para usar Docker CTF Lab")
        print("\n   💡 Para comenzar:")
        print("      • Ejecuta: ./start.sh")
        print("      • O ejecuta: python3 web_dashboard.py")
    elif passed >= total * 0.7:
        print("⚠️  SISTEMA PARCIALMENTE FUNCIONAL")
        print("\n   ⚠️  Algunos componentes necesitan atención")
        print("   💡 Revisa los errores arriba y corrígelos")
    else:
        print("❌ SISTEMA NO FUNCIONAL")
        print("\n   ❌ Varios componentes críticos fallan")
        print("   💡 Revisa los errores arriba y corrígelos")
    
    print("\n" + "=" * 70 + "\n")


def main():
    """Función principal"""
    print_header("🔍 VERIFICACIÓN DEL SISTEMA - Docker CTF Lab")
    
    results = {
        'Python': check_python(),
        'Docker': check_docker(),
        'Dependencias': check_dependencies(),
        'Archivos': check_files(),
        'Permisos': check_permissions(),
        'Configuración': check_configuration(),
        'Puertos': check_ports()
    }
    
    print_summary(results)
    
    # Código de salida
    critical = ['Python', 'Docker', 'Dependencias', 'Archivos']
    critical_passed = all(results[k] for k in critical if k in results)
    
    if critical_passed:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
