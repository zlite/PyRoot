# Drawing using a for cycle with the the pen down and then with the pen up:

from wrapi.py.devices.Root.Root_v1_0 import *

distance = 10  #cm

robot = Root_v1_0()

import time
#robot.penDown()

# This sleep allows to observe on the debugging output what happens with the
# queue when it enqueues and dequeues at the same time. If not present, the
# enqueuing will happen so fast that it will first enqueue everything and
# only after that dequeing will start:
#time.sleep(2)

# robot.speed(5, -5)

# This will fill a 100 elements TxQueue, and thus can not send the last stop
# command if there isn't a delay between the for loop and the stop:
#for i in range(60):
# This does not fill the TxQueue:
for i in range(20):
    #robot.penDown()
    #time.sleep(0.2)
    #robot.move(distance)  # cm
    #robot.rotate(90)
    #robot.penAndEraserUp()
    #time.sleep(0.2)

    robot.speed(25, -25)
    #time.sleep(0.2)
    robot.speed(0, 0)
    #time.sleep(0.2)
    print i

#time.sleep(1)

print "stop! qsize =", localBleClient._txQueue.qsize()
robot.stop()

#robot.penAndEraserUp()
#for i in range(4):
#    robot.move(distance)  # cm
#    robot.rotate(-90)
