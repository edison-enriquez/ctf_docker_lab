# ⚡ Quick Start - Sistema de Quiz

## 🎯 Resumen Rápido

Se han añadido **2 preguntas educativas por reto** (30 preguntas totales) que los estudiantes deben responder antes de ver sus flags personalizadas.

---

## ▶️ Iniciar el sistema (forma recomendada para estudiantes)

Ahora TODO puede iniciarse con un único comando desde la raíz del proyecto:

```bash
./start.sh
```

Esto arranca en modo "estudiante" los servicios mínimos (dashboard web en http://localhost:5000) en background y deja logs en `/tmp/ctf_dashboard.log`.

Si prefieres el menú interactivo ejecuta:

```bash
./start.sh menu
```

## 🚀 Cómo Usar (Estudiantes)

### Método Nuevo (Recomendado)

1. **Completar el reto Docker** (práctica)
   ```bash
   docker run hello-world
   ```

2. **Clic en botón "🚩 VER MIS FLAGS"** en el dashboard

3. **Responder quiz de repaso** (2 preguntas por reto completado)
   - Llenar los espacios con ***
   - Ejemplo: "Docker usa *** para empaquetar aplicaciones" → `contenedores`

4. **Clic en "✓ Verificar Respuestas"**
   - ✅ Verde = Correcto
   - ❌ Rojo = Incorrecto (muestra respuesta correcta)

5. **Ver flags personalizadas** (si todas correctas)
   - Cada flag tiene botón "📋 Copiar Flag"

6. **Enviar flag** en el formulario del dashboard

### Método Tradicional (Sigue funcionando)

```bash
python3 docker_challenge.py start
# Muestra todas las flags en CLI
```

---

## 📚 Ejemplo de Preguntas

**Reto 1: Primer Contenedor**
- "El comando para ejecutar un contenedor es 'docker ***'" → `run`
- "Docker primero *** la imagen si no está disponible localmente" → `descarga`

**Reto 12: Dockerfile Personalizado**
- "Un Dockerfile contiene las *** para construir una imagen de Docker" → `instrucciones`
- "El comando 'docker ***' se usa para construir una imagen desde un Dockerfile" → `build`

---

## 🎓 Beneficios Educativos

✅ **Refuerzo del aprendizaje**: No solo ejecutar comandos, entender conceptos
✅ **Validación de conocimientos**: Quiz antes de recompensa (flags)
✅ **Feedback inmediato**: Respuestas correctas mostradas al instante
✅ **Integración fluida**: Todo desde el dashboard web

---

## 🛠️ Mantenimiento (Profesores)

### Reiniciar Dashboard
```bash
pkill -f web_dashboard.py
cd /workspaces/ctf_docker_lab
python3 web_dashboard.py &
```

### Verificar Estado
```bash
curl http://localhost:5000/api/debug
curl http://localhost:5000/api/flags
```

### Añadir/Modificar Preguntas

Editar `docker_challenge.py`, buscar el reto y modificar:
```python
"preguntas": [
    {
        "pregunta": "Tu pregunta con ***",
        "respuesta": "respuesta_sin_espacios"
    }
]
```

Luego reiniciar servidor.

---

## 🎨 Interfaz

### Botón Principal
- **Ubicación**: Debajo del formulario "SUBMIT FLAG"
- **Texto**: "🚩 VER MIS FLAGS"
- **Estilo**: Gradiente morado-cyan con glow effect

### Modal de Quiz
- **Título**: "🎯 [ QUIZ DE REPASO ]"
- **Preguntas**: Solo de retos completados
- **Validación**: Case-insensitive, trim whitespace

### Modal de Flags
- **Título**: "🚩 [ TUS FLAGS PERSONALIZADAS ]"
- **Contenido**: 
  - Nombre del reto
  - Puntos obtenidos
  - Flag personalizada (UUID)
  - Botón copiar al portapapeles

---

## 📊 Estadísticas

| Item | Valor |
|------|-------|
| Total Retos | 15 |
| Preguntas por Reto | 2 |
| Total Preguntas | 30 |
| Puntos Totales | 395 |

---

## 🔐 Seguridad

- ✅ Flags UUID-based únicas por estudiante
- ✅ Quiz requiere retos completados previamente
- ✅ Validación server-side de respuestas
- ✅ No se pueden falsificar flags

---

## 💡 Flujo Completo

```
Práctica Docker → Completar Reto → Clic "Ver Flags" → Quiz (30 preguntas)
                                                              ↓
                                                         ¿Correcto?
                                                              ↓
                                        ┌─────────────────────┴─────────────────┐
                                        ↓                                       ↓
                                     ❌ NO                                    ✅ SÍ
                            Muestra correcciones                       Muestra Flags
                            Usuario reintenta                          Usuario copia
                                                                       Usuario envía
                                                                       ¡Reto validado!
```

---

## 📁 Archivos Modificados

1. **docker_challenge.py** - Añadidas 30 preguntas educativas
2. **web_dashboard.py** - Nuevo endpoint `/api/flags`
3. **templates/index.html** - Modales de quiz y flags + JavaScript

---

## 🎉 ¡Listo para Usar!

El sistema ya está funcionando. Los estudiantes pueden:
- Completar retos Docker
- Hacer clic en "🚩 VER MIS FLAGS"
- Responder quiz educativo
- Ver y copiar sus flags personalizadas
- Enviar flags para validación

**Documentación completa**: Ver `SISTEMA_QUIZ.md`

---

**Última actualización**: Sistema completamente implementado y servidor ejecutándose en puerto 5000.
