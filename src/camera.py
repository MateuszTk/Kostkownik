import imutils
from imutils.video import VideoStream
import numpy as np
import cv2
import time

def StartCameras():
    global vs0
    vs0 = VideoStream( src = 0 ).start()

    # setting camera parameters
    #vs.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0) 
    #vs.stream.set(cv2.CAP_PROP_AUTO_WB, 0)
    #vs.stream.set(cv2.CAP_PROP_GAIN, 1)

    time.sleep(1)

def ReleaseCameras():
    vs0.stop()
    cv2.destroyAllWindows()
    
def ScanColors():
    frame = vs0.read()
    return frame
        

