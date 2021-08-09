from database.database import Databases
import uuid
import time

class scoreDB(Databases):
    def __init__(self):
        super().__init__()
        self.avg_score_table = "avg_score"
        self.realtime_score_table = "realtime_score"
        self.subject_name_table = "subject"
        self.user_subject_rel = "user_subject"

    def return_all(self):
        query = "SELECT * FROM public.user_class_rel"
        row = self.execute(query)
        print(row)

    def search_AVG(self,userid):
        """ 
        유저의 평균 반환
        """
        query = f"SELECT * FROM public.userrank WHERE userid = '{userid}'"
        row = self.execute(query)
        print(row)
        return row


    def user_Rank(self):
        """
        유저별 평균을 묶어서 반환, groupby로 유저 묶고, 해당 그룹의 평균 값을 리턴
        return: 평균 묶어서 반환한 값 
        """
        query = "SELECT public.userinfo.userid,username, AVG(score) FROM public.user_class_rel, public.userinfo WHERE  public.userinfo.userid = public.user_class_rel.userid  GROUP BY public.userinfo.userid ORDER BY AVG(score) DESC"
        row = self.execute(query)
        return row

    def class_Rank(self):
        """
        과목별 평균을 묶어서 반환, groupby로 유저 묶고, 해당 그룹의 평균 값을 리턴
        return: 평균 묶어서 반환한 값 
        """
        query = "SELECT classid, AVG(score) FROM public.user_class_rel GROUP BY classid ORDER BY AVG(score) DESC"
        row = self.execute(query)
        print(row)


    def search_subject_classname(self, classname):
        """
        과목명
        해당 과목이 존재하는지 여부를 반환
        return: True, False
        """
        query = f"SELECT * FROM public.class where classname = '{classname}'"
        row = self.execute(query)
        print(row)


    def write_user_score(self, userid, classid, score):
        """
        유저의 점수를 기록
        """
        createdAt = time.localtime(time.time())
        id = str(uuid.uuid4().hex)
        query = "INSERT INTO user_class_rel(id, userid, classid, score, createdAt) VALUES (%s, %s, %s, %s, NOW()) RETURNING id"
        stocked = (id, userid, classid, score)
        row = self.execute(query, stocked)
        print(row)
        self.commit()

    def delete_class(self, classid, userid):
        class_generator = self.execute(f"SELECT generatorid FROM class WHERE classid='{classid}'")[0][0]
        if userid != class_generator:
            return False
        else:
            query = f"DELETE FROM class WHERE classid = '{classid}' RETURNING classid"
            row = self.execute(query)
            self.commit()
            return True

    def std_summary(self, classid):
        query = f"SELECT u.userid,u.username,u.useremail, AVG(score) as avgs FROM public.user_class_rel as r JOIN public.userinfo as u ON r.userid = u.userid WHERE r.classid='{classid}' GROUP BY u.userid ORDER BY avgs DESC;"
        row = self.execute(query)
        
        return row

    def search_user_subject(self, userid, classid):
        """
        유저의 과목별 점수를 검색
        return : 점수 (INT)
        """
        query = f"SELECT score FROM public.user_class_rel WHERE userid = '{userid}' AND classid = '{classid}';"
        row = self.execute(query)
        print(row)

    def subject_AVG(self, classid):
        """
        수업을 들은 유저들을 모아서 유저들의 평균을 내서 보여준다. (새로 짜기)
        """
        query = f"SELECT classid, avg(score) FROM public.user_class_rel WHERE classid = '{classid}' GROUP BY classid ;"
        row = self.execute(query)
        
        return row
    
    def class_search(self, que):
        query = f"SELECT c.classid, c.classname, u.username, u.userid FROM public.class as c JOIN public.userinfo as u ON c.generatorid = u.userid where username ilike '%%{que}%%' OR classname ilike '%%{que}%%'"
        print(query)
        row = self.execute(query)
        return row

    def my_classes(self, userid):
        query = f"SELECT c.classid, c.classname, u.username, u.userid FROM public.class as c JOIN public.userinfo as u ON c.generatorid = u.userid WHERE u.userid = '{userid}'"
        print(query)
        row = self.execute(query)
        return row

    def class_detail(self, classid):
        query = f"SELECT c.classid, c.classname, u.username, u.userid, u.useremail FROM public.class as c JOIN public.userinfo as u ON c.generatorid = u.userid where classid ='{classid}'"
        row = self.execute(query)
        return row


    def generate_class(self, generatorid, classname):   
        """
        수업 생성자 id, 수업 이름을 받아서, 임의의 classid를 부여하고, 그것으로 수업 생성
        return : None
        """     
        classid = str(uuid.uuid4().hex)
        query = "INSERT INTO public.class(classid, generatorid, classname, isopen) VALUES (%s, %s, %s, %s) RETURNING classid"
        stocked = (classid, generatorid, classname, '1')
        row = self.execute(query, stocked)
        self.commit()
        return row
        

if __name__ == "__main__":
    udb = scoreDB()
    udb.return_all()