from database import Databases
# import pandas as pd

class userDB(Databases):
    def __init__(self):
        super().__init__()
        self.table = "userinfo"

    def signin(self,userid , username, password, prof, email):
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
    # udb.signin(userid = "sta03", username="Injei", password="fef!3f2", prof=False, email = "sta5e@dfjn.com")
    udb.user_password_get("sta01")