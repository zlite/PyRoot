import time
import threading
from wrapi.py.devices.Root.Root_v1_0 import *


class ThreadDraw(threading.Thread):
    def run(self):
        try:
            for i in range(0, 5):
                print i  # ##Debug.
                robot.move(5)  # cm
                robot.rotate(90)

            robot.penAndEraserUp()
        except:
            robot.stop()

    def dummyRun(self):
        return

    def stop(self):
        robot.stop()
        self.run = self.dummyRun
        self._Thread__stop()
        self = None
        self.xyx()

robot = Root_v1_0()
t = ThreadDraw()
t.start()
import time
time.sleep(1)
robot.stop()
t._Thread__stop()
t._Thread__delete()
# del t
#t.stop()
