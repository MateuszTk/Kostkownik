from pyax12.connection import Connection
import time
serial_connection = Connection(port="/dev/ttyUSB0", baudrate=1000000)
# serial_connection.close()

def moveAFace(faceIndex, times):	
	if times == 1:
		clockWise(faceIndex)
	if times == 2:
		doubleMove(faceIndex)
	if times == 3:
		counterClockWise(faceIndex)
		
	
def clockWise(faceIndex):
	#fetch from the encoder		 motorStates[faceIndex] = encoder
	motorStates[faceIndex] += 90 #sign to encoder
		
	serial_connection.goto(motorIndexes[faceIndex], motorStates[faceIndex], speed=globalSpeed, degrees=True)
	
def counterClockWise(faceIndex):
	#fetch from the encoder		 motorStates[faceIndex] = encoder
	motorStates[faceIndex] -= 90 #sign to encoder
		
	serial_connection.goto(motorIndexes[faceIndex], motorStates[faceIndex], speed=globalSpeed, degrees=True)
	
def doubleMove(faceIndex):
	#fetch from the encoder		 motorStates[faceIndex] = encoder
	motorStates[faceIndex] += 180 #sign to encoder

	serial_connection.goto(motorIndexes[faceIndex], motorStates[faceIndex], speed=globalSpeed, degrees=True)


def solveCube(solveString):
	globalSpeed = 512

	faces = ["U", "B", "R", "D", "F", "L"]
	motorIndexes = [0, 1, 2, 3, 4, 5]
	motorStates = [0, 0, 0, 0, 0, 0]

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
			moveAFace(currentFace, inted)
			time.sleep(3)
