import wrapi.py.computing.PacketHelper as PacketHelper
from wrapi.py.computing.DeviceMessage import DeviceMessage


class RootProtocolSerial_v1_0(object):
    def __init__(self, robot, port):
        # ///////////////////// Protocol id definitions: /////////////////////
        self._rootId = 0
        self._rootGetVersionsId = 0
        self._rootSetDeviceNameId = 1
        self._rootGetDeviceNameId = 2
        self._rootStopId = 3

        self._positionDriverId = 1
        # Answers:
        self._positionDriverPositionId = 16
        self._positionDriverCumulativeDistanceId = 26
        # Commands:
        self._positionDriverSetMotorsPower = 0
        self._positionDriverSetServosSpeed = 4
        self._positionDriverMoveStraightId = 8
        self._positionDriverRotateId = 12
        self._drawingToolId = 2
        self._drawingToolPenSetStateId = 0
        self._drawingToolPenGetStateId = 1
        self._drawingToolEraserSetStateId = 2

        self._ledRgbDriverId = 3
        self._ledRgbDriverSetEffectId = 2

        self._camera1dId = 4
        self._camera1dColorsId = 2

        self._toneId = 5
        self._tonePlayId = 0
        self._toneStopId = 1

        self._timerId = 6
        self._timerDelayId = 0
        self._timerTriggerId = 1

        self._bumpersId = 12
        self._bumpersStatesId = 0

        self._touchSensorsId = 17
        self._touchSensorsStatesId = 0

        self.robot = robot
        self.port = port
        self.port.rxListener.dataDidChange = self.didReceiveData  # Rx.

        self._devices = {}
        self.setDevicesAndCommands()

    def addAddressAndChecksum(self, messageData, deviceId, command):
        # The checksum includes all the other elements:
        data = bytearray([deviceId]) + bytearray([command]) + messageData
        return data + bytearray([PacketHelper.computeChecksum(data)])

    def setDevicesAndCommands(self):
        # ##Add checks.
        robot = self.robot

        # Robot iself:
        # The messageStop command is very different from the other commands:
        # it not only sends a stop message to all the actuators, but first also
        # empties the port's queue, so no other pending commands can be
        # executed until the startTx is called again:
        def messageStopDataDidChange(message):
            # ##TEST THIS:
            #self.port.bleDevice.bleClient.stopTx()

            # This also clears any txQueue automatically:
            #self.port.bleDevice.bleClient.startTx()

            self.port.write(self.addAddressAndChecksum(
                message,
                self._rootId,
                self._rootStopId)
            )

        robot.messageStop.dataDidChange = messageStopDataDidChange

        # ///////////////////// PositionDriver: /////////////////////
        positionDriver = robot.positionDriver
        differentialDrive = positionDriver.differentialDrive

        # Tx:
        # Movement commands:
        positionDriver.messageMoveStraight.dataDidChange = lambda messageData: self.port.write(
            self.addAddressAndChecksum(
                messageData,
                self._positionDriverId,
                self._positionDriverMoveStraightId
            )
        )

        positionDriver.messageRotate.dataDidChange = lambda messageData: self.port.write(
            self.addAddressAndChecksum(
                messageData,
                self._positionDriverId,
                self._positionDriverRotateId
            )
        )

        # DifferentialDrive:
        # Fast commands for setting both servos at once:
        differentialDrive.messageSpeedSet.dataDidChange = lambda messageData: self.port.write(
            self.addAddressAndChecksum(
                messageData,
                self._positionDriverId,
                self._positionDriverSetServosSpeed
            )
        )

        # ## Future: Implement the Accessing the servos individually.

        # Rx:
        positionDriverCommands = {}
        positionDriverCommands[self._positionDriverPositionId] = positionDriver.messagePosition
        positionDriverCommands[self._positionDriverMoveStraightId] = positionDriver.messageMoveStraightFinished
        positionDriverCommands[self._positionDriverRotateId] = positionDriver.messageRotateFinished
        positionDriverCommands[self._positionDriverCumulativeDistanceId] = positionDriver.messageCumulativeDistance
        self._devices[self._positionDriverId] = positionDriverCommands

        # ///////////////////// DrawingTool: /////////////////////
        drawingTool = robot.drawingTool
        drawingTool.messageStateSet.dataDidChange = lambda messageData: self.port.write(
            self.addAddressAndChecksum(
                messageData,
                self._drawingToolId,
                self._drawingToolPenSetStateId
            )
        )

        # ///////////////////// RGB LEDs: /////////////////////
        ledRgbDriver = robot.ledRgbDriver
        ledRgbDriver.messageEffect.dataDidChange = lambda messageData: self.port.write(
            self.addAddressAndChecksum(
                messageData,
                self._ledRgbDriverId,
                self._ledRgbDriverSetEffectId
            )
        )

        # Rx:
        # Note: The pen shares the commands with the eraser, as they use the
        # same device id (drawingToolId):
        drawingToolCommands = {}
        drawingToolCommands[self._drawingToolPenGetStateId] = drawingTool.messageStateGet
        drawingToolCommands[self._drawingToolPenSetStateId] = drawingTool.messageStateSetFinished
        self._devices[self._drawingToolId] = drawingToolCommands

        # ///////////////////// Tone: /////////////////////
        tone = robot.toneDriver
        tone.messagePlay.dataDidChange = lambda messageData: self.port.write(
            self.addAddressAndChecksum(
                messageData, self._toneId, self._tonePlayId
            )
        )
        tone.messageStop.dataDidChange = lambda messageData: self.port.write(
            self.addAddressAndChecksum(
                messageData, self._toneId, self._toneStopId
            )
        )

        # Rx:
        toneCommands = {}
        toneCommands[self._tonePlayId] = tone.messagePlayFinished
        toneCommands[self._toneStopId] = tone.messagePlayFinished
        self._devices[self._toneId] = toneCommands

        # ///////////////////// Bumpers: /////////////////////
        bumpers = robot.bumpers
        bumpersCommands = {}
        bumpersCommands[self._bumpersStatesId] = bumpers.messageStates
        self._devices[self._bumpersId] = bumpersCommands

        # ///////////////////// Touch sensors: /////////////////////
        touchSensors = robot.touchSensors
        touchSensorsCommands = {}
        touchSensorsCommands[self._touchSensorsStatesId] = touchSensors.messageStates
        self._devices[self._touchSensorsId] = touchSensorsCommands

        # ///////////////////// Camara 1d: /////////////////////
        camera1d = robot.camera1d
        camera1dCommands = {}
        camera1dCommands[self._camera1dColorsId] = camera1d.messageColors
        self._devices[self._camera1dId] = camera1dCommands

    # Rx stuff:
    def didReceiveData(self, value):
        # print "RootProtocolSerial.didReceiveData: "  # ##Debug.
        # print PacketHelper.printBytearray(value)  # ##Debug.
        if len(value) < 3:
            return

        # Rx decoder here:
        device = value[0]
        command = value[1]

        # print "device=", device  # ##Debug.
        # print "command=", command  # ##Debug.
        # print self._devices  # ##Debug.

        # Of course, this asignment also triggers the callback on the device's
        # message (due to the didSet of DeviceMessage.data). It's important to
        # note that the whole information packaged on the original message is
        # made available to the device:
        try:
            # The id is sent to the device, while the checksum isn't, since it
            # should be checked here (in the protocols where device and command
            # are packaged inside the data array, the checksum affects to them
            # to, so the checksum depends on the addressing, and the addressing
            # belongs only to the protocol, not to the device):
            if (len(value) - 1) > 2:  # Extra safety, not really necessary.
                self._devices[device][command].data = value[2:len(value) - 1]
            else:
                # Just in case, messages that do not have any data inside are
                # just zeros:
                self._devices[device][command].data = PacketHelper.getArrayFilledWithZeroes(16)
        except Exception as error:
            # This try-except block is here to avoid "key errors" to halt
            # the program (key errors are perfectly fine here, since
            # the server could have sent a message to a device or command
            # that doesn't exist):
            print error  # ##Debug: Log these errors in the future.
            pass
