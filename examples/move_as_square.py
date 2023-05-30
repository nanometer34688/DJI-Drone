import sys
sys.path.append('./utils')
from tello import Tello

import signal

tello = Tello()

def handler(signum, frame):
    """
    handler function allows interuption of drone flight

    Ending the program with a CTRL-C command will land the drone immediately 
    """
    print("CTL-C pressed. Attempting to land drone...")
    tello.land()
    exit()

def move_as_square(height=70, width=100, length=100):
    """
    move_as_square function allows the drone to move from current position in a square to original position

    height: How high the drone should fly (cm)
    width: How wide the drone should fly out to (cm)
    length: How far the drone should fly out to (cm)

    Note: Drone should be pointed in the direction you want the drone to travel first. 
          It will fly down the length of the square first
    """
    tello.move_up(height)
    tello.move_forward(length)
    tello.rotate_clockwise(90)
    tello.move_forward(width)
    tello.rotate_clockwise(90)
    tello.move_forward(length)
    tello.rotate_clockwise(90)
    tello.move_forward(width)
    tello.rotate_clockwise(90)

if __name__ == "__main__":
    # Set up signal handler to cut drone if needed
    signal.signal(signal.SIGINT, handler)

    # Connect to drone
    tello.connect()

    # Drone take off
    tello.takeoff()

    # Main work
    move_as_square(height=70, width=100, length=100)

    # Land drone
    tello.land()


