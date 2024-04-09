from dbutils.pooled_db import PooledDB
from dotenv import load_dotenv
import MySQLdb
import os
from models import OrdenPedido
from services import usuarios_service, clientes_service


load_dotenv()

db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_DATABASE"),
}

pool = PooledDB(MySQLdb, 5, **db_config)


def find_orderpedido_by_id(id_orden: int):
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT o.id_orden, o.monto_total, o.estado, o.id_usuario, o.id_cliente, o.creado_por, o.actualizado_por, o.ultima_actualizacion, o.es_activo, o.fecha_creacion, op.fecha_entrega FROM orden o INNER JOIN orden_pedido OP ON o.id_orden = OP.id_orden WHERE o.id_orden = %s",
            (id_orden,)
        )
        data = cursor.fetchone()
        if data:
            usuario_id = data[3]
            usuario = usuarios_service.find_usuario_by_id(usuario_id)
            cliente_id = data[4]
            cliente = clientes_service.find_cliente_by_id(cliente_id)
            return OrdenPedido(id_orden=data[0], monto_total=data[1], estado=data[2], usuario=usuario, cliente=cliente, creado_por=data[5], actualizado_por=data[6], ultima_actualizacion=data[7], es_activo=data[8], fecha_creacion=data[9], fecha_entrega=data[10])
        else:
            None
    finally:
        conn.close()


def create_orderpedido(order_pedido: OrdenPedido):
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orden (monto_total, estado, id_usuario, id_cliente, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (order_pedido.monto_total, order_pedido.estado, order_pedido.usuario.id_usuario, order_pedido.cliente.id_cliente, order_pedido.creado_por, order_pedido.actualizado_por, order_pedido.ultima_actualizacion, order_pedido.es_activo, order_pedido.fecha_creacion)
        )
        conn.commit()
        id_orden = cursor.lastrowid
        
        cursor.execute(
            "INSERT INTO orden_pedido (id_orden, fecha_entrega) VALUES (%s, %s)",
            (id_orden, order_pedido.fecha_entrega)
        )
        conn.commit()
    finally:
        conn.close()
        
    return order_pedido