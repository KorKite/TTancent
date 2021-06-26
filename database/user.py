from database import Databases

class userDB(Databases):
    def __init__(self):
        super().__init__()
        self.table = "user"

    def signin(self,schema,table,colum,data):
        pass

    def user_search(self,schema,table,colum,data):
        pass
