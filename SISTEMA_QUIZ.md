# 🎯 Sistema de Quiz Educativo - Docker CTF Lab

## 📋 Descripción General

Se ha implementado un **sistema de quiz educativo** que refuerza el aprendizaje de conceptos de Docker antes de permitir el acceso a las flags. Este sistema incluye:

✅ **2 preguntas por reto** (30 preguntas en total)
✅ **Respuestas tipo fill-in-the-blank** (completar palabra/frase)
✅ **Validación en tiempo real**
✅ **Modal popup para quiz interactivo**
✅ **Botón para visualizar flags personalizadas**

---

## 🎓 Características del Sistema de Quiz

### 1. Preguntas Educativas por Reto

Cada uno de los 15 retos ahora incluye **2 preguntas** relacionadas con:
- Comandos de Docker
- Conceptos técnicos
- Flags y opciones
- Mejores prácticas

**Ejemplo de preguntas:**

**Reto 1: Primer Contenedor**
- "El comando para ejecutar un contenedor es 'docker ***'" → `run`
- "Docker primero *** la imagen si no está disponible localmente" → `descarga`

**Reto 8: SSH en Contenedor**
- "SSH es un protocolo de acceso *** que cifra la comunicación" → `remoto`
- "El puerto estándar de SSH es el ***" → `22`

### 2. Flujo del Usuario

```
┌─────────────────────┐
│  Completar Reto     │
│  Docker (práctica)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Clic en            │
│  "🚩 VER MIS FLAGS" │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Modal de Quiz      │
│  (30 preguntas)     │
│  Respuestas: ***    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Verificar          │
│  Respuestas         │
└──────────┬──────────┘
           │
           ▼
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌──────┐    ┌──────────┐
│ERROR │    │ SUCCESS  │
│Mostrar│    │Mostrar   │
│Correc-│    │Flags     │
│ciones │    │          │
└──────┘    └──────────┘
```

### 3. Interfaz de Usuario

#### **Botón "🚩 VER MIS FLAGS"**
- **Ubicación**: Debajo del formulario de submit de flags
- **Estilo**: Gradiente morado-cyan con efecto hover brillante
- **Funcionalidad**: Abre el modal de quiz

#### **Modal de Quiz**
- **Título**: "🎯 [ QUIZ DE REPASO ]"
- **Contenido**: Todas las preguntas de los retos completados
- **Inputs**: Campos de texto para respuestas
- **Validación**: Botón "✓ Verificar Respuestas"
- **Feedback**: Indica respuestas correctas (✓) e incorrectas (✗)

#### **Modal de Flags**
- **Título**: "🚩 [ TUS FLAGS PERSONALIZADAS ]"
- **Info**: Documento del estudiante, retos completados, puntos totales
- **Flags**: Cada flag en tarjeta individual con:
  - Nombre del reto
  - Puntos obtenidos
  - Flag personalizada (UUID-based)
  - Botón "📋 Copiar Flag"

---

## 🔧 Implementación Técnica

### Archivos Modificados

#### 1. **docker_challenge.py** (892 líneas)
```python
# Estructura de cada reto (ejemplo):
{
    "id": 1,
    "nombre": "🐳 Primer Contenedor",
    "descripcion": "...",
    "pista": "...",
    "flag": "FLAG{primer_contenedor}",
    "puntos": 10,
    "dificultad": "Principiante",
    "categoria": "Introducción",
    "preguntas": [  # ← NUEVO
        {
            "pregunta": "El comando para ejecutar un contenedor es 'docker ***'",
            "respuesta": "run"
        },
        {
            "pregunta": "Docker primero *** la imagen si no está disponible localmente",
            "respuesta": "descarga"
        }
    ]
}
```

**Total**: 15 retos × 2 preguntas = **30 preguntas educativas**

#### 2. **web_dashboard.py** (214 líneas)

**Endpoint modificado:**
```python
@app.route('/api/challenges')
def get_challenges():
    # ...
    challenges_data.append({
        # ...
        "preguntas": reto.get("preguntas", [])  # ← NUEVO
    })
```

