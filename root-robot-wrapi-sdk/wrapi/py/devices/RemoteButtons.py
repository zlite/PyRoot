from wrapi.py.computing.DeviceMessage import DeviceMessage
# import wrapi.py.computing.PacketHelper as PacketHelper  # ##Debug.


class RemoteButtons(object):
    def __init__(self, buttonsCount=16):
        self.buttonsCount = buttonsCount
        self._states = [False] * self.buttonsCount

        self._messageStates = DeviceMessage()
        self._messageStates.dataDidChange = self._processMessageStates

    @property
    def messageStates(self):
        return self._messageStates

    @property
    def states(self):
        return self._states

    def enableStatesDidChangeEvent(self):
        # ##Future: This is not implemented on the robot's firmware yet.
        pass

    def disableAllEvents(self):
        # ##Future: This is not implemented on the robot's firmware yet.
        pass

    def _processMessageStates(self, data):
        # ##Future: Add timestamp processing.
        # ##Future: Add command id processing.

        # The current protocol supports up to 16 bumpers, packaged as single
        # bits on the first 2 bytes. The bumper[0] is the MSb on the MSB, so it
        # can be expanded "to the right" in the future with more bumpers, using
        # the remaining non used bytes on the protocol:

        tempData = data[5:7]

        # ##Debug:
        # print "_processMessageStates:"
        # PacketHelper.printBytearray(tempData)

        # This is done on a temporal variable to protect potential readers of
        # the public variable while writing it:
        tempStates = []
        for i in range(2):
            for j in reversed(range(8)):
                # Adds 1 to the index because the first byte is for the
                # command's incremental id.
                tempStates.append(((tempData[i] >> j) & 0x01) == 0x01)

        self._states = tempStates[0: self.buttonsCount]
        self.dataDidChange(self, self._states)

    # User events (callback functions):
    def dataDidChange(self, source, data):
        return None
