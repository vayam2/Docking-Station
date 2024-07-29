import pygame
import time

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

# Function to remap button states to range 0 to 255
def remap_button(value):
    return value * 255

# Define a function to read and remap joystick input
def read_joystick():
    pygame.event.pump()
    
    # Read and remap axes (analog sticks)
    left_stick_x = normalize_axis(joystick.get_axis(0))
    left_stick_y = normalize_axis(joystick.get_axis(1))
    right_stick_x = normalize_axis(joystick.get_axis(4))
    right_stick_y = normalize_axis(joystick.get_axis(3))
    
    # Read and remap buttons (A, B, X, Y, etc.)
    a_button = remap_button(joystick.get_button(0))
    b_button = remap_button(joystick.get_button(1))
    x_button = remap_button(joystick.get_button(2))
    y_button = remap_button(joystick.get_button(3))
    
    # Map these inputs to RC channels
    rc_channels = {
        'left_stick_x': left_stick_x,
        'left_stick_y': left_stick_y,
        'right_stick_x': right_stick_x,
        'right_stick_y': right_stick_y,
        'a_button': a_button,
        'b_button': b_button,
        'x_button': x_button,
        'y_button': y_button
    }
    
    return rc_channels

# Main loop
try:
    while True:
        rc_channels = read_joystick()
        
        # Print the received values
        print("RC Channels:")
        for channel, value in rc_channels.items():
            print(f"{channel}: {value*100}")
        
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    pygame.joystick.quit()
    pygame.quit()
