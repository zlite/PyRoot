# More "traditional" (not that event based) line follower:

from wrapi.py.devices.Root.Root_v1_0 import *

fwSpeed = 50
robot = Root_v1_0()

# - There is another method called "ifColorChanged" that passes the 32
# elements color list to the callback:
colorSensorAreas = 5
def colorChanged(robot):
    # This property holds the last color sensor reading. So it can be used
    # in non-event based programming, which will be less efficent, since
    # events like colorChanged will be triggered only when there was a change.
    colors = robot.camera1d.colors
    if len(colors == colorSensorAreas):  # Extra safety, not of imprescindible.
        if colors[0] == clBack or colors[1] == clBack:
            robot.setSpeed(fwSpeed, 0)
        elif colors[3] == clBack or colors[4] == clBack:
            robot.setSpeed(0, fwSpeed)
        elif colors[2] == clBack:
            robot.setSpeed(fwSpeed, fwSpeed)

# Events:
robot.ifStarts(lambda: robot.setSpeed(fwSpeed, fwSpeed))
robot.ifColorsChanged(colorSensorAreas, colorChanged)  # 1st param = # of areas.

robot.start()
