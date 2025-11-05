FROM python:3.11-slim

# Metadatos
LABEL maintainer="Docker CTF Lab - Professor Monitor"
LABEL description="Monitor MQTT para seguimiento de estudiantes"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app.py db.py ./
COPY templates ./templates

# Crear usuario no-root
RUN useradd -m -u 1000 monitor && \
    chown -R monitor:monitor /app

USER monitor

# Exponer puerto
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Comando de inicio
CMD ["python", "app.py"]
