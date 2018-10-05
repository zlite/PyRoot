# Minimalist drawing of a square:

from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()
distance = 10  # cm.

robot.penDown()

robot.stop().ledsEffect(ledsEffectCircle, clRed)

robot.move(distance)
robot.rotate(90)
robot.move(distance)
robot.rotate(90)
robot.move(distance)
robot.rotate(90)
robot.move(distance)

robot.penAndEraserUp()
robot.stop()
