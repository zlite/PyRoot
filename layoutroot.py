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
from envirophat import motion


# BLE UUID's
root_identifier_uuid = '48c5d828-ac2a-442d-97a3-0c9822b04979'
uart_service_uuid = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
tx_characteristic_uuid = '6e400002-b5a3-f393-e0a9-e50e24dcca9e' # Write
rx_characteristic_uuid = '6e400003-b5a3-f393-e0a9-e50e24dcca9e' # Notify



kp = 0.6   # P term of the PID
ki = 0.0     # I term of the PID
kd = 0.4    # D term of the PID
gain = 1
cruise_speed = 50  # up to 400
temp_speed = cruise_speed
steering_gain = 1.0 #

OffsetX= (-412+450)/2 # compass calibrated min and max values for X
OffsetY= (-1000+-50)/2 # compass calibrated min and max values for X

waypoint_num = 0
waypoint=[[0 for j in range(2)] for i in range(1000)]  # dimension an array up to 1,000 waypoints

with open('waypoints1.csv') as csv_file:  # change to whatever waypoint file you want
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        waypoint[line_count][0] = float(row[0])  # x data
        waypoint[line_count][1] = float(row[1])  # y data
        line_count += 1
    print('Loaded', line_count, 'waypoints')
    waypoint_total = line_count


#initialize some global variables
hedgehog_id = 6
max_heading = 3600 # full range of heading when paired
hedgehog_x = 0
hedgehog_y = 0
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
hedge = MarvelmindHedge(tty = "/dev/ttyACM0", baud=115200, maxvaluescount=1,adr=hedgehog_id, debug=False) # create MarvelmindHedge thread
hedge.start() # start thread
time.sleep(1) # pause to let it settle
pair_heading = hedge.valuesUltrasoundPosition[0][4] # if using paired beacons
angle_offset = pair_heading


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

        print(type, message)

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

    def turn(self, direction):
        left = cruise_speed + direction * 20
        right = cruise_speed - direction * 20
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

def get_heading(): # use this if you've got paired beacons
        ##### Use the following if you're just using a compass
        raw_imu = get_imu()
        imu_correction = starting_heading - raw_imu
        imu = raw_imu + imu_correction
        imu = correct_imu(raw_imu, imu_correction)
        return imu
        ####### Use the following section if you have paired beacons
        # pair_id = hedge.valuesUltrasoundPosition[0][0] # if using paired beacons
        # pair_heading = hedge.valuesUltrasoundPosition[0][4]
        # heading = 360-(pair_heading/10)  # reverse direction to correspond the waypoint coordinate system
        # heading = 180 + heading  # rotate by 180 degrees to correspond to waypoint coordinate system
        # if heading > 360:
        #     heading = heading - 360
        # return heading

def get_imu():
    mag_values = motion.magnetometer()
    return mag_values[2]

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
    heading = round(get_heading(),3)
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
    position = hedge.position()
    hedgehog_x = position[1]
    hedgehog_y = position[2]
    delta_x = waypoint[waypoint_num][0]-hedgehog_x
    delta_y = waypoint[waypoint_num][1]-hedgehog_y
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
        get_position()
        print ('Slow turning')
        rotate(heading, desired_angle)  # rotate until you're close
        manager.robot.stop()
        time.sleep(4)  # give it time to settle
        get_position()   # reset heading
        print ('Going straight')
        draw(True)
        last_time = int(round(time.time() * 1000))
        imu_correction = heading - get_imu()
        distance = 0  # progress along path so we can stop and recalibrate
        range = 1.0
        while range >= 0.2:  # while more than 0.2m away from waypoint, switch to PID with the IMU to drive a straight line
            temp_speed = cruise_speed   # go full speed for this part
            last_range = range
            range = get_range()   # check range
            fine_steer(desired_angle, imu_correction)
            current_time = int(round(time.time() * 1000))
            delta_time = current_time - last_time
            range = get_range()
            print ('Range = ', range)
            if (delta_time > 6000) and (range > 1):  # stop every six seconds while travelling, as long as you're more than 1 m from target
                manager.robot.stop()
                print ('Recalibrating')
                time.sleep(3)  # give it time to settle
                get_position()   # reset heading
                print ('Paired beacon heading: ', heading, 'Track heading: ', heading2)
                imu_correction = heading2 - get_imu()
                distance = 0  # reset distance reading
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

