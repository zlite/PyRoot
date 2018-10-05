# Two robots drawing a saquare:

import threading
from wrapi.py.devices.Root.Root_v1_0 import *


class ThreadRobot(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.connected = False

        # This is the Robot constructor's version with connection callback:
        self.robot = Root_v1_0(None, self.robotDidConnect)

    def robotDidConnect(self):
        self.connected = True
        print "robotDidConnect"  # ##Debug.

    def run(self):
        print "run"  # ##Debug.

        # Only run after the robot has been effectively connected:
        while not self.connected:
            pass
        print "connected"  # ##Debug.

        robot = self.robot  # Just to make it shorter.
        robot.penDown()

        for i in range(0, 3):
            print i
            robot.move(30)  # 30 cm
            robot.rotate(90)

        robot.penAndEraserUp()

ThreadRobot().start()
ThreadRobot().start()
