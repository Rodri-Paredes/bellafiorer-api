from dbutils.pooled_db import PooledDB
from dotenv import load_dotenv
import MySQLdb
import os
from models import Cliente

load_dotenv()

db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_DATABASE"),
}

pool = PooledDB(MySQLdb, 5, **db_config)



def find_cliente_by_id(id_cliente: int):
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nombre, direccion, celular, email, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion FROM cliente WHERE id_cliente = %s", (id_cliente,))
        data = cursor.fetchone()
        if data:
            return Cliente(id_cliente=data[0], nombre=data[1], direccion=data[2], celular=data[3], email=data[4], creado_por=data[5], actualizado_por=data[6], ultima_actualizacion=data[7], es_activo=data[8], fecha_creacion=data[9])
        else:
            None
    finally:
        conn.close()