**Nuevo endpoint:**
```python
@app.route('/api/flags')
def get_flags():
    """
    Endpoint para obtener las flags de los retos completados
    Simula: python3 docker_challenge.py start
    """
    flags_data = []
    completados = challenge.progress.get("completados", [])
    
    for reto in challenge.retos:
        if reto["id"] in completados:
            flag_personalizada = challenge._generar_flag_personalizada(reto["flag"])
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
```

#### 3. **templates/index.html** (1,280 líneas)

**Nuevos modales:**
```html
<!-- Modal de Quiz -->
<div id="quizModal" class="modal">
    <div class="modal-content">
        <h2>🎯 [ QUIZ DE REPASO ]</h2>
        <div id="quizContent"></div>
        <button onclick="checkQuizAnswers()">✓ Verificar Respuestas</button>
    </div>
</div>

<!-- Modal de Flags -->
<div id="flagsModal" class="modal">
    <div class="modal-content">
        <h2>🚩 [ TUS FLAGS PERSONALIZADAS ]</h2>
        <div id="flagsContent"></div>
    </div>
</div>
```

**Nuevo botón:**
```html
<button onclick="showQuizModal()">
    🚩 VER MIS FLAGS
</button>
```

**Funciones JavaScript (220+ líneas):**
- `showQuizModal()`: Muestra quiz con preguntas de retos completados
- `checkQuizAnswers()`: Valida respuestas del usuario
- `showFlagsDirectly()`: Obtiene y muestra flags del endpoint `/api/flags`
- `copyFlag(flag)`: Copia flag al portapapeles
- `closeQuizModal()`: Cierra modal de quiz
- `closeFlagsModal()`: Cierra modal de flags

---

## 📊 Ejemplos de Preguntas por Categoría

### **Introducción (Retos 1-4)**
- Comandos básicos: `docker run`, `docker pull`, `docker images`
- Flags: `-d` (detached), `--name`, `-p` (ports)
- Conceptos: imágenes, contenedores, background

### **Almacenamiento (Reto 5)**
- Comandos: `docker volume create`
- Flags: `-v` (volume mounting)
- Conceptos: persistencia de datos, volúmenes

### **Redes (Retos 6-7)**
- Comandos: `docker network create`
- Flags: `--network`
- Conceptos: driver bridge, conectividad entre contenedores

### **Servicios (Retos 8-11)**
- Protocolos: SSH (puerto 22), Telnet (puerto 23)
- Conceptos: cifrado, acceso remoto, SCADA, VNC
- Aplicaciones: sistemas industriales, escritorios gráficos

### **Construcción (Retos 12-13)**
- Comandos: `docker build`, `docker-compose up`
- Archivos: Dockerfile, docker-compose.yml
- Conceptos: instrucciones, orquestación, múltiples servicios

### **Diagnóstico (Reto 14)**
- Comandos: `docker inspect`
- Conceptos: NetworkSettings.IPAddress, información detallada

### **Mantenimiento (Reto 15)**
- Comandos: `docker system prune`
- Conceptos: limpieza, volúmenes huérfanos

---

## 🎯 Objetivos Pedagógicos

### 1. **Refuerzo del Aprendizaje**
- Los estudiantes deben entender los conceptos, no solo copiar comandos
- Las preguntas tipo fill-in-the-blank obligan a recordar términos clave

### 2. **Validación de Conocimientos**
- El quiz actúa como checkpoint antes de revelar las flags
- Feedback inmediato sobre respuestas incorrectas

### 3. **Integración Práctica-Teórica**
- Primero: práctica (ejecutar comandos Docker)
- Segundo: teoría (responder preguntas conceptuales)
- Tercero: recompensa (obtener flags)

### 4. **Gamificación del Aprendizaje**
- Sistema de puntos (10-40 pts por reto)
- Progreso visual (barra de progreso)
- Desbloqueo de contenido (flags tras quiz)

