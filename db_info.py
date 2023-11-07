import mysql.connector
from os import environ
def db_info() :
    host = environ.get('DB_HOST') or 'localhost'
    user = environ.get('DB_USER') or 'root'
    password = environ.get('DB_PASSWORD') or '1234'
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database="sac"
    )