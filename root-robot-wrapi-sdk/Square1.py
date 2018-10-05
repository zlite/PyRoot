# Chained methods used to draw a square:

from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()
distance = 10  # cm.

robot.stop().penDown().move(distance).rotate(90).move(distance).rotate(90).move(distance).rotate(90).move(distance).penAndEraserUp().stop()
