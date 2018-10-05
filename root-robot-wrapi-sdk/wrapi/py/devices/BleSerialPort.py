from wrapi.py.computing.DeviceMessage import DeviceMessage


class BleSerialPort(object):
    def __init__(self, bleDevice):
        self.bleDevice = bleDevice
        self.rxListener = DeviceMessage()

        # ##Change this for the IP address and te TCP/IP ports:
        self._serialId = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"

        self.txId = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
        self._rxId = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

        self._isConnected = False

    @property
    def serialId(self):
        return self._serialId

    @serialId.setter
    def serialId(self, value):
        self._serialId = value

        # If this property changes, the bleDevice must disconnect from the previous
        # serial service:
        self.disconnect()

    @property
    def rxId(self):
        return self._rxId

    @rxId.setter
    def rxId(self, value):
        # ##Test this:
        # If this property changes, the listener must be reasigned on
        # the bleDevice:
        self.bleDevice.removeListener(self.serialId, self.rxId)
        self._rxId = value
        self.bleDevice.addListener(self.serialId, self.rxId, self.rxListener)
        # print "rxId.setter"  # ##Debug.

    @property
    def isConnected(self):
        return self._isConnected

    def connect(self):
        # This method does not do anytihng if the bleDevice is already
        # connected.
        self.bleDevice.connect()
        self.bleDevice.addListener(self.serialId, self.rxId, self.rxListener)

    def disconnect(self):
        self.bleDevice.disconnect()
        self.bleDevice.removeListener(self.serialId, self.rxId)

    def write(self, value):
        self.bleDevice.write(self.serialId, self.txId, value)
