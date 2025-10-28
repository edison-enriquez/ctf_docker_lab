# 👨‍🏫 Guía para Profesores - Docker CTF Lab

> **Manual completo para instructores sobre implementación, monitoreo y evaluación**

## 📋 Tabla de Contenidos

- [Introducción](#introducción)
- [Configuración del Curso](#configuración-del-curso)
- [Sistema de Evaluación](#sistema-de-evaluación)
- [Monitoreo de Progreso](#monitoreo-de-progreso)
- [Validación de Flags](#validación-de-flags)
- [Troubleshooting](#troubleshooting)
- [Personalización](#personalización)

---

## Introducción

Docker CTF Lab está diseñado para facilitar la enseñanza de Docker mediante retos prácticos con validación automática. Este sistema garantiza:

- ✅ **Integridad Académica**: Flags únicas por estudiante
- ✅ **Evaluación Automática**: Verificación mediante Docker API
- ✅ **Trazabilidad**: Progreso guardado con timestamps
- ✅ **Escalabilidad**: Funciona con 1 o 100 estudiantes

---

## Configuración del Curso

### Opción 1: GitHub Classroom (Recomendado)

#### Paso 1: Crear Assignment

1. Ve a GitHub Classroom
2. Crea nuevo assignment: "Docker CTF Lab"
3. Template repo: `edison-enriquez/ctf_docker_lab`
4. Individual assignment (no grupos)

#### Paso 2: Configurar Autograding (Opcional)

Crea `.github/classroom/autograding.json`:

```json
{
  "tests": [
    {
      "name": "Sistema Configurado",
      "setup": "",
      "run": "test -f ~/.docker_ctf_configured",
      "input": "",
      "output": "",
      "comparison": "included",
      "timeout": 5,
      "points": 5
    },
    {
      "name": "Progreso Mínimo",
      "setup": "pip install jq",
      "run": "cat ~/.docker_ctf_progress.json | jq '.puntos' | awk '$1 >= 100 {exit 0} {exit 1}'",
      "input": "",
      "output": "",
      "comparison": "included",
      "timeout": 5,
      "points": 20
    },
    {
      "name": "Retos Completados",
      "setup": "",
      "run": "cat ~/.docker_ctf_progress.json | jq '.completados | length' | awk '$1 >= 10 {exit 0} {exit 1}'",
      "input": "",
      "output": "",
      "comparison": "included",
      "timeout": 5,
      "points": 25
    }
  ]
}
```

#### Paso 3: Instrucciones para Estudiantes

```markdown
## Instrucciones de Entrega

1. Acepta el assignment desde GitHub Classroom
2. Abre tu repositorio en Codespaces
3. Ejecuta `./start.sh` y configura tu documento
4. Resuelve los retos (mínimo 10/15)
5. Alcanza mínimo 200 puntos
6. Commit y push tu archivo de progreso:
   ```bash
   cp ~/.docker_ctf_progress.json ./mi_progreso.json
   git add mi_progreso.json
   git commit -m "Progreso final"
   git push
   ```
```

### Opción 2: Plataforma LMS

#### Moodle

1. Crea actividad tipo "Tarea"
2. Los estudiantes entregan `mi_progreso.json`
3. Verificas usando el script de validación

#### Canvas/Blackboard

Similar a Moodle, configurar como Assignment con archivo de entrega.

---

## Sistema de Evaluación

### Rúbrica Sugerida

| Criterio | Peso | Descripción |
|----------|------|-------------|
| Retos Básicos (1-3) | 10% | Comandos fundamentales |
| Retos Intermedios (4-6, 14, 15) | 25% | Redes, volúmenes, diagnóstico |
| Retos Avanzados (7-9, 12) | 35% | Arquitectura, servicios, construcción |
| Retos Expertos (10, 11, 13) | 30% | Aplicaciones complejas, orquestación |

### Escala de Calificación

```python
def calcular_nota(puntos_obtenidos, total_puntos=380):
    """
    Calcula nota sobre 10
    
    Args:
        puntos_obtenidos: Puntos del estudiante
        total_puntos: Total disponible (380)
    
    Returns:
        Nota sobre 10
    """
    porcentaje = (puntos_obtenidos / total_puntos) * 100
    
    if porcentaje >= 90:
        return 10.0
    elif porcentaje >= 80:
        return 9.0
    elif porcentaje >= 70:
        return 8.0
    elif porcentaje >= 60:
        return 7.0
    elif porcentaje >= 50:
        return 6.0
    else:
        return 5.0
```

### Criterios de Aprobación

**Mínimos Recomendados**:
- 10/15 retos completados (67%)
- 200/380 puntos (53%)
- Al menos 1 reto experto completado

**Excelencia**:
- 15/15 retos completados (100%)
- 380/380 puntos (100%)
- Todos los niveles dominados

---

## Monitoreo de Progreso

### Archivo de Progreso del Estudiante

Cada estudiante tiene `~/.docker_ctf_progress.json`:

```json
{
  "completados": [1, 2, 3, 4, 5],
  "puntos": 70,
  "documento_estudiante": "1234567890",
  "fecha_inicio": "2025-10-28T10:00:00",
  "reto_1_fecha": "2025-10-28T10:15:00",
  "reto_2_fecha": "2025-10-28T10:30:00",
  "reto_3_fecha": "2025-10-28T10:45:00",
  "reto_4_fecha": "2025-10-28T11:00:00",
  "reto_5_fecha": "2025-10-28T11:20:00"
}
```

### Script de Análisis para Profesores

Crea `analizar_progreso.py`:

```python
#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

def analizar_progreso(archivo_json):
    """Analiza el progreso de un estudiante"""
    
    with open(archivo_json, 'r') as f:
        data = json.load(f)
    
    # Información básica
    print("=" * 60)
    print("REPORTE DE PROGRESO - DOCKER CTF LAB")
    print("=" * 60)
    print(f"\nEstudiante: {data.get('documento_estudiante', 'N/A')}")
    print(f"Fecha inicio: {data.get('fecha_inicio', 'N/A')[:19]}")
    print(f"\nRetos completados: {len(data['completados'])}/15")
    print(f"Puntos obtenidos: {data['puntos']}/380")
    print(f"Porcentaje: {(data['puntos']/380)*100:.1f}%")
    
    # Análisis de tiempo
    if data['completados']:
        fechas = []
        for reto_id in data['completados']:
            fecha_str = data.get(f'reto_{reto_id}_fecha')
            if fecha_str:
                fechas.append(datetime.fromisoformat(fecha_str))
        
        if fechas:
            tiempo_total = (max(fechas) - min(fechas)).total_seconds() / 3600
            print(f"\nTiempo total: {tiempo_total:.2f} horas")
            print(f"Tiempo promedio por reto: {tiempo_total/len(fechas):.2f} horas")
    
    # Retos pendientes
    pendientes = [i for i in range(1, 16) if i not in data['completados']]
    if pendientes:
        print(f"\nRetos pendientes: {pendientes}")
    
    # Categorías completadas
    categorias = {
        'Principiante': [1, 2, 3],
        'Intermedio': [4, 5, 6, 14, 15],
        'Avanzado': [7, 8, 9, 12],
        'Experto': [10, 11, 13]
    }
    
    print("\nPor Nivel:")
    for nivel, retos in categorias.items():
        completados = len([r for r in retos if r in data['completados']])
        print(f"  {nivel}: {completados}/{len(retos)}")
    
    # Nota final
    nota = calcular_nota(data['puntos'])
    print(f"\nNota calculada: {nota:.1f}/10.0")
    
    print("\n" + "=" * 60)

def calcular_nota(puntos):
    porcentaje = (puntos / 380) * 100
    if porcentaje >= 90: return 10.0
    elif porcentaje >= 80: return 9.0
    elif porcentaje >= 70: return 8.0
    elif porcentaje >= 60: return 7.0
    elif porcentaje >= 50: return 6.0
    else: return 5.0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 analizar_progreso.py archivo.json")
        sys.exit(1)
    
    analizar_progreso(sys.argv[1])
```

**Uso**:

```bash
python3 analizar_progreso.py estudiante_progreso.json
```

### Reporte Consolidado de Clase

```python
#!/usr/bin/env python3
import json
from pathlib import Path
import csv

def generar_reporte_clase(directorio_entregas):
    """Genera CSV con progreso de todos los estudiantes"""
    
    archivos = Path(directorio_entregas).glob("*.json")
    estudiantes = []
    
    for archivo in archivos:
        with open(archivo, 'r') as f:
            data = json.load(f)
        
        estudiantes.append({
            'documento': data.get('documento_estudiante', ''),
            'completados': len(data['completados']),
            'puntos': data['puntos'],
            'porcentaje': (data['puntos']/380)*100,
            'nivel_principiante': sum(1 for r in [1,2,3] if r in data['completados']),
            'nivel_intermedio': sum(1 for r in [4,5,6,14,15] if r in data['completados']),
            'nivel_avanzado': sum(1 for r in [7,8,9,12] if r in data['completados']),
            'nivel_experto': sum(1 for r in [10,11,13] if r in data['completados'])
        })
    
    # Ordenar por puntos
    estudiantes.sort(key=lambda x: x['puntos'], reverse=True)
    
    # Escribir CSV
    with open('reporte_clase.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=estudiantes[0].keys())
        writer.writeheader()
        writer.writerows(estudiantes)
    
    print(f"✅ Reporte generado: reporte_clase.csv")
    print(f"📊 Total estudiantes: {len(estudiantes)}")
    print(f"📈 Promedio puntos: {sum(e['puntos'] for e in estudiantes)/len(estudiantes):.1f}")
    print(f"🏆 Mejor puntuación: {estudiantes[0]['puntos']} pts")
```

---

## Validación de Flags

### Generar Flag de Cualquier Estudiante

```python
#!/usr/bin/env python3
import hashlib
import sys

def generar_flag_estudiante(documento, reto_id, texto_base):
    """
    Genera la flag para un estudiante específico
    
    Args:
        documento: Documento del estudiante
        reto_id: ID del reto (1-15)
        texto_base: Base de la flag (ej: "primer_contenedor")
    """
    datos = f"{documento}_{reto_id}_{texto_base}"
    hash_unico = hashlib.sha256(datos.encode()).hexdigest()[:8].upper()
    return f"FLAG{{{texto_base}_{hash_unico}}}"

# Mapeo de retos
RETOS = {
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

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 generar_flag.py DOCUMENTO RETO_ID")
        print("Ejemplo: python3 generar_flag.py 1234567890 1")
        sys.exit(1)
    
    documento = sys.argv[1]
    reto_id = int(sys.argv[2])
    
    if reto_id not in RETOS:
        print(f"❌ Reto ID debe ser 1-15")
        sys.exit(1)
    
    flag = generar_flag_estudiante(documento, reto_id, RETOS[reto_id])
    print(f"\n🚩 Flag del estudiante {documento} para reto #{reto_id}:")
    print(f"   {flag}\n")
```

**Uso**:

```bash
# Generar flag del reto 1 para documento 1234567890
python3 generar_flag.py 1234567890 1

# Salida: FLAG{primer_contenedor_ABC12345}
```

### Verificación Manual

Si un estudiante reporta un problema:

1. Pide su documento de identidad
2. Genera su flag con el script
3. Compara con lo que ellos tienen
4. Verifica que su archivo de progreso sea válido

---

## Troubleshooting

### Estudiante dice "Flag correcta pero no valida"

**Causa**: El sistema verifica que el recurso Docker exista, no solo la flag.

**Solución**:

```bash
# Verificar que el recurso existe
docker ps -a  # Para contenedores
docker network ls  # Para redes
docker volume ls  # Para volúmenes
docker images  # Para imágenes
```

### Estudiante perdió su progreso

**Prevención**: Instruir a hacer backup:

```bash
cp ~/.docker_ctf_progress.json ~/progreso_backup.json
```

**Recuperación**: Restaurar desde backup:

```bash
cp ~/progreso_backup.json ~/.docker_ctf_progress.json
```

### Docker no funciona en Codespaces

**Verificar**:

```bash
# Ver si Docker daemon está corriendo
docker ps

# Ver logs
sudo journalctl -u docker

# Reiniciar Docker
sudo systemctl restart docker
```

### Puerto 5000 ocupado

**Solución temporal**:

```bash
# Usar otro puerto
python3 web_dashboard.py
# Editar web_dashboard.py línea final: app.run(port=5001)
```

---

## Personalización

### Agregar Nuevos Retos

1. **Editar `docker_challenge.py`**:

```python
# En __init__, agregar a self.retos:
{
    "id": 16,
    "nombre": "🚢 Nuevo Reto",
    "descripcion": "Descripción del reto",
    "pista": "Pista útil",
    "flag": "FLAG{nuevo_reto}",
    "puntos": 25,
    "dificultad": "Avanzado",
    "categoria": "Nueva Categoría"
}
```

2. **Agregar función de verificación**:

```python
def _verificar_reto_especifico(self, reto_id: int) -> bool:
    # ... código existente ...
    
    elif reto_id == 16:
        # Tu lógica de verificación
        return True
```

3. **Agregar en submit_flag**:

```python
flag_bases = {
    # ... existentes ...
    16: "nuevo_reto"
}
```

### Cambiar Puntuación

Edita los valores de `puntos` en cada reto en `docker_challenge.py`.

### Personalizar Dashboard

Edita `templates/index.html` para cambiar:
- Colores (CSS en `<style>`)
- Textos
- Logo/branding
- Estructura

---

## Recursos para el Curso

### Presentaciones Sugeridas

**Clase 1: Introducción a Docker** (2 horas)
- ¿Qué son contenedores?
- Docker vs VMs
- Instalación y setup
- Retos 1-3

**Clase 2: Imágenes y Redes** (2 horas)
- Gestión de imágenes
- Redes en Docker
- Mapeo de puertos
- Retos 4-6

**Clase 3: Arquitectura y Volúmenes** (2 horas)
- Persistencia de datos
- Comunicación entre contenedores
- Retos 5, 7, 14

**Clase 4: Construcción y Servicios** (2 horas)
- Dockerfile
- Servicios (SSH, Telnet)
- Retos 8, 9, 12

**Clase 5: Aplicaciones Avanzadas** (3 horas)
- SCADA/ICS
- Escritorios remotos
- Docker Compose
- Retos 10, 11, 13

### Material Complementario

- [Docker Documentation](https://docs.docker.com/)
- [Play with Docker](https://labs.play-with-docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Katacoda Docker Scenarios](https://www.katacoda.com/courses/docker)

### Evaluaciones Adicionales

**Quiz Teórico**:
1. ¿Cuál es la diferencia entre imagen y contenedor?
2. ¿Qué flag usas para ejecutar un contenedor en background?
3. ¿Cómo persisten los datos en Docker?
4. ¿Qué es Docker Compose?

**Proyecto Final**:
- Crear aplicación multi-tier (frontend, backend, DB)
- Dockerizar con Dockerfile personalizado
- Orquestar con docker-compose
- Documentar con README

---

## Estadísticas Esperadas

Basado en pruebas piloto:

| Métrica | Valor |
|---------|-------|
| Tiempo promedio (completar todo) | 6-8 horas |
| Tiempo por reto (promedio) | 20-30 minutos |
| Tasa de completación | 85% (10+ retos) |
| Reto más difícil | #13 (Docker Compose) |
| Reto más fácil | #1 (Primer Contenedor) |

---

## Contacto y Soporte

Para soporte técnico o consultas:

- **Repositorio**: [github.com/edison-enriquez/ctf_docker_lab](https://github.com/edison-enriquez/ctf_docker_lab)
- **Issues**: Reportar en GitHub Issues
- **Email**: edison.enriquez@ejemplo.com

---

**¡Éxito con tu curso de Docker! 🐳🎓**
