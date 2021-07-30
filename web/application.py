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
    rank = [
        {"name":"박연엉", "id":"39fhd", "score":80},
        {"name":"김삿갓", "id":"32tfwed", "score":70},
        {"name":"황반부", "id":"sdafew", "score":60},
        {"name":"김구여", "id":"f232fa", "score":50},
        {"name":"장독대", "id":"er2f23", "score":45.7},
        {"name":"김진주", "id":"23fs21", "score":67.2343}
    ]

    return render_template("index.html", rank=rank, length = len(rank))

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

@app.route("/generate", methods=["GET","POST"])
def generate():
    """
    generate class
    """
    if request.method == "POST":
        name = request.form.get("classname")
        info ={
            "classname": name,
            "classid": "eojf#lk12=0f3",
            "generator": "Junseo Ko",
        }
        return render_template("generate_done.html", info=info)

    return render_template("generate_class.html")

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
    return render_template("login.html")

@app.route("/logout")
def logout():
    """
    """
    return "Hello World"

@app.route("/signin")
def signin():
    """
    """
    return render_template("signin.html")

@app.route("/user/<string:userid>")
def user(userid):
    """
    유저의 상세 페이지를 보여준다.
    """
    user_info = {
        "UserId":"sta076238",
        "UserName":"고준서",
        "IsProf":True,
        "UserEmail": "sta076238@gmail.com",
        "rank":30,
        "AvgScore":90
    }
    return render_template("userinfo.html", user=user_info)

if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")