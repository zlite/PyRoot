# Testing stuff for the Camera1d class:

from wrapi.py.devices.RemoteCamera1d import *
camera1d = RemoteCamera1d()

#condition = []
condition = [clYellow]
print camera1d.computeDetectionZones(condition)
print

#condition = [clBlack, clRed]

condition = [clYellow, clBlue, clRed]
print camera1d.computeDetectionZones(condition)
print

#condition = [clBlack, clRed, clRed, clRed]

condition = [clBlack, clRed, clGreen, clBlue, clYellow]
print camera1d.computeDetectionZones(condition)
print

#condition = [clBlack, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]

#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]  # ##12
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]

# 15:
condition = [clYellow, clRed, clRed, clRed, clRed, clRed, clRed, clBlue, clRed, clRed, clRed, clRed, clRed, clRed, clWhite]
print camera1d.computeDetectionZones(condition)
print

#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]

# 26:
condition = [clViolet, clRed, clRed, clRed, clRed, clRed, clYellow, clBlue, clOrange, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clWhite]
print camera1d.computeDetectionZones(condition)
print

#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]

# 30:
condition = [clYellow, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
print camera1d.computeDetectionZones(condition)
print

#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
#condition = [clBlack, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed, clRed]
