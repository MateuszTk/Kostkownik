from pyax12.connection import Connection
import time

# Connect to the serial port
serial_connection = Connection(port="/dev/ttyUSB0", baudrate=1000000)

# A 125 B -150 C -60 D 30

globalSpeed = 512

def ResetMotor(motor):
	motors[motor] = 125
	
	serial_connection.goto(motor, motors[motor], speed=globalSpeed, degrees=True)
	
def ClockWise(motor):
	motors[motor] += 90
	if motors[motor] == 215:
		motors[motor] = -150
		
	serial_connection.goto(motor, motors[motor], speed=globalSpeed, degrees=True)
	
def CounterClockWise(motor):
	motors[motor] -= 90
	if motors[motor] == -240:
		motors[motor] = 30
		
	serial_connection.goto(motor, motors[motor], speed=globalSpeed, degrees=True)

motors = { 0, 0, 0, 0, 0, 0}

# Motor reset
for toReset in range(0, 5):
	ResetMotor(toReset)

time.sleep(3)

motorId = 2

ResetMotor()


# Close the serial connection
serial_connection.close()

