import time, cv2
from threading import Thread
from tello import Tello
import face_detection

face_to_find = "Obama"
tello = Tello()

tello.connect()
tello.streamon()
found_christina = False
found_oli = False
open_camera = True
kill = False
print(tello.get_battery())

def Begin_Dance():
    tello.flip_back()   

def Emergency():
    tello.rotate_clockwise(180)
    tello.emergency()

def FaceFinder(height=360, width=240, debug=True):
    # create a VideoWrite object, recoring to ./video.avi
    # 创建一个VideoWrite对象，存储画面至./video.avi
    height, width = 360, 240
    face_recognition = face_detection.FindFaces()
    fps = 15
    global open_camera, found_christina, found_oli
    while open_camera:
        img=tello.get_frame_read().frame
        img=cv2.resize(img,(height, width))
        time.sleep(1 / fps)
        img, face_names = face_recognition.process_frame(img)
        if debug:
            cv2.imshow("Image", img)
            cv2.waitKey(1)
        for face in face_names:
            if "Christina" in face:
                found_christina = True
                Begin_Dance()
            if "Oli" in face:
                found_oli = True
                Emergency()
            if "Obama" in face:
                kill = True
                open_camera = False
        if found_oli and found_christina:
            open_camera = False
                
    


# we need to run the recorder in a seperate thread, otherwise blocking options
#  would prevent frames from getting added to the video
# 我们需要在另一个线程中记录画面视频文件，否则其他的阻塞操作会阻止画面记录
faceFinder = Thread(target=FaceFinder)
faceFinder.start()

tello.takeoff()
tello.move_up(70)
while (not found_oli or not found_christina) and not kill:
    tello.rotate_counter_clockwise(45)

tello.land()
open_camera = False
faceFinder.join()