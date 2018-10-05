# Two robots: one connected using a local BleServer and another using a
# remote BleServer.

import threading
from wrapi.py.devices.Root.Root_v1_0 import *


class ThreadDraw (threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot

    def run(self):
        robot = self.robot  # Just to make it shorter.
        robot.penDown()

        for i in range(0, 3):
            robot.move(30)  # 30 cm
            robot.rotate(90)

        robot.penAndEraserUp()

# Creates the local robot, as always:
localRobot = Root_v1_0()

# Creates the remote robot and the needed ble client:
remoteBleClient = BleSocketClient()
remoteBleClient.connect(
    None,
    None,
    "10.1.32.94"  # Your BleServer's IP address here.
    # port= The port number can be changed here if needed.
)
remoteRobot = Root_v1_0(None, None, False)  # Important: Autoconnect=False
remoteRobot.bleClient = remoteBleClient
remoteRobot.connect()

# Run each robot's tasks:
ThreadDraw(localRobot).start()
ThreadDraw(remoteRobot).start()
