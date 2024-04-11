from models import Usuario
from database import get_db_connection

def find_usuario_by_id(id_usuario: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, username, password, rol, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion FROM usuario WHERE id_usuario = %s", (id_usuario,))
        data = cursor.fetchone()
        if data:
            return Usuario(id_usuario=data[0], nombre=data[1], username=data[2], password=data[3], rol=data[4], creado_por=data[5], actualizado_por=data[6], ultima_actualizacion=data[7], es_activo=data[8], fecha_creacion=data[9])
        else:
            return None
    finally:
        conn.close()

