import imutils
from imutils.video import VideoStream
import numpy as np
import cv2
import time
import math

cosCamX = 0
sinCamX = 0
cosCamY = 0
sinCamY = 0
cosCamZ = 0
sinCamZ = 0

width = 0
height = 0
fov = 1

def setRotation( angle ):
    global cosCamX
    global cosCamY
    global cosCamZ
    global sinCamX
    global sinCamY
    global sinCamZ
    
    cosCamX = math.cos(angle[0])
    cosCamY = math.cos(angle[1])
    cosCamZ = math.cos(angle[2])
    sinCamX = math.sin(angle[0])
    sinCamY = math.sin(angle[1])
    sinCamZ = math.sin(angle[2])

def rotateWorld( x, y, z ):
    vec = [0, 0, 0]
    rotated = [x * cosCamZ + y * sinCamZ, y * cosCamZ - x * sinCamZ]
    vec[0] = rotated[0]
    vec[1] = rotated[1]

    rotated = [vec[0] * cosCamY + z * sinCamY, z * cosCamY - vec[0] * sinCamY]
    vec[0] = rotated[0]
    vec[2] = rotated[1]

    rotated = [vec[2] * cosCamX + vec[1] * sinCamX, vec[1] * cosCamX - vec[2] * sinCamX]
    vec[2] = rotated[0]
    vec[1] = rotated[1]

    return vec

def TdToScreen( x, y, z, cdist ):
    rotated = rotateWorld(x, y, z)

    multiplier = -(0.5 * width / ((rotated[2] + cdist) * fov))
    rotated[0] *= multiplier
    rotated[1] *= multiplier

    return rotated

	
def Render( frame, angle ):	
    if frame is None:
        return

    _height, _width, channels = frame.shape
    global height
    global width
    height = _height
    width = _width
    
    setRotation(angle)

    vertices = [[(1, 0, 0),(0, 1, 0),(1, 1, 0)], [(0, 1, 1),(0, 1, 0),(1, 1, 0)]]
    for face in vertices:
        pt13 = TdToScreen(face[0][0], face[0][1], face[0][2], 2)
        pt23 = TdToScreen(face[1][0], face[1][1], face[1][2], 2)
        pt33 = TdToScreen(face[2][0], face[2][1], face[2][2], 2)

        pt1 = (int(pt13[0] + width * 0.5), int(pt13[1] + height * 0.5))
        pt2 = (int(pt23[0] + width * 0.5), int(pt23[1] + height * 0.5))
        pt3 = (int(pt33[0] + width * 0.5), int(pt33[1] + height * 0.5))
        
        triangle_cnt = np.array( [pt1, pt2, pt3] )
        cv2.drawContours(frame, [triangle_cnt], 0, (0,255,0), -1)
	
