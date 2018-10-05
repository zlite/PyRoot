# Circular fractal

from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()

robot.penDown()
# robot.stop().ledsEffect(ledsEffectCircle, clRed)

# # A basic fractal example:
# def fractal(level, size):
#     if level < 1:
#         robot.move(size)
#     else:
#         fractal(level - 1, size/3)
#         robot.rotate(60)
#         fractal(level - 1, size/3)
#         robot.rotate(-120)
#         fractal(level - 1, size/3)
#         robot.rotate(60)
#         fractal(level - 1, size/3)


def square(size):
    for i in range(3):
        robot.move(size)
        robot.rotate(90)
    robot.move(2*size)


def squares(size, count):
    for i in range(count):
        square(size)

count = 4
size = 3
squares(size, count)
robot.move(4*size)
squares(size, count)

robot.rotate(90)
robot.move(4*size)

squares(size, count)
robot.move(4*size)
squares(size, count)

robot.penAndEraserUp()
robot.stop()