---

## 🚀 Uso del Sistema

### Para Estudiantes

1. **Completar Reto Docker**
   ```bash
   # Ejemplo: Reto 1
   docker run hello-world
   ```

2. **Obtener Flag del CLI** (método tradicional)
   ```bash
   python3 docker_challenge.py start
   ```

3. **Obtener Flags desde Dashboard** (nuevo método)
   - Clic en botón "🚩 VER MIS FLAGS"
   - Responder quiz de repaso
   - Ver flags personalizadas
   - Copiar flag al portapapeles

4. **Enviar Flag**
   - Pegar flag en el formulario del dashboard
   - Clic en "EXECUTE"
   - Verificación en tiempo real

### Para Profesores

El profesor puede:
- **Monitorear progreso**: Dashboard en puerto 5001
- **Ver intentos de quiz**: (futuro: logs de respuestas)
- **Estadísticas**: Retos completados, puntos, tiempo

---

## 🔐 Seguridad

### Validación de Respuestas
- **Case-insensitive**: "RUN" = "run"
- **Trim whitespace**: " run " = "run"
- **Respuestas exactas**: No acepta sinónimos

### Flags Personalizadas
- **UUID-based**: Únicas por estudiante
- **No reutilizables**: Cada documento genera flags diferentes
- **Validación servidor**: No se pueden falsificar

### Flujo Seguro
1. Usuario completa reto Docker (práctica real)
2. Sistema valida progreso (verificación)
3. Usuario pasa quiz (conocimiento)
4. Sistema revela flag personalizada (recompensa)
5. Usuario envía flag (validación final)

---

## 📈 Estadísticas del Sistema

| Métrica | Valor |
|---------|-------|
| Total de Retos | 15 |
| Total de Preguntas | 30 |
| Preguntas por Reto | 2 |
| Puntos Totales | 395 |
| Dificultades | 4 (Principiante, Intermedio, Avanzado, Experto) |
| Categorías | 7 (Introducción, Contenedores, Redes, Servicios, Aplicaciones, Construcción, Orquestación, Diagnóstico, Mantenimiento) |

---

## 🎨 Mejoras Visuales

