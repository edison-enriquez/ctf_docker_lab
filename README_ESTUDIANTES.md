# 🐳 Docker CTF Lab - Estudiantes

## 🎯 Descripción

Laboratorio de Capture The Flag (CTF) para aprender Docker de forma práctica y gamificada. Incluye:

- ✅ 15 retos Docker progresivos (Principiante → Experto)
- ✅ Sistema de quiz educativo (30 preguntas)
- ✅ Flags personalizadas por estudiante (UUID-based)
- ✅ Dashboard web interactivo con tema hacker
- ✅ Sistema de puntos y progreso en tiempo real

---

## 🚀 Inicio Rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/edison-enriquez/ctf_docker_lab.git
cd ctf_docker_lab
```

### 2. Iniciar el sistema

```bash
./start.sh
```

Esto iniciará el dashboard web en: **http://localhost:5000**

### 3. Configurar tu documento

En el primer uso, el sistema te pedirá tu número de documento para generar tus flags personalizadas:

```bash
python3 docker_challenge.py setup
```

### 4. Completar retos

1. **Lee el reto** en el dashboard
2. **Ejecuta comandos Docker** en tu terminal
3. **Copia la flag** desde la tarjeta del reto
4. **Envía la flag** en el formulario del dashboard

---

## 📚 Documentación

- **[QUIZ_QUICKSTART.md](QUIZ_QUICKSTART.md)** - Guía rápida del sistema de quiz
- **[COMO_OBTENER_FLAGS.md](COMO_OBTENER_FLAGS.md)** - Cómo funcionan las flags
- **[SISTEMA_QUIZ.md](SISTEMA_QUIZ.md)** - Documentación completa del sistema educativo

---

## 🎮 Uso del Dashboard

### Completar un Reto

```bash
# Ejemplo: Reto 1 - Primer Contenedor
docker run hello-world
```

Luego en el dashboard:
1. Clic en **"Copiar y Usar Flag"** en la tarjeta del reto
2. La flag se pega automáticamente en el formulario
3. Clic en **"EXECUTE"**
4. ¡Reto completado! ✅

### Ver Todas tus Flags

1. Completa retos Docker
2. Clic en botón **"🚩 VER MIS FLAGS"**
3. Responde el quiz educativo (2 preguntas por reto)
4. Ver todas tus flags juntas

---

## 🛠️ Comandos Útiles

### Iniciar Dashboard Web

```bash
./start.sh
```

### Ver Progreso

```bash
python3 docker_challenge.py status
```

### Ver Retos y Flags (CLI)

```bash
python3 docker_challenge.py start
```

### Obtener Pista de un Reto

```bash
python3 docker_challenge.py hint <numero_reto>
```

### Enviar Flag (CLI)

```bash
python3 docker_challenge.py submit <flag>
```

### Limpiar Contenedores de Prueba

```bash
python3 docker_challenge.py cleanup
```

---

## 📊 Sistema de Puntos

| Dificultad | Puntos |
|------------|--------|
| Principiante | 10-15 pts |
| Intermedio | 20-25 pts |
| Avanzado | 30-35 pts |
| Experto | 35-40 pts |

**Total posible**: 395 puntos

---

## 🎯 Categorías de Retos

1. **Comandos Básicos** - docker run, pull, images
2. **Ejecución** - Modos detached, puertos, nombres
3. **Almacenamiento** - Volúmenes y persistencia
4. **Redes** - Conectividad entre contenedores
5. **Servicios** - SSH, Telnet, SCADA, VNC
6. **Construcción** - Dockerfile, imágenes personalizadas
7. **Orquestación** - Docker Compose
8. **Diagnóstico** - docker inspect
9. **Mantenimiento** - Limpieza de recursos

---

## 🔐 Seguridad

- Las flags son **únicas por estudiante** (generadas con UUID + tu documento)
- No puedes usar flags de otros estudiantes
- Las flags se generan en tiempo real al completar retos
- Sistema de validación server-side

---

## 🐛 Solución de Problemas

### El dashboard no inicia

```bash
# Verificar que el puerto 5000 esté libre
lsof -i :5000

# Si está ocupado, detener el proceso
pkill -f web_dashboard.py

# Reiniciar
./start.sh
```

### Docker no responde

```bash
# Verificar estado de Docker
docker ps

# Reiniciar Docker (si es necesario)
sudo systemctl restart docker
```

### Olvidé mi documento

```bash
# Ver tu documento configurado
python3 docker_challenge.py status
```

---

## 💡 Tips

1. **Lee las descripciones** de los retos con cuidado
2. **Usa las pistas** si te atascas (botón 💡 en cada tarjeta)
3. **Prueba comandos** antes de enviar flags
4. **Completa el quiz** para reforzar tu aprendizaje
5. **Consulta documentación** de Docker si es necesario

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa la documentación en `/docs`
2. Verifica logs en `/tmp/ctf_dashboard.log`
3. Consulta con tu profesor/instructor

---

## 🎉 ¡Buena Suerte!

**Aprende Docker, hackea contenedores, captura flags.** 🚩

¡Que la fuerza del contenedor te acompañe! 🐳✨

---

**Versión**: 2.0 con Sistema de Quiz Educativo
**Última actualización**: Noviembre 2025
