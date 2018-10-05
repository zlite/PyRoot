# Basic version of programming with colors.

import time
from wrapi.py.devices.Root.Root_v1_0 import *

delay = 0.25
fwSpeed = 50
commands = []
robot = Root_v1_0()

robot.speed(fwSpeed, fwSpeed)
while len(commands) < 5:  # 5 commands for this activity.
    colors = robot.camera1D.colors
    if clBlack in colors:
        commands.append(lambda: robot.move(20))
        time.sleep(delay)  # This is to give time to go to the next color line.
        print "black:", len(commands)
    elif clGreen in colors:
        commands.append(lambda: robot.rotate(90))
        print "green:", len(commands)
        time.sleep(delay)  # This is to give time to go to the next color line.
    elif clRed in colors:
        commands.append(lambda: robot.rotate(-90))
        print "red:", len(commands)
        time.sleep(delay)  # This is to give time to go to the next color line.

print len(commands), commands

while True:
    colors = robot.camera1D.colors
    if clRed in colors:
        break

robot.rotate(-90)
for i in commands:
    i()
    ##time.sleep(2)

robot.stop()
