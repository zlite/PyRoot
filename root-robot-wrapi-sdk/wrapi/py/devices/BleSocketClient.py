import collections
import time
import threading
import socket
import Queue
# import uuid  # ##Possible future usage.

import wrapi.py.computing.PacketHelper as PacketHelper  # ##Debug.
from wrapi.py.devices.BleDevice import BleDevice

BleSocketClientDefaultPort = 44199  # ##Select a nicer number.

class ThreadTx (threading.Thread):
    def __init__(self, bleSocketClient):
        threading.Thread.__init__(self)
        self._bleSocketClient = bleSocketClient
        self._socket = bleSocketClient._dataSocket
        self._paused = False

    def resume(self):
        self._paused = False

    def pause(self):
        self._paused = True

    def run(self):
        while(True):
            # This was deprecated because the experiments with the robot
            # showed clearly that the delay introduced is unnaceptable:
            #time.sleep(self._bleSocketClient.txDelay)  # Reduces CPU usage.

            if self._paused:
                continue

            # Tries to send a message from the queue. If it's empty, does
            # nothing:
            try:
                '''
                # ##9: This timeout system does not work nice with some real
                # time activities with the robot.
                # Timeout for the tx system:
                timeDiff = time.time() - self._bleSocketClient._canWriteStartTime
                if timeDiff > 0.11:  # ##Unhardcode.
                #if timeDiff > 0.13:  # ##Unhardcode.
                #if timeDiff > 0.5:  # ##Unhardcode.
                    if not self._bleSocketClient._canWrite:
                        self._bleSocketClient._canWriteStartTime = time.time()
                        self._bleSocketClient._canWrite = True
                        print "time =", timeDiff
                '''

                message = self._bleSocketClient._txQueue.get_nowait()
                # print "txQueue.size =", self._bleSocketClient._txQueue.qsize()  # ##Debug.

                # Sends the message to the socket:
                # print "Dequeue: ", message  # ##Debug.
                self._socket.sendall(message)
            except:
                pass


class ThreadRx (threading.Thread):
    def __init__(self, bleSocketClient):
        threading.Thread.__init__(self)

        self._bleSocketClient = bleSocketClient
        self._socket = bleSocketClient._dataSocket
        self._listeners = bleSocketClient._listeners

    def run(self):
        while(True):
            # This was deprecated because the experiments with the robot
            # showed clearly that the delay introduced is unnaceptable:
            #time.sleep(self._bleSocketClient.rxDelay)  # Reduces CPU usage.

            data = self._socket.recv(1024)
            # print "Rx: "  # ##Debug.
            # print repr(data)  # ##Debug.

            # This try-except block prevents the program to crash when events
            # come too soon right after the program having started, thus
            # allowing for possible situations where the listeners may not be
            # initialized yet. This also works if no listeners are defined at
            # all by the user.
            try:
                # ##Experiment: Hardcoded call to the only listener that is set
                # by he moment. This will be extended to a generic mechanism
                # once the bleSocketServer/Client are finished:

                # print self._listeners.items()[0]  # ##Debug.
                key, value = self._listeners.items()[0]
                # ##value.data = data
                arrayData = PacketHelper.hexStringToBinaryBytearray(data)
                ans = arrayData[0]
                # print "ans =", ans  # ##Debug.

                if ans == self._bleSocketClient._ansCanWrite:
                    self._bleSocketClient._canWrite = True
                    # ##9: Resets the timeout:
                    # self._bleSocketClient._canWriteStartTime = time.time()

                    # print "canWrite!"  # ##Debug.
                elif ans == self._bleSocketClient._ansData:
                    value.data = arrayData[1:len(arrayData)]

                    # ##Debug:
                    # print "Data! payLoad ="  # ##Debug.
                    # PacketHelper.printBytearray(arrayData[1:len(arrayData)])

                # ##Implement here the stuff for Rx:
                #message = bytearray(data)
                #PacketHelper.printBytearray(message)  # ##Debug.
            except Exception as error:
                pass

            if not data:
                break

            # ##Try to reduce cpu usage here.

        self._socket.close()  # ##
        print "Socket closed"  # ##Debug.


