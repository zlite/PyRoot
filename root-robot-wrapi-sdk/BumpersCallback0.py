# Bumpers callback example.
# Prints the state of the bumpers each time a bumper is pressed.

import time
from wrapi.py.devices.Root.Root_v1_0 import *


def bumpersDidChange(source, data):
    print "bumpersDidChange: ", data

robot = Root_v1_0()
print "Robot created."
robot.bumpers.dataDidChange = bumpersDidChange
