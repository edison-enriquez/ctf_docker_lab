# 🔍 Sistema de Verificación Automática de Comandos Docker

## 📋 Descripción

El Docker CTF Lab ahora incluye un **sistema automático de verificación** que asegura que los estudiantes realmente ejecuten los comandos Docker antes de aceptar las flags.

## 🎯 ¿Cómo funciona?

### Flujo de Verificación

Cuando un estudiante presiona el botón **EXECUTE** en el dashboard:

```
1. 📤 ENVIAR FLAG
   ↓
2. 🔍 VERIFICACIÓN DOCKER (NUEVO)
   │
   ├─ ✅ Verificación Exitosa
   │  ↓
   │  3. 📨 Enviar Flag al Backend
   │  ↓
   │  4. ✨ Reto Completado
   │
   └─ ❌ Verificación Fallida
      ↓
      ⚠️  Mostrar mensaje de error
      ⛔ NO enviar la flag
```

### Proceso Detallado

#### PASO 1: Verificación Previa (Frontend)
```javascript
// Al presionar EXECUTE, primero se verifica
POST /api/verify-flag
Body: { "flag": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" }
```

**Respuestas posibles:**

✅ **Éxito** (código 200):
```json
{
  "success": true,
  "message": "✅ Verificación Docker exitosa para: 🐳 Primer Contenedor",
  "reto_id": 1,
  "reto_nombre": "🐳 Primer Contenedor"
}
```

❌ **Fallo por comando no ejecutado** (código 200):
```json
{
  "success": false,
  "message": "⚠️ Flag correcta, pero no se detectó la ejecución del comando Docker...",
  "reto_id": 1,
  "reto_nombre": "🐳 Primer Contenedor"
}
```

❌ **Flag incorrecta** (código 200):
```json
{
  "success": false,
  "message": "❌ Flag incorrecta o no válida"
}
```

#### PASO 2: Envío de Flag (Solo si verificación exitosa)
```javascript
// Solo se ejecuta si PASO 1 fue exitoso
POST /api/submit
Body: { "flag": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" }
```

## 🔧 Verificaciones por Reto

### Reto 1: Primer Contenedor
- **Comando esperado:** `docker run hello-world`
- **Verifica:** Que exista al menos un contenedor con imagen `hello-world`
- **Método Docker:** `docker.containers.list(all=True, filters={"ancestor": "hello-world"})`

### Reto 2: Imagen Descargada
- **Comando esperado:** `docker pull nginx:alpine`
- **Verifica:** Que la imagen `nginx:alpine` esté en el sistema
- **Método Docker:** `docker.images.get("nginx:alpine")`

### Reto 3: Contenedor en Background
- **Comando esperado:** `docker run -d --name webserver nginx:alpine`
- **Verifica:** Que exista un contenedor llamado `webserver` en estado `running`
- **Método Docker:** `docker.containers.get("webserver").status == "running"`

### Reto 4: Puerto Mapeado
- **Comando esperado:** `docker run -d --name webserver-port -p 8080:80 nginx:alpine`
- **Verifica:** 
  - Contenedor `webserver-port` existe
  - Puerto 80 del contenedor está mapeado al puerto 8080 del host
- **Método Docker:** Inspección de `NetworkSettings.Ports`

### Reto 5: Volumen Creado
- **Comando esperado:** `docker volume create datos_importantes`
- **Verifica:** Que exista un volumen llamado `datos_importantes`
- **Método Docker:** `docker.volumes.list(filters={"name": "datos_importantes"})`

### Reto 6: Red Creada
- **Comando esperado:** `docker network create mi_red_ctf`
- **Verifica:** Que exista una red llamada `mi_red_ctf`
- **Método Docker:** `docker.networks.list(names=["mi_red_ctf"])`

### Reto 7: Contenedores Conectados
- **Comando esperado:** 
  ```bash
  docker run -d --name contenedor1 --network mi_red_ctf alpine sleep 3600
  docker run -d --name contenedor2 --network mi_red_ctf alpine sleep 3600
  ```
- **Verifica:** 
  - Ambos contenedores existen
  - Ambos están en la red `mi_red_ctf`
  - Ambos están corriendo
- **Método Docker:** Inspección de `NetworkSettings.Networks`

### Retos 8-11: Puertos Específicos
- **Reto 8 (SSH):** Puerto 2222
- **Reto 9 (Telnet):** Puerto 2323
- **Reto 10 (SCADA):** Puerto 8000
- **Reto 11 (VNC):** Puerto 5900 o 6080

**Verificación:** Busca cualquier contenedor que tenga el puerto mapeado

### Reto 12: Dockerfile Creado
- **Comando esperado:** `docker build -t mi-app:v1 .`
- **Verifica:** Que la imagen `mi-app:v1` exista
- **Método Docker:** `docker.images.get("mi-app:v1")`

