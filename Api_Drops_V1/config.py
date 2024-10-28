import os 
from dotenv import load_dotenv

load_dotenv()
class Config:
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')


def get_db_connection():
    import mysql.connector
    return mysql.connector.connect(
        host = Config.DB_HOST,
        user = Config.DB_USER,
        password = Config.DB_PASSWORD,
        database = Config.DB_NAME
    )    