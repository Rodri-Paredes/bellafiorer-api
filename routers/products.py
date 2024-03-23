from fastapi import APIRouter
from models import Producto

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "hola mundo"}

@router.get("/productos", response_model=Producto)
def get_product():
    return {"message": "Este es el get de los productos"}

@router.get("/productos/{id_producto}", response_model=Producto)
def get_product_by_id(id_producto: int):
    producto = Producto(
        id_producto=id_producto,
        nombre="Ramo de 12 Rosas",
        descripcion="Ramos de 12 rosas con papel blanco",
        precio=65,
        stock=100,
        creado_por=1,
        actualizado_por=2,
        ultima_actualizacion=None,
        es_activo=True,
        fecha_creacion=None
    )
    return producto

@router.post("/productos", response_model=Producto)
def create_product():
    producto = Producto(
        id_producto=1,
        nombre="Ramo de 12 Rosas",
        descripcion="Ramos de 12 rosas con papel blanco",
        precio=65,
        stock=100,
        creado_por=1,
        actualizado_por=2,
        ultima_actualizacion=None,
        es_activo=True,
        fecha_creacion=None
    )
    return producto

@router.put("/productos/{id_producto}", response_model=Producto)
def put_product(id_producto: int):
    return {"message": "Este es el put de los productos"}

@router.delete("/productos/{id_producto}")
def delete_product(id_producto: int):
    return {"message": "Este es el delete de los productos"}