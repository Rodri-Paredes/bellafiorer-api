from fastapi import FastAPI
from routers import productos, clientes, usuarios, ordenes,ordenespedido,ordenesreserva 

app = FastAPI()


app.include_router(productos.router, prefix="/api/productos")
app.include_router(clientes.router, prefix="/api/clientes")
app.include_router(usuarios.router, prefix="/api/usuarios")
app.include_router(ordenes.router, prefix="/api/ordenes")
app.include_router(ordenespedido.router, prefix="/api/ordenespedido")
app.include_router(ordenesreserva.router, prefix="/api/ordenesreserva")