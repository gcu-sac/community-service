from pydantic import BaseModel
from typing import List, Optional

class Comment(BaseModel):
    idx: int
    name: str
    title: str
    content: str
    date: str

class UploadCommentRequest(BaseModel):
    name: str
    content: str

class CommentList(BaseModel):
    comments: List[Comment]