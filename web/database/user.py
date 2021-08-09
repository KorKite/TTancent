from database.database import Databases
import uuid
from database.hasher import hash_password, verify_password

# import pandas as pd


class userDB(Databases):
    def __init__(self):
        super().__init__()

    def signin(self, username, password, prof, email):
        userid = str(uuid.uuid4().hex)
        query = "INSERT INTO USERINFO(userid, username, userpassword, isprof, useremail) VALUES (%s, %s, %s, %s, %s) RETURNING userid"
        password = hash_password(password)
        print(password)
        stocked = (userid , username, password, prof, email)
        row = self.execute(query, stocked)
        print(row)
        self.commit()

    def signin_valid(self, useremail):
        query = f"SELECT * FROM USERINFO WHERE useremail = '{useremail}'; "
        row = self.execute(query)
        return row

    def user_search_by_id(self,userid):
        query = f"SELECT useremail, username, IsProf FROM USERINFO WHERE userid = '{userid}'; "
        row = self.execute(query)
        return row

    def login_valid(self,useremail,password):
        query = f"SELECT userid, userpassword,username,isprof FROM USERINFO WHERE useremail = '{useremail}'; "
        row = self.execute(query)
        if len(row)==0:
            return {"valid":False, "reason": "There is no such email", "code":3}
        else:
            userid, hashed_pass, username,isprof = row[0]
            print(hashed_pass)
            print(verify_password(password, hashed_pass))
            if not verify_password(hashed_pass, password):
                return {"valid":False, "reason": "Password is Wrong", "code":2}
            else:
                return {"valid":True, "userid":userid, "username":username, "isprof":isprof}

if __name__ == "__main__":
    udb = userDB()
    udb.signin(username="가나다", password="fef!3f2", prof=False, email = "sta5ez1@dfjn.com")
    udb.signin(username="다나가", password="fef!3f2", prof=True, email = "sta1@dfjn.com")
    # udb.user_password_get("sta01")