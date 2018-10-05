# Events-driven line follower with 5 detection zones:

from wrapi.py.devices.Root.Root_v1_0 import *

fwSpeedMax = 50
fwSpeed = 30

robot = Root_v1_0()

# Events:
robot.ifStarts(lambda data: robot.speed(fwSpeedMax, fwSpeedMax))

robot.ifColorsDetected([clRed], lambda data: robot.stop())
robot.ifColorsDetected([clBlack, clAny, clAny, clAny, clAny], lambda data: robot.speed(0, fwSpeedMax))
robot.ifColorsDetected([clAny, clAny, clAny, clAny, clBlack], lambda data: robot.speed(fwSpeedMax, 0))
robot.ifColorsDetected([clAny, clBlack, clAny, clAny, clAny], lambda data: robot.speed(fwSpeed, fwSpeedMax))
robot.ifColorsDetected([clAny, clAny, clAny, clBlack, clAny], lambda data: robot.speed(fwSpeedMax, fwSpeed))
robot.ifColorsDetected([clAny, clAny, clBlack, clAny, clAny], lambda data: robot.speed(fwSpeedMax, fwSpeedMax))

robot.start()
