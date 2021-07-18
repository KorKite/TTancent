# Python Library
from flask import Flask, url_for, redirect, render_template, request

# Our Custom Database Module
from database.score import scoreDB
from database.user import userDB

app = Flask(__name__)

@app.route("/")
def index():
    """
    rank 보여주기, 다른 곳으로 링킹하는 링크버튼을 쭉 보여주기
    """
    return "Hello World"

@app.route("/search")
def search():
    """
    수업을 검색
    DB: 교수님을 검색해도 수업이 나오고, 수업명을 검색해도 수업이 나오고, 수업 id를 검색해서 수업이 나오게.
    """
    return "Hello World"

@app.route("/class/<string:classid>")
def class_detail(classid):
    """
    수업의 세부 검색 결과 반환
    DB: 수업 한개에 대한 학생들의 집중도 평균 요약 + classid 
    """
    return "Hello World"

@app.route("/generate")
def generate():
    """
    generate class
    """
    return "Hello World"

@app.route("/summary")
def summary():
    """
    수업별 요약보기
    """
    return "Hello World"




# 유저 관리 관련 URL
@app.route("/login")
def login():
    """
    """
    return "Hello World"

@app.route("/logout")
def logout():
    """
    """
    return "Hello World"

@app.route("/signin")
def signin():
    """
    """
    return "Hello World"

@app.route("/user/<string:userid>")
def user(userid):
    """
    유저의 상세 페이지를 보여준다.
    """
    return "Hello World"

if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")