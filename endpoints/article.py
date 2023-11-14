from fastapi import APIRouter, Depends, Cookie, HTTPException
from typing import Annotated
from datetime import datetime
from db_info import SQL, get_db
from authenticate import authenticate
from dto.article import Article, ReadAllArticleResponse, UploadArticleRequest, UpdateArticleRequest


router = APIRouter(tags=["article"])

@router.get("", response_model=ReadAllArticleResponse)
async def read_all_article(sql: SQL= Depends(get_db)) -> ReadAllArticleResponse:
    try:
        data = sql.select(f"SELECT idx, name, title, content, date FROM board WHERE is_delete = 0")
        count = sql.select(f"SELECT COUNT(*) FROM board WHERE is_delete = 0")
        return ReadAllArticleResponse(articles=[Article(**item) for item in data], count=count[0]["COUNT(*)"])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="User not found")

@router.post("", status_code=201)
async def upload_article(article_data: UploadArticleRequest, jwtAuthToken: Annotated[str | None, Cookie()] = None, sql: SQL= Depends(get_db)):
    print(jwtAuthToken)
    await authenticate(jwtAuthToken)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try :
        sql.insert(f"INSERT INTO board (name, title, content, date) VALUES ('{article_data.name}', '{article_data.title}', '{article_data.content}', '{current_time}')")
        return
    except Exception as e:
        print(e)
        raise HTTPException(status_code=409, detail="Already exist article_id")

@router.get("/{article_id}", response_model=Article)
async def read_article(article_id: int, sql: SQL= Depends(get_db)) -> Article:
    try:
        data = sql.select(f"SELECT idx, name, title, content, date FROM board WHERE idx={article_id} AND is_delete = 0 LIMIT 1")
        return Article(**data[0])
    except:
        raise HTTPException(status_code=404, detail="Article not found")

@router.put("/{article_id}")
async def update_article(article_id: int, article_data: UpdateArticleRequest, jwtAuthToken: Annotated[str | None, Cookie()] = None, sql: SQL= Depends(get_db)):
    await authenticate(jwtAuthToken)
    if article_data.title is None or article_data.content is None:
        raise HTTPException(status_code=400, detail="Bad request")
    else:
        sql.update(f"UPDATE board SET title = '{article_data.title}', content = '{article_data.content}' WHERE idx = {article_id}")
        return

@router.delete("/{article_id}")
async def delete_article(article_id: int, jwtAuthToken: Annotated[str | None, Cookie()] = None, sql: SQL= Depends(get_db)):
    await authenticate(jwtAuthToken)
    try:
        sql.update(f"UPDATE board SET is_delete = 1 WHERE idx = {article_id}")
        return
    except:
        raise HTTPException(status_code=404, detail="Article not found")

@router.get("/user/{nick_name}", response_model=ReadAllArticleResponse)
async def read_user_article(nick_name: str, sql: SQL= Depends(get_db)):
    try:
        data = sql.select(f"SELECT idx, name, title, content, date FROM board WHERE name='{nick_name}' AND is_delete = 0")
        count = sql.select(f"SELECT COUNT(*) FROM board WHERE name='{nick_name}' AND is_delete = 0")
        return ReadAllArticleResponse(articles=[Article(**item) for item in data], count=count[0]["COUNT(*)"])
    except:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/search/{keyword}", response_model=ReadAllArticleResponse)
async def search_article(keyword: str, sql: SQL= Depends(get_db)):
    data = sql.select(f"SELECT idx, name, title, content, date FROM board WHERE title LIKE is_delete = 0' AND (%{keyword}%' OR content LIKE '%{keyword}%')")
    count = sql.select(f"SELECT COUNT(*) FROM board WHERE title LIKE '%{keyword}%' OR content LIKE '%{keyword}%'")
    return ReadAllArticleResponse(articles=[Article(**item) for item in data], count=count[0]["COUNT(*)"])