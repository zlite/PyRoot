from wrapi.py.devices.Root.Root_v1_0 import *

r = Root_v1_0()

r.ifBumpersDetected(bumpersRightFront, lambda data: r.ledsEffect(ledsEffectSet, clGreen))
r.ifBumpersDetected(bumpersLeftFront, lambda data: r.ledsEffect(ledsEffectSet, clYellow).delay(2).ledsEffect(ledsEffectSet, clViolet))
r.start()
r.move(5)

# Disconnection from server test: Disconnecting from the server and leaving the physical BLE device connected is not a good
# practice at all, since it's going to be difficult (or even impossible) to release the connected robot without reconnecting
# to to the server to send new commands or even shuting down it. Anyway this is possible and here it's how:
r.port.bleDevice.bleClient.disconnect()

# Further commands will not reach the robot:
r.move(-5)
#print r.events.list()
