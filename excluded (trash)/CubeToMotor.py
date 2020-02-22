import solver as sv
import numpy as np

def MoveAFace(faceIndex, times):
	print('move')
	print(motorIndexes[faceIndex])
	print(times)

cubeString = 'UUFUUFUUFRRRRRRRRRFFDFFDFFDDDBDDBDDBLLLLLLLLLUBBUBBUBB'

solveString = sv.solve(cubeString, 20, 1)
print(solveString)

faces = ["U", "R", "F", "D", "L", "B"]
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
		MoveAFace(currentFace, inted)
	
