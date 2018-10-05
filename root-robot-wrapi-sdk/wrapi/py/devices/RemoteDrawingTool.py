import RemoteDevice
import wrapi.py.computing.PacketHelper as PacketHelper
from wrapi.py.computing.DeviceMessage import DeviceMessage

# This class can be any tool that can be headed down or up, mainly for drawing
# purposes. It's an abstraction, so if in some devices the tools are
# mutually-exclusive (for example a pen and an eraser controlled by the same
# actuator), it's up to the device to interpret the protocol commands in order
# to drive the tools properly.


class RemoteDrawingTool(object):
    def __init__(self):
        self._bothUp = 0
        self._penDown = 1
        self._eraserDown = 2

        self._messageStateSet = DeviceMessage()
        self._messageStateSetFinished = DeviceMessage()
        self._messageStateGet = DeviceMessage()

        self._isStateBeingSet = False

        self.messageStateGet.dataDidChange = self.stateGetMessageDidChange
        self.messageStateSetFinished.dataDidChange = self.stateSetFinishedMessageDidChange

    @property
    def isStateBeingSet(self):
        return self._isStateBeingSet

    @property
    def bothUp(self):
        return self._bothUp

    @property
    def penDown(self):
        return self._penDown

    @property
    def eraserDown(self):
        return self._eraserDown

    @property
    def messageStateSet(self):
        return self._messageStateSet

    @property
    def messageStateSetFinished(self):
        return self._messageStateSetFinished

    @property
    def messageStateGet(self):
        return self._messageStateGet

    def _encodeState(self, message, state):
        self._isStateBeingSet = True
        id = self.messageStateSet.incrementId()
        result = bytearray([id]) + bytearray([state])
        message.data = PacketHelper.fillMessageDataWithZeroes(
            result,
            RemoteDevice.payloadSize
        )
        return id

    def bothUp(self):
        return self._encodeState(self.messageStateSet, self._bothUp)

    def penDown(self):
        return self._encodeState(self.messageStateSet, self._penDown)

    def eraserDown(self):
        return self._encodeState(self.messageStateSet, self._eraserDown)

    # ##Test this:
    def stateGetMessageDidChange(self, message):
        state = message.data[1]
        self.stateDidChange(state)

    def stateSetFinishedMessageDidChange(self, message):
        self._isStateBeingSet = False
        # print "stateSetFinishedMessageDidChange"  # ##Debug.
        self.stateSetDidFinish()

    # ##See comment about this function on the RemotePositionDriver2D class:
    def forceStopFlagsToFalse(self):
        self._isStateBeingSet = False

    def stop(self):
        self.bothUp()
        return 0  # ##

    # User events (callback functions):
    def stateDidChange(self, state): return None

    def stateSetDidFinish(self): return None
