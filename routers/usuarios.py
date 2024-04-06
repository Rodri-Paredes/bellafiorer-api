from fastapi import APIRouter, HTTPException
from models import Usuario
from dbutils.pooled_db import PooledDB
import MySQLdb
import os
import hashlib
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

@router.get("/usuarios", response_model=list[Usuario])
def get_users():
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, username, password, rol, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion FROM usuario")
        data = cursor.fetchall()
        users = [Usuario(id_usuario=row[0], nombre=row[1], username=row[2], password=row[3], rol=row[4], creado_por=row[5], actualizado_por=row[6], ultima_actualizacion=row[7], es_activo=row[8], fecha_creacion=row[9]) for row in data]
        return users
    finally:
        conn.close()

@router.get("/usuarios/{id_usuario}", response_model=Usuario)
def get_userby_id(id_usuario: int):
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, username, password, rol, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion FROM usuario WHERE id_usuario = %s", (id_usuario,))
        data = cursor.fetchone()
        if data:
            return Usuario(id_usuario=data[0], nombre=data[1], username=data[2], password=data[3], rol=data[4], creado_por=data[5], actualizado_por=data[6], ultima_actualizacion=data[7], es_activo=data[8], fecha_creacion=data[9])
        else:
            raise HTTPException(status_code=404, detail="User not found")
    finally:
        conn.close()

def encrypt_password(password : str):
    if password:
        bytes_password = password.encode('utf-8')
        hashed_password = hashlib.md5(bytes_password)
        password = hashed_password
    return password.hexdigest()

@router.post("/usuarios", response_model=Usuario)
def create_user(usuario: Usuario):
    conn = pool.connection()
    try:
        usuario.password = encrypt_password(usuario.password)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuario (nombre, username, password, rol, creado_por, actualizado_por, ultima_actualizacion, es_activo, fecha_creacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (usuario.nombre, usuario.username, usuario.password, usuario.rol, usuario.creado_por, usuario.actualizado_por, usuario.ultima_actualizacion, usuario.es_activo, usuario.fecha_creacion)
        )
        conn.commit()
        id_usuario = cursor.lastrowid
    finally:
        conn.close()
    return Usuario(id_usuario=id_usuario, nombre=usuario.nombre, username=usuario.username, password=usuario.password, rol=usuario.rol, creado_por=usuario.creado_por, actualizado_por=usuario.actualizado_por, ultima_actualizacion=usuario.ultima_actualizacion, es_activo=usuario.es_activo, fecha_creacion=usuario.fecha_creacion)

@router.put("/usuarios/{id_usuario}", response_model=Usuario)
def update_user(id_usuario: int, updated_user: Usuario):
    conn = pool.connection()

    try:
        updated_user.password = encrypt_password(updated_user.password)
        cursor = conn.cursor()
        updated_user.ultima_actualizacion = datetime.now()
        cursor.execute(
            "UPDATE usuario SET nombre=%s, username=%s, password=%s, rol=%s, creado_por=%s, actualizado_por=%s, ultima_actualizacion=%s, es_activo=%s WHERE id_usuario=%s",
            (updated_user.nombre, updated_user.username, updated_user.password, updated_user.rol, updated_user.creado_por, updated_user.actualizado_por, updated_user.ultima_actualizacion, updated_user.es_activo, id_usuario)
        )
        conn.commit()
        return updated_user
    except:
        raise HTTPException(status_code=500, detail={"error": "User cannot be updated"})
    finally:
        cursor.close()

@router.delete("/usuarios/{id_usuario}")
def delete_user(id_usuario: int):
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
        user_result = cursor.fetchone()
        if user_result is None:
            raise HTTPException(status_code=404, detail={"error": "User not found"})
        cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        return {"message": f"User with id_usuario {id_usuario} successfully deleted."}
    finally:
        conn.close()
