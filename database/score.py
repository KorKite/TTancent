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
        """ 
        
        """
        pass

    def search_Rank(self):
        """
        유저별 평균을 묶어서 반환
        return: 평균 묶어서 반환한 값 
        """
        


    def search_subject(self, classid):
        """
        해당 과목이 존재하는지 여부를 반환
        return: True, False
        """
        pass

    def search_user_subject(self, userid, classid):
        """
        유저의 과목별 점수를 검색
        return : 점수 (INT)
        """
        pass

    def generate_class(self,generatorid):   
        """
        수업 생성자 id를 받아서, 임의의 classid를 부여하고, 그것으로 수업 생성
        return : None
        """     
        pass