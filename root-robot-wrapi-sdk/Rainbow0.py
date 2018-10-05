# Minimalist drawing of a square:

import time
from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()

for i in range(1, 50):
    value = i % len(clCodeToRgb)
    if value == clBlack:
        continue
    robot.ledsEffect(ledsEffectCircle, value)

    # To visualize the colors better, just uncomment this line:
    time.sleep(0.05)

robot.stop()
