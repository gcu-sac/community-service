from pydantic import BaseModel
from typing import List
from datetime import datetime

class Article(BaseModel):
    idx: int
    nick_name: str
    title: str
    content: str
    date: datetime

class ReadAllArticleResponse(BaseModel):
    articles: List[Article]

class UploadArticleRequest(BaseModel):
    nick_name: str
    title: str
    content: str

class UpdateArticleRequest(BaseModel):
    title: str
    content: str