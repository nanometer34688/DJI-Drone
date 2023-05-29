# LOCAL SCRIPT FOR TEST PURPOSES
from tello import Tello
import signal

global tello
tello = Tello()


tello.connect()
print(tello.get_battery())
tello.takeoff()

tello.land()




