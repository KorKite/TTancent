import requests

def login_valid(useremail, password, classid):
    form = requests.get(f"http://junxxuh.gabia.io/clientvalid/{useremail}/{password}/{classid}").json()
    return form 


if __name__ == "__main__":
    print(login_valid("test@test", "test")) # Sucess Case
    print(login_valid("ttt@ttt", "ttt")) # False Case1 -> No Email
    print(login_valid("test@test", "ttt")) # False Case2 -> Password Wrong
    print(login_valid(None, None)) # False Case2 -> Password Wrong
