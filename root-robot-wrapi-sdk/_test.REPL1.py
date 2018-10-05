from wrapi.py.devices.Root.Root_v1_0 import *

r = Root_v1_0()

r.move(5)
r.rotate(90)
r.ifBumpersDetected(bumpersRightFront, lambda data: r.ledsEffect(ledsEffectSet, clGreen))
r.ifBumpersDetected(bumpersLeftFront, lambda data: r.ledsEffect(ledsEffectSet, clYellow).delay(2).ledsEffect(ledsEffectSet, clViolet))
r.start()

# Further commands will not reach the robot:
r.move(-5)
#print r.events.list()
