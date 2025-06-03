"""
Módulo con todas las consultas SQL del sistema
"""
from database.connetion import db
from datetime import datetime

class EventoQueries:
    """Consultas relacionadas con eventos"""
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los eventos"""
        query = """
        SELECT id_evento, nombre, descripcion, fecha_inicio, fecha_fin, 
               ubicacion, capacidad_maxima, categoria, estado,
               (SELECT COUNT(*) FROM inscripciones WHERE id_evento = eventos.id_evento AND estado = 'confirmado') as inscritos
        FROM eventos 
        ORDER BY fecha_inicio DESC
        """
        return db.execute_query(query)
    
    @staticmethod
    def obtener_por_id(id_evento):
        """Obtiene un evento por su ID"""
        query = "SELECT * FROM eventos WHERE id_evento = %s"
        result = db.execute_query(query, (id_evento,))
        return result[0] if result else None
    
    @staticmethod
    def crear(nombre, descripcion, fecha_inicio, fecha_fin, ubicacion, capacidad_maxima, categoria):
        """Crea un nuevo evento"""
        query = """
        INSERT INTO eventos (nombre, descripcion, fecha_inicio, fecha_fin, ubicacion, capacidad_maxima, categoria)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (nombre, descripcion, fecha_inicio, fecha_fin, ubicacion, capacidad_maxima, categoria)
        return db.execute_update(query, params)
    
    @staticmethod
    def actualizar(id_evento, nombre, descripcion, fecha_inicio, fecha_fin, ubicacion, capacidad_maxima, categoria, estado):
        """Actualiza un evento existente"""
        query = """
        UPDATE eventos 
        SET nombre = %s, descripcion = %s, fecha_inicio = %s, fecha_fin = %s, 
            ubicacion = %s, capacidad_maxima = %s, categoria = %s, estado = %s
        WHERE id_evento = %s
        """
        params = (nombre, descripcion, fecha_inicio, fecha_fin, ubicacion, capacidad_maxima, categoria, estado, id_evento)
        return db.execute_update(query, params)
    
    @staticmethod
    def eliminar(id_evento):
        """Elimina un evento"""
        query = "DELETE FROM eventos WHERE id_evento = %s"
        return db.execute_update(query, (id_evento,))
    
    @staticmethod
    def buscar(criterio):
        """Busca eventos por nombre o descripción"""
        query = """
        SELECT id_evento, nombre, descripcion, fecha_inicio, fecha_fin, 
               ubicacion, capacidad_maxima, categoria, estado,
               (SELECT COUNT(*) FROM inscripciones WHERE id_evento = eventos.id_evento AND estado = 'confirmado') as inscritos
        FROM eventos 
        WHERE nombre LIKE %s OR descripcion LIKE %s
        ORDER BY fecha_inicio DESC
        """
        criterio_like = f"%{criterio}%"
        return db.execute_query(query, (criterio_like, criterio_like))
    
    @staticmethod
    def obtener_eventos_proximos():
        """Obtiene eventos próximos (fecha >= hoy)"""
        query = """
        SELECT id_evento, nombre, descripcion, fecha_inicio, fecha_fin, 
               ubicacion, capacidad_maxima, categoria, estado,
               (SELECT COUNT(*) FROM inscripciones WHERE id_evento = eventos.id_evento AND estado = 'confirmado') as inscritos
        FROM eventos 
        WHERE fecha_inicio >= NOW() AND estado = 'activo'
        ORDER BY fecha_inicio ASC
        """
        return db.execute_query(query)

