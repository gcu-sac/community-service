from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
from datetime import datetime
import db_info

app = FastAPI()
templates = Jinja2Templates(directory='./')



import mysql.connector

class SQL:
    def __init__(self):
        self.db = db_info.db_info()

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

sql = SQL()
# @app.get("/community/article/{article_id}")
# def upload_article(article_id: int, request: Request):
#     name = request.query_params.get("name")
#     title = request.query_params.get("title")
#     content = request.query_params.get("content")
#     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     try :
#         sql.insert(f"INSERT INTO board (idx, name, title, content, date) VALUES ({article_id}, '{name}', '{title}', '{content}', '{current_time}')")
#         return {"result" : "success"}
#     except : 
#         return {"result" : "fail"}

# @app.get("/community/article/{article_id}")
# def read_article(article_id: int):
#     data = sql.select(f"SELECT * FROM board WHERE idx={article_id}")
#     is_delete = sql.select(f"SELECT * FROM board WHERE idx={article_id} AND is_delete = 1")
#     if data == [] :
#         return {"result" : "none data"}
#     elif is_delete != [] :
#         return {"result" : "delete data"}
#     else :
#         return data[0]

# @app.get("/community/article/{article_id}")
# def update_article(article_id: int, request : Request):
#     title = request.query_params.get("title")
#     content = request.query_params.get("content")

#     if title is None and content is None :
#         return {"result" : "fail"}
#     elif content is None : 
#         sql.update(f"UPDATE board SET title={title} WHERE idx = {article_id}")
#     elif title is None :
#         sql.update(f"UPDATE board SET content={content} WHERE idx = {article_id}")
#     else :
#         sql.update(f"UPDATE board SET title = {title}, content={content} WHERE idx = {article_id}")
    
#     return {"result" : "success"}

# @app.get("/community/article/{article_id}")
# def delete_article(article_id: int):
#     data = sql.select(f"SELECT * FROM board WHERE idx={article_id}")
#     is_delete = sql.select(f"SELECT * FROM board WHERE idx={article_id} AND is_delete = 1")

#     if data == [] :
#         return {"result" : "none data"}
#     elif is_delete != [] :
#         return {"result" : "already delete"}
#     else :
#         sql.update(f"UPDATE board SET is_delete = 1 WHERE idx = {article_id}")
#         return {"result" : "success"}

# @app.get("/community/article/{user_id}")
# def read_user_article(user_id: str):
#     try : 
#         data = sql.select(f"SELECT title, content, date FROM board WHERE name={user_id} AND is_delete = 0")
#         return data
#     except : 
#         return {"result" : "fail"}

# @app.get("/community/article/search/{keyword}")
# def search_article(keyword: str):
#     data = sql.select(f"SELECT name, title, content, date FROM board WHERE title LIKE '%{keyword}%' OR content LIKE '%{keyword}%'")
    
#     if data != [] :
#         return data
#     else :
#         return {"result" : "not found"}
        
# @app.get("/community/article/{article_id}/comment")
# def reply(article_id: int, request: Request) :
#     name = request.query_params.get("name")
#     content = request.query_params.get("content")
#     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#     if name is None or content is None :
#         return {"result" : "fail"}
#     else :
#         sql.insert(f"INSERT INTO reply (bidx, name, content, date) VALUES({article_id}, '{name}', '{content}', '{current_time}')")
#         data = sql.select(f"SELECT idx FROM reply WHERE date = '{current_time}'")
#         return data[0]

# @app.get("/community/article/{article_id}/comment")
# def read_reply(article_id: int) :
#     data = sql.select(f"SELECT idx, name, content, date FROM reply WHERE bidx = '{article_id}'")

#     if data == [] :
#         return {"result" : "fail"}
#     else :
#         return data

@app.get("/community/article/{article_id}/comment/{comment_id}")
def delete_reply(article_id: int, comment_id: int) :
    sql.update(f"UPDATE reply SET is_delete = 1 WHERE bidx = {article_id} AND idx = {comment_id}")
    data = sql.select(f"SELECT * FROM reply WHERE bidx = {article_id} AND idx = {comment_id} AND is_delete=1")

    if data == [] :
        return {"result" : "fail"}
    else :   
        return data