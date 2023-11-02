from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
from datetime import datetime
import db_info

app = FastAPI()
templates = Jinja2Templates(directory='./')

# MySQL 연결 설정
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="0000",
#     database="sa"
# )

db = db_info.db_info()

def select(sql) :
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    return data

def insert(sql) :
	cursor = db.cursor(dictionary=True)
	cursor.execute(sql)
	db.commit()
	cursor.close()

update = insert

@app.get("/")
def index(request: Request) :
	data_list = select("SELECT * FROM board WHERE is_delete = 0 ORDER BY date desc")
	# return data_list
	return templates.TemplateResponse('./noticeboard/index.html', context={"request":request, "data_list":data_list})

@app.get("/write")
def write(request: Request) :
	return templates.TemplateResponse('./noticeboard/write.html', context={"request":request})

@app.get("/check_write")
def check_write(request: Request):
    # Request 객체에서 쿼리 매개변수 가져오기
	name = request.query_params.get("name")
	title = request.query_params.get("title")
	content = request.query_params.get("content")
	current_time = datetime.now()

	insert(f"INSERT INTO board (name, title, content, date) VALUES ('{name}', '{title}', '{content}', '{current_time}')")
	return RedirectResponse(url="/")

@app.get("/read")
def read(request: Request):
	idx = request.query_params.get("idx")
	data = select(f"SELECT * FROM board WHERE idx={idx}")
	data = data[0]
	update(f"UPDATE board SET hit = hit+1 WHERE idx = {idx}")
	
	return templates.TemplateResponse('./noticeboard/read.html', context={"request":request,
																		#   "name" : data.name,
																		  "title" : data['title'],
																		  "content" : data['content'],
																		  "date" : data['date'],
																		  "hit" : data['hit']})

@app.get("/delete")
def delete(request: Request):
	idx = request.query_params.get("idx")
	update(f"UPDATE board SET is_delete = 1 WHERE idx = {idx}")
	return RedirectResponse(url="/")

@app.get("/reply")
def delete(request: Request):
	idx = request.query_params.get("idx")
	name = request.query_params.get("name")
	content = request.query_params.get("content")
	insert(f"INSERT board SET is_delete = 1 WHERE idx = {idx}")
	return RedirectResponse(url="/read?idx="+idx)