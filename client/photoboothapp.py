from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import time
import cv2
import os
import pause
import asyncio
from model.model import Resnext
from model.get_score import TTancent
import torch
from queue import Queue
import numpy as np
from database.write import writer
from tkinter import messagebox


classid = None

COLORS = [(255, 0, 0)] 
class PhotoBoothApp:
    def __init__(self, userid, classid):
        self.vs = cv2.VideoCapture(0)
        # self.outputPath = outputPath
        self.frame = None
        self.thread = None
        # self.thread2 = None
        self.stopEvent = None 

        self.root = tki.Tk()
        self.root.resizable(False, False)
        self.panel = None
        self.end = 0
        self.userid = userid
        self.classid = classid
        self.wdb = writer()

        

        self.ttancent = TTancent()


        #def get_text():
            #global classid
            #text = entry.get()
            #classid = text
            #label.config(text="현재 수업 코드: "+str(text))
            #with open("class_code.txt", "w") as file:
            #    file.write(text)
            #    file.close()
            #return text
 
            # label.config(text="현재 수업 코드: "+str(eval(text)))
            # with open(self.outputPath+"/class_code.txt", "w") as file:
            #     file.write(text)
            #     file.close()
         
        q = Queue()

        self.stopEvent = threading.Event()  

        self.destroyEvent = threading.Event()

        self.thread = threading.Thread(target=self.videoLoop, args=(q,))
        self.thread.daemon = True
        self.thread.start()
 
        label = tki.Label(self.root, text="Empty Room", bg="navy",fg="white")
        label.pack(fill="x")

        frame_1 = tki.Frame(self.root)

        #send_btn = tki.Button(frame_1, text = "Send", command = get_text, relief="groove")
        #send_btn.pack(side="right", padx=10, pady=5)


        textEntry = tki.StringVar()
        entry = tki.Entry(frame_1, textvariable = textEntry)      
        textEntry.set("수업에 접속했습니다.")

        entry.pack(side="right", fill="x", expand=1, padx=10, pady=5)

        frame_1.pack(fill="x")


        frame_2 = tki.Frame(self.root)

        start_btn = tki.Button(frame_2, text = "Start", command = self.onStart, relief="groove")
        start_btn.pack(side="left", fill="x", padx=10, pady=5, ipadx=55)

        end_btn = tki.Button(frame_2, text = "End", command = self.onClose, relief="groove")
        end_btn.pack(fill="x", padx=10, pady=5)

        frame_2.pack(fill="x") 

        self.root.wm_title("TTancent")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose) 
        self.root.mainloop()

    def score(self, img):
        crt_score, avg_score, (re, le), face_coord = self.ttancent.ttancent_score(img)
        return crt_score, avg_score, (re, le), face_coord

    def videoLoop(self, q):
        try: 

            image = Image.fromarray(np.zeros((225,300,3)).astype('uint8'))
            image = ImageTk.PhotoImage(image)

            self.panel = tki.Label(image=image)
            self.panel.image = image
            self.panel.pack(side="bottom", fill="both", padx=10, pady=10)
           
            self.stopEvent.wait()

            scores = []
            while self.stopEvent.is_set():  
                ret, self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=300) 

                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                crt_score, avg_score, (re, le), face_coord = self.score(image)

                head = 20
                right = 185
                if re is not None: 
                    cv2.rectangle(image, (re[0], re[1]+10), (re[2], re[3]-10), COLORS[0], 1)
                if le is not None:
                    cv2.rectangle(image, (le[0], le[1]+10), (le[2], le[3]-10), COLORS[0], 1)
                if face_coord is not None:
                    cv2.rectangle(image, (face_coord[0], face_coord[1]), (face_coord[2], face_coord[3]),
                            COLORS[0], 1) 

                cv2.putText(image, 'Current : '+str(round(crt_score, 3)), (right, head),
                            0, 0.4, COLORS[0], 1)
                
                scores.append(crt_score)
                if len(scores) == 100:
                    self.wdb.write_user_score(self.userid, self.classid, int(crt_score*100))
                    scores = []
                    
                cv2.putText(image, 'Average : '+str(round(avg_score, 3)), (right, head+20),
                        0, 0.4, COLORS[0], 1) 

                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                self.panel.configure(image=image)
                self.panel.image = image

            print('1st repeat end')
            self.vs.release()
                    

        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    # def bridge(self, q):

    #     print("sub thread start ")

    #     while not self.stopEvent.is_set():

    #         for i in range(1000):
    #             temp_frame = q.get()

    #         self.shots(temp_frame)

    #         time.sleep(5)
    

    # def shots(self, temp_frame):

    #     if temp_frame is None:
    #         print("frame is None")
                
    #     ts = datetime.datetime.now()
    #     filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
    #     # p = os.path.sep.join((self.outputPath, filename)) 

    #     # cv2.imwrite(p, temp_frame.copy()) #!!수정
    #     # print("[INFO] saved {}".format(filename))
    #     self.score(temp_frame)

 
    # def ttancent(self, path):
    #     # load model
    #     model = Resnext() 
    #     model.to(torch.device('cpu'))
    #     model.load_state_dict(torch.load('./model/models/model_eye.pt', map_location=torch.device('cpu')))
        
    #     # take shots
    #     # path = self.takeShots()
    #     # path = 'C:/Users/USER/Desktop/4-1-2/2021_coco/TTancent/client/output/2021-08-06_18-24-19.jpg'
    #     # path = 'C:/Users/USER/Desktop/4-1-2/2021_coco/TTancent/client/output/19_0_3_20170119152737588.jpg'
    #     # print(test(path, model))

        
    #     scores = test(path, model)
    #     if -1 in scores:
    #         score = -1

    #     else:
    #         score = sum(scores)/2

    #     wdb.write_user_score(userid, classid, score)     

        
    #     print('[Score] for left eye {:.2f}'.format(scores[0]))
    #     print('[Score] for right eye {:.2f}'.format(scores[1]))
 
    # def score(self, img): 
    #     crt_score, avg_score = self.ttancent.ttancent_score(img)
    #     print('[Current Score] {:.2f}'.format(crt_score))
    #     print('[Average Score] {:.2f}'.format(avg_score))
    #     # scores = test(path, model)
    #     # print('[Score] for left eye {:.2f}'.format(scores[0]))
    #     # print('[Score] for right eye {:.2f}'.format(scores[1]))
 
 
    def onStart(self):
        print("[INFO] starting...")  
        self.stopEvent.set() 
        

    def onClose(self): 
        # image = Image.fromarray(np.zeros((225,300,3)).astype('uint8'))
        # image = ImageTk.PhotoImage(image)
        
        # self.panel = tki.Label(image=image)
        # self.panel.image = image
        self.vs.release()
        messagebox.showinfo('End', '5초 후에 프로그램이 종료됩니다.')
        self.panel.destroy()
        print("[INFO] closing...")
        self.stopEvent.clear()   
        self.end = 1
        time.sleep(5)
        time.sleep(2)
        self.root.destroy() 
        

