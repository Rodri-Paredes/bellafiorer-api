from models import OrdenReserva
from services import usuarios_service, clientes_service
from database import get_db_connection
from datetime import datetime

def find_orden_reserva_by_id(id_orden: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT o.id_orden, o.monto_total, o.estado, o.id_usuario, o.id_cliente, o.creado_por, o.actualizado_por, o.ultima_actualizacion, o.es_activo, o.fecha_creacion, ore.monto_pagado, ore.metodo_pago FROM orden o INNER JOIN orden_reserva ore ON o.id_orden = ore.id_orden WHERE o.id_orden = %s",
            (id_orden,)
        )
        data = cursor.fetchone()
        if data:
            usuario_id = data[3]
            usuario = usuarios_service.find_usuario_by_id(usuario_id)
            cliente_id = data[4]
            cliente = clientes_service.find_cliente_by_id(cliente_id)
            return OrdenReserva(id_orden=data[0], monto_total=data[1], estado=data[2], usuario=usuario, cliente=cliente, creado_por=data[5], actualizado_por=data[6], ultima_actualizacion=data[7], es_activo=data[8], fecha_creacion=data[9], monto_pagado=data[10], metodo_pago=data[11])
        else:
            return None
    finally:
        conn.close()

def create_orden_reserva(orden_reserva: OrdenReserva):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orden (monto_total, estado, id_usuario, id_cliente, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (orden_reserva.monto_total, orden_reserva.estado, orden_reserva.usuario.id_usuario, orden_reserva.cliente.id_cliente, orden_reserva.creado_por, orden_reserva.actualizado_por, orden_reserva.ultima_actualizacion, orden_reserva.es_activo, orden_reserva.fecha_creacion)
    )
    id_orden = cursor.lastrowid

    cursor.execute(
        "INSERT INTO orden_reserva (id_orden, monto_pagado, metodo_pago) VALUES (%s, %s, %s)",
        (id_orden, orden_reserva.monto_pagado, orden_reserva.metodo_pago)
    )
    conn.commit()
    conn.close()
    orden_reserva.id_orden=id_orden
    return orden_reserva

