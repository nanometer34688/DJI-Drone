from tello import Tello
import signal

global tello
tello = Tello()


def handler(signum, frame):
    print("CTL-C")
    tello.land()
    # tello.emergency()


def box_landing():
    tello.move_up(70)
    tello.move_forward(150)
    tello.rotate_clockwise(90)
    tello.move_forward(80)
    tello.rotate_clockwise(90)
    tello.move_forward(150)


def look_into_middle_via_corner(height=70, width=150, length=150):
    tello.move_up(height)
    tello.move_forward(length)
    tello.rotate_clockwise(135)
    tello.rotate_counter_clockwise(45)
    tello.move_forward(width)
    tello.rotate_clockwise(135)
    tello.rotate_counter_clockwise(45)
    tello.move_forward(length)
    tello.rotate_clockwise(90)
    tello.move_forward(width)


def track_boxed_area_xyz(height=70, width=150, length=150):
    tello.move_up(height)
    tello.curve_xyz_speed(20, 50, 0, 50, 20, 0, 10)


def test_curve():
    tello.go_xyz_speed(150, 0, 0, 10)


def test_rc():
    tello.send_rc_control(50, 50, 0, 45)


signal.signal(signal.SIGINT, handler)

tello.connect()
print(tello.get_battery())
tello.takeoff()

look_into_middle_via_corner(width=100, length=100)
tello.land()




