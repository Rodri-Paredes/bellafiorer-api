from fastapi import APIRouter, HTTPException
from models import OrdenPedido
from dbutils.pooled_db import PooledDB
import MySQLdb
import os
from dotenv import load_dotenv
from services import ordenespedido_service

router = APIRouter()

load_dotenv()

db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_DATABASE"),
}

pool = PooledDB(MySQLdb, 5, **db_config)

@router.post("/ordenespedido", response_model=OrdenPedido)
def create_order_pedido(order_pedido: OrdenPedido):
    result = ordenespedido_service.create_orderpedido(order_pedido)
    return result

@router.get("/ordenespedido/{id_orden}", response_model=OrdenPedido)
def get_orderpedidoby_id(id_orden: int):
    result = ordenespedido_service.find_orderpedido_by_id(id_orden)
    if result is None:
        raise HTTPException(status_code=404, detail="Orden not found")
    else:
        return result
