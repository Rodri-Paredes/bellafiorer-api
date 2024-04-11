from fastapi import APIRouter, HTTPException
from models import OrdenReserva
from services import ordenesreserva_service

router = APIRouter()



@router.get("/ordenesreserva/{id_orden}", response_model=OrdenReserva,tags=["ordenesreserva"])
def get_orderpedidoby_id(id_orden: int):
    result = ordenesreserva_service.find_orden_reserva_by_id(id_orden)
    if result is None:
        raise HTTPException(status_code=404, detail="Orden not found")
    else:
        return result
    
@router.post("/ordenesreserva", response_model=OrdenReserva,tags=["ordenesreserva"])
def create_orden_reserva(order_reserva: OrdenReserva):
    result = ordenesreserva_service.create_orden_reserva(order_reserva)
    return result