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
font = cv2.FONT_HERSHEY_SIMPLEX

mouse_array = np.array( cv2.imread(cv2.samples.findFile("./images/mouse.png")) )

faces = {   #bgr
    'U' : (240, 240, 240),
    'R' : (0, 100, 240),
    'F' : (240, 0, 0),
    'D' : (0, 240, 240),
    'L' : (0, 0, 240),
    'B' : (0, 240, 0),
    'T' : (0, 0, 0)
}


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

def Buttons( frame, mouse, mclick, mode, _color ):
    #buttons = np.full((np.shape(frame)[0], 160, 3), np.uint8(100))
    clicked = 'T'
    global width
    global faces

    scale = 60
    top = 10
    _left = 10
    _sp = 7
    
    right = np.shape(frame)[1]
    right_margin = 10
    
    width = 180
    height = 50
    
    button_margin = 10
    
    button_unselected = (100, 70, 55) #BGR
    button_selected = (130, 90, 50)
    button_pressed = (160, 115, 40)
    
    
    #color selection buttons
    
    if mode == 1:
        
        cnt = np.array( [(_left, top), (_left, top + scale), (_left + scale,  top + scale), (_left + scale, top)] )
        
        size = 60
        margin = 0
        
        cn = cv2.pointPolygonTest(cnt, tuple(mouse), True)
        if _color == 'T':
            size = 50
            margin = 5
        elif cn > 0:
            size = 58
            margin = 1
            clicked = 'N'
        
        global mouse_array
        _mouse_array = imutils.resize(mouse_array, width = size)
        frame[10 + margin:10 + margin + size, 10 + margin:10 + margin + size] = _mouse_array
        
        
        for i, (key, color) in enumerate(faces.items()):
            if key != 'T':
                
                y = (i + 1) * scale 
                sp = (i + 1) * _sp 
                left = _left

                cnt = np.array( [(left, top + y + sp), (left, top + y + scale + sp), (left + scale,  top + y + scale + sp), (left + scale, top + y + sp)] )
                cv2.drawContours(frame, [cnt], 0, color, -1)
                
                if _color == key:
                    #cv2.drawContours(frame, [cnt], 0, (255, 255, 255), -1)
                    cv2.rectangle(frame, tuple(cnt[0]), tuple(cnt[2]), (50, 50, 50), 10)
                    
                
                #cnt = np.array( [(width + left, top + y + sp), (width + left, top + y + scale + sp), (width + left + scale,  top + y + scale + sp), (width + left + scale, top + y + sp)] )
                cn = cv2.pointPolygonTest(cnt, tuple(mouse), True)
                if cn > 0:
                    if _color != key:
                        cv2.rectangle(frame, tuple(cnt[0]), tuple(cnt[2]), (50, 50, 50), 2)
                    clicked = key
    
    top = button_margin
    color = button_unselected
    
    heights = [70, 10, 130, 360, 420]
    texts = ["Cameras", "3D Preview", "Console", "Solve", "Scramble"]
    
    action = 0 #1 - solve, 2 - scramble
    for i in range(0, 5):
        top = heights[i]
        text = texts[i]
        
        cnt = np.array( [(right - width - right_margin, top), (right - width - right_margin, top + height), (right - right_margin,  top + height), (right - right_margin, top)] )
    
        if mode == i:
            color = button_pressed
        elif cv2.pointPolygonTest(cnt, tuple(mouse), True) > 0:
            color = button_selected
            if mclick:
                if i < 3:
                    mode = i
                else:
                    action = i - 2
                mclick = 0
        else:
            color = button_unselected

        cv2.drawContours(frame, [cnt], 0, color, -1)  
        box = cv2.getTextSize(text, font, 1, 2)
        cv2.putText(frame, text, (right - right_margin - int(width/2 + box[0][0]/2), top + int(height/2 + box[0][1]/2)), font, 1,(255,255,255),2 , cv2.LINE_AA)
    
    return (frame, clicked, mode, mclick, action)
	
def Render( frame, mouse, angle, fov, cdist, cubeString, selected ):
    if frame is None:
        return
    
    #cubeString = 'TUUUUUUUUTRRRRRRRRTFFFFFFFFTDDDDDDDDTLLLLLLLLTBBBBBBBB'
    global faces
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
            cubeFaces[f][i] = [cubeString[f * 9 + i], f * 9 + i]


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
                vertices.append( [[xc + 1.0, yc + 1, zc],[xc, yc + 1, zc + 1.0],[xc + 1.0, yc + 1, zc + 1.0], cubeFaces[0][FaceId(x, 2 - z)], 0.0] )
                vertices.append( [[xc + 1.0, yc + 1, zc],[xc, yc + 1, zc + 1.0],[xc, yc + 1, zc], cubeFaces[0][FaceId(x, 2 - z)], 0.0] )

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

    prev_selected = selected
    selected[0] = 100000.0
    
    for face in vertices:
        pt1 = (int(-face[0][0] + width * 0.5), int(face[0][1] + height * 0.5))
        pt2 = (int(-face[1][0] + width * 0.5), int(face[1][1] + height * 0.5))
        pt3 = (int(-face[2][0] + width * 0.5), int(face[2][1] + height * 0.5))
        
        triangle_cnt = np.array( [pt1, pt2, pt3] )
        cn = cv2.pointPolygonTest(triangle_cnt, tuple(mouse), True)
        if cn > 0 and face[3][1] != 'T' and selected[0] > face[4]:
            selected = [face[4], face[3]]

        color = list(faces[face[3][0]])
        if prev_selected[1][1] == face[3][1]:
            color[0] = min(255, color[0] + 100)
            color[1] = min(255, color[1] + 100)
            color[2] = min(255, color[2] + 100)
        
        cv2.drawContours(frame, [triangle_cnt], 0, color, -1)
        
    if not (selected[0] != 100000.0 and selected[1][0] != 'T'):
        selected[1] = ['T', -1]

    return selected
