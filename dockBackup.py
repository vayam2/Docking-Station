import serial
import time

serial_port = '/dev/ttyUSB0'  
baud_rate = 9600

ser = serial.Serial(serial_port, baud_rate, timeout=1)

time.sleep(2)
# positions = [-100, 0, 0, 0]
positions = [-8300, 8300, -8000, 8000]	# OPEN
positions1= [8300, -8300, 8000, -8000]	# CLOSE
speeds = [1500, 1500, 1500, 1500]

while True:
	tt = int(input("Values for opening or closing the docking station \n0 : Open \n1 : Close \nEnter the Value = "))
	
	if tt == 0:
	    data_to_send = f"{positions[0]} {positions[1]} {positions[2]} {positions[3]} {speeds[0]} {speeds[1]} {speeds[2]} {speeds[3]}\n"
	    ser.write(data_to_send.encode())
	    time.sleep(5)
	elif tt == 1:
	    data_to_send = f"{positions1[0]} {positions1[1]} {positions1[2]} {positions1[3]} {speeds[0]} {speeds[1]} {speeds[2]} {speeds[3]}\n"
	    ser.write(data_to_send.encode())
	    time.sleep(5)
	else:
	    print("invalid input")
    
ser.close()
