# Events-driven robot pinball:

from wrapi.py.devices.Root.Root_v1_0 import *

fwSpeed = 50
robot = Root_v1_0()

# Events:
robot.ifStarts(lambda data: robot.ledsEffect(ledsEffectCircle, clBlue).speed(fwSpeed, fwSpeed))
robot.ifColorsDetected([clRed], lambda d+ata: robot.stop().delay(0.5).ledsEffect(ledsEffectCircle, clRed).delay(5).halt())
robot.ifColorsDetected([clBlack, clAny], lambda data: robot.rotate(-90).speed(fwSpeed, fwSpeed))
robot.ifColorsDetected([clAny, clBlack], lambda data: robot.rotate(90).speed(fwSpeed, fwSpeed))

robot.start()
