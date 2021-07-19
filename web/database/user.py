from database.database import Databases
import uuid

# import pandas as pd

class userDB(Databases):
    def __init__(self):
        super().__init__()
        self.table = "userinfo"

    def signin(self, username, password, prof, email):
        userid = str(uuid.uuid4().hex)
        query = "INSERT INTO userinfo(userid, username, userpassword, isprof, useremail) VALUES (%s, %s, %s, %s, %s) RETURNING userid"
        stocked = (userid , username, password, prof, email)
        row = self.execute(query, stocked)
        print(row)
        self.commit()

    def user_search_by_id(self,userid):
        query = f"SELECT * FROM userinfo WHERE userid = '{userid}'; "
        row = self.execute(query)
        print(row)

    def user_password_get(self,userid):
        query = f"SELECT userpassword FROM userinfo WHERE userid = '{userid}'; "
        row = self.execute(query)[0][0]
        print(row)


if __name__ == "__main__":
    udb = userDB()
    udb.signin(username="가나다", password="fef!3f2", prof=False, email = "sta5ez1@dfjn.com")
    udb.signin(username="다나가", password="fef!3f2", prof=True, email = "sta1@dfjn.com")
    # udb.user_password_get("sta01")