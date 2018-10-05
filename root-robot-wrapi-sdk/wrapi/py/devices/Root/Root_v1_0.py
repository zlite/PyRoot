import time
import threading ##

# The Colors are imported so they are re-exported to the user's code when it
# imports this module:
from wrapi.py.computing.Colors import *

# Devices:
import wrapi.py.devices.RemoteDevice as RemoteDevice
from wrapi.py.devices.RemoteDCMotor import RemoteDCMotor
from wrapi.py.devices.DeviceInfo import DeviceInfo
from wrapi.py.devices.RemotePositionDriver2D import RemotePositionDriver2D
from wrapi.py.devices.RemoteDifferentialDrive import RemoteDifferentialDrive
from wrapi.py.devices.RemoteServo import RemoteServo
from wrapi.py.devices.RemoteDrawingTool import RemoteDrawingTool
from wrapi.py.devices.RemoteLedRgbDriver import *
from wrapi.py.devices.RemoteToneDriver import RemoteToneDriver
from wrapi.py.devices.RemoteButtons import RemoteButtons
from wrapi.py.devices.RemoteCamera1d import RemoteCamera1d

# Communications stuff:
import wrapi.py.computing.PacketHelper as PacketHelper
from wrapi.py.computing.DeviceMessage import DeviceMessage
from wrapi.py.devices.BleSocketClient import *
from wrapi.py.devices.BleSerialPort import BleSerialPort
from wrapi.py.devices.Root.RootProtocolSerial_v1_0 import RootProtocolSerial_v1_0

# Events stuff:
import wrapi.py.computing.Events as Events


_localBleClient = BleSocketClient(txQueueSize=20)

# Tries to start the automatic connection to a local server and to the default
# port. Scanning starts after having defined the Root_v1_0 class with its
# unique UUID (see the last lines of this file). This is the connection
# to the BleServer through the socket, NOT to the ble devices themselves:
_localBleClient.connect()


# User constants:
# self.bumpersAny = 0  # ##Future usage.
bumpersAnyFront = 1
bumpersLeftFront = 2
bumpersRightFront = 3


