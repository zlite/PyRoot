# Bumpers callback example.
# Prints the state of the bumpers each time a bumper is pressed.

import time
from wrapi.py.devices.Root.Root_v1_0 import *


'''
def taskLeft(data):
    #robot.ledsEffect(ledsEffectSet, clRed)
    print "robot.ledsEffect:", robot.ledsEffect
    while True:
        print "hola", robot
        robot.speed(50, -50).delay(0.5).ledsEffect(ledsEffectSet, clRed).delay(0.5).ledsEffect(ledsEffectSet, clYellow)
'''

def taskRight(data):
    robot.ledsEffect(ledsEffectSet, clGreen)#.ledsEffect(ledsEffectCircle, clWhite)
    #robot.speed(50, -50)
    '''
    while True:
        robot.ledsEffect(ledsEffectSet, clGreen)
        time.sleep(0.2)
        robot.ledsEffect(ledsEffectSet, clYellow)
        time.sleep(0.2)
    '''

import time ##
def taskAny(data):
    robot.ledsEffect(ledsEffectSet, clViolet)#.ledsEffect(ledsEffectCircle, clYellow)
    #robot.tone(440, 0.5)
    #robot.speed(-50, 50)
    '''while True:
        robot.ledsEffect(ledsEffectSet, clViolet)
        time.sleep(0.2)
        robot.ledsEffect(ledsEffectSet, clOrange)
        time.sleep(0.2)
    '''

def taskIdle(data):
    print "taskIdle"

robot = Root_v1_0()
robot.ifBumpersDetected(bumpersRightFront, taskRight)
robot.ifBumpersDetected(bumpersAnyFront, taskAny)
robot.ifStarts(lambda data: robot.move(40))

print "Robot created."
robot.start()
