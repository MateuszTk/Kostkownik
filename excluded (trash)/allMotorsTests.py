from pyax12.connection import Connection
import time

# Connect to the serial port
serial_connection = Connection(port="/dev/ttyUSB0", baudrate=1000000)

# A 125 B -150 C -60 D 30

motorIds = { 2, 4 }

for motor in motorIds:
	serial_connection.goto(motor, 125, speed=512, degrees=True)
	
time.sleep(2)   
	
for motor in motorIds:
	serial_connection.goto(motor, -150, speed=512, degrees=True)
	
time.sleep(2)   
	
for motor in motorIds:
	serial_connection.goto(motor, -60, speed=512, degrees=True)
	
time.sleep(2)   
	
for motor in motorIds:
	serial_connection.goto(motor, 30, speed=512, degrees=True)
	
time.sleep(2)   

# Close the serial connection
serial_connection.close()
