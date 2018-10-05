# Minimalist line follower:

from wrapi.py.devices.Root.Root_v1_0 import *

fwSpeed = 50
robot = Root_v1_0()

# Events:
'''
    1. Default behavior: Whithout priorities explicity defined: So the system
    adds the event AFTER the last one, and generates the index automatically.
    2. Priorities are the last parameter and they are optional
    3. When defined the system takes care of the indexes, much like in Level 1.
        - This is good for editor and for REPLs.
        - The exception is when a user types weird numbers for the priorities, like "399" but that
        should be a very particular case, and not very importat probably.

    >> for deleting events, use the trash() method.
'''

robot.ifStarts(lambda data: robot.speed(fwSpeed, fwSpeed))
robot.ifColorsDetected([clAny, clAny, clBlack], lambda data: robot.speed(fwSpeed, 0))
robot.ifColorsDetected([clBlack, clAny, clAny], lambda data: robot.speed(0, fwSpeed))
robot.ifColorsDetected([clAny, clBlack, clAny], lambda data: robot.speed(fwSpeed, fwSpeed))

'''
robot.addStartEvent(lambda: robot.speed(fwSpeed, fwSpeed))
robot.addColorsDetectedEvent([clAny, clAny, clBlack, clAny, clAny], lambda: robot.speed(fwSpeed, fwSpeed))
robot.addColorsDetectedEvent([clAny, clAny, clAny, clBlack, clBlack], lambda: robot.speed(fwSpeed, 0))
robot.addColorsDetectedEvent([clAny, clAny, clAny, clBlack, clBlack], lambda: robot.speed(fwSpeed, 0))
'''

robot.start()

# Insert/Append:
    # (Probably) Insert = Better for REPL / Append = Better for editor.
    #
# Repeated numbers:
    #
# Negative numbers:
    # Raise an exception?
# Non-consecutive numbers:
    # The sustem rearranges everything behind the scenes. The user can always list the events (probably even
    # list filtering by type or whatever).

##Think about providing low level access to the list for advanced users, specially when running on REPLs:
#robot.events.add(ifColorsDetected, [clAny, clAny, clBlack, clAny, clAny], lambda: robot.speed(fwSpeed, fwSpeed))

'''
robot.ifColorsDetected([clAny, clAny, clBlack, clAny, clAny], lambda: robot.speed(fwSpeed, fwSpeed), -1)
robot.ifColorsDetected([clBlack, clBlack, clAny, clAny, clAny], lambda: robot.speed(0, fwSpeed), 0)
robot.ifStarts(lambda: robot.speed(fwSpeed, fwSpeed), 1)
robot.ifColorsDetected([clAny, clAny, clAny, clBlack, clBlack], lambda: robot.speed(fwSpeed, 0), 399)
robot.ifColorsDetected([clAny, clAny, clAny, clBlack, clBlack], lambda: robot.speed(fwSpeed, 0), 400)
'''
