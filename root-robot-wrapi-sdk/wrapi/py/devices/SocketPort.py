# ##This is not a singleton, since for sockets there may be a lot of instances:


class SocketPort(object):
    def __init__(self):
        pass  # ##Implement.

    def connect(self, peripheral, stopScan=False):
        pass  # ##Implement.

    def disconnect(self, removeAllListeners=True):
        pass  # ##Implement.

    def addListener(self, serviceId, characteristicId, listener):
        pass  # ##Implement.

    def removeListener(self, serviceId, characteristicId):
        pass  # ##Implement.

    def write(self, serviceId, characteristicId, value):
        # ##Implement.
        # ##Debug:
        print "BLEPort.write:"
        print serviceId
        print characteristicId
        print value
