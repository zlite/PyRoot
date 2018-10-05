# Simple color sensor example.

import time
from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()

robot.speed(50, 50)
while True:
    colors = robot.camera1d.colors

    if clBlack in colors or clRed in colors or clGreen in colors:
        print colors

    # Red color stops the robot:
    if clRed in colors:
        print colors
        break

    # Bumpers stop the robot too:
    if True in robot.bumper.states:
        break

    time.sleep(0.05)  # Not mandatory, but desirable (to reduce CPU usage).

robot.stop()
