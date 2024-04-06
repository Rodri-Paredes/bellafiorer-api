from pydantic import BaseModel,EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Cliente(BaseModel):
    id_cliente: Optional[int] = None
    nombre: str
    direccion: str
    celular: str
    email: EmailStr
    creado_por: Optional[int] = None
    actualizado_por: Optional[int] = None
    ultima_actualizacion: Optional[datetime] = None
    es_activo: Optional[bool] = True
    fecha_creacion: Optional[datetime] = None

class Producto(BaseModel):
    id_producto: Optional[int] = None
    nombre: str
    descripcion: str
    precio: float
    stock: int
    creado_por: Optional[int] = None
    actualizado_por: Optional[int] = None
    ultima_actualizacion: Optional[datetime] = None
    es_activo: Optional[bool] = True
    fecha_creacion: Optional[datetime] = None

class UsuarioRoles(str, Enum):
    admin = "admin"
    vendedor = "vendedor"

class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    nombre: str
    username: str
    password: str
    rol: UsuarioRoles
    creado_por: Optional[int] = None
    actualizado_por: Optional[int] = None
    ultima_actualizacion: Optional[datetime] = None
    es_activo: Optional[bool] = True
    fecha_creacion: Optional[datetime] = None

class OrdenEstado(str, Enum):
    pedido = "pedido"
    reserva = "reserva"
    vendido = "vendido"
    cancelado = "cancelado"

class Detalle(BaseModel):
    id_detalle: Optional[int] = None
    id_orden: Optional[int] = None
    producto: Producto
    cantidad: int
    precio_unitario: float
    subtotal: float
    creado_por: Optional[int] = None
    actualizado_por: Optional[int] = None
    ultima_actualizacion: Optional[datetime] = None
    es_activo: Optional[bool] = True
    fecha_creacion: Optional[datetime] = None

class Orden(BaseModel):
    id_orden: Optional[int] = None
    monto_total: float
    estado: OrdenEstado
    usuario: Optional[Usuario] = None
    cliente: Optional[Cliente] = None
    detalles: List[Detalle] = []
    creado_por: Optional[int] = None
    actualizado_por: Optional[int] = None
    ultima_actualizacion: Optional[datetime] = None
    es_activo: Optional[bool] = True
    fecha_creacion: Optional[datetime] = None

class MetodoPago(str, Enum):
    EFECTIVO = "EFECTIVO"
    QR = "QR"
    TRANSFERENCIA = "TRANSFERENCIA"

class OrdenCancelado(Orden):
    motivo_cancelacion: str

class OrdenPedido(Orden):
    fecha_entrega: datetime

class OrdenReserva(Orden):
    monto_pagado: float
    metodo_pago: MetodoPago

class OrdenVendido(Orden):
    fecha_venta: datetime
    saldo_cancelado: float
    metodo_pago:MetodoPago
