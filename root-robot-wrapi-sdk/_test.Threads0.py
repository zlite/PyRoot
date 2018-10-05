import time
import threading
from wrapi.py.devices.Root.Root_v1_0 import *


class ExceptionThread(threading.Thread):
    def run(self):
        self._running = True
        while self._running:
            time.sleep(0.05)  # ##Evaluate if this helps with CPU time and if the response time is fast enough:
        self.xyx()  # Raises an exception!

    def stop(self):
        self._running = False


class ThreadDraw(threading.Thread):
    def run(self):
        self.e = ExceptionThread()
        self.e.start()
        try:
            for i in range(0, 5):
                print i  # ##Debug.
                robot.move(5)  # cm
                robot.rotate(90)

            robot.penAndEraserUp()
        except:
            robot.stop()

    def stop(self):
        self.e.stop()

robot = Root_v1_0()
t = ThreadDraw()
t.start()
import time
time.sleep(2)
t.stop()
