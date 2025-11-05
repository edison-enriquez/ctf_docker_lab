# 🚩 Cómo Obtener las FLAGS en Docker CTF Lab

## 📚 Conceptos Básicos

Las **FLAGS** son códigos únicos que demuestran que completaste un reto correctamente. En este sistema:

- ✅ Las flags NO se muestran en el dashboard web (por seguridad)
- ✅ Las flags se obtienen completando los retos de Docker
- ✅ Las flags son personalizadas para cada estudiante
- ✅ Cada estudiante tiene flags diferentes (generadas con su documento)

---

## 🔄 Flujo Completo para Obtener una FLAG

### 1️⃣ Ver los Retos en el Dashboard

Abre el dashboard web:
```bash
http://localhost:5000
```

Verás los retos con:
- ✅ Nombre y descripción
- ✅ Puntos y dificultad
- ✅ Botón "💡 SHOW HINT" para ver pistas
- ❌ NO verás las flags (por diseño)

---

### 2️⃣ Completar el Reto en Docker

**Ejemplo - Reto 1: Primer Contenedor**

Lee la descripción:
> "Ejecuta tu primer contenedor usando la imagen 'hello-world'"

Ejecuta en la terminal:
```bash
docker run hello-world
```

Verás el mensaje:
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

### 3️⃣ Obtener la FLAG usando CLI

Ahora que completaste el reto en Docker, ejecuta:

```bash
python3 docker_challenge.py start
```

**Salida del comando:**
```
================================================================================
                      🎯 DOCKER CTF LAB - RETOS DISPONIBLES                      
================================================================================

👤 Estudiante: 1086104202
📊 Progreso: 0/15 retos completados
🏆 Puntos: 0/360

--------------------------------------------------------------------------------

❌ Reto 1: 🐳 Primer Contenedor
   📝 Ejecuta tu primer contenedor usando la imagen 'hello-world'
   🎯 Dificultad: Principiante | Puntos: 10 | Categoría: Comandos Básicos
   🚩 Flag a enviar: d959efcd-82dc-57ee-bdfe-58b0768ff55e    <-- ¡AQUÍ ESTÁ!
   ----------------------------------------------------------------------------
```

**¡Copia esa flag!** Es única para ti.

---

### 4️⃣ Enviar la FLAG

Tienes dos opciones:

#### Opción A: Dashboard Web (Recomendado)

1. Ve a http://localhost:5000
2. Pega la flag en el formulario
3. Click en **"SUBMIT FLAG"**
4. Verás: ✅ ¡Correcto! Reto completado (+10 pts)

#### Opción B: Línea de Comandos

```bash
python3 docker_challenge.py submit d959efcd-82dc-57ee-bdfe-58b0768ff55e
```

---

### 5️⃣ Verificar Completado

En el dashboard verás:
```
[✓] 🐳 Primer Contenedor (10 pts) - COMPLETADO
[✓] PWNED AT 04/11/2025 14:30:15
```

---

## 📋 Comandos Útiles

```bash
# Ver todos los retos y sus flags
python3 docker_challenge.py start

# Ver pista de un reto específico
python3 docker_challenge.py hint 1

# Enviar una flag
python3 docker_challenge.py submit <tu-flag>

# Ver tu progreso
python3 docker_challenge.py status

# Iniciar dashboard web
python3 web_dashboard.py
# O usar el menú:
./start.sh
```

---

## 🎓 Ejemplo Completo - Reto 2

### Paso 1: Ver el reto en dashboard
```
[X] 🔍 Inspector de Imágenes (10 pts)
Descarga la imagen 'nginx:alpine' y encuentra su tamaño
[💡 SHOW HINT]
```

### Paso 2: Completar en Docker
```bash
docker pull nginx:alpine
docker images nginx:alpine
```

### Paso 3: Obtener flag
```bash
python3 docker_challenge.py start
```

Salida:
```
❌ Reto 2: 🔍 Inspector de Imágenes
   🚩 Flag a enviar: ff2472c6-e310-5d83-8ead-44f4a9deb63f
```

### Paso 4: Submit flag
Dashboard web → Pegar `ff2472c6-e310-5d83-8ead-44f4a9deb63f` → SUBMIT

### Paso 5: ¡Completado!
```
✅ ¡Correcto! Reto completado (+10 pts)
```

---

## 🔐 Sobre las FLAGS Personalizadas

- Cada estudiante tiene flags únicas generadas con su documento
- Formato: UUID (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
- No puedes copiar flags de otros estudiantes
- Las flags se generan al configurar el sistema con: `python3 docker_challenge.py setup`

---

## ❓ Preguntas Frecuentes

### ¿Por qué no veo las flags en el dashboard?
Por diseño de seguridad. Las flags solo aparecen en la CLI después de completar el reto en Docker.

### ¿Puedo ver todas las flags de una vez?
Sí, ejecuta: `python3 docker_challenge.py start`

### ¿Las flags caducan?
No, tus flags son permanentes y únicas para ti.

### ¿Qué pasa si pierdo una flag?
Ejecuta `python3 docker_challenge.py start` nuevamente y verás todas las flags.

### ¿Puedo enviar una flag varias veces?
No, una vez completado un reto, no puedes reenviarlo.

---

## 🎯 Resumen Visual

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO DE FLAGS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Dashboard Web (localhost:5000)                             │
│     └─> Ver reto (SIN flag visible)                            │
│                                                                 │
│  2. Terminal - Docker                                          │
│     └─> Completar reto: docker run hello-world                 │
│                                                                 │
│  3. Terminal - CLI                                             │
│     └─> Ver flag: python3 docker_challenge.py start            │
│         ✅ 🚩 Flag: d959efcd-82dc-57ee-bdfe-58b0768ff55e       │
│                                                                 │
│  4. Dashboard Web                                              │
│     └─> Submit flag → ✅ Completado (+10 pts)                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Documentación Adicional

- `README.md` - Documentación principal
- `TALLER.md` - Guía del taller
- `USO_SISTEMA.md` - Manual de uso del sistema
- `GUIA_PROFESOR.md` - Guía para profesores

---

**¡Buena suerte con los retos! 🐳🚀**
