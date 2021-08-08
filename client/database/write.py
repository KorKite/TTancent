from database.database import Databases
import time
import uuid

class writer(Databases):
    def __init__(self):
        super().__init__()
    
    def write_user_score(self, userid, classid, score):
        """
        유저의 점수를 기록
        """
        createdAt = time.localtime(time.time())
        id = str(uuid.uuid4().hex)
        query = "INSERT INTO user_class_rel(id, userid, classid, score, createdAt) VALUES (%s, %s, %s, %s, NOW()) RETURNING id"
        stocked = (id, userid, classid, score)
        row = self.execute(query, stocked)
        self.commit()

    