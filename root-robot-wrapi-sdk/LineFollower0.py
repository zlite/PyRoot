from wrapi.py.devices.Root.Root_v1_0 import *

fwSpeed = 50

def moveToLeft(robot):
    robot.speed(0, fwSpeed)

def moveToRight(robot):
    robot.speed(fwSpeed, 0)

def moveForward(robot):
    robot.speed(fwSpeed, fwSpeed)

robot = Root_v1_0()

# Events:
robot.ifStarts(moveForward)
# - This function will check the size of the list passed and will divide the
# sensor array in "size" number of areas, up to 32. If the number is not a
# divisor of 32, it finds a divisor that allows for the "biggest possible
# central, variable-size area":
robot.ifColorsDetected([clBlack, clBlack, clWhite, clWhite, clWhite], moveToLeft)
robot.ifColorsDetected([clWhite, clWhite, clWhite, clBlack, clBlack], moveToRight)
robot.ifColorsDetected([clWhite, clWhite, clBlack, clWhite, clWhite], moveForward)

# Notes:
# - ALSO IMPORTANT: The events will not work until the "start" method is
# called. This ensures predicatbility regarding the start event, and also
# makes it optional to start the events system or not.
robot.start()
