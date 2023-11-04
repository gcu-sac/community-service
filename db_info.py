import mysql.connector

def db_info() :
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="sac"
    )