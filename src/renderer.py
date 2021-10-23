import imutils
from imutils.video import VideoStream
import numpy as np
import cv2
import time
import math
from operator import itemgetter
from typing import NamedTuple

cosCamX = 0.0
sinCamX = 0.0
cosCamY = 0.0
sinCamY = 0.0
cosCamZ = 0.0
sinCamZ = 0.0

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
    vec = [0.0, 0.0, 0.0]
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

def normalize(v):
    vm = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    return [v[0] / vm, v[1] / vm, v[2] / vm]

	
def Render( frame, mouse, angle, fov, cdist, cubeString, selected ):
    if frame is None:
        return

    #angle = [mouse[1] / 40.0, mouse[0] / 20.0, 0]
    
    #cubeString = 'TUUUUUUUUTRRRRRRRRTFFFFFFFFTDDDDDDDDTLLLLLLLLTBBBBBBBB'

    faces = {   #bgr
        'U' : (255, 255, 255),
        'R' : (0, 0, 255),
        'F' : (255, 0, 0),
        'D' : (0, 255, 255),
        'L' : (0, 100, 255),
        'B' : (0, 255, 0),
        'T' : (0, 0, 0),
        'S' : (255, 255, 0)
    }
    
    _height, _width, channels = frame.shape
    global height
    global width
    height = _height
    width = _width

    bounds = [[-1.5, -1.5, -1.5],[1.5, 1.5, 1.5]]

    setRotation(angle)

    cubeFaces = [[['T', -1] for columns in range(9)] for rows in range(6)]
    
    vertices = [ [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0], cubeFaces[0][0], 0.0] ]

    for f in range(0, 6):
        for i in range(0, 9):
            if (f * 9 + i) != selected[1][1]:
                cubeFaces[f][i] = [cubeString[f * 9 + i], f * 9 + i]
            else:
                cubeFaces[f][i] = ['S', f * 9 + i]

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
    vertices.append( [[-0.5, iz, -0.5],[0.5, iz, 0.5],[0.5, iz + 1, 0.5], ['T', 0], 0.0] )
    vertices.append( [[-0.5, iz, -0.5],[-0.5, iz + 1, -0.5],[0.5, iz + 1, 0.5], ['T', 0], 0.0] )
    #vertices.append( [[0, 0, 0],[0, 0, -9],[0, 1, -9], 'T', 0.0] )
    
                
    for i, face in enumerate(vertices):
        vertices[i][0] = TdToScreen(face[0][0], face[0][1], face[0][2], cdist, fov)
        vertices[i][1] = TdToScreen(face[1][0], face[1][1], face[1][2], cdist, fov)
        vertices[i][2] = TdToScreen(face[2][0], face[2][1], face[2][2], cdist, fov)
        vertices[i][4] = (vertices[i][0][2] + vertices[i][1][2] + vertices[i][2][2]) / 3.0
   
    vertices.sort(key=lambda x: x[4], reverse = True)

    selected[0] = 100000.0
    
    for face in vertices:
        pt1 = (int(-face[0][0] + width * 0.5), int(face[0][1] + height * 0.5))
        pt2 = (int(-face[1][0] + width * 0.5), int(face[1][1] + height * 0.5))
        pt3 = (int(-face[2][0] + width * 0.5), int(face[2][1] + height * 0.5))
        
        triangle_cnt = np.array( [pt1, pt2, pt3] )
        cn = cv2.pointPolygonTest(triangle_cnt, (mouse), True)
        if cn > 0 and face[3][1] != 'T' and selected[0] > face[4]:
            selected = [face[4], face[3]]
            	
        cv2.drawContours(frame, [triangle_cnt], 0, faces[face[3][0]], -1)
        
    if not (selected[0] != 100000.0 and selected[1][0] != 'T'):
        selected[1] = ['T', -1]

    return selected
