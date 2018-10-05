# Multirobot0 version, where each robot0 do things synchronized with the other
# robot0, so they are not running anything in paralell (see other, more
# advanced "Multirobot0" examples for how to work with the robot0s in
# parallel).

from wrapi.py.devices.Root.Root_v1_0 import *

robot0 = Root_v1_0()
robot1 = Root_v1_0()

robot0.penDown()
robot1.penDown()

for i in range(0, 3):
    robot0.move(20)  # cm
    robot1.move(20)
    robot0.rotate(90)
    robot1.rotate(90)

robot0.penAndEraserUp()
robot1.penAndEraserUp()
