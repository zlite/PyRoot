# Snowflake fractal

from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()
robot.ledsEffect(ledsEffectSet, clGreen)
robot.penDown()

# A basic fractal example:
def fractal(level, size):
    if level < 1:
        robot.move(size)
    else:
        fractal(level - 1, size/3)
        robot.rotate(60)
        robot.rotate(-120)
        fractal(level - 1, size/3)
        robot.rotate(60)
        fractal(level - 1, size/3)

for i in range(6):
    # fractal(3, 40)
    # fractal(5, 50)
    fractal(3, 40)
    robot.rotate(-120)

robot.penAndEraserUp()
robot.stop()
