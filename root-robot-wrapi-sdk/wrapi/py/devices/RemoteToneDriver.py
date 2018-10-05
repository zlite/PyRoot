import RemoteDevice
import wrapi.py.computing.PacketHelper as PacketHelper
import wrapi.py.computing.DeviceMessage as DeviceMessage


class RemoteToneDriver(object):
    def __init__(self):
        self._isPlaying = False
        self._messagePlay = DeviceMessage.DeviceMessage()
        self._messageStop = DeviceMessage.DeviceMessage()

        self._messagePlayFinished = DeviceMessage.DeviceMessage()
        self._messagePlayFinished.dataDidChange = self._processMessagePlayFinished

        self._messageStopFinished = DeviceMessage.DeviceMessage()
        self._messageStopFinished.dataDidChange = self._processMessagePlayFinished  # Same as play finished.

    @property
    def isPlaying(self):
        return self._isPlaying

    @property
    def messagePlay(self):
        return self._messagePlay

    @property
    def messageStop(self):
        return self._messageStop

    @property
    def messagePlayFinished(self):
        return self._messagePlayFinished

    # [freq] = Hz; [duration] = s
    def play(self, freq, duration):
        self._isPlaying = True
        id = self._messagePlay.incrementId()
        result = bytearray([id]) + PacketHelper.uint32ToByteArray(freq) + \
            PacketHelper.uint16ToByteArray(int(duration*1000))
        self._messagePlay.data = PacketHelper.fillMessageDataWithZeroes(result, RemoteDevice.payloadSize)
        return id

    def stop(self):
        self._isPlaying = True
        id = self._messagePlay.incrementId()
        result = bytearray([id])
        self._messageStop.data = PacketHelper.fillMessageDataWithZeroes(result, RemoteDevice.payloadSize)
        return id

    def forceStopFlagsToFalse(self):
        self._isPlaying = False

    def _processMessagePlayFinished(self, data):
        self._isPlaying = False
        self.playDidFinish(data[DeviceMessage.idIndex])

    # User events (callback functions):
    def playDidFinish(self, playCommandId):
        return None
