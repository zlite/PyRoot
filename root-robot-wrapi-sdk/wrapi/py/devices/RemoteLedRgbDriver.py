import RemoteDevice
from wrapi.py.computing.Colors import *
import wrapi.py.computing.Normalization as normalization
import wrapi.py.computing.PacketHelper as PacketHelper
from wrapi.py.computing.DeviceMessage import DeviceMessage

# Effects:
ledsEffectOff = 0
ledsEffectSet = 1
ledsEffectBlink = 2
ledsEffectCircle = 3


class RemoteLedRgbDriver(object):
    def __init__(self):
        self._messageEffect = DeviceMessage()

    @property
    def messageEffect(self):
        return self._messageEffect

    # floating "%" to byte conversion.
    def _percentageToByte(self, value):
        if value > int(normalization.maximumValue):
            value = int(normalization.maximumValue)
        elif value < 0:
            result = 0

        # For pythonic reason, this is not the same as using "2.55":
        return int(value*255/100)

    # effect should be one of the effects created as this class' members.
    # Method overloading:
    #
    #       r, g and b are floating point numbers from 0.0 to 100.0 or
    #
    #   this function can also be called as:
    #
    #       effect(effect, colorCode)
    #
    #   where colorCode = r, and it's a color code as defined in Colors.py.
    #
    def effect(self, effect, r, g=None, b=None):
        try:
            if g == None and b == None:
                colorCode = r
                intR = self._percentageToByte(clCodeToRgb[colorCode]['r'])
                intG = self._percentageToByte(clCodeToRgb[colorCode]['g'])
                intB = self._percentageToByte(clCodeToRgb[colorCode]['b'])
            else:
                intR = self._percentageToByte(r)
                intG = self._percentageToByte(g)
                intB = self._percentageToByte(b)
            #print intR, intG, intB  # ##Debug.

            id = self._messageEffect.incrementId()
            result = bytearray([id]) + bytearray([effect]) + bytearray([intR]) + bytearray([intG]) + bytearray([intB])
            self.messageEffect.data = PacketHelper.fillMessageDataWithZeroes(result, RemoteDevice.payloadSize)

            return id

        except:
            return 0  # ##Add error codes in the future.

    def stop(self):
        return 0  # ##

    '''##
    def stopDidSend(self):
        pass
    '''
