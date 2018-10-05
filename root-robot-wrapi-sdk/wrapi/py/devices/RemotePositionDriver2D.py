import RemoteDevice
import wrapi.py.computing.PacketHelper as PacketHelper
from wrapi.py.computing.DeviceMessage import DeviceMessage


class RemotePositionDriver2D(object):
    def __init__(self, differentialDrive):
        self.differentialDrive = differentialDrive

        self._isRotating = False
        self._isMovingStraight = False

        # Commands:
        self._messageMoveStraight = DeviceMessage()
        self._messageRotate = DeviceMessage()

        # Answers:
        self._messagePosition = DeviceMessage()
        self._messageCumulativeDistance = DeviceMessage()
        self._messageRotateFinished = DeviceMessage()
        self._messageMoveStraightFinished = DeviceMessage()

        # ##self._messagePosition.dataDidChange = self.positionMessageDidChange
        self._messageRotateFinished.dataDidChange = self.rotationMovementMessageDidChange
        self._messageMoveStraightFinished.dataDidChange = self.straightMovementMessageDidChange

    def rotatingDidFinish(self):
        # print "rotatingDidFinish"  # ##Debug.
        return None

    def movingStraightDidFinish(self): return None

    def positionDidChange(self, position, realHeading): return None

    @property
    def isRotating(self):
        return self._isRotating

    @property
    def isMovingStraight(self):
        return self._isMovingStraight

    @property
    def messageMoveStraight(self):
        return self._messageMoveStraight

    @property
    def messageRotate(self):
        return self._messageRotate

    @property
    def messagePosition(self):
        return self._messagePosition

    @property
    def messageCumulativeDistance(self):
        return self._messageCumulativeDistance

    @property
    def messageRotateFinished(self):
        return self._messageRotateFinished

    @property
    def messageMoveStraightFinished(self):
        return self._messageMoveStraightFinished

    ''' The system supports both polling (with the isMoving flag) and callbacks
        with the movementDidFinish() function: '''
    def rotationMovementMessageDidChange(self, message):
        self._isRotating = False
        self.rotatingDidFinish()

    def straightMovementMessageDidChange(self, message):
        self._isMovingStraight = False
        self.movingStraightDidFinish()

    # self.positionMessageDidChange(self, message):
        # ## Implement.

    '''//////////////////////////////////////////////////////////////////////
    // User commands:
    //////////////////////////////////////////////////////////////////////'''
    # ##Speed is not used by now.
    def moveStraight(self, distance, speed=0):
        self._isMovingStraight = True
        # Units: mm (by now...):

        # By now, the unit is centimeters:
        unit = 0  # ##Not used by now.
        distance = distance*10

        id = self.messageMoveStraight.incrementId()
        result = bytearray([id]) + PacketHelper.int32ToByteArray(distance) + \
            PacketHelper.int32ToByteArray(speed) + bytearray([unit])
        self.messageMoveStraight.data = PacketHelper.fillMessageDataWithZeroes(result, RemoteDevice.payloadSize)

        return id

    # Returns the rotated angle.
    # ##Speed is not used by now.
    def rotate(self, angle, speed=0):
        self._isRotating = True
        rotationType = 0  # ##Not used by now.

        # By now, the unit is degrees:
        unit = 0  # ##Not used by now.
        angle = angle*10

        id = self.messageRotate.incrementId()
        result = bytearray([id]) + PacketHelper.int32ToByteArray(angle) + \
            bytearray([rotationType]) + PacketHelper.int32ToByteArray(speed) + bytearray([unit])
        self.messageRotate.data = PacketHelper.fillMessageDataWithZeroes(
            result,
            RemoteDevice.payloadSize
        )

        return id

    # Absolute rotation:
    # ##Speed is not used by now.
    def rotateTo(self, angle, v):
        # ##Implement.
        self._isRotating = False  # ##Change this when implemented!
        pass

    # This is different than move(0), since it focuses only on stopping
    # everything regardless update cycles from timers, etc.:
    def stop(self):
        self.differentialDrive.stop()
        return 0

    def forceStopFlagsToFalse(self):
        ''' Note.

            In theory, the robot must trigger the events moveStraightDidFinish
            or moveStraightDidFinish when the stop() command is triggered, so
            this is not done on the stop() function. Thus, in some applications
            this allows the user to stop everything from the application using
            this class perspective, since if the connection is lost, the flags
            are not going to change (##timeouts and a connection lost detection
            system could be added in the future, but not now).
        '''
        self._isMovingStraight = False  # ##
        self._isRotating = False  # ##

    # ##Not implemented yet but defined on the API design:
    # This function doesn't return anything: it just tells the robot to send
    # back a position message:
    def position(self):
        # ##Implement
        pass

    def resetCumulativeDistance(self):
        # ##Implement
        return 0

    # This function doesn't return anything: it just tells the robot to send
    # back a cumulativeDistance message:
    def getCumulativeDistance(self):
        # ##Implement
        return 0
