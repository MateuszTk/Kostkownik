import time
import sys
import os
import cv2

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
cdist = 9.1

def mouse(event,x,y,flags,param):
    
    global mouseX,mouseY
    
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
faces = ["U", "B", "R", "D", "F", "L"]
cubeString = list('LRFFURUDLDULFRBBLRLFBLFLBDRRRDRDUULFUUBBLDFFUDBFDBUDBR')

selected = [100000.0, ['T', -1]]

while True:
    frame = cam.ScanColors()
    color = 'T'
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

    if color != 'T':
        cubeString[selected[1][1]] = color
        
    selected = rend.Render( frame, [mouseX, mouseY], [cubeY, cubeX, 0], fov, cdist, cubeString, selected)
    cv2.imshow("Frame", frame)

file = open("cubeString.txt", "w")
file.write("".join(cubeString) + '\n')
file.close()

solveString = sv.solve( cubeString, 20, 1 )
print( solveString )

currentFace = 0
for char in solveString: #divides solve string to moves (letter - face) (number - multiplier) (( - marks the end)
    if char == '(':
        break
        
    if char == ' ':
        continue
    
    charFound = False
    for i in range(0, 6): #check if char corresponds to any of face chars
        if faces[i] == char:
            currentFace = i
            charFound = True
            break
    
    if charFound:
        continue
    
    inted = int(char)
    
    #if inted > 0 and inted < 4: #char is a number
        #md.MoveAFace(currentFace, inted)

#md.SetMotorState( 2, 0 )
#md.SetMotorState( 2, 1 )
#md.SetMotorState( 2, 2 )
#md.SetMotorState( 2, 3 )


cam.ReleaseCameras()
#md.ReleaseMotors()
