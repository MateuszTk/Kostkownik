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
import console as cons
import random
import ast

class Logger():
    stdout = sys.stdout
    messages = []

    def flush(self):
        pass
    
    def start(self): 
        sys.stdout = self

    def stop(self): 
        sys.stdout = self.stdout

    def write(self, text): 
        self.messages.append(text)
        self.stdout.write(text)
        
        global scroll
        scroll = 0

mouseX = 0
mouseY = 0
cubeX = -5.5
cubeY = -0.4
fov = 0.35
cdist = 12
L_click = 1
L_click_down = 0
consolePrevMouseY = -1
scroll = 0
cubePrevMouse = (-1, -1)

faces = {
    'U' : 0,
    'R' : 2,
    'F' : 4,
    'D' : 3,
    'L' : 5,
    'B' : 1
}

pairs = {
    'U' : 'D',
    'R' : 'L',
    'F' : 'B',
    'D' : 'U',
    'L' : 'R',
    'B' : 'F'
}

def mouse(event,x,y,flags,param):
    
    global mouseX, mouseY, L_click, L_click_down
    
    if event == cv2.EVENT_LBUTTONDOWN:
        L_click_down = 1
        L_click = 1
        
    if event == cv2.EVENT_LBUTTONUP:
        L_click_down = 0

    if event == cv2.EVENT_MOUSEMOVE:
        mouseX,mouseY = x,y
        
    if event == cv2.EVENT_MOUSEWHEEL:
        if mode == 1:  
            global cdist
            
            if flags > 0:           
                cdist += 0.05
            else:
                cdist -= 0.05
            print('cdist' + str(cdist))
            
        if mode == 2: 
            global scroll
            
            if flags > 0:           
                scroll += 30
            else:
                scroll -= 30
                
def SolveCube(cubeString):
    #file = open("cubeString.txt", "w")
    #file.write("".join(cubeString) + '\n')
    #file.close()

    solveString = sv.solve( cubeString, 20, 1 )
    print(solveString)
    
    if solveString[0] == 'E': #there's an error
        return;
    #Error: Cube definition string contains less than 54 facelets.
    #Error: Cube definition string contains more than 54 facelets.
    #Error: Cube definition string does not contain exactly 9 facelets of each color.
    #Error: Some edges are undefined.
    #Error: Total edge flip is wrong.
    #Error: Some corners are undefined.
    #Error: Total corner twist is wrong.
    #Error: Wrong edge and corner parity
    
    currentFace = 0
    #divides solve string to moves (letter - face) (number - multiplier) ('(' - marks the end)
    char = 0
    while char < len(solveString):
        inted = []
        currentFace = []
        br = False
        previous = 'T'
        for i in range(0, 2):
            move = solveString[char:char + 2]
            if move[0] == '(':
                if i == 0:
                    br = True
                break
            if i > 0 and pairs[move[0]] != previous:
                break
            inted.append(int(move[1]))
            currentFace.append(faces[move[0]])
            previous = move[0]
            char += 3
            
        if br:
            break
        
        #if any((x > 0 and x < 4) for x in inted): #char is a number
            #md.MoveAFace(currentFace, inted)

            

def ScrambleCube():
    moves = 10
    
    print("scrambling...")
    prevFace = -1
    while moves > 0:
       face = random.randint(0,5)
       count = random.randint(1, 3)
       
       if face != prevFace:
           moves = moves - 1
           #md.MoveAFace([face], [count]) #0-5, 1-3
           prevFace = face
    print("scrambled!")
    
    

#md.ResetAllMotors()

log = Logger()
log.start()

cam.StartCameras()
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', mouse)



#U1-U9, R1-R9, F1-F9, D1-D9, L1-L9, B1-B9
#face letter and its servo id


