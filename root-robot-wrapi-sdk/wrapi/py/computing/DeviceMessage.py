idIndex = 0

class DeviceMessage(object):
    def __init__(self):
        self._id = 0

        self._data = bytearray()

    def id(self): return self._id

    def dataDidChange(self, data): return None

    def incrementId(self):
        if self._id < 255:
            self._id += 1
        else:
            self._id = 0
        return self._id

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = bytearray(value)  # Makes a copy.
        self.dataDidChange(bytearray(self._data))  # Callback WITH A COPY.


# Examples:

def printBytearray(value):
    print ''.join(format(x, ' 02d') for x in value)

msg = DeviceMessage()


def dataDidChange(data):
    print "msg.dataDidChange called: "
    printBytearray(data)
msg.dataDidChange = dataDidChange

# Examples:
'''
print msg.id()
msg.incrementId()

arr = bytearray(10)
arr[0] = 0xaa
msg.data = arr
arr[1] = 0xbb

print
printBytearray(arr)
printBytearray(msg.data)
print msg._id
'''
