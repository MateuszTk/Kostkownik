from pyax12.connection import Connection
serial_connection = Connection(port="/dev/ttyUSB0", baudrate=1000000)
import time

def ResetAllMotors():
	for i in range(0, 6):
		ResetMotor(i)
		time.sleep(0.1)
		
def ResetMotor(faceIndex):
	motorStates[faceIndex] = 125
	serial_connection.goto(motorIndexes[faceIndex], motorStates[faceIndex], speed=512, degrees=True)

motorIndexes = [0, 1, 2, 3, 4, 5]
motorStates = [0, 0, 0, 0, 0, 0]

ResetAllMotors()
time.sleep(3)

serial_connection.close()
