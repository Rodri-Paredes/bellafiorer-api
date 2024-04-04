from fastapi import FastAPI
from routers import productos

app = FastAPI()
app.include_router(productos.router, prefix="/api")
