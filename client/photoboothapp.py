# import the necessary packages
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

class PhotoBoothApp:
    def __init__(self, vs, outputPath):
        self.vs = vs
        self.outputPath = outputPath
        self.frame = None
        self.thread = None
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
            

        label = tki.Label(self.root)
        label.pack()

        entry = tki.Entry(self.root)
        entry.pack()

        button = tki.Button(self.root, text = "수업코드 입력", command = get_text)
        button.pack()

        start_btn = tki.Button(self.root, text = "시작", command=self.takeShots)
        start_btn.pack(fill="both", expand="yes", padx=5, pady=5)

        end_btn = tki.Button(self.root, text = "종료", command=self.onClose)
        end_btn.pack(fill="both", expand="yes", padx=5, pady=5)

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        self.root.wm_title("PyImageSearch PhotoBooth")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        self.root.mainloop()


    def videoLoop(self):

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

        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    async def takeShots(self):

        while True:
        
            ts = datetime.datetime.now()
            filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
            print(self.outputPath)
            p = os.path.sep.join((self.outputPath, filename))

            cv2.imwrite(p, self.frame.copy())
            print("[INFO] saved {}".format(filename))
            
            pause.until(ts+datetime.timedelta(seconds=10))

            await asyncio.sleep(10)           
        

    def onClose(self):
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()
        




