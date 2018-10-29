
import gatt

manager = gatt.DeviceManager(adapter_name='hci0')

class AnyDevice(gatt.Device):
    def services_resolved(self):
        super().services_resolved()

        device_information_service = next(
            s for s in self.services
            if s.uuid == 'c8:8b:3f:aa:14:32'

        firmware_version_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == 'c8:8b:3f:aa:14:32'

        firmware_version_characteristic.read_value()

    def characteristic_value_updated(self, characteristic, value):
        print("Firmware version:", value.decode("utf-8"))


device = AnyDevice(mac_address='c8:8b:3f:aa:14:32', manager=manager)
device.connect()

manager.run()
print ('Finished')
