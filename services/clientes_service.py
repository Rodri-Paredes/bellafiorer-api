
from models import Cliente
from database import get_db_connection

def find_cliente_by_id(id_cliente: int):
    conn = get_db_connection() 
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nombre, direccion, celular, email, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion FROM cliente WHERE id_cliente = %s", (id_cliente,))
        data = cursor.fetchone()
        if data:
            return Cliente(id_cliente=data[0], nombre=data[1], direccion=data[2], celular=data[3], email=data[4], creado_por=data[5], actualizado_por=data[6], ultima_actualizacion=data[7], es_activo=data[8], fecha_creacion=data[9])
        else:
            return None
    finally:
        conn.close()