### Reto 13: Docker Compose
- **Comando esperado:** `docker-compose up -d`
- **Verifica:** 
  - Contenedor con imagen nginx corriendo
  - Contenedor con imagen redis corriendo
- **Método Docker:** Búsqueda en tags de imágenes de contenedores

### Reto 14: Inspección
- **Comando esperado:** `docker inspect <contenedor>`
- **Verifica:** Que haya al menos un contenedor para inspeccionar
- **Método Docker:** `docker.containers.list()`

### Reto 15: Limpieza
- **Verificación simbólica:** Siempre retorna `True`
- Razón: Difícil verificar que se eliminaron recursos

## 💻 Ejemplo de Uso

### Escenario 1: Usuario NO ejecuta el comando

```bash
# Usuario obtiene la flag pero NO ejecuta el comando
# Luego presiona EXECUTE en el dashboard
```

**Resultado en el dashboard:**
```
[ VERIFYING ] Verificando ejecución del comando Docker...
[ VERIFICATION FAILED ] ⚠️ Flag correcta, pero no se detectó la 
ejecución del comando Docker. Asegúrate de ejecutar el comando 
requerido para: 🐳 Primer Contenedor
```

❌ **La flag NO se envía al backend**

---

### Escenario 2: Usuario ejecuta el comando correctamente

```bash
# Usuario ejecuta el comando
docker run hello-world

# Luego ingresa la flag y presiona EXECUTE
```

**Resultado en el dashboard:**
```
[ VERIFYING ] Verificando ejecución del comando Docker...
[ SUBMITTING ] Enviando flag...
[ SUCCESS ] 
🎉 ¡CORRECTO! 🎉
Reto 1: 🐳 Primer Contenedor
+10 puntos
Total: 10 puntos
Completados: 1/15
```

✅ **La flag se acepta y el reto se marca como completado**

## 🎨 Interfaz de Usuario

### Notificaciones Visuales

El sistema usa diferentes colores para las notificaciones:

- 🔵 **AZUL (info):** Proceso de verificación en curso
  ```css
  background: rgba(0, 217, 255, 0.2);
  border-color: var(--accent-cyan);
  color: var(--accent-cyan);
  ```

- 🟢 **VERDE (success):** Verificación y envío exitoso
  ```css
  background: rgba(0, 255, 65, 0.2);
  border-color: var(--accent-green);
  color: var(--accent-green);
  ```

- 🔴 **ROJO (error):** Verificación fallida o error
  ```css
  background: rgba(255, 0, 110, 0.2);
  border-color: var(--accent-red);
  color: var(--accent-red);
  ```

## 🔒 Seguridad

### Prevención de Trampas

El sistema previene que los estudiantes:
- ❌ Envíen flags sin ejecutar comandos
- ❌ Usen flags de otros retos
- ❌ Reenvíen retos ya completados
- ❌ Usen flags inválidas o modificadas

### Validación en Múltiples Capas

1. **Frontend (JavaScript):** Verificación previa antes de enviar
2. **Backend (Python):** Validación de la flag
3. **Docker API:** Verificación del estado real de Docker
4. **Base de datos:** Registro del progreso

## 📊 Logging y Monitoreo

### Logs del Servidor

```bash
127.0.0.1 - - [05/Nov/2025 04:53:50] "POST /api/verify-flag HTTP/1.1" 200 -
127.0.0.1 - - [05/Nov/2025 04:53:52] "POST /api/submit HTTP/1.1" 200 -
```

### Monitoreo MQTT (Branch: profesor)

Cuando un reto se completa exitosamente:

```json
{
  "tipo": "flag_submit",
  "documento_estudiante": "1086104202",
  "reto_id": 1,
  "reto_nombre": "🐳 Primer Contenedor",
  "puntos": 10,
  "total_puntos": 10,
  "completados": 1,
  "timestamp": "2025-11-05T04:53:52.123456"
}
```

## 🚀 Endpoints API

### POST /api/verify-flag
**Propósito:** Verificar comando Docker antes de aceptar flag

