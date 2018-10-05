# Line follower using listeners (5 sensor areas):

from wrapi.py.devices.Root.Root_v1_0 import *


def camera1dDidChange(source, data):
    # Slices the colors array in 5 areas:
    colorsLeft0 = data[0:6]
    colorsLeft1 = data[6:12]
    colorsCenter = data[12:20]
    colorsRight1 = data[20:26]
    colorsRight0 = data[26:32]
    #print colorsLeft0, colorsLeft1, colorsCenter, colorsRight0, colorsRight1

    if clBlack in colorsLeft0:
        robot.speed(0, fwSpeed)
        return True
    if clBlack in colorsRight0:
        robot.speed(fwSpeed, 0)
        return True
    if clBlack in colorsLeft1:
        robot.speed(0.5*fwSpeed, fwSpeed)
        return True
    if clBlack in colorsRight1:
        robot.speed(fwSpeed, 0.5*fwSpeed)
        return True
    if clBlack in colorsCenter:
        robot.speed(fwSpeed, fwSpeed)
        return True

    return False

fwSpeed = 50
robot = Root_v1_0()
robot.camera1d.dataDidChange = camera1dDidChange

robot.speed(50, 50)
