# Improved polling line follower (5 sensor areas):

from wrapi.py.devices.Root.Root_v1_0 import *

fwSpeed = 50
robot = Root_v1_0()

robot.speed(fwSpeed, fwSpeed)
while True:
    # Slices the colors array in 5 areas:
    colorsLeft0 = robot.camera1d.colors[0:6]
    colorsLeft1 = robot.camera1d.colors[6:12]
    colorsCenter = robot.camera1d.colors[12:20]
    colorsRight1 = robot.camera1d.colors[20:26]
    colorsRight0 = robot.camera1d.colors[26:32]
    #print colorsLeft0, colorsLeft1, colorsCenter, colorsRight0, colorsRight1

    if clBlack in colorsLeft0:
        robot.speed(0, fwSpeed)
        #print "1.speed"  # ##Debug.
    elif clBlack in colorsRight0:
        robot.speed(fwSpeed, 0)
        #print "2.speed"  # ##Debug.
    elif clBlack in colorsLeft1:
        robot.speed(0.5*fwSpeed, fwSpeed)
        #print "3.speed"  # ##Debug.
    elif clBlack in colorsRight1:
        robot.speed(fwSpeed, 0.5*fwSpeed)
        #print "4.speed"  # ##Debug.
    elif clBlack in colorsCenter:
        robot.speed(fwSpeed, fwSpeed)
        #print "5.speed"  # ##Debug.