# ##Implement everything (search for "pass" and for "##"):
class Root_v1_0(object):
    @staticmethod
    def getUniqueUuid():
        return "48c5d828-ac2a-442d-97a3-0c9822b04979"

    def __init__(
        self,
        name=None,
        didConnectCallback=None,
        autoConnect=True,
        connectionTimeOut=None
    ):
        # ##Improve these notes:
        # - If the name is not specified (None), it connects to the first robot
        # offered by the connection system.
        # - If didConnectCallback is not specified (None), this constructor
        # will block program execution until the robot is connected.
        # - If autoConnect == False: the system must do the connection manually
        # by using the methods on the robot's exposed port.
        # - connectionTimeOut is given in milliseconds: By default there is
        # no timeout, meaning that the system will continue trying to connect
        # to the robot:
        #   - In multithreading apps this is desirable, since the app can
        #   start with other robots and the robots that did not connect just
        #   keep waiting.
        #   - In non multithreading apps this is desirable too, since if the
        #   user is expecting the app to connect and that just doesn't happen,
        #   the user will stop the app. But if the user just wants the app to
        #   be waiting undefinetely until a robot appears, this is what will
        #   happen anyway.
        #   - Also, the user can always specify a timeout.

        # In WRAPI, Robots are mainly aggregates of devices:
        self._messageStop = DeviceMessage()
        self.info = DeviceInfo()

        self.positionDriver = RemotePositionDriver2D(
            RemoteDifferentialDrive(
                # ##Not providing acceleration by now but in the roadmap:
                RemoteServo(RemoteDCMotor(), True, True, True),
                RemoteServo(RemoteDCMotor(), True, True, True)
            )
        )

        self.drawingTool = RemoteDrawingTool()
        self.ledRgbDriver = RemoteLedRgbDriver()
        self.toneDriver = RemoteToneDriver()

        self.bumpers = RemoteButtons(2)
        self.touchSensors = RemoteButtons(4)
        self.camera1d = RemoteCamera1d()

        # ##Complete the robot's peripherals here.

        # Those are not private since an advance user may want to access them:
        self._delay = 0.3
        self.bleClient = _localBleClient
        self.port = None
        self.protocol = None
        if autoConnect:
            self.connect(name, didConnectCallback, connectionTimeOut)

        # Events system:
        self.events = Events.EventsManager()

        # ##Try to eliminate this in the future:
        # This has been added after experimenting with the robot, to prevent
        # some undesired behaviors after the connection (like the robot
        # not receiving commands for a small interval):
        time.sleep(1)

        # self._startDebugTime = time.time() # ##Debug.
        self.stop()

    # ///////////////////// Communications stuff: /////////////////////

    def connect(self, name=None, didConnectCallback=None,
                connectionTimeOut=None):
        # This is a BLOCKING METHOD:
        #
        # ##Add the timeout logic: Think if it will be provided by each
        # method (ie: bleClient.nextFreeDevice and port.connect or
        # if this whole thing will go to a thread followed by a blocking
        # loop that waits for the timeout, which is what I think that
        # should be done to really control the timeout as a whole and
        # reliable number).

        # Only the "connect" operations are blocking, not the getters that
        # query arrays of devices, etc. That's why nextFreeDevice is
        # non-blocking, while port.connect() is blocking:
        while self.port is None:
            self.port = BleSerialPort(self.bleClient.nextFreeDevice(name))
            self.protocol = RootProtocolSerial_v1_0(self, self.port)
            time.sleep(self._delay)  # Reduces cpu usage.

        # ##Add a timeout parameter to the BleDevice.connect method, and pass
        # to it the difference between the original timeout and the time used
        # on the previous while loop:
        self.port.connect()

        # Is didConnectCallback a function?
        if hasattr(didConnectCallback, '__call__'):
            didConnectCallback()

    def disconnect(self):
        if hasattr(self.port.disconnect, '__call__'):  # ##Test this.
            self.port.disconnect()
        self.port = None
        self.protocol = None

    # ///////////////////// Robot's own high level members: ///////////////////

    @property
    def messageStop(self):
        return self._messageStop

    # Low level stop command, that returns the id. Useful for users whom may
    # be taking care of the incremental ids traveling through the communication
    # channel:
    def _stop(self):
        id = self.messageStop.incrementId()
        result = bytearray([id])
        self.messageStop.data = PacketHelper.fillMessageDataWithZeroes(
            result,
            RemoteDevice.payloadSize
        )

        return id

    ## Change this in a way that only stops the motion: find the ocurrences of "stop" everywhere and refactor everything:
    def stop(self):
        self._stop()
        return self  # Supports chained methods.

    # Stops the robot, with its drivers, motors, LEDs, buzzer, pencil, etc.,
    # and optionally the events sytem:
    def halt(self, stopEvents=True):
        if stopEvents:
            self.events.stop()
        return self.stop()

    # ///////////////////// High level robot commands: ///////////////////

    def _checkIfThreadIsRunning(self, currentThread):
        if not getattr(currentThread, 'running', True):
            #self._stopEvent()
            raise ValueError('Thread stopped.')  # ##i18n.

    # ##Future: Add speed parameter.
    # ##Future: Add unit parameter?
    # These are "blocking methods" but they can be interrupted by robot events:
    def move(self, distance):
        self.positionDriver.moveStraight(distance)

        # Calculates the timeout based on the distance:
        # ## The measured constant for rotations will be different once
        # speed becomes configurable for move commands.
        # ##Improve this: the constant is not linear, since there is more
        # "dead time" (due to communications overhead) for smaller distances
        # than the dead time for bigger instances.

        #timeout = abs(distance*0.135)  # 2.7s/20cm
        timeout = abs(distance*0.25)
        start = time.time()
        currentThread = threading.current_thread()

        while self.positionDriver.isMovingStraight:
            self._checkIfThreadIsRunning(currentThread)

            diff = time.time() - start
            if diff > timeout:
                # print "Move ended by timeout =", diff  # ##Log this.
                break

        return self

    # ##Future: Add speed parameter.
    # ##Future: Add unit parameter?
    def rotate(self, angle):
        self.positionDriver.rotate(angle)

        # Calculates the timeout based on the angle:
        # ## The measured constant for rotations will be different once
        # speed becomes configurable for rotate commands:
        # ##Improve this: the constant is not linear, since there is more
        # "dead time" (due to communications overhead) for smaller angles
        # than the dead time for bigger angles.

        # timeout = abs(angle*0.018)
        timeout = abs(angle*0.03)
        start = time.time()
        # print "timeout =", timeout  # ##Debug.
        currentThread = threading.current_thread()

        while self.positionDriver.isRotating:
            self._checkIfThreadIsRunning(currentThread)

            diff = time.time() - start
            # print diff  # ##Debug.
            if diff > timeout:
                # print "Rotate ended by timeout =", diff  # ##Log this.
                break
        # print "rotate finished, diff = ", diff  # ##Debug.

        return self

    # Absolute rotation: ##Not finished yet.
    # ##Future: Add speed parameter.
    # ##Future: Add unit parameter?
    def rotateTo(self, angle):
        self.positionDriver.rotateTo(angle)

        ## This timeout does not work yet, since it needs to calculate
        # the final angle, by knowing the current angle, which is not yet
        # implemented.

        # Calculates the timeout based on the angle:
        # ## The measured constant for rotations will be different once
        # speed becomes configurable for rotate commands:
        # ##Improve this: the constant is not linear, since there is more
        # "dead time" (due to communications overhead) for smaller angles
        # than the dead time for bigger angles.

        # timeout = abs(angle*0.018)
        timeout = abs(angle*0.03)
        start = time.time()
        currentThread = threading.current_thread()

        while self.positionDriver.isRotating:
            self._checkIfThreadIsRunning(currentThread)

            diff = time.time() - start
            if diff > timeout:
                # print "Rotate ended by timeout =", diff  # ##Log this.
                break

        return self

    # ##Future:
    # @property
    # Returns the last state saved from the "speed call and the
    # setSpeed finished message":
    # def speed(self):
    #    pass

    # ##Analyse if this will be a setter or if this is ok:
    def speed(self, leftSpeed, rightSpeed, unit=0):
        self._checkIfThreadIsRunning(threading.current_thread())
        # print "0.canWrite =", _localBleClient.canWrite  # ##Debug.
        self.positionDriver.differentialDrive.speed(leftSpeed, rightSpeed)
        self.bleClient.waitUntilCanWrite()
        return self

    # ##Future:
    # Add other getters which work with the protocolo "finsihed" messages.

    # ##Future:
    # @property
    # def speed(self):
    #    pass

    # def power(leftPower, rightPower):
    #    pass

    def _waitForDrawingtool(self):
        # The timeout for the drawing tool is fixed:
        timeout = 2.0  # Seconds.
        start = time.time()
        currentThread = threading.current_thread()

        while self.drawingTool.isStateBeingSet:
            self._checkIfThreadIsRunning(currentThread)
            diff = time.time() - start
            if diff > timeout:
                # ##Log this:
                print "Drawingtool command ended by timeout =", diff
                break

    def penDown(self):
        self._checkIfThreadIsRunning(threading.current_thread())
        self.drawingTool.penDown()
        self._waitForDrawingtool()
        return self

    def eraserDown(self):
        self._checkIfThreadIsRunning(threading.current_thread())
        self.drawingTool.eraserDown()
        self._waitForDrawingtool()
        return self

    def penAndEraserUp(self):
        self._checkIfThreadIsRunning(threading.current_thread())
        self.drawingTool.bothUp()
        self._waitForDrawingtool()
        return self

    # [freq] = Hz; [duration] = s
    def tone(self, freq, duration):
        self.toneDriver.play(freq, duration)

        # Calculates the timeout based on the duration, adding a safety margin:
        timeout = abs(duration*3)
        start = time.time()
        currentThread = threading.current_thread()

        while self.toneDriver.isPlaying:
            self._checkIfThreadIsRunning(currentThread)
            diff = time.time() - start
            if diff > timeout:
                print "Tone ended by timeout =", diff  # ##Log this.
                break

        return self

    # This method can be overloaded, so r becomes "colorCode" (from Colors.py):
    def ledsEffect(self, effect, r, g=None, b=None):
        self._checkIfThreadIsRunning(threading.current_thread())
        self.ledRgbDriver.effect(effect, r, g, b)
        self.bleClient.waitUntilCanWrite()
        return self

    def eyes(self, leftIntensity, rightIntensity):
        self._checkIfThreadIsRunning(threading.current_thread())
        ##Implement.
        self.bleClient.waitUntilCanWrite()
        return self

    # This method exists in order to support chained methods with delays.
    # [freq] = Hz; [duration] = s
    # TODO: It will change to wait, in order to improve consistency with Square Level 2.
    def delay(self, seconds):
        time.sleep(seconds)
        return self

    # ///////////////////// Events subsystem (high level API): ////////////////
    def _sensorDidChange(self, source, data):
        self.events.arbitrate(source, data)

    def _stopEvent(self):
        # Only stops move/rotate/rotateTo commands but does not change
        # movements due to speed states previously set or any other state
        # of the robot:
        if self.positionDriver.isRotating or self.positionDriver._isMovingStraight:
            self.positionDriver.stop()
        #       time.sleep(0.02)  ##
        # self.positionDriver.stop()

    # ///////////////////// Start:

    # This method also DOES NOT support method chaining on purpose, since
    # it triggers an asunchronous event, and so the commands chained with it
    # will not be arbitrated by the events subsystem.
    def start(self):
        # Only assigns the events if the events system is being used:
        self.bumpers.dataDidChange = self._sensorDidChange
        self.touchSensors.dataDidChange = self._sensorDidChange
        self.camera1d.dataDidChange = self._sensorDidChange
        self.events.start()

    def ifStarts(self, callback, priority=Events.priorityLower):
        event = Events.Event()
        event.source = self.events
        event.condition = None
        event.testFunction = lambda data, event: True
        event.task = callback
        event.stop = self._stopEvent

        self.events.insert(priority, event)

    # ///////////////////// Bumpers:
    def _bumpersTest(self, data, event):
        if event.condition == bumpersLeftFront:
            return data[0]
        elif event.condition == bumpersRightFront:
            return data[1]
        else:  # bumpersAnyFront
            return data[0] or data[1]
        return False

    def ifBumpersDetected(
        self, bumperStates, callback, priority=Events.priorityLower
    ):
        event = Events.Event()
        event.source = self.bumpers
        event.condition = bumperStates
        event.testFunction = self._bumpersTest
        event.task = callback
        event.stop = self._stopEvent

        self.events.insert(priority, event)

    # ///////////////////// Touch sensors:
    def _ifTouchSensorsTest(self, data, event):
        ##Implmement:
        ##Pass data as an array of bool, given that this is an "AND" (where the bumpers where an "OR").
        return False

    def ifTouchSensorsDetected(
        self, touchSensorStates, callback, priority=Events.priorityLower
    ):
        event = Events.Event()
        event.source = self.touchSensors
        event.condition = touchSensorStates
        event.testFunction = self._ifTouchSensorsTest
        event.task = callback
        event.stop = self._stopEvent

        self.events.insert(priority, event)

    # ///////////////////// Camera1d:
    def _ifColorsTest(self, data, event):
        # print "data  = ", data  # ##Debug.
        # print "zones = ", event.zones  # ##Debug.

        for i in range(0, len(event.zones)):
            zoneColor = event.zones[i]
            if zoneColor != clAny and zoneColor == data[i]:
                return True
        return False

    def ifColorsDetected(self, colors, callback, priority=Events.priorityLower):
        event = Events.Event()
        event.source = self.camera1d
        event.condition = colors
        event.testFunction = self._ifColorsTest
        event.task = callback
        event.stop = self._stopEvent

        # Custom members with precomputed values:
        event.zones = self.camera1d.computeDetectionZones(colors)

        self.events.insert(priority, event)

    # ##Future:
    # Add light sensor events.
    # Add battery sensor events.
    # Add gyro events.
    # Add accelerometer events.
    # Add magenetic force sensor events.
    # Add distance traveled events?
    # Add methods for init/deinit the events for a particular subsystem:
        ## Something that calls the events.remove method and also a list method.
    # Methods for the expansion port.

# Searches for BLE devices with Root's unique UUID:
_localBleClient.startScanning([Root_v1_0.getUniqueUuid()])
