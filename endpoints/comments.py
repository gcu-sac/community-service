from fastapi import APIRouter, Request, Depends, Cookie, Response, HTTPException
from typing import Annotated
from datetime import datetime
from db_info import SQL, get_db
from authenticate import authenticate

from dto.comment import UploadCommentRequest, Comment, CommentList

router = APIRouter(tags=["comment"])

@router.post("/{article_id}/comment", status_code=201)
async def reply(article_id: int, comment_data: UploadCommentRequest, jwtAuthToken: Annotated[str | None, Cookie()] = None, sql: SQL= Depends(get_db)):
    await authenticate(jwtAuthToken)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if comment_data.name is None or comment_data.content is None:
        raise HTTPException(status_code=400, detail="Bad Request")
    else:
        sql.insert(f"INSERT INTO reply (bidx, name, content, date) VALUES({article_id}, '{comment_data.name}', '{comment_data.content}', '{current_time}')")
        return

@router.get("/{article_id}/comment", response_model=CommentList)
async def read_reply(article_id: int, sql: SQL= Depends(get_db)):
    try:
        data = sql.select(f"SELECT idx, name, content, date FROM reply WHERE bidx = {article_id} AND is_delete != 1")
        return CommentList(comments=[Comment(**item) for item in data])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Article not found")

@router.delete("/{article_id}/comment/{comment_id}")
async def deleteReply(article_id: int, comment_id: int, jwtAuthToken: Annotated[str | None, Cookie()] = None, sql: SQL = Depends(get_db)):
    await authenticate(jwtAuthToken)
    try:
        sql.update(f"UPDATE reply SET is_delete = 1 WHERE bidx = {article_id} AND idx = {comment_id}")
        return
    except:
        raise HTTPException(status_code=404, detail="Comment not found")