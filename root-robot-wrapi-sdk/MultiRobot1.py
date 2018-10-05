# Simplest (and probably more elegant) form of multhreading with the robots:

import threading
from wrapi.py.devices.Root.Root_v1_0 import *

# This version does not ensure that the robots start together to run their
# code, as each robot only starts once it has a valid connection. So a nice
# excercice to show why a different approach may be needed to run this
# program with one robot on and the other off, and after the first robot has
# started, turn on the second one.


class ThreadDraw (threading.Thread):
    def run(self):
        # Blocking version of the constructors, but INSIDE each robot's thread:
        robot = Root_v1_0()
        robot.penDown()

        for i in range(0, 3):
            print i  # ##Debug.
            robot.move(20)  # cm
            robot.rotate(90)

        robot.penAndEraserUp()

ThreadDraw().start()
ThreadDraw().start()
