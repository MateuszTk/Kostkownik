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

def mouse(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_MOUSEMOVE:
        mouseX,mouseY = x,y

#md.ResetAllMotors()
cam.StartCameras()
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', mouse)

while True:
    frame = cam.ScanColors()
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    print(mouseX)
    rend.Render( frame, [mouseY / 10.0, mouseX / 10.0, 0] )
    cv2.imshow("Frame", frame)


faces = ["U", "B", "R", "D", "F", "L"]
cubeString = 'LRFFURUDLDULFRBBLRLFBLFLBDRRRDRDUULFUUBBLDFFUDBFDBUDBR'
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
