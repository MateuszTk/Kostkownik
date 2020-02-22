
import imutils
from imutils.video import VideoStream
import numpy as np
import cv2

import time


# START KAMERY
def startKamery():
	global vs
	vs = VideoStream(src=0).start()

	# Proba ustawiania paremtrow kamerki
	vs.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0) 
	vs.stream.set(cv2.CAP_PROP_AUTO_WB, 0) 
	vs.stream.set(cv2.CAP_PROP_GAIN, 1) 
	#vs.stream.set(cv2.CAP_PROP_ISO_SPEED, 100) 

	time.sleep(2.0)

# OBJECT DETECTION
def wykryjObiekt(PixelColor, x, y):
	#frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	pixel = hsv[x, y]
	return (pixel)

def drawCircle(a, b):
	radius = 8
	cv2.circle(frame, (int(a), int(b)), int(8),
				(0, 255, 255), 2)

startKamery()
blue = np.array([120, 160, 45])
green = np.array([70, 200, 80])
red = np.array([180, 180, 170])
yellow = np.array([24, 100, 190])
orange = np.array([6, 150, 200])
white = np.array([30, 20, 164])
kolory = np.array([blue, green, red, yellow, orange, white])
colorStr = np.array(["blue", "green", "red", "yellow", "orange", "white"])

row = np.array(["n", "n", "n"])
result = np.array([row, row, row])


while True:
	key = cv2.waitKey(1) & 0xFF
		
	frame = vs.read()
	
	if frame is None:
		break
	
	for a in range(0, 3):
		for b in range(0, 3):
			drawCircle(a * 140 + 100, b * 140 + 100)
		
	if key == ord("c"):
		for x in range(0, 3):
			for y in range(0, 3):
				najb = 1000000
				najbKolor = 88
				color = wykryjObiekt(frame, x * 140 + 100, y * 140 + 100)	
				for k in range(0, 6):
					kolor = abs(color[0] - kolory[k][0]) + abs(color[1] - kolory[k][1]) + abs(color[2] - kolory[k][2])
					#print(kolor)
					if kolor < najb:
						najb = kolor
						najbKolor = k
				result[x][y] = colorStr[najbKolor]
				#print(colorStr[najbKolor])
			
		#print(color)
		print(result)
		
	cv2.imshow("Frame", frame)
	
 	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
		
vs.stop()
vs.release()
cv2.destroyAllWindows()

