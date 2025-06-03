"""
Utilidades para validaciones del sistema
"""
import re
from datetime import datetime

class Validaciones:
    """Clase con métodos estáticos para validaciones comunes"""
    
    @staticmethod
    def validar_email(email):
        """
        Valida el formato de un email
        Returns: (bool, str) - (es_valido, mensaje_error)
        """
        if not email or email.strip() == "":
            return False, "El email es obligatorio"
        
        email = email.strip()
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(patron, email):
            return False, "El formato del email no es válido"
        
        if len(email) > 100:
            return False, "El email no puede exceder 100 caracteres"
        
        return True, ""
    
    @staticmethod
    def validar_telefono(telefono):
        """
        Valida el formato de un teléfono
        Returns: (bool, str) - (es_valido, mensaje_error)
        """
        if not telefono:
            return True, ""  # El teléfono es opcional
        
        telefono = telefono.strip()
        if telefono == "":
            return True, ""
        
        # Eliminar espacios, guiones, paréntesis para validar solo números
        telefono_limpio = re.sub(r'[\s\-\(\)\+]', '', telefono)
        
        if not telefono_limpio.isdigit():
            return False, "El teléfono solo puede contener números, espacios, guiones y paréntesis"
        
        if len(telefono_limpio) < 8 or len(telefono_limpio) > 15:
            return False, "El teléfono debe tener entre 8 y 15 dígitos"
        
        return True, ""
    
    @staticmethod
    def validar_nombre(nombre, campo="nombre"):
        """
        Valida un nombre o apellido
        Returns: (bool, str) - (es_valido, mensaje_error)
        """
        if not nombre or nombre.strip() == "":
            return False, f"El {campo} es obligatorio"
        
        nombre = nombre.strip()
        
        if len(nombre) < 2:
            return False, f"El {campo} debe tener al menos 2 caracteres"
        
        if len(nombre) > 100:
            return False, f"El {campo} no puede exceder 100 caracteres"
        
        # Permitir solo letras, espacios, acentos y algunos caracteres especiales
        patron = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\'\-\.]+$'
        if not re.match(patron, nombre):
            return False, f"El {campo} contiene caracteres no válidos"
        
        return True, ""
    
    @staticmethod
    def validar_fecha(fecha_str, formato="%Y-%m-%d %H:%M"):
        """
        Valida y convierte una fecha en string
        Returns: (bool, datetime/str) - (es_valido, fecha_convertida/mensaje_error)
        """
        if not fecha_str or fecha_str.strip() == "":
            return False, "La fecha es obligatoria"
        
        try:
            fecha = datetime.strptime(fecha_str.strip(), formato)
            return True, fecha
        except ValueError:
            return False, f"El formato de fecha debe ser: {formato.replace('%Y', 'AAAA').replace('%m', 'MM').replace('%d', 'DD').replace('%H', 'HH').replace('%M', 'MM')}"
    
    @staticmethod
    def validar_fecha_evento(fecha_inicio_str, fecha_fin_str=None, formato="%Y-%m-%d %H:%M"):
        """
        Valida fechas de evento (inicio y fin)
        Returns: (bool, dict/str) - (es_valido, {fechas}/mensaje_error)
        """
        # Validar fecha de inicio
        valido_inicio, fecha_inicio = Validaciones.validar_fecha(fecha_inicio_str, formato)
        if not valido_inicio:
            return False, f"Fecha de inicio: {fecha_inicio}"
        
        # Validar que la fecha de inicio no sea en el pasado (opcional)
        # if fecha_inicio < datetime.now():
        #     return False, "La fecha de inicio no puede ser en el pasado"
        
        resultado = {"fecha_inicio": fecha_inicio}
        
        # Si hay fecha de fin, validarla
        if fecha_fin_str and fecha_fin_str.strip():
            valido_fin, fecha_fin = Validaciones.validar_fecha(fecha_fin_str, formato)
            if not valido_fin:
                return False, f"Fecha de fin: {fecha_fin}"
            
            # Validar que fecha fin sea posterior a fecha inicio
            if fecha_fin <= fecha_inicio:
                return False, "La fecha de fin debe ser posterior a la fecha de inicio"
            
            resultado["fecha_fin"] = fecha_fin
        
        return True, resultado
    
    @staticmethod
    def validar_numero_entero(valor_str, campo="valor", minimo=None, maximo=None):
        """
        Valida un número entero
        Returns: (bool, int/str) - (es_valido, numero/mensaje_error)
        """
        if not valor_str or str(valor_str).strip() == "":
            return False, f"El {campo} es obligatorio"
        
        try:
            numero = int(str(valor_str).strip())
            
            if minimo is not None and numero < minimo:
                return False, f"El {campo} debe ser mayor o igual a {minimo}"
            
            if maximo is not None and numero > maximo:
                return False, f"El {campo} debe ser menor o igual a {maximo}"
            
            return True, numero
            
        except ValueError:
            return False, f"El {campo} debe ser un número entero válido"
    
    @staticmethod
    def validar_texto(texto, campo="texto", minimo=0, maximo=None, obligatorio=True):
        """
        Valida un campo de texto
        Returns: (bool, str) - (es_valido, mensaje_error)
        """
        if not texto:
            texto = ""
        
        texto = texto.strip()
        
        if obligatorio and texto == "":
            return False, f"El {campo} es obligatorio"
        
        if len(texto) < minimo:
            return False, f"El {campo} debe tener al menos {minimo} caracteres"
        
        if maximo and len(texto) > maximo:
            return False, f"El {campo} no puede exceder {maximo} caracteres"
        
        return True, ""
    
    @staticmethod
    def limpiar_texto(texto):
        """Limpia un texto eliminando espacios extra y caracteres especiales"""
        if not texto:
            return ""
        
        # Eliminar espacios al inicio y final
        texto = texto.strip()
        
        # Reemplazar múltiples espacios por uno solo
        texto = re.sub(r'\s+', ' ', texto)
        
        return texto
    
    @staticmethod
    def formatear_telefono(telefono):
        """Formatea un teléfono a un formato estándar"""
        if not telefono:
            return ""
        
        # Eliminar todos los caracteres no numéricos excepto el +
        telefono_limpio = re.sub(r'[^\d\+]', '', telefono)
        
        # Si tiene 8 dígitos, asumir que es local y agregar formato
        if len(telefono_limpio) == 8:
            return f"{telefono_limpio[:4]}-{telefono_limpio[4:]}"
        
        # Si tiene más dígitos, mantener como está
        return telefono_limpio
    
    @staticmethod
    def es_email_valido_simple(email):
        """Validación simple de email (solo formato básico)"""
        if not email:
            return False
        
        patron = r'^[^@]+@[^@]+\.[^@]+$'
        return re.match(patron, email.strip()) is not None