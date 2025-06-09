"""
Modelo para la entidad Participante
"""
import re
from datetime import datetime
from database.queries import ParticipanteQueries
from utils.validations import Validaciones

class Participante:
    """Clase modelo para representar un participante"""

    def __init__(self, id_participante=None, nombre="", apellido="", email="",
                 telefono="", fecha_registro=None, total_eventos=0):
        self.id_participante = id_participante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.fecha_registro = fecha_registro
        self.total_eventos = total_eventos

    @classmethod
    def from_dict(cls, data):
        """Crea una instancia de Participante desde un diccionario"""
        return cls(
            id_participante=data.get('id_participante'),
            nombre=data.get('nombre', ''),
            apellido=data.get('apellido', ''),
            email=data.get('email', ''),
            telefono=data.get('telefono', ''),
            fecha_registro=data.get('fecha_registro'),
            total_eventos=data.get('total_eventos', 0)
        )

    def to_dict(self):
        """Convierte la instancia a diccionario"""
        return {
            'id_participante': self.id_participante,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_registro': self.fecha_registro,
            'total_eventos': self.total_eventos
        }

    def guardar(self):
        """Guarda el participante en la base de datos (crear o actualizar)"""
        errores = self.validar()
        if errores:
            raise ValueError("Errores de validación: " + ", ".join(errores))

        if self.id_participante:
            result = ParticipanteQueries.actualizar(
                self.id_participante, self.nombre, self.apellido,
                self.email, self.telefono
            )
            return result is not None
        else:
            result = ParticipanteQueries.crear(
                self.nombre, self.apellido, self.email, self.telefono
            )
            if result:
                self.id_participante = result
                return True
            return False

    def eliminar(self):
        """Elimina el participante de la base de datos"""
        if self.id_participante:
            return ParticipanteQueries.eliminar(self.id_participante) is not None
        return False

    @staticmethod
    def obtener_todos():
        """Obtiene todos los participantes como objetos Participante"""
        datos = ParticipanteQueries.obtener_todos()
        if datos:
            return [Participante.from_dict(participante) for participante in datos]
        return []

    @staticmethod
    def obtener_por_id(id_participante):
        """Obtiene un participante por su ID"""
        datos = ParticipanteQueries.obtener_por_id(id_participante)
        if datos:
            return Participante.from_dict(datos)
        return None

    @staticmethod
    def buscar(criterio):
        """Busca participantes por criterio"""
        datos = ParticipanteQueries.buscar(criterio)
        if datos:
            return [Participante.from_dict(participante) for participante in datos]
        return []

    def validar(self):
        """Valida los datos del participante"""
        errores = []

        # Validar nombre
        valido, mensaje = Validaciones.validar_nombre(self.nombre, "nombre")
        if not valido:
            errores.append(mensaje)

        # Validar apellido
        valido, mensaje = Validaciones.validar_nombre(self.apellido, "apellido")
        if not valido:
            errores.append(mensaje)

        # Validar email
        valido, mensaje = Validaciones.validar_email(self.email)
        if not valido:
            errores.append(mensaje)

        # Validar teléfono
        valido, mensaje = Validaciones.validar_telefono(self.telefono)
        if not valido:
            errores.append(mensaje)

        return errores
