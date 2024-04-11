from fastapi import APIRouter, HTTPException
from models import Cliente
from datetime import datetime
from services import clientes_service
from database import get_db_connection

router = APIRouter()

@router.get("/clientes", response_model=list[Cliente],tags=["clientes"])
def get_clientes():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nombre, direccion, celular, email, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion FROM cliente")
        data = cursor.fetchall()
        clientes = [Cliente(id_cliente=row[0], nombre=row[1], direccion=row[2], celular=row[3], email=row[4], creado_por=row[5], actualizado_por=row[6], ultima_actualizacion=row[7], es_activo=row[8], fecha_creacion=row[9]) for row in data]
        return clientes
    finally:
        conn.close()

@router.get("/clientes/{id_cliente}", response_model=Cliente,tags=["clientes"])
def get_cliente_by_id(id_cliente: int):
    result = clientes_service.find_cliente_by_id(id_cliente)
    if result is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    else:
        return result


@router.post("/clientes", response_model=Cliente,tags=["clientes"])
def create_cliente(cliente: Cliente):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cliente (nombre, direccion, celular, email, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (cliente.nombre, cliente.direccion, cliente.celular, cliente.email, cliente.creado_por, cliente.actualizado_por, cliente.ultima_actualizacion, cliente.es_activo, cliente.fecha_creacion)
        )
        conn.commit()
        id_cliente = cursor.lastrowid
    finally:
        conn.close()
    return Cliente(id_cliente=id_cliente, nombre=cliente.nombre, direccion=cliente.direccion, celular=cliente.celular, email=cliente.email, creado_por=cliente.creado_por, actualizado_por=cliente.actualizado_por, ultima_actualizacion=cliente.ultima_actualizacion, es_activo=cliente.es_activo, fecha_creacion=cliente.fecha_creacion)

@router.put("/clientes/{id_cliente}", response_model=Cliente,tags=["clientes"])
def put_cliente(id_cliente: int, updated_cliente: Cliente):
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        updated_cliente.ultima_actualizacion = datetime.now()
        cursor.execute(
            "UPDATE cliente SET nombre=%s, direccion=%s, celular=%s, email=%s, creado_por=%s, actualizado_por=%s, ultima_actualizacion=%s, es_activo=%s WHERE id_cliente=%s",
            (updated_cliente.nombre, updated_cliente.direccion, updated_cliente.celular, updated_cliente.email, updated_cliente.creado_por, updated_cliente.actualizado_por, updated_cliente.ultima_actualizacion, updated_cliente.es_activo, id_cliente)
        )
        conn.commit()
        return updated_cliente
    except:
        raise HTTPException(status_code=500, detail={"error": "Cliente cannot be updated"})
    finally:
        cursor.close()


@router.delete("/clientes/{id_cliente}",tags=["clientes"])
def delete_cliente(id_cliente: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cliente WHERE id_cliente = %s", (id_cliente,))
        cliente_result = cursor.fetchone()
        if cliente_result is None:
            raise HTTPException(status_code=404, detail={"error": "Cliente not found"})
        cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,))
        conn.commit()
        return {"message": f"Cliente with id_cliente {id_cliente} successfully deleted."}
    finally:
        conn.close()