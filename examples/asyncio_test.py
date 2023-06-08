
import asyncio
from tello_asyncio import Tello, Vector


async def main(altitude=70, width=100, length=100):
    drone = Tello()
    try:
        await drone.connect()
        await drone.set_speed(100)
        await drone.takeoff()
        await drone.move_up(altitude)
        await drone.move_forward(length)
        await drone.turn_clockwise(90)
        await drone.move_forward(width)
        await drone.turn_clockwise(90)
        await drone.move_forward(length)
        await drone.turn_clockwise(90)
        await drone.move_forward(width)
        await drone.turn_clockwise(90)
    finally:
        await drone.disconnect()


# Python 3.7+
# asyncio.run(main())
loop = asyncio.get_event_loop()
loop.run_until_complete(main())