"""
Módulo de conexión a la base de datos MySQL
"""
import mysql.connector
from mysql.connector import Error
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Clase para manejar la conexión a MySQL"""
    
    def __init__(self):
        self.host = 'localhost'
        self.database = 'gestor_eventos'
        self.user = 'root'  # Usuario por defecto de XAMPP
        self.password = ''  # Contraseña vacía por defecto en XAMPP
        self.port = 3306
        self.connection = None
    
    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                autocommit=True
            )
            
            if self.connection.is_connected():
                logger.info("Conexión exitosa a MySQL")
                return True
                
        except Error as e:
            logger.error(f"Error al conectar a MySQL: {e}")
            return False
    
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Conexión cerrada")
    
    def get_connection(self):
        """Retorna la conexión activa"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection
    
    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta SELECT y retorna los resultados
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchall()
            cursor.close()
            return result
            
        except Error as e:
            logger.error(f"Error ejecutando consulta: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """
        Ejecuta consultas INSERT, UPDATE, DELETE
        Retorna el ID del último registro insertado o el número de filas afectadas
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Para INSERT, retorna el ID del último registro
            if query.strip().upper().startswith('INSERT'):
                result = cursor.lastrowid
            else:
                # Para UPDATE/DELETE, retorna el número de filas afectadas
                result = cursor.rowcount
            
            cursor.close()
            return result
            
        except Error as e:
            logger.error(f"Error ejecutando actualización: {e}")
            return None
    
    def test_connection(self):
        """Prueba la conexión a la base de datos"""
        try:
            if self.connect():
                cursor = self.connection.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()
                return result is not None
        except Error as e:
            logger.error(f"Error en test de conexión: {e}")
            return False

# Instancia global de la conexión
db = DatabaseConnection()