import speech_recognition as sr
import os

import sys
sys.path.append('./utils')
from tello import Tello
import mute_alsa

take_off = ["start engine", "start engines", "take off", "takeoff"]
land = ["land", "stop", "down"]
cmd_360 = ["three sixty", "360", "three hundred and sixty", "turn around", "spin"]
flip = ["flip"]

def takeCommand():
     
    r = sr.Recognizer()
     
    with sr.Microphone() as source:
         
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
  
    try:
        print("Recognizing...")   
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
  
    except Exception as e:
        print(e)   
        print("Unable to Recognize your voice.") 
        return "None"
     
    return query


if __name__ == '__main__':
    clear = lambda: os.system('cls')
    tello = Tello()

    # Connect to drone
    tello.connect()

    # This Function will clean any
    # command before execution of this python file
    print("Battery: {}%".format(tello.get_battery()))

    while True:
         
        query = takeCommand().lower()
            
        # All the commands said by user will be
        # stored here in 'query' and will be
        # converted to lower case for easily
        # recognition of command
        if query in take_off:
            # Drone take off
            tello.takeoff()
            print("Taking off...")
        elif query in land:
            # Land drone
            tello.land()
            print("Landing...")
            exit()
        elif query in cmd_360:
            tello.rotate_clockwise(360)
            print("You spin me right round...")
        elif query in flip:
            tello.flip_back()