#cubeString = list('LRFFURUDLDULFRBBLRLFBLFLBDRRRDRDUULFUUBBLDFFUDBFDBUDBR')
#cubeString = list('FUUFUUFUURRRRRRRRRDFFDFFDFFBDDBDDBDDLLLLLLLLLBBUBBUBBU')
#cubeString = list('BUUBUUBUURRRRRRRRRUFFUFFUFFFDDFDDFDDLLLLLLLLLBBDBBDBBD')
cubeString = list('UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB')

marks1 = [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1]]
marks2 = [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1]]

file = open("marks1.txt", "r")
marks1 = ast.literal_eval(file.read())
file.close()

file = open("marks2.txt", "r")
marks2 = ast.literal_eval(file.read())
file.close()

samplePositions = [[0] * 2 for i in range(54)]

samplePositions[0:27] = geo.ConstructPositions(marks1)
samplePositions[27:54] = geo.ConstructPositions(marks2, True)

focusedCamera1 = True

selected = [100000.0, ['T', -1]]
color = 'T'
global mode
mode = 1

while True:
    if mode == 0: #Cameras
        frame, cubeString = cam.ScanColors(marks1, marks2, samplePositions, focusedCamera1, cubeString)
        
        if L_click and mouseX < frame.shape[1]:
            if (not focusedCamera1 and mouseX < 160 and mouseY < 120) or (focusedCamera1 and mouseX < 160 and mouseY > 360): #switch focused camera
                focusedCamera1 = not focusedCamera1
            else: #mark the circles
                marks = marks2
                if focusedCamera1:
                    marks = marks1
    
                removed = False
                
                for i in range(0, 7):
                    if marks[i] != [-1, -1]:
                        dist = ((mouseX - marks[i][0]) ** 2.0 + (mouseY - marks[i][1]) ** 2.0) ** (1/2.0)
                        if dist < 10:
                            marks[i] = [-1, -1]
                            removed = True
                
                if removed == False:
                    for i in range(0, 7):
                        if marks[i] == [-1, -1]:
                            marks[i] = [mouseX, mouseY]
                            break
                            
                marks.sort()
                marks[0:2] = sorted(marks[0:2], key=lambda x: x[1])
                marks[2:5] = sorted(marks[2:5], key=lambda x: x[1])
                marks[5:7] = sorted(marks[5:7], key=lambda x: x[1])
                
                
                full = True
                for mark in marks:
                    if mark == [-1, -1]:
                        full = False
                        
                if full:
                    if focusedCamera1:
                        samplePositions[0:27] = geo.ConstructPositions(marks)
                    else:
                        samplePositions[27:54] = geo.ConstructPositions(marks, True)
                        
                file = open("marks1.txt", "w")
                file.write(str(marks1))
                file.close()
                
                file = open("marks2.txt", "w")
                file.write(str(marks2))
                file.close()

    elif mode == 1: #preview
        frame = np.full((480, 800, 3), np.uint8(50))
        
    elif mode == 2: #console
        frame, consolePrevMouseY, scroll = cons.GetConsole(log.messages, L_click_down, consolePrevMouseY, scroll, mouseY)
        
    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        SolveCube(cubeString)
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
            
        
    
    if L_click_down and color == 'T' and mode == 1:
        if cubePrevMouse != (-1, -1):
            cubeX -= (mouseX - cubePrevMouse[0]) / 100
            cubeY -= (mouseY - cubePrevMouse[1]) / 100
        cubePrevMouse = (mouseX, mouseY)
    else:
        cubePrevMouse = (-1, -1)
    
    frame, _color, mode, L_click, action = rend.Buttons( frame, [mouseX, mouseY], L_click, mode, color )
    
    if action == 1:
        SolveCube(cubeString)
    elif action == 2:
        ScrambleCube()
    
    if mode == 1 and _color != 'T' and L_click:
        if _color == 'N':
            _color = 'T'
            
        color = _color
        L_click = 0
        #print(color)
        
    L_click *= 2
    if L_click >= 4:
        L_click = 0
    cv2.imshow("Frame", frame)

cam.ReleaseCameras()
md.ReleaseMotors()
