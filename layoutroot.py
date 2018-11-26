#!/usr/bin/env python3

'''
Layout bot

By Chris Anderson, 3DR, 2018
'''

import time
from marvelmind import MarvelmindHedge
import sys
import os
import struct
import math
import logging
import csv
import gatt
import threading
from Adafruit_BNO055 import BNO055

# BLE UUID's
root_identifier_uuid = '48c5d828-ac2a-442d-97a3-0c9822b04979'
uart_service_uuid = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
tx_characteristic_uuid = '6e400002-b5a3-f393-e0a9-e50e24dcca9e' # Write
rx_characteristic_uuid = '6e400003-b5a3-f393-e0a9-e50e24dcca9e' # Notify

# Enable the IMU with serial UART and RST connected to GPIO 18:
bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
status, self_test, error = bno.get_system_status()
print('IMU system status: {0}'.format(status))
print('IMU self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.

if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

OffsetX= (-412+450)/2 # compass calibrated min and max values for X
OffsetY= (-1000+-50)/2 # compass calibrated min and max values for X

kp = 0.6   # P term of the PID
ki = 0.0     # I term of the PID
kd = 0.4    # D term of the PID
gain = 1
cruise_speed = 50  # up to 80
temp_speed = cruise_speed
steering_gain = 1.0 #

OffsetX= (-412+450)/2 # compass calibrated min and max values for X
OffsetY= (-1000+-50)/2 # compass calibrated min and max values for X

waypoint_num = 0
waypoint=[[0 for j in range(2)] for i in range(1000)]  # dimension an array up to 1,000 waypoints

with open('waypoints_home.csv') as csv_file:  # change to whatever waypoint file you want
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        waypoint[line_count][0] = float(row[0])  # x data
        waypoint[line_count][1] = float(row[1])  # y data
        line_count += 1
    print('Loaded', line_count, 'waypoints')
    waypoint_total = line_count


#initialize some global variables
hedgehog_id = 1
max_heading = 3600 # full range of heading when paired
hedgehog_x = 0
hedgehog_y = 0
imu_correction = 0
old_x = 0
old_y = 0
temp_angle = 0
counter = 0
offset = 0
heading = 0
heading2 = 0
range = 0
direction = 0
filecounter = 0
now = 0
old_time = int(round(time.time() * 1000))
old_error = 0
i_term = 0
radians_degrees = 57.3 # constant to convert from radians to degrees

# initiate local positioning
hedge = MarvelmindHedge(tty = "/dev/ttyACM0", maxvaluescount=1,adr=hedgehog_id, debug=False) # create MarvelmindHedge thread
hedge.start() # start thread
time.sleep(1) # pause to let it settle

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
        type = ""
        for byte in value:
            message.append(byte)
#        print ("Messages from Root:")
        if message[0] == 4: type = "Color Sensor"
        if message[0] == 12: type = "Bumper"
        if message[0] == 13: type = "Light Sensor"
        if message[0] == 17: type = "Touch Sensor"
        if message[0] == 20: type = "Cliff Sensor"

#        print(type, message)

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

    def turn_rate(self, rate):
        left = 0
        right = 0
        if rate >= 0:
            left = rate
        if rate < 0:
            right = -1*rate
        leftbytes = left.to_bytes(4,byteorder='big',signed=True)  # need to convert to byte string
        rightbytes = right.to_bytes(4,byteorder='big',signed=True)
        # note that we're not dynamically calculating the CRC at the end, so just leaving it 0 (unchecked)
        self.tx_characteristic.write_value([0x01, 0x04, 0x00, leftbytes[0], leftbytes[1], leftbytes[2], leftbytes[3], rightbytes[0], rightbytes[1], rightbytes[2], rightbytes[3], 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0])

    def rotate(self, direction):
        print ("Turning", direction)
        left = direction * 20  # Send the motors in opposite directions
        right = direction * -20
        leftbytes = left.to_bytes(4,byteorder='big',signed=True)  # need to convert to byte string
        rightbytes = right.to_bytes(4,byteorder='big',signed=True)
        # note that we're not dynamically calculating the CRC at the end, so just leaving it 0 (unchecked)
        self.tx_characteristic.write_value([0x01, 0x04, 0x00, leftbytes[0], leftbytes[1], leftbytes[2], leftbytes[3], rightbytes[0], rightbytes[1], rightbytes[2], rightbytes[3], 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0])


    def turn(self, direction):
        print ("Turning", direction)
        left = cruise_speed - direction * 20
        right = cruise_speed + direction * 20
        leftbytes = left.to_bytes(4,byteorder='big',signed=True)  # need to convert to byte string
        rightbytes = right.to_bytes(4,byteorder='big',signed=True)
        # note that we're not dynamically calculating the CRC at the end, so just leaving it 0 (unchecked)
        self.tx_characteristic.write_value([0x01, 0x04, 0x00, leftbytes[0], leftbytes[1], leftbytes[2], leftbytes[3], rightbytes[0], rightbytes[1], rightbytes[2], rightbytes[3], 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0])

    def steer(self, left, right):
        leftbytes = left.to_bytes(4,byteorder='big',signed=True)  # need to convert to byte string
        rightbytes = right.to_bytes(4,byteorder='big',signed=True)
        # note that we're not dynamically calculating the CRC at the end, so just leaving it 0 (unchecked)
        self.tx_characteristic.write_value([0x01, 0x04, 0x00, leftbytes[0], leftbytes[1], leftbytes[2], leftbytes[3], rightbytes[0], rightbytes[1], rightbytes[2], rightbytes[3], 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0])


def constrain(value, min, max):
    if value < min :
        return min
    if value > max :
        return max
    else:
        return value

def update_pid(measured_angle, set_angle):
    global old_error, i_term
    now = int(round(time.time() * 1000))
    dt = now - old_time
    error = set_angle - measured_angle
    de = error - old_error
    p_term = kp * error
    i_term += ki * error
    i_term = constrain(i_term, 0, 100)
    d_term = (de / dt) * kd
    old_error = error
    output = gain * (p_term + i_term + d_term)
    return output

def get_imu():
    heading, roll, pitch = bno.read_euler()
    return heading

def get_position():
    global position
    global desired_angle
    global direction
    global range
    global heading
    global heading2
    global old_x, old_y
    position = hedge.position()
    hedgehog_x = position[1]
    hedgehog_y = position[2]
    delta_x = waypoint[waypoint_num][0]-hedgehog_x  # calculate angle to target
    delta_y = waypoint[waypoint_num][1]-hedgehog_y
    range = math.sqrt(delta_y**2 + delta_x**2)
    heading = round(get_imu(),3)
    desired_angle = 180-round(math.degrees(math.atan2(delta_y,delta_x)))  # all converted into degrees
    delta_x = hedgehog_x - old_x
    delta_y = hedgehog_y - old_y
    heading2 = 180-round(math.degrees(math.atan2(delta_y,delta_x)))  #  now get angle from position since last measurement
    old_x = hedgehog_x
    old_y = hedgehog_y
    direction = dir(heading, desired_angle)

def get_range():
    global position
    global range
    x_offset = 0
    y_offset = 0
    position = hedge.position()
    hedgehog_x = position[1]
    if hedgehog_x < 0: x_offset = hedgehog_x  # compensate for fact that pythogorean theorum doesn't deal with negative coordinates
    hedgehog_y = position[2]
    if hedgehog_y < 0: y_offset = hedgehog_x
    print ("Waypoint #:", waypoint_num, " Current x:", hedgehog_x, " Current y:", hedgehog_y)
    delta_x = waypoint[waypoint_num][0] + x_offset - hedgehog_x
    delta_y = waypoint[waypoint_num][1] + y_offset - hedgehog_y
    range = math.sqrt(delta_y**2 + delta_x**2)
    return range

def navigate():
        global waypoint
        global waypoint_num
        global heading
        global desired_angle
        global direction
        global range
        global last_range
        global temp_speed
        get_position()  # This generates heading2 and desired angle as global variables
        print ('Rotating')
        rotate(heading2, desired_angle)  # rotate until you're close
        print ('Going straight')
        draw(True)
        last_time = int(round(time.time() * 1000))
        range = 1.0
        while range >= 0.1:
            range = get_range()   # check range
            print ('Range = ', range)
            current_time = int(round(time.time() * 1000))
            delta_time = current_time - last_time
            manager.robot.drive_forward()  # drive straight
            if (delta_time > 3000) and (range > 0.2):  # stop every three seconds while travelling, as long as you're more than 1 m from target
                manager.robot.stop()
                print ('Recalibrating')
                time.sleep(3)  # give it time to settle
                get_position()   # reset heading
                rotate(heading2, desired_angle)
                last_time = current_time
        draw(False)
        waypoint_num = waypoint_num + 1  # increment to next waypoint
        if waypoint_num > 3:    # TEMPORARY  start from beginning again
            waypoint_num = 1
        print ('Next waypoint is:', waypoint_num)

def motors(steer_angle):
        steer_angle = radians_degrees * math.tan(steer_angle/radians_degrees) # take the tangent to create a non-linear response curve
        print('Steer_angle:', round(steer_angle,3))
        left = int((temp_speed)+(steer_angle*steering_gain))
        left = constrain (left, -100, 100)
        right = int((temp_speed)-(steer_angle*steering_gain))
        right = constrain (right, -100, 100)
        print('Left: ', left, 'Right: ', right)
        manager.robot.steer(left,right)

def correct_imu(raw_imu, imu_correction):
        imu = raw_imu + imu_correction
        if imu > 360:
            imu = imu - 360
        if imu < 0:
            imu = imu + 360
        imu = round(imu,3)
        return imu

def calibrate_compass():
        get_position()  # take one reading
        time.sleep(1)
        print ("Driving straight for three seconds to get heading")
        manager.robot.steer(50,50) # drive straight for three seconds to get an orientation
        time.sleep(3)
        get_position() # now take a second reading
        print ("Heading: ", heading2)
        time.sleep(1)
        compass_correction = heading2 - get_imu()
        print ("Compass correction:", compass_correction)
        return compass_correction

def rotate (starting_heading, desired_angle):
        draw(False)
        print('Starting rotation')
        raw_imu = get_imu()
        imu = correct_imu(raw_imu, imu_correction)
        direction = dir(imu, desired_angle)
        while (imu < desired_angle -3) or (imu > desired_angle + 3):  # do the coarse roation fast
            manager.robot.rotate(direction)
            raw_imu = get_imu()
            imu = correct_imu(raw_imu, imu_correction)
            direction = dir(imu, desired_angle)
            print("Current rotation angle: ", imu, "Target angle: ", desired_angle, 'IMU Correction: ', imu_correction)
        manager.robot.stop()
        return imu

def draw(state):
    if state == True:
        manager.robot.pen_up()
    else:
        manager.robot.pen_down()

def dir(heading, desired_angle):
    if (heading >= desired_angle):
        if (heading - desired_angle) >= 180:
            direction = 1  # clockwise
        else:
            direction = -1  # counterclockwise
    else:
        if abs(heading - desired_angle) >= 180:
            direction = -1  # counterclockwise
        else:
            direction = 1  # clockwise
    return direction


if __name__ == "__main__":
    manager = BluetoothDeviceManager(adapter_name = 'hci0')
    manager.start_discovery(service_uuids=[root_identifier_uuid])
    thread = threading.Thread(target = manager.run)
    thread.start()
    char = ""
    try:
        while manager.robot is None:
            pass # wait for a root robot to be discovered
        char = input ("press a key to start")
        print ("Calibrating")
        imu_correction = calibrate_compass()  # the first time, drive straight to get an orientation
        while waypoint_num < waypoint_total:
            navigate()     # do all the steering work here
        print ('Mission finished')
        hedge.stop()  # stop and close serial port
        manager.robot.stop()
        manager.stop()
        manager.robot.disconnect()
        thread.join()
    except KeyboardInterrupt:
        hedge.stop()  # stop and close serial port
        manager.robot.stop()
