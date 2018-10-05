# Events-driven Bumpers example.

import time
from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()
robot.ifBumpersDetected(bumpersRightFront, lambda data: robot.ledsEffect(ledsEffectSet, clGreen))
robot.ifBumpersDetected(bumpersLeftFront, lambda data: robot.ledsEffect(ledsEffectSet, clYellow).delay(2).ledsEffect(ledsEffectSet, clViolet))
robot.ifStarts(lambda data: robot.ledsEffect(ledsEffectCircle, clBlue).move(40))

#print robot.events.list()
robot.start()
