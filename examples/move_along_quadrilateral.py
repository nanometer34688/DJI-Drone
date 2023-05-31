import sys
sys.path.append('./utils')
from tello import Tello
import argparse

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

def move_as_quad(altitude=70, width=100, length=100):
    """
    move_as_quad function allows the drone to move from current position in a quadrilateral to original position

    altitude: How high the drone should fly (cm)
    width: How wide the drone should fly out to (cm)
    length: How far the drone should fly out to (cm)

    Note: Drone should be pointed in the direction you want the drone to travel first. 
          It will fly down the length of the quadrilateral first
    """
    tello.move_up(altitude)
    tello.move_forward(length)
    tello.rotate_clockwise(90)
    tello.move_forward(width)
    tello.rotate_clockwise(90)
    tello.move_forward(length)
    tello.rotate_clockwise(90)
    tello.move_forward(width)
    tello.rotate_clockwise(90)

if __name__ == "__main__":

    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Moves the drone from current position in a quadrilateral shape back to original position. The drone will move along the length of the quadrilateral first.')

    # Optional positional argument
    parser.add_argument('-l', '--length', type=int,  default=100,
                        help='Length of quadrilateral (cm)')
    parser.add_argument('-w', '--width', type=int,  default=100,
                        help='Width of quadrilateral (cm)')
    parser.add_argument('-a', '--altitude', type=int,  default=70,
                        help='Altitude of drone relative to surface (cm)')

    args = parser.parse_args()

    # Set up signal handler to cut drone if needed
    signal.signal(signal.SIGINT, handler)

    # Connect to drone
    tello.connect()

    # Drone take off
    tello.takeoff()

    # Main work
    move_as_quad(altitude=args.altitude, width=args.width, length=args.length)

    # Land drone
    tello.land()


