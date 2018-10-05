# Two robots drawing a saquare:

import threading
from wrapi.py.devices.Root.Root_v1_0 import *


class ThreadDraw(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot

    def run(self):
        robot = self.robot  # Just to make it shorter to type.
        robot.penDown()

        for i in range(0, 3):
            robot.move(30)  # 30 cm
            robot.rotate(90)

        robot.penAndEraserUp()

# Blocking version of the constructors: they will not continue until the
# robots are connected. So this version ensures that the robots start
# together to run their code:
robot0 = Root_v1_0()
robot1 = Root_v1_0()

ThreadDraw(robot0).start()
ThreadDraw(robot1).start()
