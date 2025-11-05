# 📦 Paquete de Deployment - Dashboard Profesor

## ✅ Contenido del Paquete

El archivo `deployment_profesor.tar.gz` contiene todo lo necesario para desplegar el dashboard de monitoreo del profesor en un servidor persistente.

### 📁 Estructura del Paquete (22 KB comprimido):

```
deployment_profesor/
├── README.md                    # Documentación completa (12 KB)
├── QUICKSTART.md                # Guía rápida de 5 minutos
├── deploy.sh                    # Script automático de deployment
├── backup.sh                    # Script de respaldo automático
├── docker-compose.yml           # Orquestación de servicios
├── Dockerfile                   # Imagen del monitor Flask
├── init.sql                     # Schema de PostgreSQL (12 KB)
├── app.py                       # Aplicación Flask (16 KB)
├── db.py                        # Manejador de base de datos (16 KB)
├── requirements.txt             # Dependencias Python
├── .env.example                 # Variables de entorno (plantilla)
└── templates/
    └── dashboard.html          # Dashboard del profesor
```

## 🎯 ¿Qué Incluye?

### Servicios Docker:
1. **PostgreSQL 15** - Base de datos con esquema pre-configurado
2. **Flask Monitor** - Dashboard web del profesor
3. **Adminer** - Gestor web de base de datos

### Scripts de Automatización:
- ✅ `deploy.sh` - Deployment automático con validaciones
- ✅ `backup.sh` - Respaldo automático de base de datos
- ✅ Logs y diagnósticos integrados

### Configuración Pre-integrada:
- ✅ Conexión al broker MQTT externo (cygnus.uniajc.edu.co)
- ✅ Autenticación MQTT configurada
- ✅ Schema de base de datos con 6 tablas y 3 vistas
- ✅ Dashboard responsive con métricas en tiempo real

## 🚀 Deployment en 3 Pasos

```bash
# 1. Descomprimir
tar -xzf deployment_profesor.tar.gz
cd deployment_profesor

# 2. Configurar
cp .env.example .env
nano .env  # Cambiar passwords

# 3. Desplegar
./deploy.sh
```

## 🌐 Acceso al Sistema

Después del deployment:
- **Dashboard Profesor**: `http://TU_SERVIDOR:5001`
- **Adminer (DB)**: `http://TU_SERVIDOR:8080`

## 📊 Características del Dashboard

### Métricas en Tiempo Real:
- 📈 Estudiantes activos
- 🎯 Retos completados por estudiante
- ⏱️ Tiempo promedio de solución
- 📊 Distribución de puntos
- 🔥 Estudiantes más activos
- 📉 Retos más difíciles

### Funcionalidades:
- ✅ Actualización automática cada 30 segundos
- ✅ Gráficos interactivos
- ✅ Exportación de datos
- ✅ Filtros por estudiante/reto
- ✅ Histórico completo

## 🔒 Seguridad

### Configuración Recomendada:
1. ✅ Passwords seguros en `.env`
2. ✅ Firewall configurado (puertos 5001, 8080)
3. ✅ Nginx como proxy reverso
4. ✅ SSL con Let's Encrypt
5. ✅ Backups automáticos programados

### Credenciales MQTT:
- Broker: `cygnus.uniajc.edu.co:1883`
- Usuario: `aiot`
- Password: `aiot123`
- Topic: `docker_ctf_lab/#`

## 📦 Requisitos del Servidor

### Mínimos:
- **SO**: Ubuntu 20.04+, Debian 11+, CentOS 8+
- **CPU**: 2 cores
- **RAM**: 2 GB
- **Disco**: 10 GB
- **Software**: Docker 20.10+, Docker Compose 2.0+

### Recomendados:
- **CPU**: 4 cores
- **RAM**: 4 GB
- **Disco**: 20 GB SSD
- **Red**: 100 Mbps

## 🔧 Mantenimiento

### Comandos Básicos:
```bash
# Ver logs en tiempo real
docker compose logs -f

# Reiniciar servicios
docker compose restart

# Backup manual
./backup.sh

# Ver estado
docker compose ps

# Actualizar
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Backup Automático:
```bash
# Agregar a crontab (diario a las 2 AM)
0 2 * * * cd /ruta/deployment_profesor && ./backup.sh
```

## 🆘 Troubleshooting

### Puerto ocupado:
```bash
# Cambiar puerto en .env
FLASK_PORT=5002
docker compose down && docker compose up -d
```

### No conecta MQTT:
```bash
# Ver logs
docker compose logs monitor_app | grep MQTT

# Verificar credenciales
cat .env | grep MQTT
```

### Base de datos no carga:
```bash
# Recrear desde cero
docker compose down -v
docker compose up -d
```

## 📚 Documentación

- **README.md** - Guía completa con todos los detalles
- **QUICKSTART.md** - Inicio rápido en 5 minutos
- Scripts comentados para fácil comprensión

## 🎓 Soporte

### Logs de Diagnóstico:
```bash
# Recopilar información para soporte
docker compose ps > diagnostico.txt
docker compose logs >> diagnostico.txt
docker system df >> diagnostico.txt
```

### Información del Sistema:
```bash
docker --version
docker compose version
free -h
df -h
```

## ✅ Checklist Post-Deployment

- [ ] Dashboard accesible en http://servidor:5001
- [ ] Adminer accesible en http://servidor:8080
- [ ] Logs muestran "MQTT conectado"
- [ ] Logs muestran "Base de datos conectada"
- [ ] PostgreSQL con datos de estudiantes
- [ ] Puertos abiertos en firewall
- [ ] Backup automático programado
- [ ] Nginx configurado (opcional)
- [ ] SSL activo (opcional)

## 📈 Escalabilidad

El sistema puede manejar:
- ✅ ~100 estudiantes simultáneos
- ✅ ~1000 eventos MQTT por minuto
- ✅ Base de datos hasta 1 GB
- ✅ Histórico de 6 meses

Para más estudiantes, aumentar recursos del servidor.

## 🔄 Actualización

Cuando salga una nueva versión:

```bash
# Descargar nueva versión
wget https://url/deployment_profesor_v2.1.tar.gz

# Hacer backup
./backup.sh

# Detener servicios
docker compose down

# Descomprimir nueva versión
tar -xzf deployment_profesor_v2.1.tar.gz

# Mantener .env existente
cp .env deployment_profesor/.env

# Redesplegar
cd deployment_profesor
./deploy.sh
```

## 📞 Contacto

Para soporte o consultas:
- GitHub Issues: https://github.com/edison-enriquez/ctf_docker_lab
- Documentación: Ver README.md en el paquete

---

## 🎉 Ventajas del Paquete

✅ **Todo incluido** - No necesita configuración adicional  
✅ **Scripts automáticos** - Deployment en minutos  
✅ **Documentación completa** - Guías paso a paso  
✅ **Pre-configurado** - MQTT, PostgreSQL, Flask listos  
✅ **Seguro** - Plantillas con mejores prácticas  
✅ **Portable** - Funciona en cualquier servidor con Docker  

---

**🐳 Docker CTF Lab - Dashboard Profesor v2.0**

*Paquete generado: 5 de noviembre de 2025*  
*Versión: 2.0.0*  
*Tamaño: 22 KB comprimido*
