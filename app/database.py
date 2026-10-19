import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class DatabaseConnection:
    """Clase encargada de la gestión de conexiones a Amazon RDS."""
    
    @staticmethod
    def get_connection():
        """Crea y retorna una conexión a MySQL en Amazon RDS."""
        return pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME", "vehiculo_iot"),
            port=int(os.getenv("DB_PORT", 3306)),
            cursorclass=DictCursor,
            autocommit=False  # Para manejo manual de transacciones
        )