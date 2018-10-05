# Draws a simple spiral by changing the speed of the wheels incrementally.

import time
from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()

robot.penDown()

leftSpeed = -5
for i in range(1, 32):
    leftSpeed += 1.5
    print i, ":", leftSpeed
    robot.speed(leftSpeed, 50)

    time.sleep(1)

robot.stop()
