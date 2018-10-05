

class BleDevice(object):
    def __init__(self, bleClient, uuid):
        self._isConnected = False

        self.bleClient = bleClient
        self._uuid = uuid
        self.name = ""

    @property
    def isConnected(self):
        return self._isConnected

    @property
    def uuid(self):
        return self._uuid

    # This method will do nothing if the port is already connected, but if
    # it's not, it will block until the port connects with the device.
    def connect(self):
        # This is a blocking method because bleClient.connectDevice is so:
        self.bleClient.connectDevice(self._uuid)

    def disconnect(self):
        self.bleClient.disconnectDevice(self._uuid)

    def write(self, serviceId, characteristicId, value):
        self.bleClient.write(self._uuid, serviceId, characteristicId, value)

    def addListener(self, serviceId, characteristicId, listener):
        self.bleClient.addListener(
            self._uuid, serviceId, characteristicId, listener
        )

    def removeListener(self, serviceId, characteristicId):
        self.bleClient.removeListener(self._uuid, serviceId, characteristicId)
