import time
from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()

def moveRobot():
    robot.speed(50, -50)
    time.sleep(2)

    robot.speed(100, 100)
    time.sleep(0.5)

    robot.speed(0, 0)
    time.sleep(0.1)

    robot.speed(-55, -55)
    time.sleep(1)

    robot.speed(55, -55)
    time.sleep(2)

# By default, the speed is limited to half the maximum speed:
moveRobot()
moveRobot()
robot.stop()
