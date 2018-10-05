## Update this file to the latest WRAPI version.

from wrapi.py.devices.RemoteDCMotor import RemoteDCMotor

from wrapi.py.devices.RemoteServo import RemoteServo
from wrapi.py.devices.RemoteDifferentialDrive import RemoteDifferentialDrive
from wrapi.py.devices.RemotePositionDriver2D import RemotePositionDriver2D
from wrapi.py.devices.SocketPort import SocketPort
from wrapi.py.devices.BleSerialPort import BleSerialPort
from wrapi.py.devices.Root.RemoteRoot_v1_0 import RemoteRoot_v1_0
from wrapi.py.devices.Root.RootProtocolSerial_v1_0 \
    import RootProtocolSerial_v1_0
import wrapi.py.computing.PacketHelper as PacketHelper


print
print "RemoteDCMotor:"

motor = RemoteDCMotor()
print motor.powerMaximum
print motor.powerMinimum


print
print "RemoteServo:"


def messageDidChange(data):
    PacketHelper.printBytearray(data)

leftServo = RemoteServo(RemoteDCMotor(), False, True, False)
rightServo = RemoteServo(RemoteDCMotor(), False, True, False)

leftServo.messageAccelerationSet.dataDidChange = messageDidChange
leftServo.messageSpeedSet.dataDidChange = messageDidChange
leftServo.messagePositionSet.dataDidChange = messageDidChange
leftServo.acceleration(50)
leftServo.acceleration(50)
leftServo.speed(80)
leftServo.speed(80)
leftServo.speed(-80)
leftServo.speed(-80)
leftServo.speed(1000)
leftServo.speed(1000)
leftServo.position(-100)
leftServo.position(-100)

# Works:
# Cyclic message id test.
# for i in range(0, 299):
#     leftServo.position(i)


print
print "RemoteDifferentialDrive:"
drive = RemoteDifferentialDrive(leftServo, rightServo)

drive.messagePowerSet.dataDidChange = messageDidChange
drive.messageSpeedSet.dataDidChange = messageDidChange
drive.messagePositionSet.dataDidChange = messageDidChange

drive.speed(80, 80)
drive.speed(80, 80)
drive.speed(1000, -1000)
drive.speed(-80, -1)
drive.position(-80, -1)
drive.position(-80, -1)


print
print "RemotePositionDriver2D:"
positionDriver = RemotePositionDriver2D(drive)

positionDriver.messageMoveStraight.dataDidChange = messageDidChange
positionDriver.messageRotate.dataDidChange = messageDidChange

positionDriver.moveStraight(100)
positionDriver.moveStraight(-100)
positionDriver.moveStraight(-100)
#PacketHelper.printBytearray(positionDriver.messageMoveStraight.data)
positionDriver.rotate(90)
positionDriver.rotate(80)
positionDriver.rotate(80)
positionDriver.rotate(90)
#PacketHelper.printBytearray(positionDriver.messageRotate.data)


print
print "RemoteRoot:"
robot0 = RemoteRoot_v1_0()

robot0.messageStop.dataDidChange = messageDidChange
robot0.stop()
robot0.stop()


a = [5, 1, 2, 3, 4, 5]
b = [5, 1, 8, 3, 6, 5]
# print [x for x in a if x in b]  # nice!
c = []
def compareLists(a, b):
    for element in a:
        if element in b:
            c.append(element)
        else:
            c.append(0)
    return c
print compareLists(a, b)

'''
print
print "RootProtocolSerial:"
serialPort = SocketSerialPort(IP, portNumber)
UUID?
rootProtocolSerial = RootProtocolSerial(serialPort)
rootProtocolSerial.addRobot(robot0)
serialPort.didConnect = serialPortDidConnect
'''

'''
let RemoteRoot_v1_0 = require("./RemoteRoot.js")
let bleSerialPort = require("../BLESerialPort.js")
let robot = new RemoteRoot_v1_0()
let rootProtocolSerial = new RootProtocolSerial(robot, bleSerialPort)
robot.positionDriver.rotate(90)
robot.positionDriver.rotate(-90)
robot.positionDriver.moveStraight(1000)
robot.positionDriver.moveStraight(0)
robot.positionDriver.moveStraight(-1000)
robot.positionDriver.differentialDrive.speed(50, 50)
robot.positionDriver.differentialDrive.speed(0, -50)

//##Think about multidevice and if it's possible to do it without multithreading in Node.js:
//##Work on the syntax to see what to do:
robot.commands = {
    move: 100
    rotate: 90
    move: -100
}

//Same function with blocking and non-blocking syntax:
robot.move(100)
robot.move(100, function():

})
robot.rotate(90)

//##console.log(devices)
'''
