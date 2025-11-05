#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker CTF Lab - Monitor Database Module
Módulo para interactuar con PostgreSQL
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from datetime import datetime
from contextlib import contextmanager
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MonitorDB:
    """Clase para manejar la conexión y operaciones con PostgreSQL"""
    
    def __init__(self, database_url=None):
        """
        Inicializar conexión a base de datos
        
        Args:
            database_url: URL de conexión PostgreSQL
        """
        self.database_url = database_url or os.getenv(
            'DATABASE_URL',
            'postgresql://monitor_user:monitor_pass_2024@localhost:5432/ctf_monitor'
        )
        self._test_connection()
    
    def _test_connection(self):
        """Probar conexión a la base de datos"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT version();')
                    version = cur.fetchone()[0]
                    logger.info(f"✅ Conectado a PostgreSQL: {version.split(',')[0]}")
        except Exception as e:
            logger.error(f"❌ Error conectando a PostgreSQL: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Context manager para obtener conexión a BD"""
        conn = psycopg2.connect(self.database_url)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Error en transacción: {e}")
            raise
        finally:
            conn.close()
    
    # ========================================================================
    # ESTUDIANTES
    # ========================================================================
    
    def upsert_estudiante(self, documento, nombre=None, email=None, status='online'):
        """
        Crear o actualizar estudiante
        
        Args:
            documento: Número de documento del estudiante
            nombre: Nombre completo (opcional)
            email: Email (opcional)
            status: Estado (online, offline, idle)
        
        Returns:
            ID del estudiante
        """
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO estudiantes (documento, nombre, email, status, last_seen)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (documento) 
                    DO UPDATE SET
                        nombre = COALESCE(EXCLUDED.nombre, estudiantes.nombre),
                        email = COALESCE(EXCLUDED.email, estudiantes.email),
                        status = EXCLUDED.status,
                        last_seen = CURRENT_TIMESTAMP
                    RETURNING id;
                """, (documento, nombre, email, status))
                
                return cur.fetchone()[0]
    
    def get_estudiante(self, documento):
        """Obtener datos de un estudiante por documento"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM estudiantes WHERE documento = %s
                """, (documento,))
                
                return cur.fetchone()
    
    def get_all_estudiantes(self):
        """Obtener todos los estudiantes"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        e.*,
                        COUNT(rc.id) as retos_completados,
                        COALESCE(SUM(rc.puntos_ganados), 0) as puntos_totales,
                        EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - e.last_seen)) as segundos_inactivo
                    FROM estudiantes e
                    LEFT JOIN retos_completados rc ON e.id = rc.estudiante_id
                    GROUP BY e.id
                    ORDER BY puntos_totales DESC, retos_completados DESC
                """)
                
                return cur.fetchall()
    
    def update_estudiante_stats(self, documento, total_puntos, total_retos, porcentaje):
        """Actualizar estadísticas del estudiante"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE estudiantes
                    SET total_puntos = %s,
                        total_retos_completados = %s,
                        porcentaje_completado = %s,
                        last_seen = CURRENT_TIMESTAMP
                    WHERE documento = %s
                """, (total_puntos, total_retos, porcentaje, documento))
    
    def set_estudiante_status(self, documento, status):
        """Cambiar status de estudiante (online, offline, idle)"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE estudiantes
                    SET status = %s, last_seen = CURRENT_TIMESTAMP
                    WHERE documento = %s
                """, (status, documento))
    
    def delete_estudiante(self, documento):
        """
        Eliminar estudiante y todos sus registros relacionados
        
        Args:
            documento: Documento del estudiante a eliminar
            
        Returns:
            True si se eliminó, False si no existía
        """
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # Verificar si existe
                cur.execute("SELECT id FROM estudiantes WHERE documento = %s", (documento,))
                if not cur.fetchone():
                    return False
                
                # Eliminar (CASCADE eliminará retos_completados, eventos_mqtt, sesiones)
                cur.execute("DELETE FROM estudiantes WHERE documento = %s", (documento,))
                logger.info(f"🗑️  Estudiante {documento} eliminado de la base de datos")
                return True
    
    # ========================================================================
    # RETOS COMPLETADOS
    # ========================================================================
    
    def registrar_reto_completado(self, documento, reto_id, reto_nombre, puntos, flag=None):
        """
        Registrar reto completado por estudiante
        
        Args:
            documento: Documento del estudiante
            reto_id: ID del reto
            reto_nombre: Nombre del reto
            puntos: Puntos ganados
            flag: Flag enviada (opcional)
        
        Returns:
            ID del registro o None si ya existía
        """
        # Primero asegurar que el estudiante existe
        estudiante_id = self.upsert_estudiante(documento)
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO retos_completados 
                            (estudiante_id, documento, reto_id, reto_nombre, puntos_ganados, flag_submitted)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING id
                    """, (estudiante_id, documento, reto_id, reto_nombre, puntos, flag))
                    
                    return cur.fetchone()[0]
                except psycopg2.IntegrityError:
                    # Ya existe, ignorar
                    return None
    
    def get_retos_estudiante(self, documento):
        """Obtener todos los retos completados por un estudiante"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        rc.*,
                        r.nombre as reto_nombre_completo,
                        r.categoria,
                        r.dificultad
                    FROM retos_completados rc
                    JOIN estudiantes e ON rc.estudiante_id = e.id
                    LEFT JOIN retos r ON rc.reto_id = r.id
                    WHERE e.documento = %s
                    ORDER BY rc.completed_at DESC
                """, (documento,))
                
                return cur.fetchall()
    
    # ========================================================================
    # EVENTOS MQTT
    # ========================================================================
    
    def registrar_evento_mqtt(self, documento, event_type, payload, topic=None):
        """
        Registrar evento MQTT recibido
        
        Args:
            documento: Documento del estudiante
            event_type: Tipo de evento (heartbeat, progress, flag_submit)
            payload: Datos del evento (dict)
            topic: Tópico MQTT
        
        Returns:
            ID del evento
        """
        estudiante_id = self.upsert_estudiante(documento)
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO eventos_mqtt (estudiante_id, documento, event_type, payload, topic)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (estudiante_id, documento, event_type, Json(payload), topic))
                
                return cur.fetchone()[0]
    
    def get_eventos_recientes(self, limit=100):
        """Obtener eventos MQTT más recientes"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM v_actividad_reciente
                    LIMIT %s
                """, (limit,))
                
                return cur.fetchall()
    
    # ========================================================================
    # ESTADÍSTICAS Y VISTAS
    # ========================================================================
    
    def get_leaderboard(self, limit=None):
        """Obtener tabla de posiciones"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                query = "SELECT * FROM v_leaderboard"
                if limit:
                    query += f" LIMIT {limit}"
                
                cur.execute(query)
                return cur.fetchall()
    
    def get_progreso_retos(self):
        """Obtener progreso por cada reto"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM v_progreso_por_reto")
                return cur.fetchall()
    
    def get_estadisticas_globales(self):
        """Obtener estadísticas globales del sistema"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        COUNT(DISTINCT e.id) as total_estudiantes,
                        COUNT(DISTINCT CASE WHEN e.status = 'online' THEN e.id END) as estudiantes_online,
                        COUNT(rc.id) as total_completados,
                        COALESCE(AVG(e.total_retos_completados), 0) as promedio_retos,
                        COALESCE(AVG(e.total_puntos), 0) as promedio_puntos,
                        MAX(e.total_puntos) as max_puntos,
                        (SELECT COUNT(*) FROM retos WHERE activo = true) as total_retos_disponibles
                    FROM estudiantes e
                    LEFT JOIN retos_completados rc ON e.id = rc.estudiante_id
                """)
                
                return cur.fetchone()
    
    def get_actividad_por_hora(self, horas=24):
        """Obtener actividad de las últimas N horas"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        DATE_TRUNC('hour', received_at) as hora,
                        COUNT(*) as total_eventos,
                        COUNT(DISTINCT documento) as estudiantes_unicos,
                        COUNT(CASE WHEN event_type = 'flag_submit' THEN 1 END) as flags_enviadas
                    FROM eventos_mqtt
                    WHERE received_at >= NOW() - INTERVAL '%s hours'
                    GROUP BY DATE_TRUNC('hour', received_at)
                    ORDER BY hora DESC
                """, (horas,))
                
                return cur.fetchall()
    
    # ========================================================================
    # SESIONES
    # ========================================================================
    
    def iniciar_sesion(self, documento):
        """Iniciar nueva sesión para estudiante"""
        estudiante_id = self.upsert_estudiante(documento)
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # Cerrar sesiones activas previas
                cur.execute("""
                    UPDATE sesiones
                    SET session_end = CURRENT_TIMESTAMP,
                        duration = CURRENT_TIMESTAMP - session_start,
                        is_active = FALSE
                    WHERE estudiante_id = %s AND is_active = TRUE
                """, (estudiante_id,))
                
                # Crear nueva sesión
                cur.execute("""
                    INSERT INTO sesiones (estudiante_id, documento)
                    VALUES (%s, %s)
                    RETURNING id
                """, (estudiante_id, documento))
                
                return cur.fetchone()[0]
    
    def finalizar_sesion(self, documento):
        """Finalizar sesión activa del estudiante"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE sesiones s
                    SET session_end = CURRENT_TIMESTAMP,
                        duration = CURRENT_TIMESTAMP - session_start,
                        is_active = FALSE
                    FROM estudiantes e
                    WHERE s.estudiante_id = e.id 
                        AND e.documento = %s 
                        AND s.is_active = TRUE
                """, (documento,))
    
    # ========================================================================
    # UTILIDADES
    # ========================================================================
    
    def cleanup_old_events(self, days=30):
        """Limpiar eventos MQTT antiguos"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM eventos_mqtt
                    WHERE received_at < NOW() - INTERVAL '%s days'
                """, (days,))
                
                deleted = cur.rowcount
                logger.info(f"🧹 Eliminados {deleted} eventos antiguos")
                return deleted
    
    def get_health(self):
        """Health check de la base de datos"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT 1')
                    return {'status': 'healthy', 'database': 'connected'}
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}


# ============================================================================
# Instancia global (singleton)
# ============================================================================
_db_instance = None

def get_db():
    """Obtener instancia singleton de la base de datos"""
    global _db_instance
    if _db_instance is None:
        _db_instance = MonitorDB()
    return _db_instance
