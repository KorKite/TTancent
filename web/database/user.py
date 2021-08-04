from database.database import Databases
import uuid, bcrypt

# import pandas as pd


def hashing(plain_text_password):
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check(org, hashed):
    return bcrypt.checkpw(org, hashed)

class userDB(Databases):
    def __init__(self):
        super().__init__()

    def signin(self, username, password, prof, email):
        userid = str(uuid.uuid4().hex)
        query = "INSERT INTO USERINFO(userid, username, userpassword, isprof, useremail) VALUES (%s, %s, %s, %s, %s) RETURNING userid"
        password = hashing(password.encode('utf-8'))
        print(password)
        stocked = (userid , username, password, prof, email)
        row = self.execute(query, stocked)
        print(row)
        self.commit()

    def user_search_by_id(self,userid):
        query = f"SELECT * FROM USERINFO WHERE userid = '{userid}'; "
        row = self.execute(query)
        print(row)

    def user_password_get(self,userid):
        query = f"SELECT userpassword FROM USERINFO WHERE userid = '{userid}'; "
        row = self.execute(query)[0][0]
        print(row)


if __name__ == "__main__":
    udb = userDB()
    udb.signin(username="가나다", password="fef!3f2", prof=False, email = "sta5ez1@dfjn.com")
    udb.signin(username="다나가", password="fef!3f2", prof=True, email = "sta1@dfjn.com")
    # udb.user_password_get("sta01")