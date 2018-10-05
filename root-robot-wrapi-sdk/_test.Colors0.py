from wrapi.py.computing.Colors import *


print websafeToRgb(0x333)
print websafeToRgb(0x036)
print websafeToRgb(0xf0f, False)
print websafeToRgb(0xff0, False)


print rgbToClosestWebsafe(25, 76, 127, False)
print rgbToClosestWebsafe(26, 77, 128, False)
print rgbToClosestWebsafe(0, 255, 178, False)
print rgbToClosestWebsafe(229, 230, 179, False)
