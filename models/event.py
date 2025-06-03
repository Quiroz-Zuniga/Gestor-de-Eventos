"""
Modelo para la entidad Evento
"""
from datetime import datetime
from database.queries import EventoQueries

class Evento:
    """Clase modelo para representar un evento"""
    
    def __init__(self, id_evento=None, nombre="", descripcion="", fecha_inicio=None, 
                 fecha_fin=None, ubicacion="", capacidad_maxima=50, categoria="General", 
                 estado="activo", fecha_creacion=None, inscritos=0):
        self.id_evento = id_evento
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.ubicacion = ubicacion
        self.capacidad_maxima = capacidad_maxima
        self.categoria = categoria
        self.estado = estado
        self.fecha_creacion = fecha_creacion
        self.inscritos = inscritos
    
    @classmethod
    def from_dict(cls, data):
        """Crea una instancia de Evento desde un diccionario"""
        return cls(
            id_evento=data.get('id_evento'),
            nombre=data.get('nombre', ''),
            descripcion=data.get('descripcion', ''),
            fecha_inicio=data.get('fecha_inicio'),
            fecha_fin=data.get('fecha_fin'),
            ubicacion=data.get('ubicacion', ''),
            capacidad_maxima=data.get('capacidad_maxima', 50),
            categoria=data.get('categoria', 'General'),
            estado=data.get('estado', 'activo'),
            fecha_creacion=data.get('fecha_creacion'),
            inscritos=data.get('inscritos', 0)
        )
    
    def to_dict(self):
        """Convierte la instancia a diccionario"""
        return {
            'id_evento': self.id_evento,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'ubicacion': self.ubicacion,
            'capacidad_maxima': self.capacidad_maxima,
            'categoria': self.categoria,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion,
            'inscritos': self.inscritos
        }
    
    def guardar(self):
        """Guarda el evento en la base de datos (crear o actualizar)"""
        if self.id_evento:
            # Actualizar evento existente
            result = EventoQueries.actualizar(
                self.id_evento, self.nombre, self.descripcion, 
                self.fecha_inicio, self.fecha_fin, self.ubicacion,
                self.capacidad_maxima, self.categoria, self.estado
            )
            return result is not None
        else:
            # Crear nuevo evento
            result = EventoQueries.crear(
                self.nombre, self.descripcion, self.fecha_inicio,
                self.fecha_fin, self.ubicacion, self.capacidad_maxima,
                self.categoria
            )
            if result:
                self.id_evento = result
                return True
            return False
    
    def eliminar(self):
        """Elimina el evento de la base de datos"""
        if self.id_evento:
            return EventoQueries.eliminar(self.id_evento) is not None
        return False
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los eventos como objetos Evento"""
        datos = EventoQueries.obtener_todos()
        if datos:
            return [Evento.from_dict(evento) for evento in datos]
        return []
    
    @staticmethod
    def obtener_por_id(id_evento):
        """Obtiene un evento por su ID"""
        datos = EventoQueries.obtener_por_id(id_evento)
        if datos:
            return Evento.from_dict(datos)
        return None
    
    @staticmethod
    def buscar(criterio):
        """Busca eventos por criterio"""
        datos = EventoQueries.buscar(criterio)
        if datos:
            return [Evento.from_dict(evento) for evento in datos]
        return []
    
    @staticmethod
    def obtener_proximos():
        """Obtiene eventos próximos"""
        datos = EventoQueries.obtener_eventos_proximos()
        if datos:
            return [Evento.from_dict(evento) for evento in datos]
        return []
    
    def validar(self):
        """Valida los datos del evento"""
        errores = []
        
        if not self.nombre or self.nombre.strip() == "":
            errores.append("El nombre del evento es obligatorio")
        
        if not self.fecha_inicio:
            errores.append("La fecha de inicio es obligatoria")
        
        if self.fecha_fin and self.fecha_inicio and self.fecha_fin < self.fecha_inicio:
            errores.append("La fecha de fin debe ser posterior a la fecha de inicio")
        
        if self.capacidad_maxima <= 0:
            errores.append("La capacidad máxima debe ser mayor a 0")
        
        if not self.ubicacion or self.ubicacion.strip() == "":
            errores.append("La ubicación es obligatoria")
        
        return errores
    
    def tiene_cupos_disponibles(self):
        """Verifica si el evento tiene cupos disponibles"""
        return self.inscritos < self.capacidad_maxima
    
    def cupos_disponibles(self):
        """Retorna el número de cupos disponibles"""
        return max(0, self.capacidad_maxima - self.inscritos)
    
    def porcentaje_ocupacion(self):
        """Retorna el porcentaje de ocupación del evento"""
        if self.capacidad_maxima == 0:
            return 0
        return round((self.inscritos / self.capacidad_maxima) * 100, 1)
    
    def esta_activo(self):
        """Verifica si el evento está activo"""
        return self.estado == 'activo'
    
    def fecha_inicio_str(self):
        """Retorna la fecha de inicio como string formateado"""
        if self.fecha_inicio:
            if isinstance(self.fecha_inicio, str):
                # Si viene como string desde la BD, parsearlo
                try:
                    fecha = datetime.strptime(self.fecha_inicio, "%Y-%m-%d %H:%M:%S")
                    return fecha.strftime("%d/%m/%Y %H:%M")
                except:
                    return self.fecha_inicio
            else:
                return self.fecha_inicio.strftime("%d/%m/%Y %H:%M")
        return ""
    
    def fecha_fin_str(self):
        """Retorna la fecha de fin como string formateado"""
        if self.fecha_fin:
            if isinstance(self.fecha_fin, str):
                try:
                    fecha = datetime.strptime(self.fecha_fin, "%Y-%m-%d %H:%M:%S")
                    return fecha.strftime("%d/%m/%Y %H:%M")
                except:
                    return self.fecha_fin
            else:
                return self.fecha_fin.strftime("%d/%m/%Y %H:%M")
        return ""
    
    def __str__(self):
        """Representación string del evento"""
        return f"Evento: {self.nombre} - {self.fecha_inicio_str()} - {self.ubicacion}"
    
    def __repr__(self):
        """Representación para debugging"""
        return f"Evento(id={self.id_evento}, nombre='{self.nombre}', fecha_inicio='{self.fecha_inicio}')"