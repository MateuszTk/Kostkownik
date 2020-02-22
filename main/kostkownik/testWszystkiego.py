from pyax12.connection import Connection
import imutils
from imutils.video import VideoStream
import numpy as np
import cv2

import time

#greenLower = (0, 130, 95)
#greenUpper = (10, 255, 255)

#greenLower = (0, 130,160)
#greenUpper = (10, 255, 255)

#26 grudnia: kamera autogain=off, gain=1 reszta ustawien auto, oswietlenie sztuczne - latarka mala
# trzeba wylaczyc automatic gain: v4l2-ctl --set-ctrl gain_automatic=0
# listowanie ustawien: v4l2-ctl --list-ctrls

greenLower = (4, 100,60)
greenUpper = (11, 250, 255)



kat = 0;
serial_connection = Connection(port="/dev/ttyUSB0", baudrate=1000000)

dynamixel_id = 2
serial_connection.goto(dynamixel_id, kat, speed=512, degrees=True)
vs = VideoStream(src=0).start()

vs.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0) 
#vs.stream.set(cv2.CAP_PROP_EXPOSURE, 1) 

vs.stream.set(cv2.CAP_PROP_AUTO_WB, 1)  # DZIALA!!!!
vs.stream.set(cv2.CAP_PROP_GAIN, 1) #DZIALA, ale recznie trzeba wylaczyc automatic gain
#vs.stream.set(cv2.CAP_PROP_ISO_SPEED, 100) 





time.sleep(2.0)


while True:
	

	# grab the current frame
#	ret, frame = vs.read()
	frame = vs.read()
	
	if frame is None: # or not ret:
		break
	#frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			
			odlegloscOdSrodka = x - 320
			a = 1/16
			zmianaKata = -a * odlegloscOdSrodka
			if abs(zmianaKata) > 1 and abs(kat + zmianaKata) <= 150:
				kat += zmianaKata
			
			# if x > 450 and kat > -150+10:
				# kat -= 10
			# elif x > 330 and kat > -150+4:
				# kat -= 4
				
			# elif x < 150 and kat < 150-10:
				# kat += 10
			# elif x < 270 and kat < 150-4:
				# kat += 4


			serial_connection.goto(dynamixel_id, kat, speed=1024, degrees=True)
	
	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
		
vs.stop()
#vs.release()
cv2.destroyAllWindows()
