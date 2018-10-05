# Minimalist drawing of a square:

import time
from random import randint
from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()

for i in range(1, 100):
    robot.ledsEffect(ledsEffectSet, randint(0, len(clCodeToRgb)))

    # To visualize the colors better, just uncomment this line:
    time.sleep(0.05)

robot.stop()
