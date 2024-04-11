from dotenv import load_dotenv
from dbutils.pooled_db import PooledDB
import MySQLdb
import os

load_dotenv()

def get_db_connection():
    db_config = {
            'host': os.getenv("DB_HOST"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'database': os.getenv("DB_DATABASE"),
        }
    pool = PooledDB(MySQLdb, 5, **db_config)

    return pool.connection()