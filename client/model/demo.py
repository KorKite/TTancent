from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
from get_score import TTancent

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()
ttancent = TTancent()
COLORS = [(0,0,255), (0,0,0)]

while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	# grab the frame dimensions and convert it to a blob
	# (h, w) = frame.shape[:2]
	# blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    # show the output frame
	crt_score, avg_score, (re, le), face_coord = ttancent.ttancent_score(frame)
	head = 50
	right = 250
	if re is not None: 
		cv2.rectangle(frame, (re[0], re[1]+5), (re[2], re[3]-5), COLORS[0], 1)
	if le is not None:
		cv2.rectangle(frame, (le[0], le[1]+5), (le[2], le[3]-5), COLORS[0], 1)
	if face_coord is not None:
		cv2.rectangle(frame, (face_coord[0], face_coord[1]), (face_coord[2], face_coord[3]),
				COLORS[0], 1)
		head = min(face_coord[1], 250)
		right = min(face_coord[2], 300)

	cv2.putText(frame, 'Current : '+str(round(crt_score, 3)), (right, head),
				cv2.FONT_HERSHEY_COMPLEX, 0.5, COLORS[0], 1)
	cv2.putText(frame, 'Average : '+str(round(avg_score, 3)), (right, head+20),
			cv2.FONT_HERSHEY_COMPLEX, 0.5, COLORS[0], 1) 

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
	# update the FPS counter
	fps.update()