def rotate (starting_heading, desired_angle):
        draw(False)
        raw_imu = get_imu()
        imu_correction = starting_heading - raw_imu
        print('IMU correction: ', imu_correction)
        print('Starting coarse rotation')
        imu = raw_imu + imu_correction
        imu = correct_imu(raw_imu, imu_correction)
        direction = dir(imu, desired_angle)
        while (imu < desired_angle -5) or (imu > desired_angle + 5):  # do the coarse roation fast
            manager.robot.turn(direction)
            raw_imu = get_imu()
            imu = correct_imu(raw_imu, imu_correction)
            direction = dir(imu, desired_angle)
            print("Coarse rotation angle: ", imu, "Target angle: ", desired_angle, 'IMU Correction: ', imu_correction)
        manager.robot.stop()
        time.sleep(4) # pause to let measurements settle
        get_position()  # update heading
        raw_imu = get_imu()
        imu_correction = heading - raw_imu
        imu = correct_imu(raw_imu, imu_correction)
        direction = dir(imu, desired_angle)
        print ('Starting fine rotation')
        while (imu < desired_angle - 2) or (imu > desired_angle + 2):  # do the fine rotation slow
            manager.robot.turn(direction)
            raw_imu = get_imu()
            imu = correct_imu(raw_imu, imu_correction)
            direction = dir(imu, desired_angle)
            print("Fine rotation angle: ", imu, "Target angle: ", desired_angle, 'IMU Correction: ', imu_correction)
        manager.robot.stop()
        return imu

def fine_steer(desired_angle, imu_correction): # do this one with the onboard IMU
        global old_time
        imu = 0 # initialize variable
        raw_imu = get_imu()
        imu = round(raw_imu + imu_correction,3)
        now = int(round(time.time() * 1000))
        if  now > (old_time + 100):  # milliseconds passed since last measurement; do the PID at 20hz (100 miliseconds)
            delta_angle = desired_angle - imu   # watch out for singularities around the 360 - 0 transition
            if delta_angle > 340:  # this means the IMU moved from the 360 to the zero side (to the right)
                imu = imu + 360
                print ('Singularity! delta_angle = ', delta_angle, 'New imu = ', imu)
            if delta_angle < -340: # this means that the IMU moved from the zero to the 360 side (to the left)
                imu = imu - 360
                print ('Singularity! delta_angle = ', delta_angle, 'imu = ', imu)
            steer_angle = update_pid(imu, desired_angle)
            print('Current IMU heading: ', imu, 'Target heading: ', desired_angle, 'Steer command: ', steer_angle, 'Range: ', range)
            old_time = now
            motors(steer_angle)

def draw(state):
    if state == True:
        manager.robot.pen_up()
    else:
        manager.robot.pen_down()

def dir(heading, desired_angle):
    if (heading >= desired_angle):
        if (heading - desired_angle) >= 180:
            direction = -1  # clockwise
        else:
            direction = 1  # counterclockwise
    else:
        if abs(heading - desired_angle) >= 180:
            direction = 1  # counterclockwise
        else:
            direction = -1  # clockwise
    return direction


def main():
    manager = BluetoothDeviceManager(adapter_name = 'hci0')
    manager.start_discovery(service_uuids=[root_identifier_uuid])
    thread = threading.Thread(target = manager.run)
    thread.start()
    char = ""
    try:
        while manager.robot is None:
            pass # wait for a root robot to be discovered
        manager.robot.drive_forward()
        time.sleep(1)
        while char != "q":
            while waypoint_num < waypoint_total:
                char = input() # wait for keyboard input
                navigate()     # do all the steering work here
            print ('Mission finished')
            hedge.stop()  # stop and close serial port
            manager.robot.stop()
            sys.exit()
        print("Quitting")
        manager.stop()
        manager.robot.disconnect()
        thread.join()
    except KeyboardInterrupt:
        hedge.stop()  # stop and close serial port
        manager.robot.stop()

main()
