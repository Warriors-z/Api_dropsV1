import os 

class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'univalle')
    DB_NAME = os.getenv('DB_NAME', 'db_drops')


def get_db_connection():
    import mysql.connector
    return mysql.connector.connect(
        host = Config.DB_HOST,
        user = Config.DB_USER,
        password = Config.DB_PASSWORD,
        database = Config.DB_NAME
    )    