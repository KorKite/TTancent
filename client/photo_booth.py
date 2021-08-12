# import the necessary packages
from __future__ import print_function
#from pyimagesearch.photoboothapp import PhotoBoothApp
from photoboothapp import PhotoBoothApp
from imutils.video import VideoStream
import argparse
import time
from login import Login

ap = argparse.ArgumentParser()
#ap.add_argument("-o", "--output", required=True, default = 'output',
#	help="path to output directory to store snapshots")
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())


login = Login()
userid = login.userid
classid = login.classid
classname = login.classname

# print("[INFO] warming up camera...")
# vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
# time.sleep(1.0)

#pba = PhotoBoothApp(vs, args["output"])
#print(args['output'])
pba = PhotoBoothApp(userid, classid, classname)
pba.root.mainloop()
