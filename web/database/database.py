import psycopg2
import json

with open("database/dbinfo.json", "r") as f:
    dbinfo = json.load(f)

class Databases():
    def __init__(self):
        self.db = psycopg2.connect(host=dbinfo["host"], dbname=dbinfo["dbname"],user=dbinfo["user"],  password=dbinfo["password"],port=dbinfo["port"])
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self,query,args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()