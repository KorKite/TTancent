from database import Databases
import uuid

class scoreDB(Databases):
    def __init__(self):
        super().__init__()
        self.avg_score_table = "avg_score"
        self.realtime_score_table = "realtime_score"
        self.subject_name_table = "subject"
        self.user_subject_rel = "user_subject"

    def search_AVG(self,schema,table,colum,data):
        pass

    def search_realtime(self,schema,table,colum,data):
        pass

    def search_subject(self,schema,table,colum,data):
        pass

    def search_user_subject(self,schema,table,colum,data):
        pass

    def generate_class(self,schema,table,colum,data):        
        pass
