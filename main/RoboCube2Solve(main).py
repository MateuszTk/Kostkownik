import solver as sv
import numpy as np

from pyax12.connection import Connection
import time

# Connect to the serial port
serial_connection = Connection(port="/dev/ttyUSB0", baudrate=1000000)

def MoveAFace(faceIndex, times):	
	if times == 1:
		ClockWise(faceIndex)
	if times == 2:
		DoubleMove(faceIndex)
	if times == 3:
		CounterClockWise(faceIndex)
	
def ResetAllMotors():
	for i in range(0, 6):
		ResetMotor(i)
		time.sleep(0.1)
		
def ResetMotor(faceIndex):
	motorStates[faceIndex] = 125
	
	serial_connection.goto(motorIndexes[faceIndex], motorStates[faceIndex], speed=globalSpeed, degrees=True)
	
def ClockWise(faceIndex):
	motorStates[faceIndex] += 90
	if motorStates[faceIndex] == 215:
		motorStates[faceIndex] = -150
		
	serial_connection.goto(motorIndexes[faceIndex], motorStates[faceIndex], speed=globalSpeed, degrees=True)
	
def CounterClockWise(faceIndex):
	motorStates[faceIndex] -= 90
	if motorStates[faceIndex] == -240:
		motorStates[faceIndex]  = 30
		
	serial_connection.goto(motorIndexes[faceIndex], motorStates[faceIndex], speed=globalSpeed, degrees=True)
	
def DoubleMove(faceIndex):
	motorStates[faceIndex] += 180
	if motorStates[faceIndex] == 215:
		motorStates[faceIndex]  = -150
	
	if motorStates[faceIndex] == 305:
		motorStates[faceIndex]  = -60
		
	serial_connection.goto(motorIndexes[faceIndex], motorStates[faceIndex], speed=globalSpeed, degrees=True)

cubeString = 'LRFFURUDLDULFRBBLRLFBLFLBDRRRDRDUULFUUBBLDFFUDBFDBUDBR'

solveString = sv.solve(cubeString, 20, 1)
print(solveString)

globalSpeed = 512

#["U", "R", "F", "D", "L", "B"]

faces = ["U", "B", "R", "D", "F", "L"]
motorIndexes = [0, 1, 2, 3, 4, 5]
motorStates = [0, 0, 0, 0, 0, 0]

ResetAllMotors()
time.sleep(3)

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
		MoveAFace(currentFace, inted)
		time.sleep(3)
	
	
serial_connection.close()
