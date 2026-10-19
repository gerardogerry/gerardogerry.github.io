from app.database import DatabaseConnection

class VehiculoService:
    """Servicio con POO que mapea los 21 Stored Procedures de vehiculo_iot en Amazon RDS."""

    # ==========================================
    # 1. VEHÍCULOS (5 SPs)
    # ==========================================
    @staticmethod
    def obtener_vehiculos():
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_vehiculos")
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def obtener_vehiculo_por_id(vehiculo_id: int):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_vehiculo_por_id", (vehiculo_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def insertar_vehiculo(nombre: str, modelo: str, estado: str):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_insertar_vehiculo", (nombre, modelo, estado))
                conn.commit()
                return cursor.fetchone()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def actualizar_vehiculo(vehiculo_id: int, nombre: str, modelo: str, estado: str):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_actualizar_vehiculo", (vehiculo_id, nombre, modelo, estado))
                conn.commit()
                return cursor.fetchone()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def eliminar_vehiculo(vehiculo_id: int):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_eliminar_vehiculo", (vehiculo_id,))
                conn.commit()
                return cursor.fetchone()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # ==========================================
    # 2. COMANDOS (4 SPs)
    # ==========================================
    @staticmethod
    def obtener_comandos():
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_comandos")
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def obtener_comando_por_id(comando_id: int):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_comando_por_id", (comando_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def insertar_comando(nombre: str, descripcion: str, instruccion: str):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_insertar_comando", (nombre, descripcion, instruccion))
                conn.commit()
                return cursor.fetchone()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def eliminar_comando(comando_id: int):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_eliminar_comando", (comando_id,))
                conn.commit()
                return cursor.fetchone()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # ==========================================
    # 3. ESTADO (2 SPs)
    # ==========================================
    @staticmethod
    def obtener_ultimo_estado(vehiculo_id: int):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_ultimo_estado", (vehiculo_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def actualizar_estado(vehiculo_id: int, estado: str, posicion_x: float, posicion_y: float):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_actualizar_estado", (vehiculo_id, estado, posicion_x, posicion_y))
                conn.commit()
                return cursor.fetchone()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # ==========================================
    # 4. HISTORIAL (2 SPs)
    # ==========================================
    @staticmethod
    def registrar_movimiento_historial(vehiculo_id: int, comando_id: int, detalle: str):
        """Registra un movimiento en el historial."""
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_registrar_movimiento_historial", (vehiculo_id, comando_id, detalle))
                conn.commit()
                return cursor.fetchone()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def obtener_historial_reciente(vehiculo_id: int, limite: int = 10):
        """Obtiene hasta los N movimientos individuales recientes (sin DEMO)."""
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_historial_reciente", (vehiculo_id, limite))
                return cursor.fetchall()
        finally:
            conn.close()

    # ==========================================
    # 5. DEMO (4 SPs)
    # ==========================================
    @staticmethod
    def obtener_demos():
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_demos")
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def obtener_demo_por_id(demo_id: int):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_demo_por_id", (demo_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def insertar_demo(nombre: str, descripcion: str):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_insertar_demo", (nombre, descripcion))
                conn.commit()
                return cursor.fetchone()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def eliminar_demo(demo_id: int):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_eliminar_demo", (demo_id,))
                conn.commit()
                return cursor.fetchone()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # ==========================================
    # 6. MOVIMIENTOS DEMO (4 SPs)
    # ==========================================
    @staticmethod
    def obtener_movimientos_demo(demo_id: int):
        """Obtiene la secuencia de N movimientos temporizados para una DEMO."""
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_movimientos_demo", (demo_id,))
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def agregar_movimiento_demo(demo_id: int, comando_id: int, orden: int, duracion_ms: int, pausa_ms: int):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_agregar_movimiento_demo", (demo_id, comando_id, orden, duracion_ms, pausa_ms))
                conn.commit()
                return cursor.fetchone()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def actualizar_movimiento_demo(movimiento_demo_id: int, orden: int, duracion_ms: int, pausa_ms: int):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_actualizar_movimiento_demo", (movimiento_demo_id, orden, duracion_ms, pausa_ms))
                conn.commit()
                return cursor.fetchone()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def eliminar_movimiento_demo(movimiento_demo_id: int):
        conn = DatabaseConnection.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc("sp_eliminar_movimiento_demo", (movimiento_demo_id,))
                conn.commit()
                return cursor.fetchone()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()