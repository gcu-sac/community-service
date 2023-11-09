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


class SQL:
    def __init__(self):
        self.db = db_info()

    def select(self, sql):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return data

    def insert(self, sql):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute(sql)
        self.db.commit()
        cursor.close()

    def update(self, sql):
        self.insert(sql)

    def close(self):
        self.db.close()


def get_db():
    sql = SQL()
    try:
        yield sql
    finally:
        sql.close()