from database import Databases

class userDB(Databases):
    def __init__(self):
        super().__init__()
        self.table = "userinfo"

    def signin(self):
        print(self.db)
        query = "SELECT * FROM CLASS"
        rows = self.execute(query)
        self.commit()
        print(rows)

    def user_search(self,schema,table,colum,data):
        pass

if __name__ == "__main__":
    udb = userDB()
    udb.signin()