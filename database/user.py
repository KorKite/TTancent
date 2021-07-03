from database import Databases
import pandas as pd

class userDB(Databases):
    def __init__(self):
        super().__init__()
        self.table = "userinfo"

    def signin(self):
        query = "SELECT * FROM CLASS"
        row = self.execute(query)
        print(row)

    def user_search(self,schema,table,colum,data):
        pass

if __name__ == "__main__":
    udb = userDB()
    udb.signin()