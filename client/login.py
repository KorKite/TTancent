
# from database.write import writer
from tkinter import messagebox
import tkinter as tki


# wdb = writer()


class Session:
    def __init__(self, email, userid):
        self.email = email
        self.userid = userid
        self.valid = True

    def __str__(self):
        return self.userid


class Login:
    def __init__(self):
        self.root = tki.Tk()
        self.root.title("Login")
        self.root.geometry("255x150") 
        self.root.resizable(False, False)

        
        label = tki.Label(self.root, text="Please enter the details below", bg="navy",fg="white")
        label.pack(fill="x")

        
        self.frame_sub = tki.Frame(self.root)
        self.frame_1 = tki.Frame(self.frame_sub)

        label_email = tki.Label(self.frame_1, text="E-mail *")
        label_email.pack()

        label_pwd = tki.Label(self.frame_1, text="Password *")
        label_pwd.pack()

        self.frame_1.pack(side="left", pady=5)


        self.frame_2 = tki.Frame(self.frame_sub)

        email = tki.StringVar()
        self.etr_email = tki.Entry(self.frame_2, textvariable = email)      
        email.set("abc@1234.com")
        self.etr_email.bind('<Button-1>', lambda e: email.set(''))
        self.etr_email.pack(fill="x", expand=1, padx=10, pady=5)

        pwd = tki.StringVar()
        self.etr_pwd = tki.Entry(self.frame_2, textvariable = pwd, show="*")
        pwd.set('1234')      
        self.etr_pwd.bind('<Button-1>', lambda e: pwd.set(''))
        self.etr_pwd.pack(fill="x", expand=1, padx=10, pady=5)

        self.frame_2.pack(fill="x", padx=10, pady=5)
        self.frame_sub.pack(padx=10, pady=5)


        btn_login = tki.Button(self.root, text = "Login", relief="groove", command=self.login)
        btn_login.pack(fill="x", padx=25, pady=5)

        self.root.mainloop()

    def get_info(self):
        email = self.etr_email.get()
        pwd = self.etr_pwd.get()
        return email, pwd

    def login(self):
        email, pwd = self.get_info()

        if len(email) == 0:
            messagebox.showinfo('Warning!', 'E-mail을 한 글자 이상 입력하세요')
        elif len(pwd) == 0:
            messagebox.showinfo('Warning!', 'Password를 한 글자 이상 입력하세요')
        else:
            pass # login
            self.root.destroy()
        print(email, pwd)
        
    