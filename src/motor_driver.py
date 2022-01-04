from pyax12.connection import Connection
import time

serial_connection = Connection(port="/dev/ttyUSB0", baudrate=1000000)

motorStates = [125, -145, -57, 33]
currentStates = [0, 0, 0, 0, 0, 0]
step_delay = 0.25

def MoveAFace(faceIndex, times):
    delay = 0.0
    for i in range(0, len(faceIndex)):
        #print( str(faceIndex[i]) + ' ' + str(times[i]) )
        prev_state = currentStates[faceIndex[i]]
        currentStates[faceIndex[i]] += times[i]       
        currentStates[faceIndex[i]] %= 4
        SetMotorState(faceIndex[i], currentStates[faceIndex[i]])
        delay = max(delay, step_delay * abs(prev_state - currentStates[faceIndex[i]]))
    time.sleep(delay)    
    
def SetMotorState( motor_id, state_id):
    serial_connection.goto(motor_id, motorStates[state_id], speed=1023, degrees=True)


def ResetAllMotors():
    print('Resetting motors...')
    for i in range(0, 6):
        #serial_connection.goto(i, motorStates[0], speed=1023, degrees=True)
        time.sleep(1)
    print('Done!')
      
def ReleaseMotors():
    serial_connection.close()
