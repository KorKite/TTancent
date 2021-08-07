# Python Library
from flask import Flask, url_for, redirect, render_template, request, flash, session

# Our Custom Database Module
from database.score import scoreDB
from database.user import userDB

app = Flask(__name__)
app.secret_key = "ewlkjfo30!2jkfljs#"

udb = userDB()
sdb = scoreDB()

@app.route("/")
def index():
    """
    rank 보여주기, 다른 곳으로 링킹하는 링크버튼을 쭉 보여주기
    """
    rank = sdb.user_Rank()
    print(rank)
    rank = [{"userid":i[0], "username":i[1], "score":i[2]} for i in rank]


    return render_template("index.html", rank=rank, length = len(rank))

@app.route("/search", methods=["GET"])
def search():
    """
    수업을 검색
    DB: 교수님을 검색해도 수업이 나오고, 수업명을 검색해도 수업이 나오고, 수업 id를 검색해서 수업이 나오게.
    """
    que = request.args.get("q")
    result = sdb.class_search(que) 
    # SQL 쿼리 다시짜야해...
    if len(result) == 0:
        result = {
            "state":False
        }
    else:
        result = {
            "state": True,
            "result":result
        }
    return render_template("search_result.html", result=result)

@app.route("/class/<string:classid>")
def class_detail(classid):
    """
    수업의 세부 검색 결과 반환
    DB: 수업 한개에 대한 학생들의 집중도 평균 요약 + classid 
    """
    avg = sdb.subject_AVG(classid)
    if len(avg) ==0:
        avg_score = "수업을 시작하세요."
    else:
        avg_score = str(round(float(avg[0][1]), 3)) + "점"
    classid, subject_name, generatorname, generatorid, email  = sdb.class_detail(classid)[0]
    result = {
        "classid":classid,
        "subject_name":subject_name,
        "generatorname":generatorname,
        "generatorid":generatorid,
        "generatoremail":email,
        "avg":avg_score
    }
    return render_template("classinfo.html", result=result)

@app.route("/generate", methods=["GET","POST"])
def generate():
    """
    generate class
    """
    if request.method == "POST":

        name = request.form.get("classname")
        classid = sdb.generate_class(session["userid"], name)
        info ={
            "classname": name,
            "classid": classid[0][0],
            "generator": session["username"],
        }
        return render_template("generate_done.html", info=info)
    print(session.get("userid"), session.get("isprof"))
    if session.get("userid") and session.get("isprof") == True:
        return render_template("generate_class.html")
    else:
        return redirect(url_for("index"))

@app.route("/summary")
def summary():
    """
    수업별 요약보기
    """
    return "Hello World"




# 유저 관리 관련 URL
@app.route("/login", methods=["POST", "GET"])
def login():
    """
    """
    if request.method == "POST":
        print("redirected")
        email = request.form["email"]
        password = request.form["password"]
        valid_form = udb.login_valid(useremail=email, password=password)
        if valid_form["valid"]:
            session["userid"] = valid_form["userid"]
            session["username"] = valid_form["username"]
            session["isprof"] = valid_form["isprof"]
            return redirect(url_for("index"))
        else:
            flash("가입되지 않은 이메일이거나, 잘못된 비밀번호입니다.")
            return redirect(url_for("login"))
        

    return render_template("login.html")

@app.route("/logout")
def logout():
    """
    """
    session.clear()
    return redirect(url_for("index"))

@app.route("/signin", methods=["GET", "POST"])
def signin():
    """
    """
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]
        password_confirm = request.form["password-confirm"]
        userid = udb.signin_valid(useremail=email)
        if len(userid) == 0:
            if password == password_confirm:
                udb.signin(username=firstname+lastname, password= password, prof=False, email=email)
                return redirect(url_for("index"))
            else:
                flash("비밀번호가 일치하지 않습니다.")
        else:
            flash("이미 존재하는 아이디 입니다.")

    return render_template("signin.html")


@app.route("/user/<string:userid>")
def user(userid):
    """
    유저의 상세 페이지를 보여준다.
    """
    get_db = udb.user_search_by_id(userid)
    avg = sdb.search_AVG(userid)
    if len(avg) == 0:
        avg = 0
    else:
        avg = int(avg[0][1])

    user_info = {
        "UserId":userid,
        "UserName":get_db[0][1],
        "IsProf":get_db[0][2],
        "UserEmail": get_db[0][0],
        "rank":30,
        "AvgScore":avg
    }
    return render_template("userinfo.html", user=user_info)

if __name__ == "__main__":
    print("✅Server Run on: http://junxxuh.gabia.io")
    app.run(port=8080, debug=True, host="0.0.0.0")