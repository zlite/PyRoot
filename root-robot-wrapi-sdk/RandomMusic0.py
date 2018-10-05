## Update this file to the latest WRAPI version.

from random import randint
from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()

for i in range(1, 30):
    #robot.tone(randint(100, 3000), 0.05)
    robot.tone(randint(100, 3000), 0.03)
    # Try this too:
    # robot.toneDriver.stop()

robot.stop()
