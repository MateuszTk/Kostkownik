
import imutils
from imutils.video import VideoStream
import numpy as np
import cv2

import time


# START KAMERY
def startKamery():
	global vs
	vs = VideoStream(src=0).start()

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
	
	
	if key == ord("r"):	
		kolory[2] = wykryjObiekt(frame, 240, 240)
		print(colorStr[2])
		print(kolory[2])
	
	if key == ord("o"):	
		kolory[4] = wykryjObiekt(frame, 240, 240)
		print(colorStr[4])
		print(kolory[4])
		
	if key == ord("b"):	
		kolory[0] = wykryjObiekt(frame, 240, 240)
		print(colorStr[0])
		print(kolory[0])
		
	if key == ord("g"):	
		kolory[1] = wykryjObiekt(frame, 240, 240)
		print(colorStr[1])
		print(kolory[1])
		
	if key == ord("y"):	
		kolory[3] = wykryjObiekt(frame, 240, 240)
		print(colorStr[3])
		print(kolory[3])
		
	if key == ord("w"):	
		kolory[5] = wykryjObiekt(frame, 240, 240)
		print(colorStr[5])
		print(kolory[5])
		
	if key == ord("c"):
		for x in range(0, 3):
			for y in range(0, 3):
				najb = 1000000
				najbKolor = 88
				color = wykryjObiekt(frame, x * 140 + 100, y * 140 + 100)	
				for k in range(0, 6):
					kolor = abs(color[0] - kolory[k][0]) + abs(color[1] - kolory[k][1]) + abs(color[2] - kolory[k][2])
					if kolor < najb:
						najb = kolor
						najbKolor = k
				result[x][y] = colorStr[najbKolor]
			
		#print(color)
		print(result)
	for a in range(0, 3):
		for b in range(0, 3):
			drawCircle(a * 140 + 100, b * 140 + 100)	
	cv2.imshow("Frame", frame)
	
 	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
		
vs.stop()
vs.release()
cv2.destroyAllWindows()

