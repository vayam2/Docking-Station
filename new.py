import pygame
import time
from dronekit import connect, VehicleMode
from pymavlink import mavutil

# Initialize Pygame
pygame.init()

# Initialize the joystick
pygame.joystick.init()

# Check if there is at least one joystick
if pygame.joystick.get_count() < 1:
    print("No joystick detected")
    exit()

# Get the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick name: {joystick.get_name()}")

# Function to normalize axis values to range 0 to 1
def normalize_axis(value):
    return (value + 1) / 2
def remap_button(value):
    return value * 255
# Connect to the vehicle
print("Connecting to vehicle on: tcp:127.0.0.1:5760")
vehicle = connect('127.0.0.1:6969', wait_ready=True)
flag = 0
# Function to send RC channel override command
def send_rc_override(roll, pitch, throttle, yaw):
    rc_channels = [0,0,0,0,0,0,0,0]
    rc_channels[0] = roll     # RC1: Roll
    rc_channels[1] = pitch    # RC2: Pitch
    rc_channels[2] = throttle # RC3: Throttle
    rc_channels[3] = yaw      # RC4: Yaw

    # Create the RC_CHANNELS_OVERRIDE message
    msg = vehicle.message_factory.rc_channels_override_encode(
        0,  # target system
        0,  # target component
        *rc_channels
    )
    # Send the message
    vehicle.send_mavlink(msg)

def arm_and_takeoff(aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """

        print("Basic pre-arm checks")
        # Don't let the user try to arm until autopilot is ready
        while not vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        print("Arming motors")
        # Copter should arm in GUIDED mode
        vehicle.mode = VehicleMode("GUIDED")
        vehicle.armed = True

        while not vehicle.armed:      
            print(" Waiting for arming...")
            time.sleep(1)

        print("Taking off!")
        vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
        #  after Vehicle.simple_takeoff will execute immediately).
        while True:
            print(" Altitude: ", vehicle.location.global_relative_frame.alt)      
            if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
                print("Reached target altitude")
                break
            time.sleep(1)

# Main loop
try:
    while True:
        pygame.event.pump()
        vehicle.mode = VehicleMode("POSHOLD")
        # Read and normalize axes (analog sticks)
        left_stick_x = normalize_axis(joystick.get_axis(0))
        left_stick_y = normalize_axis(joystick.get_axis(1))
        right_stick_x = normalize_axis(joystick.get_axis(4))
        right_stick_y = normalize_axis(joystick.get_axis(3))
        a_button = remap_button(joystick.get_button(0))
        b_button = remap_button(joystick.get_button(1))
        x_button = remap_button(joystick.get_button(2))
        y_button = remap_button(joystick.get_button(3))
        
        # Convert normalized values to PWM range (1000-2000)
        roll = int(1250 + right_stick_y * 500) 
        pitch = int(1250 + right_stick_x * 500) 
        throttle = int(2000 - left_stick_y * 1000) 
        yaw = int(1250 + left_stick_x * 500) 
        if x_button >= 200:  
            vehicle.mode = VehicleMode("LAND")
        if y_button >= 200:  
            vehicle.mode = VehicleMode("RTL")
        # Send RC override command
        send_rc_override(roll, pitch, throttle, yaw)
        
        # Print the received values
        print(f"Roll: {roll}, Pitch: {pitch}, Throttle: {throttle}, Yaw: {yaw}")
        if flag == 0 and a_button >= 200:    
            send_rc_override(1500, 1500, 1000, 1500)
            arm_and_takeoff(10)
            flag = 1
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("Exiting...")
finally:
    vehicle.close()
    pygame.joystick.quit()
    pygame.quit()
