

def boolToByte(value):
    return 1 if value else 0


def nibbleToByte(value, nibbleIndex):
    if nibbleIndex == 0:
        return value & 0xf
    # nibbleIndex === 1, but any value != 0 will work here:
    return (value >> 4) & 0xf


def int16ToByteArray(value):
    """Notes.

    --  Does not check if the integer is bigger than a 16 bits integer
        (given the fact that a JS number is a 64 bits float).
    --  result[0] is the MSB.
    """
    result = bytearray()
    result.append((value >> 8) & 0xff)
    result.append(value & 0xff)
    return result


def uint16ToByteArray(value):
    """Notes.

    --  All the notes for int16ToByteArray apply to this function.
    --  If the number is signed, this just discards ths sign by calling
        abs.
    """
    return int16ToByteArray(abs(value))


def int32ToByteArray(value):
    """Notes.

    --  Works for 32 bits but obviously loses decimals on floats.
    --  Does not check if the integer is bigger than a 32 bits integer
        (given the fact that a JS number is a 64 bits float).
    --  In the case df dealing with floats, it rounds. The round function
        works dlightly different than in the JavaScript version of the API
        when negative floating point numbers like -4.5 are passed as arguments.
    --  result[0] is the MSB.
    """
    intValue = int(round(value))
    result = bytearray()
    result.append((intValue >> 24) & 0xff)
    result.append((intValue >> 16) & 0xff)
    result.append((intValue >> 8) & 0xff)
    result.append(intValue & 0xff)

    return result


def uint32ToByteArray(value):
    """Notes.

    --  All the notes for int32ToByteArray apply to this function.
    --  If the number is signed, this just discards ths sign by calling
        abs.
    """
    return int32ToByteArray(abs(value))


def byteArrayToInt32(value):
    """Notes.

    --  Works for 32 bits but obviously loses decimals on floats.
    --  Does not check if the integer is bigger than a 32 bits integer
        (given the fact that a JS number is a 64 bits float).
    --  In the case of dealing with floats, it rounds.
    --  result[0] is the MSB.
    """
    result = (value[0] & 0xff) << 24
    result |= (value[1] & 0xff) << 16
    result |= (value[2] & 0xff) << 8
    result |= value[3] & 0xff

    return result


# ## Test:
def byteArrayToInt16(value):
    value32 = [0, 0, value[1], value[0]]
    return byteArrayToInt32(value32)


def getArrayFilledWithZeroes(size):
    return bytearray(size)


def fillMessageDataWithZeroes(message, payloadSize):
    '''Notes: Adds 1 to fit the id byte, which is not part of the payload.'''
    result = message
    result = result + getArrayFilledWithZeroes(payloadSize - len(message) + 1)
    return result


def modularSum(value):
    # ## Not implemented yet.
    return 0


def computeChecksum(data, checksumFunction=modularSum):
    """Notes.

    This is just an alias function, so in the future the checksum algorithm
    can be easily changed just by passing another
    block as an argument (or even editing the default value here, WHICH IS
    NOT RECOMENDED):
    """
    return checksumFunction(data)


# Note: If the string is formed by an odd number of characters, the last
# character is ignored.
# Note: The try-except block protects agains crashes produced by non-hex
# characters (which may be caused by communication errors, for example).
def hexStringToBinaryBytearray(value):
    arrayData = bytearray(value)
    result = bytearray()

    try:
        i = 0
        while i < len(arrayData) - 1:
            strByte = "".join([chr(arrayData[i]), chr(arrayData[i + 1])])
            byte = int(strByte, 16)
            result.append(byte)
            i += 2
    except:
        pass

    return bytearray(result)

def printBytearray(value):
    print ''.join(format(x, ' 02d') for x in value)


# Examples:
'''
printBytearray(hexStringToBinaryBytearray("0aff00"))
printBytearray(hexStringToBinaryBytearray("0aff001"))
printBytearray(hexStringToBinaryBytearray("0afz00")) # ##Non-fatal exception.

print
print boolToByte(True)
print boolToByte(False)
# print boolToByte(0)
print
print nibbleToByte(0xab, 0)
print nibbleToByte(0xab, 1)
print nibbleToByte(0xf2, 0)
print nibbleToByte(0xf2, 1)
print
printBytearray(int32ToByteArray(100))
printBytearray(int32ToByteArray(2100))
print int32ToByteArray(2100)[0]
print int32ToByteArray(2100)[3]
printBytearray(int32ToByteArray(-2100))

print
printBytearray(int32ToByteArray(-999.49))

# Slightly different in JS version of the API:
printBytearray(int32ToByteArray(-999.5))
printBytearray(int32ToByteArray(-999.5001))

print
print byteArrayToInt32(int32ToByteArray(999.5))
# print byteArrayToInt32(int16ToByteArray(999.5))  # Must fail.
print
printBytearray(int16ToByteArray(30123))
printBytearray(int16ToByteArray(-30123))
print
printBytearray(fillMessageDataWithZeroes(bytearray([1, 2, 3]), 10))
'''
