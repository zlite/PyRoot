#!/usr/bin/env python3

import gatt
import threading
import time
import signal
import curses
stdscr = curses.initscr()
state = ""

# BLE UUID's
root_identifier_uuid = '48c5d828-ac2a-442d-97a3-0c9822b04979'
uart_service_uuid = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
tx_characteristic_uuid = '6e400002-b5a3-f393-e0a9-e50e24dcca9e' # Write
rx_characteristic_uuid = '6e400003-b5a3-f393-e0a9-e50e24dcca9e' # Notify

class BluetoothDeviceManager(gatt.DeviceManager):
    robot = None # root robot device

    def device_discovered(self, device):
        print("[%s] Discovered: %s" % (device.mac_address, device.alias()))
        self.stop_discovery() # Stop searching
        self.robot = RootDevice(mac_address=device.mac_address, manager=self)
        self.robot.connect()

class RootDevice(gatt.Device):
    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))

    def services_resolved(self):
        super().services_resolved()
        print("[%s] Resolved services" % (self.mac_address))

        self.uart_service = next(
            s for s in self.services
            if s.uuid == uart_service_uuid)

        self.tx_characteristic = next(
            c for c in self.uart_service.characteristics
            if c.uuid == tx_characteristic_uuid)

        self.rx_characteristic = next(
            c for c in self.uart_service.characteristics
            if c.uuid == rx_characteristic_uuid)

        self.rx_characteristic.enable_notifications() # listen to RX messages

    def characteristic_value_updated(self, characteristic, value):
        message = []
        for byte in value:
            message.append(byte)
        print ("Messages from Root:")
        print(message)

    def drive_forward(self):
        self.tx_characteristic.write_value([0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xD1])

    def drive_left(self):
        self.tx_characteristic.write_value([0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8A])

    def drive_right(self):
        self.tx_characteristic.write_value([0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x25])

    def stop(self):
        self.tx_characteristic.write_value([0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7E])

    def drive_backwards(self):
        self.tx_characteristic.write_value([0x01, 0x04, 0x00, 0xFF, 0xFF, 0xFF, 0x9C, 0xFF, 0xFF, 0xFF, 0x9C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x71])

    def pen_up(self):
        self.tx_characteristic.write_value([0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def pen_down(self):
        self.tx_characteristic.write_value([0x02, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

def loop(stdscr, *args, **kwds) :
    global state
    state = ""
    stdscr.nodelay(1)
    while True:
        ch = stdscr.getch()
        if ch == -1 :
            pass
        else :
            if ch == curses.KEY_UP : state = "FORWARD"
            elif ch == curses.KEY_DOWN : state = "BACKWARD"
            elif ch == curses.KEY_RIGHT : state = "RIGHT"
            elif ch == curses.KEY_LEFT : state = "LEFT"
            elif ch == ord('s') : state = "STOP"
            elif ch == ord('u'): state = "UP"
            elif ch == ord('d'): state = "DOWN"
            else : pass
        time.sleep(0.01)

def drive_root():
    global state
    while True:
        if state == "FORWARD":
            manager.robot.drive_forward()
        if state == "BACKWARD":
            manager.robot.drive_backwards()
        if state == "RIGHT":
            manager.robot.drive_right()
        if state == "LEFT":
            manager.robot.drive_left()
        if state == "STOP":
            manager.robot.stop()
        if state == "UP":
            manager.robot.pen_up()
        if state == "DOWN":
            manager.robot.pen_down()
        time.sleep(0.01)

# start here if run as program / not imported as module
if __name__ == "__main__":
    manager = BluetoothDeviceManager(adapter_name = 'hci0')
    manager.start_discovery(service_uuids=[root_identifier_uuid])
    thread = threading.Thread(target = manager.run)
    thread.start()
    while manager.robot is None:
            print('Waiting...')
            time.sleep(0.1)
            pass # wait for a root robot to be discovered
    print ("Found one!")
    t1=threading.Thread(target=drive_root)
    t1.setDaemon(True)
    t1.start()
    curses.wrapper(loop)  # start keyboard input thread
        #    stopper = threading.Event()