# Color constants:
#
# Note: there are 16 colors that fit into 4 bits indexes used by the Camera1D,
# but those colors can be used on the API for the LEDs too. Over the 16th
# color (index = 15), more colors can be added but these can not be used by
# the color sensor (Camera1D) at all. In fact, the only useful colors from
# a color sensor point of view are clear marked on this file:

# ##Change these in the future on robot's firmware to match the
# resistor colors (like black=0, red=2, green=5...):.
# Colors usable by the color sensor (Camera 1D):

# clAny is mainly used with color sensors, when a color in an specific area of
# the sensor doesn't matter:
clAny = -1

clWhite = 0
clBlack = 1
clRed = 2
clGreen = 3
clBlue = 4

# More colors:
clYellow = 5
clOrange = 6
clViolet = 7
clMidGrey = 8

clCodeToRgb = {
    clWhite: {'r': 100.0, 'g': 100.0, 'b': 100.0},
    clBlack: {'r': 0.0, 'g': 0.0, 'b': 0.0},
    clRed: {'r': 100.0, 'g': 0.0, 'b': 0.0},
    clGreen: {'r': 0.0, 'g': 100.0, 'b': 0.0},
    clBlue: {'r': 0.0, 'g': 0.0, 'b': 100.0},
    clYellow: {'r': 100.0, 'g': 100.0, 'b': 0.0},
    clOrange: {'r': 100.0, 'g': 33.0, 'b': 0.0},
    clViolet: {'r': 56.0, 'g': 0.0, 'b': 100.0},
    clMidGrey: {'r': 50.0, 'g': 50.0, 'b': 50.0}
}


######
def _normalize(value):
    return value*100.0/255.0


def _rgbChannelToClosestWebsafe(value, normalized):
    result = int(51*round((5*value)/255.0))
    if normalized:
        return _normalize(result)
    return result


# This can be also precomputed on a table, but it's not very CPU intensive:
def rgbToClosestWebsafe(r, g, b, normalized=True):
    r = _rgbChannelToClosestWebsafe(r, normalized)
    g = _rgbChannelToClosestWebsafe(g, normalized)
    b = _rgbChannelToClosestWebsafe(b, normalized)
    return {'r': r, 'g': g, 'b': b}


def _websafeChannelToRgb(value, index, normalized):
    result = (value & (0xf << index*4)) >> index*4
    result = ((result << 4) + result)

    # Normalized means 0.0 to 100.0:
    if normalized:
        return _normalize(result)
    return result


# value is a number from 0x000 to 0xfff.
# returns an rgb (dictionary) with values from 0.0 to 100. if normalized=True,
# or with values from 0 to 255 if normalized=False.
def websafeToRgb(value, normalized=True):
    if value > 0xfff:
        value = 0xff
    elif value < 0:
        value = 0
    r = _websafeChannelToRgb(value, 2, normalized)
    g = _websafeChannelToRgb(value, 1, normalized)
    b = _websafeChannelToRgb(value, 0, normalized)
    return {'r': r, 'g': g, 'b': b}


_colorCodesTable = []


##Not normalized table:
def _initColorCodesTable():
    for r in range(0, 6):
        for b in range(0, 6):
            for g in range(0, 6):
                _colorCodesTable.append({'r': r*51, 'g': g*51, 'b': b*51})


def colorCodeToRgb(value, normalized=True):
    if value < 0:
        value = 0
    elif value >= len(_colorCodesTable):
        value = len(_colorCodesTable) - 1
    result = _colorCodesTable[value]
    if normalized:
        return _normalize(result)
    return result


def rgbToColorCode(r, g, b):

    return _colorCodesTable.index({'r': r, 'g': g, 'b': b})

_initColorCodesTable()
#print _colorCodesTable  # ##Debug.
