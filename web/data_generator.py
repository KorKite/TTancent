from application import user
from database.score import scoreDB
from database.user import userDB

sDB = scoreDB()
uDB = userDB()

# sDB.generate_class("5fe6329cfc784eae995f9550fc4a2d0b", "Confusionism")
sDB.write_user_score("5fe6329cfc784eae995f9550fc4a2d0b      ", "fb15125d353c4dc88d2b00afdf9cd652   ", 30)
sDB.write_user_score("5fe6329cfc784eae995f9550fc4a2d0b      ", "fb15125d353c4dc88d2b00afdf9cd652   ", 90)
sDB.write_user_score("5fe6329cfc784eae995f9550fc4a2d0b      ", "fb15125d353c4dc88d2b00afdf9cd652   ", 40)
sDB.write_user_score("bdd6de482e354595ab04eae2504565d4      ", "fb15125d353c4dc88d2b00afdf9cd652   ", 40)
sDB.write_user_score("bdd6de482e354595ab04eae2504565d4      ", "fb15125d353c4dc88d2b00afdf9cd652   ", 90)
sDB.write_user_score("bdd6de482e354595ab04eae2504565d4      ", "fb15125d353c4dc88d2b00afdf9cd652   ", 60)
sDB.write_user_score("4bd79a5930e5470a8d721177e8c6d494      ", "fb15125d353c4dc88d2b00afdf9cd652   ", 60)
sDB.write_user_score("4bd79a5930e5470a8d721177e8c6d494      ", "fb15125d353c4dc88d2b00afdf9cd652   ", 64)
sDB.write_user_score("4bd79a5930e5470a8d721177e8c6d494      ", "fb15125d353c4dc88d2b00afdf9cd652   ", 90)