
import gatt

manager = gatt.DeviceManager(adapter_name='hci0')

<<<<<<< HEAD
=======
# device 1, command 4, left motor speed 100, right motor speed 100
forward_cmd="0x01 0x04 0x00 0x00 0x00 0x00 0x64 0x00 0x00 0x00 0x64"
" 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0xD1"

# device 1, command 4, left motor speed -100, right motor speed -100
back_cmd="0x01 0x04 0x00 0xFF 0xFF 0xFF 0x9C 0xFF 0xFF 0xFF 0x9C"
" 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x71"

# device 1, command 4, left motor speed 0, right motor speed 100
left_cmd="0x01 0x04 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x64"
" 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x8A"

# device 1, command 4, left motor speed 100, right motor speed 0
right_cmd="0x01 0x04 0x00 0x00 0x00 0x00 0x64 0x00 0x00 0x00 0x00"
" 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x25"

# device 1, command 4, left motor speed 0, right motor speed 0
stop_cmd="0x01 0x04 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00"
" 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x7E"

>>>>>>> a35b98cd64e3a408cc27eb0aa4c827c1be150174
class AnyDevice(gatt.Device):
    def services_resolved(self):
        super().services_resolved()

        device_information_service = next(
            s for s in self.services
<<<<<<< HEAD
            if s.uuid == 'c8:8b:3f:aa:14:32'

        firmware_version_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == 'c8:8b:3f:aa:14:32'
=======
            if s.uuid == '0000180a-0000-1000-8000-00805f9b34fb')

        firmware_version_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == '00002a26-0000-1000-8000-00805f9b34fb')
>>>>>>> a35b98cd64e3a408cc27eb0aa4c827c1be150174

        firmware_version_characteristic.read_value()

    def characteristic_value_updated(self, characteristic, value):
        print("Firmware version:", value.decode("utf-8"))


device = AnyDevice(mac_address='c8:8b:3f:aa:14:32', manager=manager)
device.connect()
<<<<<<< HEAD

manager.run()
print ('Finished')
=======
print ('Hello world')
manager.run()
print ('Write value')
write_value(forward_cmd)
print ('wrote value)')
>>>>>>> a35b98cd64e3a408cc27eb0aa4c827c1be150174