### Diseño Cyberpunk/Hacker
- **Tema oscuro**: Fondo #0a0e27
- **Colores neón**: Verde (#00ff41), Cyan (#00d9ff), Morado (#9d4edd)
- **Efectos**: Glow, box-shadow, gradientes
- **Tipografía**: Fira Code (monospace)
- **Animaciones**: Matrix rain, hover effects

### UX Mejorado
- **Modales centrados**: Fácil de leer
- **Feedback visual**: Colores para correcto/incorrecto
- **Botones interactivos**: Hover effects
- **Copiar al portapapeles**: Un clic para copiar flags
- **Responsive**: Adaptable a diferentes pantallas

---

## 🔄 Comparación: Antes vs Después

### Antes (Sistema Original)
```
1. Completar reto Docker
2. python3 docker_challenge.py start  ← CLI obligatorio
3. Copiar flag manualmente
4. Enviar en dashboard
```

### Después (Sistema con Quiz)
```
1. Completar reto Docker
2. Clic en "🚩 VER MIS FLAGS"  ← UI integrada
3. Responder quiz de repaso     ← Educativo
4. Ver flags personalizadas     ← Visual
5. Copiar con un clic           ← Conveniente
6. Enviar en dashboard
```

**Ventajas:**
- ✅ **Integración completa**: Todo desde el dashboard
- ✅ **Educativo**: Refuerzo del aprendizamiento
- ✅ **UX mejorada**: No requiere cambiar a terminal
- ✅ **Visual**: Flags mostradas claramente
- ✅ **Conveniente**: Copiar/pegar simplificado

---

## 🛠️ Mantenimiento

### Añadir Nueva Pregunta
1. Editar `docker_challenge.py`
2. Localizar el reto
3. Añadir pregunta al array:
```python
"preguntas": [
    {
        "pregunta": "Tu pregunta con ***",
        "respuesta": "respuesta_exacta"
    }
]
```
4. Reiniciar `web_dashboard.py`

### Modificar Pregunta Existente
1. Editar `docker_challenge.py`
2. Buscar pregunta por texto
3. Modificar `pregunta` o `respuesta`
4. Reiniciar servidor

### Cambiar Validación de Quiz
- Editar función `checkQuizAnswers()` en `templates/index.html`
- Actualmente: case-insensitive + trim
- Posible: fuzzy matching, sinónimos, múltiples respuestas válidas

---

## 🎯 Próximas Mejoras Sugeridas

### Funcionalidades
- [ ] **Timer de quiz**: Límite de tiempo para responder
- [ ] **Pistas en quiz**: Ayuda si respuesta incorrecta
- [ ] **Estadísticas de quiz**: Tracking de intentos
- [ ] **Ranking de quiz**: Leaderboard de mejores tiempos
- [ ] **Preguntas aleatorias**: Orden diferente para cada estudiante

### Analytics
- [ ] **Logs de respuestas**: Guardar intentos en BD
- [ ] **Preguntas más difíciles**: Identificar patrones
- [ ] **Tiempo promedio**: Medir velocidad de respuesta
- [ ] **Tasa de éxito**: % de respuestas correctas

### Gamificación
- [ ] **Badges**: Logros por quiz perfecto
- [ ] **Streaks**: Racha de respuestas correctas
- [ ] **Bonus points**: Puntos extra por quiz sin errores
- [ ] **Challenge mode**: Modo difícil con preguntas bonus

---

## 📞 Soporte

### Reiniciar Sistema
```bash
# Detener servidor
pkill -f web_dashboard.py

# Iniciar servidor
cd /workspaces/ctf_docker_lab
python3 web_dashboard.py &
```

### Verificar Estado
```bash
# Dashboard del estudiante
curl http://localhost:5000/api/debug

# Flags disponibles
curl http://localhost:5000/api/flags
```

### Limpiar Progreso
```bash
# Eliminar archivo de progreso
rm docker_ctf_progress_1086104202.json

# Reiniciar dashboard
pkill -f web_dashboard.py
python3 web_dashboard.py &
```

---

## 📝 Notas Importantes

1. **Las preguntas se muestran SOLO para retos completados**
2. **Las flags se generan dinámicamente** (UUID-based por estudiante)
3. **El quiz es opcional**: El CLI `python3 docker_challenge.py start` sigue funcionando
4. **Validación estricta**: Respuestas deben ser exactas (case-insensitive)
5. **Feedback educativo**: Muestra respuestas correctas si hay errores

---

## ✅ Checklist de Implementación

- [x] Añadir campo "preguntas" a cada reto en `docker_challenge.py`
- [x] Crear 30 preguntas educativas (2 por reto)
- [x] Modificar endpoint `/api/challenges` para incluir preguntas
- [x] Crear endpoint `/api/flags` para obtener flags
- [x] Añadir modal de quiz en HTML
- [x] Añadir modal de flags en HTML
- [x] Implementar botón "VER MIS FLAGS"
- [x] Crear función `showQuizModal()`
- [x] Crear función `checkQuizAnswers()`
- [x] Crear función `showFlagsDirectly()`
- [x] Implementar validación de respuestas
- [x] Añadir función copiar al portapapeles
- [x] Estilizar modales con tema cyberpunk
- [x] Añadir feedback visual (✓/✗)
- [x] Reiniciar servidor web_dashboard.py
- [x] Documentar sistema en SISTEMA_QUIZ.md

---

**🎉 Sistema Completo y Funcional!**

El Docker CTF Lab ahora incluye un sistema educativo completo que combina:
- 🐳 **Práctica real** de Docker
- 📚 **Aprendizaje teórico** con quiz
- 🚩 **Validación** con flags personalizadas
- 🎯 **Gamificación** con puntos y progreso

¡Feliz Hacking y Aprendizaje! 🚀
