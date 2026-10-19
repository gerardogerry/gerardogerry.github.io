from typing import List, Dict, Any, Optional
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="instancia-rds-iot.cfyzylsylqy4.us-east-1.rds.amazonaws.com",
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "Admin1234#"),
        database=os.getenv("DB_NAME", "vehiculo_iot"),
        port=int(os.getenv("DB_PORT", 3306))
    )
def format_row(row: Dict[str, Any]) -> Dict[str, Any]:
    if not row:
        return row
    formatted = {}
    for key, value in row.items():
        if isinstance(value, datetime):
            formatted[key] = value.isoformat()
        else:
            formatted[key] = value
    return formatted

class VehiculoService:

    @staticmethod
    def listar_vehiculos() -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_obtener_vehiculos")
            vehiculos = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    vehiculos.append(format_row(row))
            return vehiculos
        finally:
            cursor.close()
            conn.close()

    # Alias para resolver el AttributeError
    obtener_vehiculos = listar_vehiculos

    @staticmethod
    def obtener_vehiculo_por_id(vehiculo_id: int) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_obtener_vehiculo", (vehiculo_id,))
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    return format_row(row)
            return None
        finally:
            cursor.close()
            conn.close()

    obtener_vehiculo = obtener_vehiculo_por_id

    @staticmethod
    def listar_comandos_vehiculo(vehiculo_id: int = 1) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_obtener_comandos_vehiculo", (vehiculo_id,))
            comandos = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    comandos.append(format_row(row))
            return comandos
        finally:
            cursor.close()
            conn.close()

    obtener_comandos = listar_comandos_vehiculo

    @staticmethod
    def obtener_ultimo_estado(vehiculo_id: int) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_obtener_estado", (vehiculo_id,))
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    return format_row(row)
            return None
        finally:
            cursor.close()
            conn.close()

    obtener_estado = obtener_ultimo_estado

    @staticmethod
    def obtener_historial_reciente(vehiculo_id: int) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_obtener_historial", (vehiculo_id,))
            historial = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    historial.append(format_row(row))
            return historial[:10]
        finally:
            cursor.close()
            conn.close()

    obtener_historial = obtener_historial_reciente

    @staticmethod
    def registrar_movimiento(vehiculo_id: int, comando_id: int, origen: str = "MANUAL") -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_actualizar_estado", (vehiculo_id, comando_id, True))
            cursor.callproc("sp_registrar_historial", (vehiculo_id, comando_id, origen))
            conn.commit()
            return VehiculoService.obtener_ultimo_estado(vehiculo_id)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_demos_vehiculo(vehiculo_id: int) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_obtener_demos", (vehiculo_id,))
            demos = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    demos.append(format_row(row))
            return demos
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_movimientos_demo(demo_id: int) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_obtener_movimientos_demo", (demo_id,))
            movimientos = []
            for result in cursor.stored_results():
                for row in result.fetchall():
                    movimientos.append(format_row(row))
            return movimientos
        finally:
            cursor.close()
            conn.close()

