import imutils
from imutils.video import VideoStream
import numpy as np
import cv2
import time
import math
from operator import itemgetter
from typing import NamedTuple
	
font = cv2.FONT_HERSHEY_SIMPLEX

def GetConsole(text, L_click, consolePrevMouseY, scroll, mouseY):
    frame = np.zeros((480, 800, 3), np.uint8)
    frame[:,:] = (50, 50, 50)
    
    if L_click:
        if consolePrevMouseY != -1:
            scroll -= consolePrevMouseY - mouseY
        
        consolePrevMouseY = mouseY
    else:
        consolePrevMouseY = -1

    maxHeight = 0
    output = ''
    
    for line in text:
        for letter in line:
            box = cv2.getTextSize(output + letter, font, 0.5, 1)
            if letter == '\n' or box[0][0] >= 610:
                maxHeight += 20
                
                if box[0][0] >= 600:
                    output = letter
                else:
                    output = ''
            else:
                output += letter
    
    if scroll < 0:
        scroll = 0
    
    height = -maxHeight + 480 + scroll - 10
    
    if height > 0:
        scroll -= height
        height = 0
    
    for line in text:
        for letter in line:
            box = cv2.getTextSize(output + letter, font, 0.5, 1)
            if letter == '\n' or box[0][0] >= 610:
                height += 20
                cv2.putText(frame,output,(0, height), font, 0.5,(255,255,255),1,cv2.LINE_AA)
                
                if box[0][0] >= 600:
                    output = letter
                else:
                    output = ''
            else:
                output += letter
        
    
    return frame, consolePrevMouseY, scroll