class ParticipanteQueries:
    """Consultas relacionadas con participantes"""
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los participantes"""
        query = """
        SELECT id_participante, nombre, apellido, email, telefono, fecha_registro,
               (SELECT COUNT(*) FROM inscripciones WHERE id_participante = participantes.id_participante) as total_eventos
        FROM participantes 
        ORDER BY apellido, nombre
        """
        return db.execute_query(query)
    
    @staticmethod
    def obtener_por_id(id_participante):
        """Obtiene un participante por su ID"""
        query = "SELECT * FROM participantes WHERE id_participante = %s"
        result = db.execute_query(query, (id_participante,))
        return result[0] if result else None
    
    @staticmethod
    def crear(nombre, apellido, email, telefono):
        """Crea un nuevo participante"""
        query = """
        INSERT INTO participantes (nombre, apellido, email, telefono)
        VALUES (%s, %s, %s, %s)
        """
        params = (nombre, apellido, email, telefono)
        return db.execute_update(query, params)
    
    @staticmethod
    def actualizar(id_participante, nombre, apellido, email, telefono):
        """Actualiza un participante existente"""
        query = """
        UPDATE participantes 
        SET nombre = %s, apellido = %s, email = %s, telefono = %s
        WHERE id_participante = %s
        """
        params = (nombre, apellido, email, telefono, id_participante)
        return db.execute_update(query, params)
    
    @staticmethod
    def eliminar(id_participante):
        """Elimina un participante"""
        query = "DELETE FROM participantes WHERE id_participante = %s"
        return db.execute_update(query, (id_participante,))
    
    @staticmethod
    def buscar(criterio):
        """Busca participantes por nombre, apellido o email"""
        query = """
        SELECT id_participante, nombre, apellido, email, telefono, fecha_registro,
               (SELECT COUNT(*) FROM inscripciones WHERE id_participante = participantes.id_participante) as total_eventos
        FROM participantes 
        WHERE nombre LIKE %s OR apellido LIKE %s OR email LIKE %s
        ORDER BY apellido, nombre
        """
        criterio_like = f"%{criterio}%"
        return db.execute_query(query, (criterio_like, criterio_like, criterio_like))
    
    @staticmethod
    def verificar_email_existe(email, id_participante=None):
        """Verifica si un email ya existe (para validaciones)"""
        if id_participante:
            query = "SELECT COUNT(*) as count FROM participantes WHERE email = %s AND id_participante != %s"
            params = (email, id_participante)
        else:
            query = "SELECT COUNT(*) as count FROM participantes WHERE email = %s"
            params = (email,)
        
        result = db.execute_query(query, params)
        return result[0]['count'] > 0 if result else False

class InscripcionQueries:
    """Consultas relacionadas con inscripciones"""
    
    @staticmethod
    def inscribir_participante(id_evento, id_participante, notas=""):
        """Inscribe un participante a un evento"""
        query = """
        INSERT INTO inscripciones (id_evento, id_participante, notas)
        VALUES (%s, %s, %s)
        """
        params = (id_evento, id_participante, notas)
        return db.execute_update(query, params)
    
    @staticmethod
    def cancelar_inscripcion(id_evento, id_participante):
        """Cancela la inscripción de un participante"""
        query = """
        UPDATE inscripciones 
        SET estado = 'cancelado' 
        WHERE id_evento = %s AND id_participante = %s
        """
        return db.execute_update(query, (id_evento, id_participante))
    
    @staticmethod
    def obtener_participantes_evento(id_evento):
        """Obtiene todos los participantes de un evento"""
        query = """
        SELECT p.id_participante, p.nombre, p.apellido, p.email, p.telefono,
               i.fecha_inscripcion, i.estado, i.notas
        FROM participantes p
        JOIN inscripciones i ON p.id_participante = i.id_participante
        WHERE i.id_evento = %s
        ORDER BY i.fecha_inscripcion DESC
        """
        return db.execute_query(query, (id_evento,))
    
    @staticmethod
    def obtener_eventos_participante(id_participante):
        """Obtiene todos los eventos de un participante"""
        query = """
        SELECT e.id_evento, e.nombre, e.descripcion, e.fecha_inicio, e.fecha_fin,
               e.ubicacion, e.categoria, i.fecha_inscripcion, i.estado, i.notas
        FROM eventos e
        JOIN inscripciones i ON e.id_evento = i.id_evento
        WHERE i.id_participante = %s
        ORDER BY e.fecha_inicio DESC
        """
        return db.execute_query(query, (id_participante,))
    
    @staticmethod
    def verificar_inscripcion_existe(id_evento, id_participante):
        """Verifica si ya existe una inscripción"""
        query = """
        SELECT COUNT(*) as count 
        FROM inscripciones 
        WHERE id_evento = %s AND id_participante = %s AND estado != 'cancelado'
        """
        result = db.execute_query(query, (id_evento, id_participante))
        return result[0]['count'] > 0 if result else False
    
    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas generales del sistema"""
        query = """
        SELECT 
            (SELECT COUNT(*) FROM eventos WHERE estado = 'activo') as eventos_activos,
            (SELECT COUNT(*) FROM participantes) as total_participantes,
            (SELECT COUNT(*) FROM inscripciones WHERE estado = 'confirmado') as inscripciones_confirmadas,
            (SELECT COUNT(*) FROM eventos WHERE fecha_inicio >= NOW() AND estado = 'activo') as eventos_proximos
        """
        result = db.execute_query(query)
        return result[0] if result else None