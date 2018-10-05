from wrapi.py.computing.Colors import *
from wrapi.py.computing.DeviceMessage import DeviceMessage
import wrapi.py.computing.PacketHelper as PacketHelper

class RemoteCamera1d(object):
    def __init__(self, sensorsCount=32):
        self.sensorsCount = sensorsCount
        self._colors = [0] * self.sensorsCount

        self._messageColors = DeviceMessage()
        self._messageColors.dataDidChange = self._processMessageColors

    @property
    def messageColors(self):
        return self._messageColors

    @property
    def colors(self):
        return self._colors

    def enableStatesDidChangeEvent(self):
        # ##Future: This is not implemented on the robot's firmware yet.
        pass

    def disableAllEvents(self):
        # ##Future: This is not implemented on the robot's firmware yet.
        pass

    def _processMessageColors(self, data):
        # ##The first byte is command id: Add processing for them in the future
        # on a common interface for all the devices.

        tempColors = []
        # ##Debug:
        # print "len(data) = ", len(data) - 1
        # PacketHelper.printBytearray(data)
        # print range(1, len(data) - 1)
        for i in range(1, len(data)):
            # print data[i]  # ##Debug.
            tempColors.append(PacketHelper.nibbleToByte(data[i], 1))
            tempColors.append(PacketHelper.nibbleToByte(data[i], 0))

        # This is done on a temporal variable in order to protect potential
        # readers of the public variable while writing it:
        self._colors = tempColors
        self.dataDidChange(self, self._colors)

    # User events (callback functions):
    def dataDidChange(self, source, data):
        return False

    # Auxiliary helper functions:

    # This function calculates the pixels per zone and returns an array of
    # detection zones ready to be used by high level methods that deal with
    # the Camera1d sensor. The distribution can be improved a lot, but by now
    # the following are the numbers of zones that work better:
    #
    # Work nicely:
    #    1, 2, 3, 4, 5, 6, 8, 10, 14, 15, 16, 28, 29, 30, 31, 32
    #
    # Acceptable:
    #    7, 26.
    # Horrible:
    #    9, 11, 12, 13, 17 (the worst), 18, 19, 20, 21, 22, 23, 24, 25, 27
    #
    # ##Future: Add a patch that takes into account the difference between
    # the "enhanced" zones and then redistributes more uniformly the extra
    # pixels.
    #
    def computeDetectionZones(self, colors):
        zones = []
        zonesCount = len(colors)

        if zonesCount <= 0:
            # ##i18n:
            raise ValueError('There must be at least one detection zone.')

        pixelsPerZone = self.sensorsCount // zonesCount
        remainingPixels = self.sensorsCount % zonesCount

        # ##Debug:
        # print "zonesCount =", zonesCount
        # print "pixelsPerZone =", pixelsPerZone
        # print "remainingPixels =", remainingPixels

        for i in range(0, zonesCount):
            newZone = [colors[i]] * pixelsPerZone
            zones += newZone

        # Try to distribute the remaining pixels (if any) in a symmetric way:
        if remainingPixels != 0:
            if zonesCount % 2 == 0:
                if remainingPixels % 2 == 0:
                    # Picks the color of the corresponding zone to generate the extra pixels:
                    zones = [colors[0]] * (remainingPixels // 2) + zones  # First zone.
                    zones += [colors[zonesCount - 1]] * (remainingPixels // 2)  # Last zone.
                else:
                    # Pixels can not be distributed symmetrically:
                    raise ValueError('Invalid detection zones quantity.')
            else:
                # extraPixels = [-8] * (remainingPixels)  # ##Debug.
                # Picks the color from the central zone to generate the extra pixels:
                extraPixels = [colors[zonesCount // 2]] * (remainingPixels)
                for i in extraPixels:
                    zones.insert(len(zones) // 2, i)  # Central zone.

        # print "len(zones) =", len(zones)  # ##Debug.
        return zones
