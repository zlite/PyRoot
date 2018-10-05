# Improved "traditional" (not that event based) line follower:

from wrapi.py.devices.Root.Root_v1_0 import *

fwSpeed = 50
colorSensorAreas = 3
robot = Root_v1_0()


def colorChanged(robot):
    colors = robot.camera1d.colors
    if len(colors) == colorSensorAreas:  # Extra safety, not mandatory.
        if clBack in colors[0]:
            robot.setSpeed(fwSpeed, 0)
        elif clBack in colors[2]:
            robot.setSpeed(0, fwSpeed)
        elif clBack in colors[1]:
            robot.setSpeed(fwSpeed, fwSpeed)

# Events:
robot.ifStarts(lambda: robot.setSpeed(fwSpeed, fwSpeed))
robot.ifColorsChanged(colorSensorAreas, colorChanged)

robot.start()
