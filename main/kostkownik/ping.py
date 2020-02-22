from pyax12.connection import Connection

print("Przed connection")


# Connect to the serial port
serial_connection = Connection(port="/dev/ttyUSB0", baudrate=1000000)

dynamixel_id = 2

print("Przed ping")

# Ping the third dynamixel unit
is_available = serial_connection.ping(dynamixel_id)

print(is_available)

# Close the serial connection
serial_connection.close()
