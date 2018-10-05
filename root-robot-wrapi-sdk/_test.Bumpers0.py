# Line follower using listeners (5 sensor areas):

from wrapi.py.devices.Root.Root_v1_0 import *


def bumpersDidChange(source, states):
    print states
    if states[0]:
        robot.rotate(180)
        robot.move(5)
        robot.move(-5)
    if states[1]:
        robot.rotate(-180)
    return False

fwSpeed = 50
robot = Root_v1_0()
robot.bumpers.dataDidChange = bumpersDidChange

#robot.speed(50, 50)
