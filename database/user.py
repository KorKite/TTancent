from database import Databases
import pandas as pd

class userDB(Databases):
    def __init__(self):
        super().__init__()
        self.table = "userinfo"

    def signin(self, userid, username, password, prof, email):
        query = f"INSERT INTO userinfo (UserId, UserName, UserPassword, IsProf, UserEmail) VALUES ('{userid}', '{username}', '{password}', '{prof}', '{email}');"
        self.execute(query)

    def user_search_by_id(self,userid):
        query = f"SELECT * FROM userinfo WHERE userid = '{userid}'; "
        row = self.execute_getlow(query)
        print(row)

if __name__ == "__main__":
    udb = userDB()
    udb.signin(userid = "sta01", username="InsuKim", password="df30fsj!ef", prof=True, email = "stae@dfjn.com")
