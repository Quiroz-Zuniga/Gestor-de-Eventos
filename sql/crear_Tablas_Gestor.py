import mysql.connector
from mysql.connector import Error

try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestor_eventos"
    )

    cursor = conexion.cursor()

    # Tabla participantes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS participantes (
            id_participante INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100),
            apellido VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            telefono VARCHAR(20),
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla eventos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id_evento INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(150),
            descripcion TEXT,
            fecha_inicio DATETIME,
            fecha_fin DATETIME,
            ubicacion VARCHAR(150),
            capacidad_maxima INT,
            categoria VARCHAR(100),
            estado VARCHAR(50) DEFAULT 'activo',
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla inscripciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inscripciones (
            id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
            id_evento INT,
            id_participante INT,
            fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado VARCHAR(50) DEFAULT 'confirmado',
            notas TEXT,
            FOREIGN KEY (id_evento) REFERENCES eventos(id_evento) ON DELETE CASCADE,
            FOREIGN KEY (id_participante) REFERENCES participantes(id_participante) ON DELETE CASCADE
        )
    """)

    print("Tablas creadas correctamente.")

except Error as err:
    print(f"Error al crear las tablas: {err}")

finally:
    if conexion.is_connected():
        cursor.close()
        conexion.close()
