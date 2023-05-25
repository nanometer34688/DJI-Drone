from threading import Thread
import cv2
from tello import Tello

tello = Tello()

tello.connect()
tello.streamon()

def CaptureFace():
    while True:
        img=tello.get_frame_read().frame
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        

captureFace = Thread(target=CaptureFace)
captureFace.start()
captureFace.join()