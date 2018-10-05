# Touch sensors polling example.
# Rotates the robot until the touch sensors are touched. Then this short
# program continues to monitor the bumpers and prints their states.

import time
from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()

robot.speed(25, -25)
while True:
    buttons = robot.touchSensors.states
    if buttons[0] or buttons[1] or buttons[2] or buttons[3]:
        robot.stop()
    print buttons
    time.sleep(0.05)  # Not mandatory, but desirable (to reduce CPU usage).
