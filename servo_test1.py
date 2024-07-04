import serial
import time

# Define serial port and baud rate
serial_port = 'COM3'  # Replace with your Arduino's serial port (e.g., '/dev/ttyUSB0' on Linux)
baud_rate = 9600

# Initialize serial communication
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Delay to allow connection to stabilize
time.sleep(2)

# Example data to send
# positions = [13000, 13000, 13000, 13000]


positions = []
for i in range(4):
    pos = int(input(f"Enter position for servo {i+1}: "))
    positions.append(pos)


speeds = [1500, 1500, 1500, 1500]

# Format data as a string and send over serial
data_to_send = f"{positions[0]} {positions[1]} {positions[2]} {positions[3]} {speeds[0]} {speeds[1]} {speeds[2]} {speeds[3]}\n"
ser.write(data_to_send.encode())

# Optional: Read response from Arduino
# response = ser.readline().decode().strip()
# print(f"Response from Arduino: {response}")

# Close serial connection
ser.close()



