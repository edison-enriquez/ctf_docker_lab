-- ============================================================================
-- Docker CTF Lab - Monitor Database Schema
-- Base de datos para seguimiento de estudiantes en tiempo real
-- ============================================================================

-- Extensiones
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- Tabla: estudiantes
-- Registro de todos los estudiantes que han conectado al sistema
-- ============================================================================
CREATE TABLE IF NOT EXISTS estudiantes (
    id SERIAL PRIMARY KEY,
    documento VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(200),
    email VARCHAR(200),
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'offline', -- online, offline, idle
    total_puntos INTEGER DEFAULT 0,
    total_retos_completados INTEGER DEFAULT 0,
    porcentaje_completado DECIMAL(5,2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para estudiantes
CREATE INDEX idx_estudiantes_documento ON estudiantes(documento);
CREATE INDEX idx_estudiantes_status ON estudiantes(status);
CREATE INDEX idx_estudiantes_last_seen ON estudiantes(last_seen);

-- ============================================================================
-- Tabla: retos
-- Catálogo de todos los retos disponibles
-- ============================================================================
CREATE TABLE IF NOT EXISTS retos (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(100),
    dificultad VARCHAR(50),
    puntos INTEGER DEFAULT 0,
    orden INTEGER,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Tabla: retos_completados
-- Registro de retos completados por cada estudiante
-- ============================================================================
CREATE TABLE IF NOT EXISTS retos_completados (
    id SERIAL PRIMARY KEY,
    estudiante_id INTEGER REFERENCES estudiantes(id) ON DELETE CASCADE,
    documento VARCHAR(50) NOT NULL,
    reto_id INTEGER REFERENCES retos(id) ON DELETE CASCADE,
    reto_nombre VARCHAR(200),
    puntos_ganados INTEGER DEFAULT 0,
    flag_submitted VARCHAR(500),
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tiempo_resolucion INTERVAL, -- Tiempo desde first_seen hasta completar
    
    UNIQUE(estudiante_id, reto_id)
);

-- Índices para retos_completados
CREATE INDEX idx_retos_completados_estudiante ON retos_completados(estudiante_id);
CREATE INDEX idx_retos_completados_documento ON retos_completados(documento);
CREATE INDEX idx_retos_completados_reto ON retos_completados(reto_id);
CREATE INDEX idx_retos_completados_fecha ON retos_completados(completed_at);

-- ============================================================================
-- Tabla: eventos_mqtt
-- Log de todos los eventos MQTT recibidos
-- ============================================================================
CREATE TABLE IF NOT EXISTS eventos_mqtt (
    id SERIAL PRIMARY KEY,
    estudiante_id INTEGER REFERENCES estudiantes(id) ON DELETE CASCADE,
    documento VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL, -- heartbeat, progress, flag_submit
    payload JSONB,
    topic VARCHAR(200),
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para eventos_mqtt
CREATE INDEX idx_eventos_mqtt_estudiante ON eventos_mqtt(estudiante_id);
CREATE INDEX idx_eventos_mqtt_documento ON eventos_mqtt(documento);
CREATE INDEX idx_eventos_mqtt_type ON eventos_mqtt(event_type);
CREATE INDEX idx_eventos_mqtt_fecha ON eventos_mqtt(received_at);
CREATE INDEX idx_eventos_mqtt_payload ON eventos_mqtt USING GIN (payload);

-- ============================================================================
-- Tabla: sesiones
-- Registro de sesiones de trabajo de estudiantes
-- ============================================================================
CREATE TABLE IF NOT EXISTS sesiones (
    id SERIAL PRIMARY KEY,
    estudiante_id INTEGER REFERENCES estudiantes(id) ON DELETE CASCADE,
    documento VARCHAR(50) NOT NULL,
    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_end TIMESTAMP,
    duration INTERVAL,
    retos_completados_sesion INTEGER DEFAULT 0,
    puntos_ganados_sesion INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

-- Índices para sesiones
CREATE INDEX idx_sesiones_estudiante ON sesiones(estudiante_id);
CREATE INDEX idx_sesiones_activas ON sesiones(is_active) WHERE is_active = TRUE;

-- ============================================================================
-- Tabla: estadisticas_globales
-- Estadísticas agregadas del sistema
-- ============================================================================
CREATE TABLE IF NOT EXISTS estadisticas_globales (
    id SERIAL PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
    total_estudiantes INTEGER DEFAULT 0,
    estudiantes_activos INTEGER DEFAULT 0,
    total_retos_completados INTEGER DEFAULT 0,
    promedio_completados DECIMAL(5,2) DEFAULT 0.0,
    promedio_puntos DECIMAL(10,2) DEFAULT 0.0,
    reto_mas_dificil INTEGER, -- reto_id con menos completados
    reto_mas_facil INTEGER, -- reto_id con más completados
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(fecha)
);

-- ============================================================================
-- Función: Actualizar timestamp de updated_at
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para estudiantes
CREATE TRIGGER update_estudiantes_updated_at
    BEFORE UPDATE ON estudiantes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Función: Calcular tiempo de resolución
-- ============================================================================
CREATE OR REPLACE FUNCTION calculate_resolution_time()
RETURNS TRIGGER AS $$
BEGIN
    -- Calcular tiempo desde que el estudiante se registró hasta completar el reto
    SELECT CURRENT_TIMESTAMP - e.first_seen INTO NEW.tiempo_resolucion
    FROM estudiantes e
    WHERE e.documento = NEW.documento;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para calcular tiempo
CREATE TRIGGER calculate_reto_resolution_time
    BEFORE INSERT ON retos_completados
    FOR EACH ROW
    EXECUTE FUNCTION calculate_resolution_time();

-- ============================================================================
-- Vista: Leaderboard en tiempo real
-- ============================================================================
CREATE OR REPLACE VIEW v_leaderboard AS
SELECT 
    e.documento,
    e.nombre,
    e.total_puntos,
    e.total_retos_completados,
    e.porcentaje_completado,
    e.last_seen,
    e.status,
    RANK() OVER (ORDER BY e.total_puntos DESC, e.total_retos_completados DESC) as ranking,
    COUNT(rc.id) as badges_earned
FROM estudiantes e
LEFT JOIN retos_completados rc ON e.id = rc.estudiante_id
GROUP BY e.id, e.documento, e.nombre, e.total_puntos, e.total_retos_completados, e.porcentaje_completado, e.last_seen, e.status
ORDER BY e.total_puntos DESC, e.total_retos_completados DESC;

-- ============================================================================
-- Vista: Progreso por reto
-- ============================================================================
CREATE OR REPLACE VIEW v_progreso_por_reto AS
SELECT 
    r.id as reto_id,
    r.nombre,
    r.categoria,
    r.dificultad,
    r.puntos,
    COUNT(rc.id) as veces_completado,
    COUNT(DISTINCT rc.estudiante_id) as estudiantes_unicos,
    ROUND(AVG(EXTRACT(EPOCH FROM rc.tiempo_resolucion) / 60), 2) as tiempo_promedio_minutos,
    MIN(rc.completed_at) as primera_completado,
    MAX(rc.completed_at) as ultima_completado
FROM retos r
LEFT JOIN retos_completados rc ON r.id = rc.reto_id
GROUP BY r.id, r.nombre, r.categoria, r.dificultad, r.puntos
ORDER BY r.id;

-- ============================================================================
-- Vista: Actividad reciente
-- ============================================================================
CREATE OR REPLACE VIEW v_actividad_reciente AS
SELECT 
    e.documento,
    e.nombre,
    em.event_type,
    em.payload,
    em.received_at,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - em.received_at)) as segundos_atras
FROM eventos_mqtt em
JOIN estudiantes e ON em.estudiante_id = e.id
ORDER BY em.received_at DESC
LIMIT 100;

-- ============================================================================
-- Insertar retos por defecto (los 15 del sistema)
-- ============================================================================
INSERT INTO retos (id, nombre, descripcion, categoria, dificultad, puntos, orden) VALUES
(1, '🐳 Primer Contenedor', 'Ejecuta tu primer contenedor usando la imagen hello-world', 'Comandos Básicos', 'Principiante', 10, 1),
(2, '🔍 Inspector de Imágenes', 'Descarga la imagen nginx:alpine y encuentra su tamaño', 'Imágenes', 'Principiante', 10, 2),
(3, '🚀 Contenedor en Background', 'Ejecuta un contenedor nginx en modo detached con nombre webserver', 'Ejecución', 'Principiante', 15, 3),
(4, '🔌 Mapeo de Puertos', 'Ejecuta nginx mapeando puerto 8080 del host al 80 del contenedor', 'Redes', 'Intermedio', 15, 4),
(5, '📦 Contenedor con Nombre', 'Ejecuta un contenedor Alpine Linux con nombre específico', 'Comandos Básicos', 'Principiante', 15, 5),
(6, '🔗 Red Personalizada', 'Crea una red bridge y conecta dos contenedores', 'Redes', 'Intermedio', 20, 6),
(7, '💾 Volúmenes Persistentes', 'Crea un volumen y monta datos persistentes', 'Volúmenes', 'Intermedio', 20, 7),
(8, '🔐 Acceso SSH', 'Despliega contenedor con servidor SSH y conéctate', 'Servicios', 'Intermedio', 25, 8),
(9, '📡 Servidor Telnet', 'Configura servidor Telnet en contenedor Alpine', 'Servicios', 'Avanzado', 25, 9),
(10, '🏭 SCADA Simulation', 'Despliega sistema SCADA simulado con Modbus', 'SCADA', 'Avanzado', 30, 10),
(11, '🖥️ VNC Desktop', 'Ejecuta escritorio gráfico accesible por VNC', 'Servicios', 'Avanzado', 30, 11),
(12, '🐋 Docker Compose Básico', 'Orquesta múltiples contenedores con Docker Compose', 'Orquestación', 'Experto', 35, 12),
(13, '🌐 Stack Web Completo', 'Despliega aplicación web completa (frontend + backend + DB)', 'Orquestación', 'Experto', 40, 13),
(14, '🔄 Multi-Container Network', 'Crea red compleja con múltiples contenedores interconectados', 'Redes', 'Experto', 40, 14),
(15, '🏆 Desafío Final', 'Combina todos los conocimientos en un despliegue completo', 'Challenge', 'Experto', 45, 15)
ON CONFLICT (id) DO NOTHING;

-- ============================================================================
-- Comentarios en tablas
-- ============================================================================
COMMENT ON TABLE estudiantes IS 'Registro de todos los estudiantes del CTF Lab';
COMMENT ON TABLE retos IS 'Catálogo de retos disponibles en el sistema';
COMMENT ON TABLE retos_completados IS 'Historial de retos completados por estudiantes';
COMMENT ON TABLE eventos_mqtt IS 'Log completo de eventos MQTT recibidos';
COMMENT ON TABLE sesiones IS 'Sesiones de trabajo de estudiantes';
COMMENT ON TABLE estadisticas_globales IS 'Estadísticas agregadas del sistema';

-- ============================================================================
-- Datos iniciales de prueba (opcional, comentar en producción)
-- ============================================================================
-- INSERT INTO estudiantes (documento, nombre, email, status) VALUES
-- ('1111111111', 'Estudiante Demo 1', 'demo1@example.com', 'online'),
-- ('2222222222', 'Estudiante Demo 2', 'demo2@example.com', 'online'),
-- ('3333333333', 'Estudiante Demo 3', 'demo3@example.com', 'offline');

-- ============================================================================
-- Permisos
-- ============================================================================
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO monitor_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO monitor_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO monitor_user;

-- ============================================================================
-- Fin del script de inicialización
-- ============================================================================
