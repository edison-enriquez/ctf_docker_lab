# 🐳 Taller Docker CTF Lab - Write-ups y Soluciones

> **Guía completa de resolución de todos los retos del Docker CTF Lab**

## 📖 Índice

- [Introducción](#introducción)
- [Configuración Inicial](#configuración-inicial)
- [Nivel Principiante](#nivel-principiante)
- [Nivel Intermedio](#nivel-intermedio)
- [Nivel Avanzado](#nivel-avanzado)
- [Nivel Experto](#nivel-experto)
- [Tips y Trucos](#tips-y-trucos)

## Introducción

Este taller te guiará paso a paso en la resolución de los 15 retos de Docker CTF Lab. Cada reto incluye:

- 📝 Descripción detallada
- 💡 Pistas y conceptos clave
- 🔧 Comandos específicos
- ✅ Verificación de la solución
- 🚩 Obtención de la flag

## Configuración Inicial

### Paso 1: Acceso al Laboratorio

```bash
# Opción A: En Codespaces (automático)
./start.sh

# Opción B: Local
python3 docker_challenge.py setup
```

### Paso 2: Registro de Documento

Ingresa tu documento de identidad cuando se solicite. Este documento se usará para generar tus flags personalizadas.

```
👤 Ingresa tu documento de identidad: 1234567890
✅ Código registrado: 1234567890
¿Es correcto? (s/n): s
```

⚠️ **IMPORTANTE**: Anota tu documento. Lo necesitarás si reconfiguras.

### Paso 3: Iniciar Dashboard

```bash
python3 web_dashboard.py
```

Accede a: http://localhost:5000

---

## Nivel Principiante

### Reto 1: 🐳 Primer Contenedor (10 pts)

**Objetivo**: Ejecutar tu primer contenedor usando la imagen 'hello-world'

**Conceptos**:
- `docker run`: Ejecuta un contenedor
- Imágenes vs Contenedores
- Ciclo de vida básico

**Solución**:

```bash
# Ejecutar hello-world
docker run hello-world
```

**¿Qué sucede?**
1. Docker busca la imagen `hello-world` localmente
2. Si no existe, la descarga de Docker Hub
3. Crea un contenedor a partir de la imagen
4. Ejecuta el comando predeterminado
5. El contenedor se detiene automáticamente

**Verificación**:

```bash
# Ver contenedores (incluso los detenidos)
docker ps -a

# Deberías ver hello-world en la lista
CONTAINER ID   IMAGE         COMMAND    STATUS
abc123         hello-world   "/hello"   Exited (0)
```

**Obtener la flag**:

Ve al dashboard o ejecuta:
```bash
python3 docker_challenge.py start
```

Tu flag personalizada será: `FLAG{primer_contenedor_TU_HASH}`

---

### Reto 2: 🔍 Inspector de Imágenes (10 pts)

**Objetivo**: Descargar la imagen 'nginx:alpine' y verificar su tamaño

**Conceptos**:
- `docker pull`: Descargar imágenes
- `docker images`: Listar imágenes locales
- Tags de imágenes

**Solución**:

```bash
# Descargar nginx:alpine
docker pull nginx:alpine

# Listar imágenes
docker images

# O filtrar por nombre
docker images nginx
```

**Salida esperada**:
```
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
nginx        alpine    abc123def      2 weeks ago   23.5MB
```

**¿Por qué Alpine?**
- Distribución Linux minimalista
- Tamaño reducido (< 5 MB base)
- Ideal para contenedores

**Flag**: `FLAG{imagen_descargada_TU_HASH}`

---

### Reto 3: 🚀 Contenedor en Background (15 pts)

**Objetivo**: Ejecutar nginx en modo detached con nombre 'webserver'

**Conceptos**:
- `-d` o `--detach`: Ejecutar en background
- `--name`: Asignar nombre al contenedor
- `docker ps`: Ver contenedores en ejecución

**Solución**:

```bash
# Ejecutar nginx en background
docker run -d --name webserver nginx:alpine

# Verificar que está corriendo
docker ps
```

**Salida**:
```
CONTAINER ID   IMAGE          COMMAND                  STATUS
abc123         nginx:alpine   "/docker-entrypoint.…"   Up 5 seconds
```

**Comandos útiles**:

```bash
# Ver logs del contenedor
docker logs webserver

# Detener el contenedor
docker stop webserver

# Iniciarlo de nuevo
docker start webserver

# Eliminar el contenedor (debe estar detenido)
docker rm webserver
```

**Flag**: `FLAG{contenedor_background_TU_HASH}`

---

## Nivel Intermedio

### Reto 4: 🔌 Mapeo de Puertos (15 pts)

**Objetivo**: Ejecutar nginx mapeando puerto 8080 del host al 80 del contenedor

**Conceptos**:
- `-p` o `--publish`: Mapear puertos HOST:CONTAINER
- Redes de Docker
- Acceso desde el navegador

**Solución**:

```bash
# Mapear puerto 8080 -> 80
docker run -d -p 8080:80 --name webserver-port nginx:alpine

# Verificar mapeo
docker ps
```

**Salida**:
```
PORTS
0.0.0.0:8080->80/tcp
```

**Probar**:

```bash
# Desde el terminal
curl http://localhost:8080

# O abre en navegador
# http://localhost:8080
```

Deberías ver la página de bienvenida de nginx.

**Múltiples puertos**:
```bash
# Ejemplo con varios puertos
docker run -d -p 8080:80 -p 8443:443 --name web nginx:alpine
```

**Flag**: `FLAG{puerto_mapeado_TU_HASH}`

---

### Reto 5: 💾 Volúmenes Persistentes (20 pts)

**Objetivo**: Crear un volumen llamado 'datos_importantes' y usarlo

**Conceptos**:
- Persistencia de datos
- `docker volume`: Gestión de volúmenes
- Montaje de volúmenes con `-v`

**Solución**:

```bash
# Crear volumen
docker volume create datos_importantes

# Listar volúmenes
docker volume ls

# Usar el volumen en un contenedor
docker run -d \
  -v datos_importantes:/data \
  --name contenedor-persistente \
  alpine sleep 3600

# Verificar
docker inspect contenedor-persistente
```

**Escribir datos en el volumen**:

```bash
# Ejecutar comando en el contenedor
docker exec contenedor-persistente sh -c "echo 'Datos persistentes' > /data/archivo.txt"

# Leer datos
docker exec contenedor-persistente cat /data/archivo.txt
```

**Los datos persisten**:

```bash
# Eliminar contenedor
docker rm -f contenedor-persistente

# Crear nuevo contenedor con mismo volumen
docker run -d \
  -v datos_importantes:/data \
  --name nuevo-contenedor \
  alpine sleep 3600

# Los datos siguen ahí
docker exec nuevo-contenedor cat /data/archivo.txt
```

**Gestión de volúmenes**:

```bash
# Inspeccionar volumen
docker volume inspect datos_importantes

# Eliminar volumen (sin contenedores usándolo)
docker volume rm datos_importantes

# Limpiar volúmenes no usados
docker volume prune
```

**Flag**: `FLAG{volumen_creado_TU_HASH}`

---

### Reto 6: 🌐 Red Personalizada (20 pts)

**Objetivo**: Crear una red bridge personalizada llamada 'mi_red_ctf'

**Conceptos**:
- Redes Docker: bridge, host, none
- `docker network`: Gestión de redes
- Aislamiento de contenedores

**Solución**:

```bash
# Crear red bridge
docker network create --driver bridge mi_red_ctf

# Listar redes
docker network ls
```

**Salida**:
```
NETWORK ID     NAME         DRIVER    SCOPE
abc123         mi_red_ctf   bridge    local
```

**Inspeccionar red**:

```bash
docker network inspect mi_red_ctf
```

**Diferencias entre redes**:

| Red | Descripción | Uso |
|-----|-------------|-----|
| bridge | Red aislada por defecto | Contenedores en mismo host |
| host | Usa la red del host | Alto rendimiento, sin aislamiento |
| none | Sin red | Contenedor completamente aislado |

**Flag**: `FLAG{red_creada_TU_HASH}`

---

### Reto 14: 🔍 Inspección Avanzada (25 pts)

**Objetivo**: Inspeccionar un contenedor y encontrar su IP interna

**Solución**:

```bash
# Crear un contenedor si no existe
docker run -d --name test-inspect nginx:alpine

# Inspeccionar y filtrar IP
docker inspect test-inspect | grep IPAddress

# O más específico
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' test-inspect
```

**Información útil de inspect**:

```bash
# Ver todas las variables de entorno
docker inspect -f '{{.Config.Env}}' test-inspect

# Ver puertos mapeados
docker inspect -f '{{.NetworkSettings.Ports}}' test-inspect

# Ver volúmenes montados
docker inspect -f '{{.Mounts}}' test-inspect
```

**Flag**: `FLAG{inspeccion_exitosa_TU_HASH}`

---

## Nivel Avanzado

### Reto 7: 🔗 Conectando Contenedores (25 pts)

**Objetivo**: Crear dos contenedores alpine en 'mi_red_ctf' que puedan comunicarse

**Conceptos**:
- Comunicación entre contenedores
- DNS automático en redes custom
- Comando `ping`

**Solución**:

```bash
# Asegúrate que la red existe (del reto 6)
docker network create mi_red_ctf 2>/dev/null || true

# Crear primer contenedor
docker run -dit \
  --name contenedor1 \
  --network mi_red_ctf \
  alpine sh

# Crear segundo contenedor
docker run -dit \
  --name contenedor2 \
  --network mi_red_ctf \
  alpine sh

# Verificar conexión
docker ps | grep contenedor
```

**Probar conectividad**:

```bash
# Desde contenedor1 hacer ping a contenedor2
docker exec contenedor1 ping -c 3 contenedor2

# Debería funcionar usando el NOMBRE
PING contenedor2 (172.18.0.3): 56 data bytes
64 bytes from 172.18.0.3: seq=0 ttl=64 time=0.123 ms
```

**¿Por qué funciona?**
- Docker proporciona DNS interno
- Los contenedores se pueden alcanzar por nombre
- Solo funciona en redes custom (no en bridge default)

**Instalarpaquetes en Alpine**:

```bash
# Si necesitas herramientas adicionales
docker exec contenedor1 apk add curl
docker exec contenedor1 curl http://contenedor2
```

**Flag**: `FLAG{contenedores_conectados_TU_HASH}`

---

### Reto 8: 🔐 SSH en Contenedor (30 pts)

**Objetivo**: Desplegar un contenedor con SSH en puerto 2222

**Conceptos**:
- Servicios en contenedores
- Configuración de SSH
- Seguridad básica

**Solución Opción 1: Imagen pre-construida**

```bash
# Usar linuxserver/openssh-server
docker run -d \
  --name ssh-server \
  -p 2222:2222 \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=America/Guayaquil \
  -e USER_NAME=ctfuser \
  -e USER_PASSWORD=ctfpassword \
  linuxserver/openssh-server

# Verificar
docker logs ssh-server
```

**Conectar**:

```bash
# Desde otro terminal
ssh ctfuser@localhost -p 2222
# Password: ctfpassword
```

**Solución Opción 2: Dockerfile personalizado**

Crea `Dockerfile`:

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd && \
    echo 'root:password' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
```

```bash
# Construir
docker build -t ssh-custom .

# Ejecutar
docker run -d -p 2222:22 --name ssh-server ssh-custom
```

**Flag**: `FLAG{ssh_configurado_TU_HASH}`

---

### Reto 9: 📡 Telnet Antiguo (30 pts)

**Objetivo**: Desplegar contenedor con Telnet en puerto 2323

**Conceptos**:
- Protocolos legacy
- Telnetd
- Configuración de servicios

**Solución**:

Crea `Dockerfile-telnet`:

```dockerfile
FROM alpine:latest

RUN apk add --no-cache busybox-extras

EXPOSE 23

CMD ["telnetd", "-F", "-p", "23"]
```

```bash
# Construir imagen
docker build -f Dockerfile-telnet -t telnet-server .

# Ejecutar en puerto 2323
docker run -d -p 2323:23 --name telnet-server telnet-server

# Verificar
docker ps | grep telnet
```

**Probar conexión**:

```bash
# Instalar telnet client si no lo tienes
# Ubuntu: sudo apt install telnet
# Mac: brew install telnet

telnet localhost 2323
```

**⚠️ Seguridad**:
- Telnet NO es seguro (texto plano)
- Solo para laboratorios/educación
- En producción usar SSH

**Flag**: `FLAG{telnet_activo_TU_HASH}`

---

### Reto 12: 🏗️ Dockerfile Personalizado (30 pts)

**Objetivo**: Crear Dockerfile con Python y Flask, construir como 'mi-app:v1'

**Conceptos**:
- Creación de imágenes personalizadas
- Multi-stage builds (opcional)
- Optimización de capas

**Solución**:

Crea `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Metadata
LABEL maintainer="tu@email.com"
LABEL description="App Flask para CTF Docker"

# Directorio de trabajo
WORKDIR /app

# Instalar Flask
RUN pip install --no-cache-dir flask

# Copiar código (si tienes app.py)
# COPY app.py .

# Puerto
EXPOSE 5000

# Comando por defecto
CMD ["python", "-c", "print('Flask instalado correctamente')"]
```

**Construir imagen**:

```bash
# Construir con tag
docker build -t mi-app:v1 .

# Verificar
docker images | grep mi-app
```

**Ejecutar**:

```bash
# Probar la imagen
docker run --rm mi-app:v1

# Salida: Flask instalado correctamente
```

**Ejemplo app.py**:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '🐳 Docker CTF Lab App!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Con app.py**:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
RUN pip install flask
EXPOSE 5000
CMD ["python", "app.py"]
```

```bash
docker build -t mi-app:v1 .
docker run -d -p 5000:5000 mi-app:v1
curl http://localhost:5000
```

**Flag**: `FLAG{dockerfile_creado_TU_HASH}`

---

## Nivel Experto

### Reto 10: 🏭 SCADA Industrial (35 pts)

**Objetivo**: Desplegar OpenPLC o sistema SCADA en puerto 8000

**Conceptos**:
- Sistemas de control industrial (ICS)
- SCADA en contenedores
- Seguridad OT

**Solución**:

```bash
# Opción 1: OpenPLC (recomendado)
docker run -d \
  -p 8000:8080 \
  --name scada-server \
  openplc/openplc:latest

# Opción 2: ScadaBR (alternativa)
docker run -d \
  -p 8000:8080 \
  --name scadabr \
  iegomez/scadabr
```

**Acceder a OpenPLC**:

1. Abre navegador: http://localhost:8000
2. Credenciales por defecto:
   - Usuario: `openplc`
   - Contraseña: `openplc`

**Características de OpenPLC**:
- PLC (Controlador Lógico Programable) open source
- Soporta IEC 61131-3
- Modbus, DNP3, EtherNet/IP
- Simulación de procesos industriales

**Casos de uso**:
- Automatización industrial
- Control de procesos
- Domótica
- Educación en OT/ICS

**Flag**: `FLAG{scada_desplegado_TU_HASH}`

---

### Reto 11: 🖥️ Escritorio Remoto VNC (35 pts)

**Objetivo**: Desplegar escritorio gráfico accesible por VNC en puerto 5900

**Conceptos**:
- VNC (Virtual Network Computing)
- Escritorios remotos en contenedores
- noVNC para acceso web

**Solución**:

```bash
# Ubuntu Desktop con LXDE y VNC
docker run -d \
  -p 6080:80 \
  -p 5900:5900 \
  -e VNC_PASSWORD=password \
  --name vnc-desktop \
  dorowu/ubuntu-desktop-lxde-vnc
```

**Espera que se inicie** (1-2 minutos):

```bash
# Ver logs
docker logs -f vnc-desktop

# Cuando veas "Ready", está listo
```

**Acceder**:

**Opción A: Navegador (noVNC)**
- URL: http://localhost:6080
- Click en "Connect"
- Password: `password`

**Opción B: Cliente VNC**
- Instala VNC Viewer
- Conecta a: `localhost:5900`
- Password: `password`

**Qué puedes hacer**:
- Navegar con Firefox incluido
- Abrir terminal
- Instalar software con apt
- Editar archivos gráficamente

**Personalización**:

```bash
# Con resolución específica
docker run -d \
  -p 6080:80 \
  -p 5900:5900 \
  -e RESOLUTION=1920x1080 \
  -e VNC_PASSWORD=mipassword \
  --name vnc-desktop \
  dorowu/ubuntu-desktop-lxde-vnc
```

**Flag**: `FLAG{vnc_funcionando_TU_HASH}`

---

### Reto 13: 📦 Docker Compose Multi-Servicio (40 pts)

**Objetivo**: Crear docker-compose.yml con nginx y redis, levantarlos

**Conceptos**:
- Docker Compose
- Orquestación de servicios
- Redes automáticas
- Dependencias entre servicios

**Solución**:

Crea `docker-compose.yml`:

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    container_name: compose-nginx
    ports:
      - "8080:80"
    networks:
      - app-network
    depends_on:
      - redis

  redis:
    image: redis:alpine
    container_name: compose-redis
    networks:
      - app-network
    volumes:
      - redis-data:/data

networks:
  app-network:
    driver: bridge

volumes:
  redis-data:
```

**Levantar servicios**:

```bash
# Iniciar en background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Ver servicios corriendo
docker-compose ps
```

**Verificar**:

```bash
# Nginx debería responder
curl http://localhost:8080

# Redis debería estar corriendo
docker exec compose-redis redis-cli ping
# Respuesta: PONG
```

**Comandos útiles**:

```bash
# Detener servicios
docker-compose stop

# Detener y eliminar
docker-compose down

# Detener y eliminar con volúmenes
docker-compose down -v

# Ver logs de servicio específico
docker-compose logs nginx

# Escalar servicios
docker-compose up -d --scale nginx=3
```

**Compose avanzado con app**:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis
    networks:
      - backend

  redis:
    image: redis:alpine
    networks:
      - backend
    volumes:
      - redis-data:/data

networks:
  backend:

volumes:
  redis-data:
```

**Flag**: `FLAG{compose_desplegado_TU_HASH}`

---

### Reto 15: 🧹 Limpieza Maestra (20 pts)

**Objetivo**: Limpiar contenedores detenidos, imágenes sin usar y volúmenes

**Conceptos**:
- Mantenimiento del sistema Docker
- Liberación de espacio
- Buenas prácticas

**Solución**:

```bash
# ⚠️ CUIDADO: Esto elimina TODOS los recursos no usados

# Ver espacio usado
docker system df

# Limpiar todo (contenedores, imágenes, redes, volúmenes)
docker system prune -a --volumes

# Confirma con 'y'
```

**Limpieza selectiva**:

```bash
# Solo contenedores detenidos
docker container prune

# Solo imágenes sin tag
docker image prune

# Solo imágenes no usadas
docker image prune -a

# Solo volúmenes no usados
docker volume prune

# Solo redes no usadas
docker network prune
```

**Ver espacio liberado**:

```bash
# Antes
docker system df

# Después de limpiar
docker system df
```

**Automatización**:

```bash
# Cron job para limpieza semanal (Linux)
0 2 * * 0 docker system prune -f
```

**Flag**: `FLAG{limpieza_completa_TU_HASH}`

---

## Tips y Trucos

### Comandos Docker Esenciales

```bash
# Ver ayuda de cualquier comando
docker <comando> --help

# Logs en tiempo real
docker logs -f <contenedor>

# Ejecutar comando en contenedor
docker exec -it <contenedor> sh

# Copiar archivos
docker cp archivo.txt contenedor:/ruta/
docker cp contenedor:/ruta/archivo.txt .

# Estadísticas en tiempo real
docker stats

# Ver procesos dentro de contenedor
docker top <contenedor>
```

### Debugging

```bash
# Inspeccionar todo
docker inspect <contenedor/imagen/red/volumen>

# Ver diferencias en filesystem
docker diff <contenedor>

# Eventos en tiempo real
docker events

# Ver qué construyó la imagen
docker history <imagen>
```

### Productividad

```bash
# Aliases útiles
alias dps='docker ps'
alias dpsa='docker ps -a'
alias di='docker images'
alias dex='docker exec -it'

# Limpiar rápido
alias dclean='docker system prune -f'

# Ver último contenedor creado
docker ps -l
```

### Troubleshooting Común

**Puerto ya en uso**:
```bash
# Encontrar qué usa el puerto
lsof -i :8080

# Usar otro puerto
docker run -p 8081:80 nginx
```

**Contenedor no inicia**:
```bash
# Ver logs
docker logs <contenedor>

# Ejecutar comando manual
docker run -it <imagen> sh
```

**Espacio en disco lleno**:
```bash
# Ver uso
docker system df

# Limpiar
docker system prune -a --volumes
```

---

## Resumen de Flags

Al completar todos los retos, tendrás:

- ✅ 15 retos completados
- 🏆 380 puntos totales
- 🎓 Conocimiento completo de Docker
- 📜 Certificado virtual de maestría

## Próximos Pasos

Después de completar el CTF:

1. **Kubernetes**: Orquestación a escala
2. **Docker Swarm**: Clustering nativo
3. **CI/CD**: Integración con Jenkins/GitLab
4. **Seguridad**: Escaneo de vulnerabilidades
5. **Optimización**: Multi-stage builds, imágenes mínimas

---

**¡Felicitaciones por completar el Docker CTF Lab! 🐳🎉**

Comparte tu progreso con #DockerCTFLab
