# Drawing of a square, using the start event and a for cycle:

from wrapi.py.devices.Root.Root_v1_0 import *


def square(robot):
    robot.penDown()
    for i in range(4):
        robot.move(10)  # cm
        robot.rotate(90)
    robot.penAndEraserUp()

robot = Root_v1_0()
robot.ifStarts(square)
robot.start()
