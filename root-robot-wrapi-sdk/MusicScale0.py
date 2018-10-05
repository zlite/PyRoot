## Update this file to the latest WRAPI version.

from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()

for i in range(1, 20):
    robot.tone(i*100, 0.25)

robot.stop()
