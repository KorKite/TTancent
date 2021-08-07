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
from model.test import test
import torch
from queue import Queue

class PhotoBoothApp:
    def __init__(self, vs, outputPath):
        self.vs = vs
        self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.thread2 = None
        self.stopEvent = None

        self.root = tki.Tk()
        self.panel = None


        def get_text():
            text = entry.get()
            print(text)
            label.config(text="현재 수업 코드: "+str(eval(text)))
            with open(self.outputPath+"/class_code.txt", "w") as file:
                file.write(text)
                file.close()
            

        q = Queue()
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=(q,))
        self.thread.start()

        self.thread2 = threading.Thread(target=self.bridge, args=(q,))
        
        label = tki.Label(self.root)
        label.pack()

        entry = tki.Entry(self.root)
        entry.pack()

        button = tki.Button(self.root, text = "수업코드 입력", command = get_text)
        button.pack()

        start_btn = tki.Button(self.root, text = "시작", command= self.thread2.start)
        start_btn.pack(fill="both", expand="yes", padx=5, pady=5)

        end_btn = tki.Button(self.root, text = "종료", command=self.onClose)
        end_btn.pack(fill="both", expand="yes", padx=5, pady=5)

        self.root.wm_title("PyImageSearch PhotoBooth")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        self.root.mainloop()


    # def videoLoop(self):
    #     try:
    #         while True: #not self.stopEvent.is_set()
    #             self.frame = self.vs.read()
    #             self.frame = imutils.resize(self.frame, width=300)

    #             image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
    #             image = Image.fromarray(image)
    #             image = ImageTk.PhotoImage(image)

    #             if self.panel is None:
    #                 self.panel = tki.Label(image=image)
    #                 self.panel.image = image
    #                 self.panel.pack(side="left", padx=10, pady=10)

    #             else:
    #                 self.panel.configure(image=image)
    #                 self.panel.image = image

    #     except RuntimeError:
    #         print("[INFO] caught a RuntimeError")

    # def takeShots(self): 
    #     ts = datetime.datetime.now()
    #     filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
    #     print(self.outputPath)
    #     p = os.path.sep.join((self.outputPath, filename))

    #     cv2.imwrite(p, self.frame.copy())
    #     print("[INFO] saved {}".format(filename))
            
    #     time.sleep(0.1)
    #     time.sleep(0.5)
    #     return p

    def videoLoop(self, q):

        try:
            while not self.stopEvent.is_set():
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=300)

                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)

                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

                q.put(self.frame)                

        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def bridge(self, q):

        print("sub thread start ")

        while not self.stopEvent.is_set():

            for i in range(1000):
                temp_frame = q.get()

            self.shots(temp_frame)

            time.sleep(5)
    

    def shots(self, temp_frame):

        if temp_frame is None:
            print("frame is None")
                
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.sep.join((self.outputPath, filename)) 

        cv2.imwrite(p, temp_frame.copy())
        print("[INFO] saved {}".format(filename))
        self.ttancent(p)



    def ttancent(self, path):
        # load model
        model = Resnext() 
        model.to(torch.device('cpu'))
        model.load_state_dict(torch.load('C:/Users/USER/Desktop/4-1-2/2021_coco/TTancent/client/model/models/model_eye.pt', map_location=torch.device('cpu')))
        
        # take shots
        # path = self.takeShots()
        # path = 'C:/Users/USER/Desktop/4-1-2/2021_coco/TTancent/client/output/2021-08-06_18-24-19.jpg'
        # path = 'C:/Users/USER/Desktop/4-1-2/2021_coco/TTancent/client/output/19_0_3_20170119152737588.jpg'
        # print(test(path, model))

        
        scores = test(path, model)
        print('[Score] for left eye {:.2f}'.format(scores[0]))
        print('[Score] for right eye {:.2f}'.format(scores[1]))

 

    def onClose(self):
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()
        

