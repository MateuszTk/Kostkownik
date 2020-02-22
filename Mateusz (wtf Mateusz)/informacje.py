from pyax12.connection import Connection

# Connect to the serial port
serial_connection = Connection(port="/dev/ttyUSB0", baudrate=1000000)

dynamixel_id = 2

# Print the control table of the specified Dynamixel unit
serial_connection.pretty_print_control_table(dynamixel_id)

# Close the serial connection
serial_connection.close()
