from fastapi import APIRouter, HTTPException
from models import Orden
from dbutils.pooled_db import PooledDB
import MySQLdb
import os
from dotenv import load_dotenv
from datetime import datetime

router = APIRouter()

load_dotenv()

db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_DATABASE"),
}

pool = PooledDB(MySQLdb, 5, **db_config)

@router.get("/ordenes", response_model=list[Orden])
def get_orders():
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_orden, monto_total, estado, id_usuario, id_cliente, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion FROM orden")
        data = cursor.fetchall()
        orders = [Orden(id_orden=row[0], monto_total=row[1], estado=row[2], id_usuario=row[3], id_cliente=row[4], creado_por=row[5], actualizado_por=row[6], ultima_actualizacion=row[7], es_activo=row[8], fecha_creacion=row[9]) for row in data]
        return orders
    finally:
        conn.close()

@router.get("/ordenes/{id_orden}", response_model=Orden)
def get_orderby_id(id_orden: int):
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_orden, monto_total, estado, id_usuario, id_cliente, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion FROM orden WHERE id_orden = %s", (id_orden,))
        data = cursor.fetchone()
        if data:
            return Orden(id_orden=data[0], monto_total=data[1], estado=data[2], id_usuario=data[3], id_cliente=data[4], creado_por=data[5], actualizado_por=data[6], ultima_actualizacion=data[7], es_activo=data[8], fecha_creacion=data[9])
        else:
            raise HTTPException(status_code=404, detail="Order not found")
    finally:
        conn.close()

@router.post("/ordenes", response_model=Orden)
def create_order(order: Orden):  
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orden (monto_total, estado, id_usuario, id_cliente, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (order.monto_total, order.estado, order.id_usuario, order.id_cliente, order.creado_por, order.actualizado_por, order.ultima_actualizacion, order.es_activo, order.fecha_creacion)
        )
        conn.commit()
        id_orden = cursor.lastrowid
        return Orden(id_orden=id_orden)
    finally:
        conn.close()


@router.put("/ordenes/{id_orden}", response_model=Orden)
def update_order(id_orden: int, updated_order: Orden):
    conn = pool.connection()

    try:
        cursor = conn.cursor()
        updated_order.ultima_actualizacion = datetime.now()
        cursor.execute(
            "UPDATE orden SET monto_total=%s, estado=%s, id_usuario=%s, id_cliente=%s, creado_por=%s, actualizado_por=%s, ultima_actualizacion=%s, es_activo=%s WHERE id_orden=%s",
            (updated_order.monto_total, updated_order.estado, updated_order.id_usuario, updated_order.id_cliente, updated_order.creado_por, updated_order.actualizado_por, updated_order.ultima_actualizacion, updated_order.es_activo, id_orden)
        )
        conn.commit()
        return updated_order
    except:
        raise HTTPException(status_code=500, detail={"error": "Order cannot be updated"})
    finally:
        cursor.close()

@router.delete("/ordenes/{id_orden}")
def delete_order(id_orden: int):
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orden WHERE id_orden = %s", (id_orden,))
        order_result = cursor.fetchone()
        if order_result is None:
            raise HTTPException(status_code=404, detail={"error": "Order not found"})
        cursor.execute("DELETE FROM orden WHERE id_orden = %s", (id_orden,))
        conn.commit()
        return {"message": f"Order with id_orden {id_orden} successfully deleted."}
    finally:
        conn.close()

