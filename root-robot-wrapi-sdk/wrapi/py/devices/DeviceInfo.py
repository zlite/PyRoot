

class DeviceInfo(object):
    def __init__(self):
        # These properties are nil if not used / nor defined for a device:
        self._String = ""
        self._hardwareVersion = ""
        self._firmwareVersion = ""
        self._protocolVersion = ""

        # ##Add the getters (@property)
