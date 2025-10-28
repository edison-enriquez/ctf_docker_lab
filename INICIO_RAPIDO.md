# 🚀 INICIO RÁPIDO - Docker CTF Lab

## Para Estudiantes

### En GitHub Codespaces (Recomendado)

1. **Fork** este repositorio a tu cuenta
2. Click en **Code** → **Codespaces** → **Create codespace**
3. Espera que termine la configuración automática (1-2 min)
4. Ejecuta:
   ```bash
   ./start.sh
   ```
5. Sigue las instrucciones para configurar tu documento
6. ¡Comienza a resolver retos!

### Instalación Local

```bash
# Clonar
git clone https://github.com/TU_USUARIO/ctf_docker_lab.git
cd ctf_docker_lab

# Instalar dependencias
pip install -r requirements.txt

# Verificar sistema
python3 verify_system.py

# Configurar
python3 docker_challenge.py setup

# Iniciar dashboard
python3 web_dashboard.py
```

Accede a: **http://localhost:5000**

## Comandos Principales

```bash
# Ver retos disponibles
python3 docker_challenge.py start

# Ver tu progreso
python3 docker_challenge.py status

# Ver pista de un reto
python3 docker_challenge.py hint 1

# Enviar una flag
python3 docker_challenge.py submit FLAG{tu_flag_aqui}

# Limpiar contenedores de prueba
python3 docker_challenge.py cleanup
```

## ¿Necesitas Ayuda?

- 📖 Lee [TALLER.md](TALLER.md) para write-ups completos
- 💡 Usa el botón "Ver Pista" en el dashboard
- 🐛 [Reporta issues](https://github.com/edison-enriquez/ctf_docker_lab/issues)

## Estructura de Retos

- **Principiante** (1-3): Comandos básicos
- **Intermedio** (4-6, 14-15): Redes, volúmenes
- **Avanzado** (7-9, 12): Arquitectura, servicios
- **Experto** (10-11, 13): SCADA, VNC, Compose

**Total**: 15 retos | 380 puntos

---

**¡Buena suerte! 🐳**
