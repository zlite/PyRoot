# Polling line follower:

from wrapi.py.devices.Root.Root_v1_0 import *

fwSpeed = 50
robot = Root_v1_0()

robot.speed(fwSpeed, fwSpeed)
while True:
    # Slices the colors array in 3 areas:
    colorsLeft = robot.camera1d.colors[0:10]
    colorsCenter = robot.camera1d.colors[10:22]
    colorsRight = robot.camera1d.colors[22:32]
    # print colorsLeft, colorsCenter, colorsRight

    if clBlack in colorsLeft:
        robot.speed(0, fwSpeed)
    elif clBlack in colorsRight:
        robot.speed(fwSpeed, 0)
    elif clBlack in colorsCenter:
        robot.speed(fwSpeed, fwSpeed)
