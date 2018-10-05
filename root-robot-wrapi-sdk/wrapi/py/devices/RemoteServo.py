import RemoteDevice
import wrapi.py.computing.Normalization as normalization
import wrapi.py.computing.PacketHelper as PacketHelper
from wrapi.py.computing.DeviceMessage import DeviceMessage


class RemoteServo(object):
    def __init__(
        self,
        motor,
        providesAcceleration,
        providesSpeed,
        providesPosition
    ):
        # ##Add safety checks here.
        self.motor = motor

        self._providesAcceleration = providesAcceleration
        self._providesSpeed = providesSpeed
        self._providesPosition = providesPosition

        self._messageAccelerationSet = DeviceMessage()
        self._messageSpeedSet = DeviceMessage()
        self._messagePositionSet = DeviceMessage()

    @property
    def providesAcceleration(self):
        return self._providesAcceleration

    @property
    def providesSpeed(self):
        return self._providesSpeed

    @property
    def providesPosition(self):
        return self._providesPosition

    @property
    def messageAccelerationSet(self):
        return self._messageAccelerationSet

    @property
    def messageSpeedSet(self):
        return self._messageSpeedSet

    @property
    def messagePositionSet(self):
        return self._messagePositionSet

    # ##Future: add uniform unit support (see other classes wiht unit support
    # like PwmOut).
    # ##Future: Also add a callback system that reads the property from the
    # remote device (that's why these properties can only be set
    # and not read and thus they are just functions).

    # If value is not an integer, it will be rounded to the nearest integer.
    # All the values on the servo protocol range from -65535 5o +65535 and
    # are normalized on the user's API from -100.0 to +100.0.
    def _encodeMessage(self, value):
        if value > normalization.maximumValue:
            value = normalization.maximumValue
        elif value < normalization.minimumValue:
            value = normalization.minimumValue

        value = value*65535/normalization.maximumValue
        #print "value=", value  # ##Debug.

        return PacketHelper.int32ToByteArray(value)

    def _encodeMessageWithValue(self, message, value, unit):
        id = message.incrementId()
        result = bytearray([id]) + self._encodeMessage(value) + bytearray([unit])
        message.data = PacketHelper.fillMessageDataWithZeroes(
            result,
            RemoteDevice.payloadSize
        )

        return id

    ''' These encode aliases are necessary: they provide the encoding ability
        to external objects without knowning much about the
        encoding itself: '''
    # ##Unit is not used by now.
    def encodeAccelerationMessage(self, value, unit=0):
        return self._encodeMessage(value)

    # ##Unit is not used by now.
    def encodeSpeedMessage(self, value, unit=0):
        return self._encodeMessage(value)

    # ##Unit is not used by now.
    def encodePositionMessage(self, value, unit=0):
        return self._encodeMessage(value)

    def acceleration(self, value):
        return self._encodeMessageWithValue(self.messageAccelerationSet, value)

    def speed(self, value):
        return self._encodeMessageWithValue(self.messageSpeedSet, value)

    def position(self, value):
        return self._encodeMessageWithValue(self.messagePositionSet, value)

    # ##Test this:
    def stop(self):
        speed(0)  # This should overwrite any other ongoing speed command.
        return 0  # ##
