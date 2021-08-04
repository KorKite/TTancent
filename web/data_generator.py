from application import user
from database.score import scoreDB
from database.user import userDB

sDB = scoreDB()
uDB = userDB()

# sDB.generate_class("5fe6329cfc784eae995f9550fc4a2d0b", "Confusionism")
sDB.write_user_score("a3fdb1d60c2144049050231d2f30ed78      ", "1360a47595e7491c951bcdf009e5aa32   ", 30)
sDB.write_user_score("a3fdb1d60c2144049050231d2f30ed78      ", "1360a47595e7491c951bcdf009e5aa32   ", 90)
sDB.write_user_score("a3fdb1d60c2144049050231d2f30ed78      ", "1360a47595e7491c951bcdf009e5aa32   ", 40)
sDB.write_user_score("a3fdb1d60c2144049050231d2f30ed78      ", "1360a47595e7491c951bcdf009e5aa32   ", 40)
sDB.write_user_score("a3fdb1d60c2144049050231d2f30ed78      ", "1360a47595e7491c951bcdf009e5aa32   ", 90)
sDB.write_user_score("a3fdb1d60c2144049050231d2f30ed78      ", "1360a47595e7491c951bcdf009e5aa32   ", 60)
sDB.write_user_score("a3fdb1d60c2144049050231d2f30ed78      ", "1360a47595e7491c951bcdf009e5aa32   ", 60)