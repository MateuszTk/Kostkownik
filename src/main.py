import time
import sys
import os
import cv2
import numpy as np
import geometrySolver as geo

module_dir = os.path.join( os.path.dirname( __file__ ), 'Solver' )
sys.path.append( module_dir )


import solver as sv
#import motor_driver as md
import camera as cam
import renderer as rend

mouseX = 0
mouseY = 0
cubeX = 0.0
cubeY = 0.0
fov = 0.35
cdist = 10
L_click = 1

def mouse(event,x,y,flags,param):
    
    global mouseX, mouseY, L_click
    
    if event == cv2.EVENT_LBUTTONDOWN:
        L_click = 1

    if event == cv2.EVENT_MOUSEMOVE:
        mouseX,mouseY = x,y
        
    if event == cv2.EVENT_MOUSEWHEEL:
        global cdist
        
        if flags > 0:           
            cdist += 0.05
        else:
            cdist -= 0.05
        print('cdist' + str(cdist))
        
#md.ResetAllMotors()
cam.StartCameras()
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', mouse)

#U1-U9, R1-R9, F1-F9, D1-D9, L1-L9, B1-B9
#face letter and its servo id
faces = {
    'U' : 0,
    'R' : 2,
    'F' : 4,
    'D' : 3,
    'L' : 5,
    'B' : 1
}

#cubeString = list('LRFFURUDLDULFRBBLRLFBLFLBDRRRDRDUULFUUBBLDFFUDBFDBUDBR')
#cubeString = list('FUUFUUFUURRRRRRRRRDFFDFFDFFBDDBDDBDDLLLLLLLLLBBUBBUBBU')
#cubeString = list('BUUBUUBUURRRRRRRRRUFFUFFUFFFDDFDDFDDLLLLLLLLLBBDBBDBBD')
cubeString = list('UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB')

marks1 = [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1]]
marks2 = [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1]]
samplePositions = [[0] * 2 for i in range(54)]
focusedCamera1 = True

selected = [100000.0, ['T', -1]]
color = 'T'
mode = 1

while True:
    if mode == 0:
        cS_wrap = [cubeString]  
        frame = cam.ScanColors(marks1, marks2, samplePositions, focusedCamera1, cS_wrap)
        cubeString = cS_wrap[0]
        
        if L_click and mouseX < frame.shape[1]:
            if mouseX < frame.shape[1] / 4 and mouseY < frame.shape[0] / 4: #switch focused camera
                focusedCamera1 = not focusedCamera1
            else: #mark the circles
                marks = marks2
                if focusedCamera1:
                    marks = marks1
    
                removed = False
                
                for i in range(0, 6):
                    if marks[i] != [-1, -1]:
                        dist = ((mouseX - marks[i][0]) ** 2.0 + (mouseY - marks[i][1]) ** 2.0) ** (1/2.0)
                        if dist < 10:
                            marks[i] = [-1, -1]
                            removed = True
                
                if removed == False:
                    for i in range(0, 6):
                        if marks[i] == [-1, -1]:
                            marks[i] = [mouseX, mouseY]
                            break
                            
                marks.sort()
                marks[0:2] = sorted(marks[0:2], key=lambda x: x[1])
                marks[2:4] = sorted(marks[2:4], key=lambda x: x[1])
                marks[4:7] = sorted(marks[4:7], key=lambda x: x[1])
                
                
                full = True
                for mark in marks:
                    if mark == [-1, -1]:
                        full = False
                        
                if full:
                    if focusedCamera1:
                        samplePositions[0:27] = geo.ConstructPositions(marks)
                    else:
                        samplePositions[27:54] = geo.ConstructPositions(marks, True)

        
    else:
        frame = np.full((480, 640, 3), np.uint8(50))

    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        break
    if key == ord('z'):
        fov += 0.05
        print('fov' + str(fov))
    elif key == ord('x'):
        fov -= 0.05
        print('fov' + str(fov))
    elif key == ord('w'):
        cubeY += 0.1
    elif key == ord('s'):
        cubeY -= 0.1
    elif key == ord('d'):
        cubeX += 0.1
    elif key == ord('a'):
        cubeX -= 0.1

    elif key == ord('1'):
        color = 'U'
    elif key == ord('2'):
        color = 'R'
    elif key == ord('3'):
        color = 'F'
    elif key == ord('4'):
        color = 'D'
    elif key == ord('5'):
        color = 'L'
    elif key == ord('6'):
        color = 'B'    

    if mode == 1:
        selected = rend.Render( frame, [mouseX, mouseY], [cubeY, cubeX, 0], fov, cdist, cubeString, selected )
        if color != 'T' and selected[1][0] != 'T' and L_click and mouseX < 640:        
            cubeString[selected[1][1]] = color

    frame, _color, mode, L_click = rend.Buttons( frame, [mouseX, mouseY], L_click, mode )
    if mode == 1 and _color != 'T' and L_click:
        color = _color
        L_click = 0
        print(color)
        
    L_click *= 2
    if L_click >= 4:
        L_click = 0
    cv2.imshow("Frame", frame)

file = open("cubeString.txt", "w")
file.write("".join(cubeString) + '\n')
file.close()

solveString = sv.solve( cubeString, 20, 1 )
print( solveString )

currentFace = 0
#divides solve string to moves (letter - face) (number - multiplier) ('(' - marks the end)
for char in solveString:
    if char == '(':
        break
        
    if char == ' ':
        continue

    if char in faces:
        currentFace = faces[char]
        continue   
    
    inted = int(char)

    #if inted > 0 and inted < 4: #char is a number
        #md.MoveAFace(currentFace, inted)


cam.ReleaseCameras()
#md.ReleaseMotors()
