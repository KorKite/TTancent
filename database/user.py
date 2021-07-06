from database import Databases
# import pandas as pd

class userDB(Databases):
    def __init__(self):
        super().__init__()
        self.table = "userinfo"

    def signin(self):
        # query = "SELECT * FROM CLASS"
        query = "INSERT INTO userinfo(userid, username, userpassword, isprof, useremail) VALUES (%s, %s, %s, %s, %s) RETURNING userid"
        # row = self.execute(query)
        stock_data=('asfdf', '01011', '0', '1', '111')
        row = self.execute(query, stock_data)
        print(row)
        self.commit()



    def user_search_by_id(self,userid):
        query = f"SELECT * FROM userinfo WHERE userid = '{userid}'; "
        row = self.execute_getlow(query)
        print(row)

if __name__ == "__main__":
    udb = userDB()
    udb.signin(userid = "sta01", username="InsuKim", password="df30fsj!ef", prof=True, email = "stae@dfjn.com")
