import sys
sys.path.append('../Kostkownik/solver_package')

import time
import solver as sv
import numpy as np
import custom_ui as ui

#import motor_controller as mc

#solve parameters:
solvable = False
_cubeString = ''
solveString = 'Solve String'


#main loop:
while True:
	ui.update(solveString)
	
	cubeString = str(input()) #Fetch from cameras
	
	#  LRFFURUDLDULFRBBLRLFBLFLBDRRRDRDUULFUUBBLDFFUDBFDBUDBR   
	#  RDBDUDDUDBFLBRRRUULLLBFUBLFRDDUDFLRFBBFLLLFRUURDBBFRFU		-known correct scrambles
	
	if _cubeString != cubeString: #if new cube string
		print("Cube string update, solving: ")
		
		start_time = time.time()
		solveString = sv.solve(cubeString, 20, 1)
		elapsed_time = time.time() - start_time
		
		print(solveString)
		solvable = solveString[0:5] != "Error"
		
		if solvable:
			print("Solved!, Solve time: " + str(elapsed_time))
			
		_cubeString = cubeString
		
	time.sleep(0.1)
