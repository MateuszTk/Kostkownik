from pyax12.connection import Connection
import time

serial_connection = Connection(port="/dev/ttyUSB0", baudrate=1000000)

motorStates = [125, -145, -57, 33]
currentStates = [0, 0, 0, 0, 0, 0]

def MoveAFace(faceIndex, times):
    currentStates[faceIndex] += times       
    currentStates[faceIndex] %= 4
    SetMotorState(faceIndex, currentStates[faceIndex])
    
    
def SetMotorState( motor_id, state_id ):
	serial_connection.goto(motor_id, motorStates[state_id], speed=512, degrees=True)
	time.sleep(2)


def ResetAllMotors():
	print('Resetting motors...')
    for i in range(0, 6):
        serial_connection.goto(i, motorStates[0], speed=512, degrees=True)
        time.sleep(2)
	print('Done!')
      
def ReleaseMotors():
	serial_connection.close()
