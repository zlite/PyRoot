# Turtle geometry simple spiral:

from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()

robot.penDown()

for i in range(0, 40):
    print i
    # ##"10" constant will be removed once the new robot's firmware is in place:
    robot.rotate(2*i + 10)
    robot.move(5)

robot.stop()
