from fastapi import APIRouter, Request, Depends, Cookie, Response
from typing import Annotated
from datetime import datetime
from db_info import SQL, get_db
from authenticate import authenticate
from dto.article import Article, ReadAllArticleResponse, UploadArticleRequest, UpdateArticleRequest


router = APIRouter(tags=["article"])

@router.get("", response_model=ReadAllArticleResponse)
def read_all_article(sql: SQL= Depends(get_db)):
    try:
        data = sql.select(f"SELECT idx, name, title, content, date FROM board WHERE is_delete = 0")
        articles = ReadAllArticleResponse(articles=[Article(**item) for item in data])
        return articles
    except:
        return Response(status_code=404, content="User not found")

@router.post("")
async def upload_article(article_data: UploadArticleRequest, jwtAuthToken: Annotated[str | None, Cookie()] = None, sql: SQL= Depends(get_db)):
    authenticate(jwtAuthToken)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try :
        sql.insert(f"INSERT INTO board (name, title, content, date) VALUES ('{article_data.name}', '{article_data.title}', '{article_data.content}', '{current_time}')")
        return Response(status_code=201, content="Upload success")
    except : 
        return Response(status_code=409, content="Already exist article_id")

@router.get("/{article_id}", response_model=Article)
def read_article(article_id: int, sql: SQL= Depends(get_db)):
    try:
        data = sql.select(f"SELECT * FROM board WHERE idx={article_id} AND is_delete != 1 LIMIT 1")
        article = Article(**data[0])
        return Response(status_code=200, content=article)
    except:
        return Response(status_code=404, content="Article not found")

@router.put("/{article_id}")
def update_article(article_id: int, article_data: UpdateArticleRequest, jwtAuthToken: Annotated[str | None, Cookie()] = None, sql: SQL= Depends(get_db)):
    authenticate(jwtAuthToken)
    if article_data.title is None or article_data.content is None:
        return Response(status_code=400, content="Bad request")
    else:
        sql.update(f"UPDATE board SET title = '{article_data.title}', content = '{article_data.content}' WHERE idx = {article_id}")
        return Response(status_code=200, content="Update success")

@router.delete("/{article_id}")
def delete_article(article_id: int, jwtAuthToken: Annotated[str | None, Cookie()] = None, sql: SQL= Depends(get_db)):
    authenticate(jwtAuthToken)
    try:
        sql.update(f"UPDATE board SET is_delete = 1 WHERE idx = {article_id}")
        return Response(status_code=200, content="Delete success")
    except:
        return Response(status_code=404, content="Article not found")

@router.get("/user/{user_id}", response_model=ReadAllArticleResponse)
def read_user_article(user_id: str, sql: SQL= Depends(get_db)):
    try:
        data = sql.select(f"SELECT title, content, date FROM board WHERE name={user_id} AND is_delete = 0")
        result = ReadAllArticleResponse(articles=[Article(**item) for item in data])
        return Response(status_code=200, content=result)
    except: 
        return Response(status_code=404, content="User not found")

@router.get("/search/{keyword}", response_model=ReadAllArticleResponse)
def search_article(keyword: str, sql: SQL= Depends(get_db)):
    data = sql.select(f"SELECT name, title, content, date FROM board WHERE title LIKE '%{keyword}%' OR content LIKE '%{keyword}%'")
    return ReadAllArticleResponse(articles=[Article(**item) for item in data])