**Request:**
```json
{
  "flag": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

**Response (Exitosa):**
```json
{
  "success": true,
  "message": "✅ Verificación Docker exitosa para: 🐳 Primer Contenedor",
  "reto_id": 1,
  "reto_nombre": "🐳 Primer Contenedor"
}
```

**Response (Fallida):**
```json
{
  "success": false,
  "message": "⚠️ Flag correcta, pero no se detectó la ejecución del comando Docker...",
  "reto_id": 1,
  "reto_nombre": "🐳 Primer Contenedor"
}
```

### POST /api/submit
**Propósito:** Enviar flag (solo después de verificación exitosa)

**Request:**
```json
{
  "flag": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

**Response:**
```json
{
  "success": true,
  "message": "🎉 ¡CORRECTO! 🎉...",
  "reto_id": 1,
  "puntos_totales": 10,
  "completados": 1,
  "total_retos": 15
}
```

## 🧪 Testing

### Script de Prueba Automática

Ejecuta el script de prueba incluido:

```bash
./test_verification.sh
```

Este script:
1. ✅ Intenta verificar sin ejecutar comando (debe fallar)
2. ✅ Ejecuta el comando Docker
3. ✅ Verifica nuevamente (debe pasar)
4. ✅ Muestra logs del proceso

### Prueba Manual

```bash
# 1. Inicia el dashboard
python3 web_dashboard.py

# 2. En otra terminal, obtén tu flag
python3 docker_challenge.py start

# 3. Intenta enviar la flag SIN ejecutar el comando
# Resultado: Verificación fallará

# 4. Ejecuta el comando
docker run hello-world

# 5. Envía la flag nuevamente
# Resultado: Verificación exitosa, reto completado
```

## 📝 Notas Técnicas

### Dependencias Python
```python
import docker  # Docker SDK para Python
from flask import Flask, jsonify, request
```

### Verificación en Modo Desarrollo

Si Docker no está disponible (desarrollo sin Docker):
```python
if not self.docker_client:
    return True  # Acepta la flag en modo desarrollo
```

### Manejo de Errores

```python
try:
    # Verificación Docker
    verificacion_exitosa = challenge._verificar_reto_especifico(reto_id)
except Exception as e:
    print(f"⚠️ Error en verificación: {e}")
    return False  # Por seguridad, falla la verificación en caso de error
```

## 🎓 Beneficios Educativos

### Para Estudiantes
- ✅ Aprenden haciendo (no solo copiando flags)
- ✅ Verificación inmediata del aprendizaje
- ✅ Feedback claro sobre qué falta
- ✅ No pueden "hacer trampa" sin aprender

### Para Profesores
- ✅ Garantía de que ejecutaron los comandos
- ✅ Monitoreo en tiempo real vía MQTT
- ✅ Logs detallados de cada intento
- ✅ Métricas precisas del progreso real

## 🔄 Flujo Completo del Sistema

```
ESTUDIANTE                    DASHBOARD                  BACKEND                   DOCKER
    |                             |                         |                         |
    | 1. Ejecuta comando          |                         |                         |
    |--------------------------->|------------------------>|------------------------>|
    |   docker run hello-world   |                         |                         |
    |                             |                         |                         |
    | 2. Obtiene flag             |                         |                         |
    | (via dashboard o CLI)       |                         |                         |
    |                             |                         |                         |
    | 3. Ingresa flag             |                         |                         |
    | y presiona EXECUTE          |                         |                         |
    |--------------------------->|                         |                         |
    |                             |                         |                         |
    |                             | 4. POST /verify-flag    |                         |
    |                             |------------------------>|                         |
    |                             |                         |                         |
    |                             |                         | 5. Verifica Docker API  |
    |                             |                         |------------------------>|
    |                             |                         |                         |
    |                             |                         | 6. Estado de contenedor |
    |                             |                         |<------------------------|
    |                             |                         |                         |
    |                             | 7. Respuesta (exitosa)  |                         |
    |                             |<------------------------|                         |
    |                             |                         |                         |
    | 8. Notificación:            |                         |                         |
    | "Verificación exitosa"      |                         |                         |
    |<----------------------------|                         |                         |
    |                             |                         |                         |
    |                             | 9. POST /submit         |                         |
    |                             |------------------------>|                         |
    |                             |                         |                         |
    |                             |                         | 10. Registra completado |
    |                             |                         |    + Publica MQTT       |
    |                             |                         |                         |
    |                             | 11. Respuesta (éxito)   |                         |
    |                             |<------------------------|                         |
    |                             |                         |                         |
    | 12. Notificación:           |                         |                         |
    | "¡CORRECTO! +10 puntos"     |                         |                         |
    |<----------------------------|                         |                         |
```

## 🎯 Conclusión

El sistema de verificación automática asegura que los estudiantes:
1. ✅ **Ejecuten** realmente los comandos Docker
2. ✅ **Aprendan** haciendo, no solo copiando
3. ✅ **Completen** los retos correctamente
4. ✅ **Obtengan** feedback inmediato

El profesor tiene la garantía de que cuando un estudiante completa un reto, realmente aprendió y ejecutó los comandos requeridos.

---

**Última actualización:** 5 de Noviembre de 2025  
**Versión:** 2.0  
**Branch:** profesor (también disponible en main)
