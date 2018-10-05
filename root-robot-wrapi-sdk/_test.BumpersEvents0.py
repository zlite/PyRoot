# Bumpers callback example.
# Prints the state of the bumpers each time a bumper is pressed.

import time
from wrapi.py.devices.Root.Root_v1_0 import *


def taskLeft(data):
    print "taskLeft:", data

    '''
    while True:
        print "currentIndex:", robot.events._currentEventIndex
        time.sleep(0.5)
    '''

def taskRight(data):
    print "taskRight:", data

import time ##
def taskAny(data):
    while True:
        print "taskAny:", time.time()
        time.sleep(1)

def taskIdle(data):
    print "taskIdle"

robot = Root_v1_0()
robot.ifBumpersDetected(bumpersLeftFront, taskLeft)
##print robot.events._events
robot.ifBumpersDetected(bumpersLeftFront, taskRight)
##print robot.events._events
robot.ifBumpersDetected(bumpersAnyFront, taskAny)
##print robot.events._events

robot.start()
print "Robot created."
