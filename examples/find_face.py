import time, cv2
from threading import Thread
import sys
sys.path.append('./utils')
sys.path.append('./examples')
from tello import Tello
import face_detection
import signal

# Set face to find - Must match ./face_detection.py
face_to_find_1 = "Obama"
face_to_find_2 = "Biden"
face_to_find_3 = "Trump"
open_camera = True

global tello
tello = Tello()

tello.connect()
tello.streamon()

def handler(signum, frame):
    """
    handler function allows interuption of drone flight

    Ending the program with a CTRL-C command will land the drone immediately 
    """
    print("CTL-C pressed. Attempting to land drone...")
    tello.land()
    exit()


def found_face_1():
    global tello
    tello.flip_back() 

def found_face_2():
    global tello
    tello.rotate_clockwise(90)

def found_face_3():
    global tello, open_camera
    open_camera = False
    tello.land()
    
def FaceFinder(height=360, width=240, debug=True):
    height, width = 360, 240
    face_recognition = face_detection.FindFaces()
    fps = 15
    global open_camera
    while open_camera:
        img=tello.get_frame_read().frame
        img=cv2.resize(img,(height, width))
        time.sleep(1 / fps)
        img, face_names = face_recognition.process_frame(img)
        if debug:
            cv2.imshow("Image", img)
            cv2.waitKey(1)
        for face in face_names:
            if face_to_find_1 in face:
                found_face_1()
            elif face_to_find_2 in face:
                found_face_2()
            elif face_to_find_3 in face:
                found_face_3()
                
    
if __name__ == "__main__":
    # Set up signal handler to cut drone if needed
    signal.signal(signal.SIGINT, handler)
    # We need to run the recorder in a seperate thread, otherwise blocking options
    # Would prevent frames from getting added to the video
    faceFinder = Thread(target=FaceFinder)
    faceFinder.start()

    tello.takeoff()
    tello.move_up(70)


    faceFinder.join()