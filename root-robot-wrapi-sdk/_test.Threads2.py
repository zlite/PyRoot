import time
import threading
from wrapi.py.devices.Root.Root_v1_0 import *


class ThreadDraw(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False

    def run(self):
        self.running = True
        try:
            for i in range(0, 5):
                # xx ##Raise an exception to try how it works.
                print i  # ##Debug.
                robot.move(10)  # cm
                print "moved"
                robot.rotate(90)

            robot.penAndEraserUp()
        except ValueError as error:
            print error.args[0]
            #robot.stop()

    def dummyRun(self):
        return

    def stop(self):
        self.running = False
        #robot.stop()

robot = Root_v1_0()
t = ThreadDraw()
t.start()
import time
time.sleep(1)
t.stop()

'''
time.sleep(2)
t = ThreadDraw()
t.start()
'''
