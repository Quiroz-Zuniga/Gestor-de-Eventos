import mysql.connector
from mysql.connector import Error
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.port = 3306
        self.database = 'gestor_eventos'
        self.connection = None

    def crear_base_datos_si_no_existe(self):
        try:
            temp_conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )
            cursor = temp_conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()
            temp_conn.close()
            logger.info(f"Base de datos '{self.database}' verificada o creada.")
        except Error as e:
            logger.error(f"Error creando base de datos: {e}")

    def connect(self):
        try:
            self.crear_base_datos_si_no_existe()
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                autocommit=True
            )
            if self.connection.is_connected():
                logger.info("Conexión exitosa a MySQL")
                return True
        except Error as e:
            logger.error(f"Error al conectar a MySQL: {e}")
            return False

    def get_connection(self):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Conexión cerrada")

# Bloque ejecutable
if __name__ == "__main__":
    db = DatabaseConnection()
    if db.connect():
        print("Conexión exitosa.")
    else:
        print("No se pudo conectar a la base de datos.")
