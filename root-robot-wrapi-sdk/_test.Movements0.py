## Update this file to the latest WRAPI version.

from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()

for i in range(10):
    #robot.move(1)
    #robot.move(-1)
    #robot.move(1.5)
    #robot.move(-1.5)
    #robot.move(2)
    #robot.move(-2)
    #robot.move(20)
    #robot.move(-20)

    #robot.rotate(11)  # 11 is the absolute minimum that the robot currently accepts.
    #robot.rotate(-11)
    robot.rotate(20)
    robot.rotate(-20)
    #robot.rotate(45)
    #robot.rotate(-45)
    #robot.rotate(360)
    #robot.rotate(-360)

robot.ledsEffect(robot.ledRgbDriver.set, clBlue)
