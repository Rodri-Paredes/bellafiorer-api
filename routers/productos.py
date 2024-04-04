from fastapi import APIRouter,HTTPException
from models import Producto
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

@router.get("/")
def read_root():
    return {"message": "hola mundo"}

@router.get("/productos", response_model=list[Producto])
def get_product():
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_producto,nombre, descripcion, precio, stock,creado_por,actualizado_por,ultima_actualizacion, es_activo,fecha_creacion FROM producto")
        data = cursor.fetchall()
        products = [Producto(id_producto=row[0],nombre=row[1], descripcion=row[2], precio=row[3], stock=row[4], creado_por=row[5],actualizado_por=row[6],ultima_actualizacion=row[7], es_activo=row[8],fecha_creacion=row[9]) for row in data]
        return products
    finally:
        conn.close()

@router.get("/productos", response_model=Producto)
def get_product():
    return {"message": "Este es el get de los productos"}

@router.get("/productos/{id_producto}", response_model=Producto)
def get_product_by_id(id_producto: int):
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_producto, nombre, descripcion, precio, stock, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion FROM producto WHERE id_producto = %s", (id_producto,))
        data = cursor.fetchone()
        if data:
            return Producto(id_producto=data[0], nombre=data[1], descripcion=data[2], precio=data[3], stock=data[4], creado_por=data[5], actualizado_por=data[6], ultima_actualizacion=data[7], es_activo=data[8], fecha_creacion=data[9])
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    finally:
        conn.close()

@router.post("/productos", response_model=Producto)
def create_product(producto: Producto):
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO producto (nombre, descripcion, precio, stock, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (producto.nombre, producto.descripcion, producto.precio, producto.stock, producto.creado_por, producto.actualizado_por, producto.ultima_actualizacion, producto.es_activo, producto.fecha_creacion)
        )
        conn.commit()
        id_producto = cursor.lastrowid
    finally:
        conn.close()
    return Producto(id_producto=id_producto, nombre=producto.nombre, descripcion=producto.descripcion, precio=producto.precio, stock=producto.stock, creado_por=producto.creado_por, actualizado_por=producto.actualizado_por, ultima_actualizacion=producto.ultima_actualizacion, es_activo=producto.es_activo, fecha_creacion=producto.fecha_creacion)

@router.put("/productos/{id_producto}", response_model=Producto)
def put_product(id_producto: int, updated_product: Producto):
    conn = pool.connection()

    try:
        cursor = conn.cursor()
        updated_product.ultima_actualizacion = datetime.now()
        cursor.execute(
            "UPDATE producto SET nombre=%s, descripcion=%s, precio=%s, stock=%s, creado_por=%s, actualizado_por=%s, ultima_actualizacion=%s, es_activo=%s WHERE id_producto=%s",
            (updated_product.nombre, updated_product.descripcion, updated_product.precio, updated_product.stock, updated_product.creado_por, updated_product.actualizado_por,updated_product.ultima_actualizacion, updated_product.es_activo, id_producto)
        )
        conn.commit()
        return updated_product
    except:
        raise HTTPException(status_code=500, detail={"error": "Product cannot be updated"})
    finally:
        cursor.close()

@router.delete("/productos/{id_producto}")
def delete_product(id_producto: int):
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM producto WHERE id_producto = %s", (id_producto,))
        product_result = cursor.fetchone()
        if product_result is None:
            raise HTTPException(status_code=404, detail={"error": "Product not found"})
        cursor.execute("DELETE FROM producto WHERE id_producto = %s", (id_producto,))
        conn.commit()
        return {"message": f"Product with id_producto {id_producto} successfully deleted."}
    finally:
        conn.close()