# This is a class and not a module (singleton) because multiple instances must
# be allowed: They are useful for the case when there is are different ble
# servers running in different computers, available through the network. Also
# in theory, in the future, it could be possible to have different servers on
# the same computer accessing different ble hardware (but this will imply
# implementing a new kind of BleServer that right now is not implemented).
class BleSocketClient(object):
    def __init__(self, txQueueSize):
        self._isConnected = False  # ##

        # Return the list containing the scanned devices:
        self._devices = collections.OrderedDict()
        self._listeners = collections.OrderedDict()

        self._txQueue = Queue.Queue(txQueueSize)
        self._canWrite = True
        # ##9: self._canWriteStartTime = time.time()
        # self.rxDelay = 0.01
        # self.txDelay = 0.01  # BLE's measured minimum was 32 ms so this is ok

    @property
    def isConnected(self):
        return self._isConnected

    @property
    def canWrite(self):
        return self._canWrite

    # ##Improve this in the future, to use real timeout (with time.time),
    # although this worked well with the real robot:
    def waitUntilCanWrite(self, maxWaitings=20):
        waitings = 0
        while not self._canWrite:
            if waitings >= maxWaitings:
                self._canWrite = True
                print "timeout", time.time()  # ##Debug.
                break
            waitings += 1
            # print waitings  # ##Debug.
            time.sleep(0.005)  # ##Experiment: Put this delay on a constant.

    # ##Future: This is a blocking method, but by now, it just raises an error
    # if it can not connect to the server. So in the future, add all the
    # automatic features for starting the server, waiting until a connection
    # is made, etc.
    # - ##Future: didConnect is a callback, we do not necessary need to use it
    # and this could be used as a blocking method for most usages.
    # - By default it will use the local adddress and the default port number.
    # - If the server is not running, by default it will try to start it.
    # - timeout's default value is without timeout. ##Evaluate if this is ok.
    # - ##Future: See if a callback will be provided for a non blocking
    # version (not by now).
    def connect(
        self,
        didConnect=None,
        timeout=None,
        ip="127.0.0.1",
        port=BleSocketClientDefaultPort,
        serverPath=None,
        startServer=True
    ):
        self._ansCanWrite = 10
        self._ansData = 20

        self._cmdGetVersion = bytearray([10])
        self._cmdStartScanning = bytearray([20])
        self._cmdStopScanning = bytearray([30])
        self._cmdConnectDevice = bytearray([40])
        self._cmdDisconnectDevice = bytearray([50])
        # ## Not used by now:
        # self._cmdStartTx = bytearray([60])
        # self._cmdStopTx = bytearray([70])
        self._cmdWrite = bytearray([80])

        self._delay = 0.5

        self._sizeOfPayloadLen = 2
        self._bleIdLen = 36
        self._serverCommandPos = 0
        self._lenPos = 1
        self._bleDeviceIdPos = self._lenPos + 2
        self._bleServiceIdPos = self._bleDeviceIdPos + self._bleIdLen
        self._bleCharacteristicIdPos = self._bleServiceIdPos + self._bleIdLen
        self._bleCommandPos = self._bleCharacteristicIdPos + self._bleIdLen

        ##self._dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # This is the blocking stuff:
        self._isConnected = False
        while not self._isConnected:
            try:
                # print "Trying to connect 0"  # ##Debug.
                self._dataSocket = None  # Probably not necessary.
                self._dataSocket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                self._dataSocket.connect((ip, port))
                self._isConnected = True
                # print "Connected 0"  # ##Debug.
            except Exception as error:
                # print "Trying to connect 1"  # ##Debug.
                time.sleep(self._delay)  # Reduces cpu usage.
        # print "Connected 1"  # ##Debug.

        self._threadRx = ThreadRx(self)
        # We don't care about the thread once the program ends:
        self._threadRx.start()

        # TxQueue management:
        self._threadTx = ThreadTx(self)
        self._threadTx.start()

    def disconnect(self):
        self._dataSocket.shutdown(socket.SHUT_RDWR)
        self._dataSocket.close()
        self._devices.clear()
        self._isConnected = False

    def _addLenByte(self, message):
        # print "payLoad.len = ", len(message) - 3  # ##Debug.
        payLoadLenArray = PacketHelper.int16ToByteArray(len(message) - 3)
        message[self._lenPos] = payLoadLenArray[0]
        message[self._lenPos + 1] = payLoadLenArray[1]

    def _finishAndSendMessage(self, message):
        self._addLenByte(message)
        self._dataSocket.sendall(message)

    # - Returns the lowest index available BLE device.
    # - If a name is provided, this filters by name.
    # - uuid allows to filter a specific device by using its uique
    # identifier (uuid). This allows for apps to store the uuid of a device
    # that is often used and then try to connect directly to it.
    def nextFreeDevice(self, name=None, uuid=None, timeout=None):
        # This is a NON-BLOCKING METHOD:
        #
        # ##Implement:
        #   ##Add the device name.
        #   ##Add the device uuid.
        #   ##Evaluate if there will be an UNIQUE index or something:
        #   ##Be carefull because the list of devices can change and still
        #   events could arrive when there is a device already connected?
        #   Timeout subsystem.
        key, value = self.freeDevices().items()[0]
        return value

    # This method should return a list of the available devices:
    def freeDevices(self):
        # ##Implement.
        # ##This is a temporal result, just for testing.
        # This should be filled with the message from the server sent by the
        # callback which is triggered whenever the server discovers a new
        # device:
        result = collections.OrderedDict()  # ##
        id = "7740c885-90cd-40bc-8462-d36049093824"
        result[id] = BleDevice(self, id)
        return result

    # ##Evaluate if those methods are necessary:
    def connectedDevices(self):
        # ##Implement.
        return {}

    def allDevices(self):
        tempCopy = self.freeDevices.copy()
        tempCopy.update(self.connectedDevices)
        return tempCopy

    # Rx:
    def addListener(self, deviceId, serviceId, characteristicId, listener):
        key = deviceId + serviceId + characteristicId
        # print "key=", key  # ##Debug.
        self._listeners[key] = listener

    def removeListener(self, deviceId, serviceId, characteristicId):
        key = deviceId + serviceId + characteristicId
        # print "key=", key  # ##Debug.
        del self._listeners[key]

    # Commands for the server:

    '''
    # Future: This command will retreive the version of the server (which
    # defines the protocol used too):
    def getVersion(self):
        message = self._cmdGetVersion + bytearray(self._sizeOfPayloadLen)
        self._finishAndSendMessage(message)
    '''

    # - Starts a BLE device scanning.
    # - If UUIDs are provided, filters by them, only listing the devices
    # having services with these UUIDs.
    # - didFindDevice is a callback that is called whenever a new device is
    # found.
    # - Note: this function will not stop scanning until a stopScan is
    # explicity called.
    # - Note: The filtering by service UUIDs must be done here, since it can
    # not be done later on methods like nextFreeDevice.
    # - Note: A call to the startScanning method shouldn't necessarily
    # disconnect any connected device. So a call to this method just
    # add devices to the freeDevices list, that's all.
    def startScanning(self, uuids=None, didFindDevice=None):
        # print "startScanning: ", uuids  # ##Debug.
        self._devices.clear()  # ##Evaluate if this action is always desired.

        uuidsArray = bytearray()
        for uuid in uuids:
            uuidsArray += bytearray(uuid)
        # print "startScanning: ", uuidsArray  # ##Debug.

        message = self._cmdStartScanning + bytearray(self._sizeOfPayloadLen) + uuidsArray
        self._finishAndSendMessage(message)
        time.sleep(self._delay)  # ## Evaluate later if it's necessary.
        # print "end startScanning"  # ##Debug.

    def stopScanning(self):
        message = self._cmdStopScanning + bytearray(self._sizeOfPayloadLen)
        self._finishAndSendMessage(message)

    def connectDevice(self, deviceId):
        message = self._cmdConnectDevice + bytearray(self._sizeOfPayloadLen) + bytearray(deviceId)
        self._finishAndSendMessage(message)
        time.sleep(self._delay)  # ## Evaluate later if it's necessary.
        # print "end connectDevice" # ##Debug.

    def disconnectDevice(self, deviceId):
        message = self._cmdDisconnectDevice + bytearray(self._sizeOfPayloadLen) + bytearray(deviceId)
        self._finishAndSendMessage(message)

    # Tx and TxQueue stuff:
    def startTx(self):
        # ##If there is finally device tx queues on the BleSocketServer side,
        # this should send the command to the BleSocketServer to empty the
        # specific queue belonging to this device.

        # ##This should be thread-safe in our specific case, but TEST IT:
        self._txQueue.mutex.acquire()
        self._txQueue.queue.clear()
        self._txQueue.mutex.release()
        self._threadTx.resume()

    def stopTx(self):
        self._threadTx.pause()

    def write(self, deviceId, serviceId, characteristicId, value):
        # ##Evaluate if a Tx queue is necessary for tx operations:
        # In that case: use the txThread for dequeue.

        '''##Future: Compress the uuid into 128 bits long numbers?:
        message = bytearray([uuid.UUID(deviceId).bytes_le]) + bytearray([uuid.UUID(serviceId).bytes_le]) + \
                bytearray([uuid.UUID(characteristicId).bytes_le]) + value
        '''

        message = self._cmdWrite + \
            bytearray(self._sizeOfPayloadLen) + \
            bytearray(deviceId) + \
            bytearray(serviceId) + \
            bytearray(characteristicId) + value
        ''' ##Debug:
        print "value:"
        PacketHelper.printBytearray(message)
        print str(message[self._serverCommandPos])
        print message[self._lenPos:self._lenPos + 1]
        print message[self._bleDeviceIdPos:self._bleServiceIdPos]
        print message[self._bleServiceIdPos:self._bleCharacteristicIdPos]
        print message[self._bleCharacteristicIdPos:self._bleCommandPos]

        # ##IF this is not commented, COMMENT IT on final version:
        PacketHelper.printBytearray(message[self._bleCommandPos:])
        print "---"
        '''

        self._addLenByte(message)

        # Tries to send the message to the queue, but if it's full, does
        # nothing.
        # Note: ONLY the write commands needs a queue, since the delays
        # are on the BLE system trying to send commands to the robot, and thus
        # the tx multithreading subsystem is for writing these commands, not
        # server commands (like "startScanning" etc.)
        self._canWrite = False
        try:
            # print "enqueue: ", message  # ##Debug.
            self._txQueue.put_nowait(message)
            # print "txQueue.size =", self._txQueue.qsize()  # ##Debug.
        except:
            pass
