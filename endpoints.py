from typing import Annotated
from fastapi import APIRouter, Request, Depends, Cookie, HTTPException
from datetime import datetime
from db_info import SQL
from db_info import get_db
from authenticate import authenticate

router = APIRouter()

@router.get("/article")
def read_all_article(sql: SQL= Depends(get_db)):
    data = sql.select(f"SELECT idx, name, title, content, date FROM board WHERE is_delete = 0")
    
    return data

@router.post("/article/{article_id}")
async def upload_article(article_id: int, request: Request, jwtAuthToken: Annotated[str | None, Cookie()] = None, sql: SQL= Depends(get_db)):
    authenticate(jwtAuthToken)
    data = await request.json()
    name = data.get("name")
    title = data.get("title")
    content = data.get("content")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try :
        sql.insert(f"INSERT INTO board (idx, name, title, content, date) VALUES ({article_id}, '{name}', '{title}', '{content}', '{current_time}')")
        return {"result" : "success"}
    except : 
        return {"result" : "fail"}

@router.get("/article/{article_id}")
def read_article(article_id: int, sql: SQL= Depends(get_db)):
    data = sql.select(f"SELECT * FROM board WHERE idx={article_id}")
    is_delete = sql.select(f"SELECT * FROM board WHERE idx={article_id} AND is_delete = 1")
    if data == []:
        return {"result" : "none data"}
    elif is_delete != [] :
        return {"result" : "delete data"}
    else :
        return data[0]

@router.put("/article/{article_id}")
def update_article(article_id: int, request: Request, jwtAuthToken: Annotated[str | None, Cookie()] = None, sql: SQL= Depends(get_db)):
    authenticate(jwtAuthToken)
    title = request.query_params.get("title")
    content = request.query_params.get("content")
    if title is None and content is None:
        return {"result": "fail"}
    elif content is None:
        sql.update(f"UPDATE board SET title = '{title}' WHERE idx = {article_id}")
    elif title is None:
        sql.update(f"UPDATE board SET content = '{content}' WHERE idx = {article_id}")
    else:
        sql.update(f"UPDATE board SET title = '{title}', content = '{content}' WHERE idx = {article_id}")

    return {"result": "success"}

@router.delete("/article/{article_id}")
def delete_article(article_id: int, jwtAuthToken: Annotated[str | None, Cookie()] = None, sql: SQL= Depends(get_db)):
    authenticate(jwtAuthToken)
    data = sql.select(f"SELECT * FROM board WHERE idx={article_id}")
    is_delete = sql.select(f"SELECT * FROM board WHERE idx={article_id} AND is_delete = 1")

    if data == [] :
        return {"result" : "none data"}
    elif is_delete != [] :
        return {"result" : "already delete"}
    else :
        sql.update(f"UPDATE board SET is_delete = 1 WHERE idx = {article_id}")
        return {"result" : "success"}

@router.get("/article/user/{user_id}")
def read_user_article(user_id: str, sql: SQL= Depends(get_db)):
    try : 
        data = sql.select(f"SELECT title, content, date FROM board WHERE name={user_id} AND is_delete = 0")
        return data
    except : 
        return {"result" : "fail"}

@router.get("/article/search/{keyword}")
def search_article(keyword: str, sql: SQL= Depends(get_db)):
    data = sql.select(f"SELECT name, title, content, date FROM board WHERE title LIKE '%{keyword}%' OR content LIKE '%{keyword}%'")
    
    if data != [] :
        return data
    else :
        return {"result" : "not found"}
        
@router.post("/article/{article_id}/comment")
async def reply(article_id: int, request: Request, jwtAuthToken: Annotated[str | None, Cookie()] = None, sql: SQL= Depends(get_db)) :
    authenticate(jwtAuthToken)
    data = await request.json()
    name = data.get("name")
    content = data.get("content")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if name is None or content is None :
        return {"result" : "fail"}
    else :
        sql.insert(f"INSERT INTO reply (bidx, name, content, date) VALUES({article_id}, '{name}', '{content}', '{current_time}')")
        data = sql.select(f"SELECT idx FROM reply WHERE date = '{current_time}'")
        return data[0]

@router.get("/article/{article_id}/comment")
def read_reply(article_id: int, sql: SQL= Depends(get_db)) :
    data = sql.select(f"SELECT idx, name, content, date FROM reply WHERE bidx = '{article_id}'")

    if data == [] :
        return {"result" : "fail"}
    else :
        return data

@router.get("/article/{article_id}/comment/{comment_id}")
def delete_reply(article_id: int, comment_id: int, sql: SQL= Depends(get_db)) :
    sql.update(f"UPDATE reply SET is_delete = 1 WHERE bidx = {article_id} AND idx = {comment_id}")
    data = sql.select(f"SELECT * FROM reply WHERE bidx = {article_id} AND idx = {comment_id} AND is_delete=1")

    if data == [] :
        return {"result" : "fail"}
    else :   
        return {"result" : "success"}
