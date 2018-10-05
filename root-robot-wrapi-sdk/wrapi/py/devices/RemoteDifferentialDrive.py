import RemoteDevice
import wrapi.py.computing.PacketHelper as PacketHelper
from wrapi.py.computing.DeviceMessage import DeviceMessage


class RemoteDifferentialDrive(object):
    def __init__(self, leftServo, rightServo):
        self.leftServo = leftServo
        self.rightServo = rightServo

        self._messagePowerSet = DeviceMessage()
        self._messageSpeedSet = DeviceMessage()
        self._messagePositionSet = DeviceMessage()

    @property
    def messagePowerSet(self):
        return self._messagePowerSet

    @property
    def messageSpeedSet(self):
        return self._messageSpeedSet

    @property
    def messagePositionSet(self):
        return self._messagePositionSet

    ''' Note: Acceleration is not needed here, since it's a configuration
        paramater, and thus doesn't need a fast setter for both servos at the
        same time. self functionality is exposed by accessing the servos
        themselves, if they expose it, since not all servo models allow
        acceleration to be configured. '''

    def _encodeMessage(
        self,
        message,
        encodingFunction,
        leftValue,
        rightValue,
        unit
    ):
        encodedLeftValue = self.leftServo.encodeSpeedMessage(leftValue)
        encodedRightValue = self.rightServo.encodeSpeedMessage(rightValue)

        id = message.incrementId()
        result = bytearray([id]) + encodedLeftValue + encodedRightValue + bytearray([unit])
        message.data = PacketHelper.fillMessageDataWithZeroes(
            result,
            RemoteDevice.payloadSize
        )

        return id

    # ##Not implemented by now:
    def power(self, leftValue, rightValue):
        pass

    # ##Unit is not used by now: Zero means that the value is %,
    # with 100% == 65535:
    def speed(self, leftValue, rightValue, unit=0):
        return self._encodeMessage(
            self.messageSpeedSet,
            self.leftServo.encodeSpeedMessage,
            leftValue,
            rightValue,
            unit
        )

    def position(self, leftValue, rightValue):
        return self._encodeMessage(
            self.messagePositionSet,
            self.leftServo.encodePositionMessage,
            leftValue,
            rightValue
        )

    def stop(self):
        self.speed(0, 0)
        return 0  # ##
