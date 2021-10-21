import imutils
from imutils.video import VideoStream
import numpy as np
import cv2
import time
import math
from operator import itemgetter






cosCamX = 0
sinCamX = 0
cosCamY = 0
sinCamY = 0
cosCamZ = 0
sinCamZ = 0

width = 0
height = 0

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

def TdToScreen( x, y, z, cdist, fov ):
    rotated = rotateWorld(x, y, z)

    multiplier = -(0.5 * width / ((rotated[2] + cdist) * fov))
    rotated[0] *= multiplier
    rotated[1] *= multiplier

    return rotated

	
def Render( frame, angle, fov, cdist, cubeString ):	
    if frame is None:
        return

    #cubeString = 'TUUUUUUUUTRRRRRRRRTFFFFFFFFTDDDDDDDDTLLLLLLLLTBBBBBBBB'

    faces = {   #bgr
        'U' : (255, 255, 255),
        'R' : (0, 0, 255),
        'F' : (255, 0, 0),
        'D' : (0, 255, 255),
        'L' : (0, 100, 255),
        'B' : (0, 255, 0),
        'T' : (0, 0, 0)
    }
    
    _height, _width, channels = frame.shape
    global height
    global width
    height = _height
    width = _width
    
    setRotation(angle)

    cubeFaces = [['T' for columns in range(9)] for rows in range(6)]
    
    vertices = [ [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0], cubeFaces[0][0], 0.0] ]

    for f in range(0, 6):
        for i in range(0, 9):
            cubeFaces[f][i] = cubeString[f * 9 + i]

    FaceId = lambda x, y : (y * 3 + x)
    
    for x in range(0, 3):
        for y in range(0, 3):
            for z in range(0, 3):
                xc = x - 1.5
                yc = y - 1.5
                zc = z - 1.5

                #front F
                vertices.append( [[xc + 1.0, yc, zc],[xc, yc + 1.0, zc],[xc + 1.0, yc + 1.0, zc], cubeFaces[2][FaceId(x, 2 - y)], 0.0] )
                vertices.append( [[xc + 1.0, yc, zc],[xc, yc + 1.0, zc],[xc, yc, zc], cubeFaces[2][FaceId(x, 2 - y)], 0.0] )

                #back B
                vertices.append( [[xc + 1.0, yc, zc + 1],[xc, yc + 1.0, zc + 1],[xc + 1.0, yc + 1.0, zc + 1], cubeFaces[5][FaceId(2 - x, 2 - y)], 0.0] )
                vertices.append( [[xc + 1.0, yc, zc + 1],[xc, yc + 1.0, zc + 1],[xc, yc, zc + 1], cubeFaces[5][FaceId(2 - x, 2 - y)], 0.0] )

                #down D
                vertices.append( [[xc + 1.0, yc, zc],[xc, yc, zc + 1.0],[xc + 1.0, yc, zc + 1.0], cubeFaces[3][FaceId(x,z)], 0.0] )
                vertices.append( [[xc + 1.0, yc, zc],[xc, yc, zc + 1.0],[xc, yc, zc], cubeFaces[3][FaceId(x,z)], 0.0] )

                #upper U
                vertices.append( [[xc + 1.0, yc + 1, zc],[xc, yc + 1, zc + 1.0],[xc + 1.0, yc + 1, zc + 1.0], cubeFaces[0][FaceId(2 - z,x)], 0.0] )
                vertices.append( [[xc + 1.0, yc + 1, zc],[xc, yc + 1, zc + 1.0],[xc, yc + 1, zc], cubeFaces[0][FaceId(2 - z,x)], 0.0] )

                #left L
                vertices.append( [[xc, yc, zc + 1.0],[xc, yc + 1.0, zc],[xc, yc + 1.0, zc + 1.0], cubeFaces[4][FaceId(2 - z, 2 - y)], 0.0] )
                vertices.append( [[xc, yc, zc + 1.0],[xc, yc + 1.0, zc],[xc, yc, zc], cubeFaces[4][FaceId(2 - z, 2 - y)], 0.0] )

                #right R
                vertices.append( [[xc + 1, yc, zc + 1.0],[xc + 1, yc + 1.0, zc],[xc + 1, yc + 1.0, zc + 1.0], cubeFaces[1][FaceId(z, 2 - y)], 0.0] )
                vertices.append( [[xc + 1, yc, zc + 1.0],[xc + 1, yc + 1.0, zc],[xc + 1, yc, zc], cubeFaces[1][FaceId(z, 2 - y)], 0.0] )

    iz = 1.5 
    vertices.append( [[-0.5, iz, -0.5],[0.5, iz, 0.5],[0.5, iz + 1, 0.5], 'T', 0.0] )
    vertices.append( [[-0.5, iz, -0.5],[-0.5, iz + 1, -0.5],[0.5, iz + 1, 0.5], 'T', 0.0] )
                
    for i, face in enumerate(vertices):
        vertices[i][0] = TdToScreen(face[0][0], face[0][1], face[0][2], cdist, fov)
        vertices[i][1] = TdToScreen(face[1][0], face[1][1], face[1][2], cdist, fov)
        vertices[i][2] = TdToScreen(face[2][0], face[2][1], face[2][2], cdist, fov)
        vertices[i][4] = (vertices[i][0][2] + vertices[i][1][2] + vertices[i][2][2]) / 3.0
   
    vertices.sort(key=lambda x: x[4], reverse = True)
    
    for face in vertices:
        pt1 = (int(-face[0][0] + width * 0.5), int(face[0][1] + height * 0.5))
        pt2 = (int(-face[1][0] + width * 0.5), int(face[1][1] + height * 0.5))
        pt3 = (int(-face[2][0] + width * 0.5), int(face[2][1] + height * 0.5))
        
        triangle_cnt = np.array( [pt1, pt2, pt3] )
        cv2.drawContours(frame, [triangle_cnt], 0, faces[face[3]], -1)
	
