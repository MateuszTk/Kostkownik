import time
import sys
import os

module_dir = os.path.join( os.path.dirname( __file__ ), 'Solver' )
sys.path.append( module_dir )
import solver as sv
import motor_driver as md
import camera as cam

md.ResetAllMotors()
cam.StartCameras()

#while True:
#	cam.ScanColors()

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
    
    if inted > 0 and inted < 4: #char is a number
        md.MoveAFace(currentFace, inted)

#md.SetMotorState( 2, 0 )
#md.SetMotorState( 2, 1 )
#md.SetMotorState( 2, 2 )
#md.SetMotorState( 2, 3 )


cam.ReleaseCameras()
md.ReleaseMotors()
