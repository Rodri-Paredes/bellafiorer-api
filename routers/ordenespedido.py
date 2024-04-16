from fastapi import APIRouter, HTTPException
from models import OrdenPedido
from services import ordenespedido_service

router = APIRouter()

@router.post("/ordenespedido", response_model=OrdenPedido,tags=["ordenespedido"])
def create_order_pedido(order_pedido: OrdenPedido):
    result = ordenespedido_service.create_orderpedido(order_pedido)
    return result

@router.get("/ordenespedido/{id_orden}", response_model=OrdenPedido,tags=["ordenespedido"])
def get_orderpedidoby_id(id_orden: int):
    result = ordenespedido_service.find_orderpedido_by_id(id_orden)
    if result is None:
        raise HTTPException(status_code=404, detail="Orden not found")
    else:
        return result

@router.get("/ordenespedido", response_model=list[OrdenPedido],tags=["ordenespedido"])
def get_all_order_pedidos():
    result = ordenespedido_service.get_all_orderpedidos()
    if result is None:
        raise HTTPException(status_code=404, detail="Orden not found")
    else:
        return result

@router.put("/ordenespedido/{id_orden}", response_model=OrdenPedido,tags=["ordenespedido"])
def put_orderpedido_by_id(id_orden: int, updated_order: OrdenPedido):
    result = ordenespedido_service.update_orderpedido(id_orden, updated_order)
    if result is None:
        raise HTTPException(status_code=404, detail="Orden not found")
    else:
        return result

@router.delete("/ordenespedido/{id_orden}" ,tags=["ordenespedido"])
def delete_orderpedido_by_id(id_orden: int):
    result = ordenespedido_service.delete_orderpedido(id_orden)
    if result is None:
        raise HTTPException(status_code=404, detail="Orden not found")
    else:
        return {"message": "Orden deleted successfully"}
