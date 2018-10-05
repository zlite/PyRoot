# Bumpers polling example.
# Rotates the robot until the bumpers detect an obstacle. Then this short
# program continues to monitor the bumpers and prints their states.

import time
from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()

robot.speed(50, -50)
while True:
    if robot.bumpers.states[0] or robot.bumpers.states[1]:
        robot.stop()
    print robot.bumpers.states
    time.sleep(0.05)  # Not mandatory, but desirable (to reduce CPU usage).
