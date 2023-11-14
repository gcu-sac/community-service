from pydantic import BaseModel
from typing import List
from datetime import datetime

class Comment(BaseModel):
    idx: int
    nick_name: str
    content: str
    date: datetime

class UploadCommentRequest(BaseModel):
    nick_name: str
    content: str

class CommentList(BaseModel):
    comments: List[Comment]