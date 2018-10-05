# Stripped version of VideoTracking9: Here only the tracking is important.

import threading
import cv2
import numpy as np
import math
import imutils
# from wrapi.py.devices.Root.Root_v1_0 import *

# robot = Root_v1_0()
# robot.ledsEffect(ledsEffectSet, clGreen)


class ThreadDraw (threading.Thread):
    def run(self):
        robot.delay(0.5)  # Allows the video system to be initialized.
        distanceTh = 20
        angleTh = 10

        for wp in waypoints:
            # Find the angle to the next waypoint:
            robot.speed(rotSpeed, -rotSpeed)
            angleToWp = 180
            while abs(angleToWp) > angleTh:
                wpAngle = getAngle(center, wp[0])
                angleToWp = wpAngle - heading
                # print angleToWp  # ##Debug.
            robot.positionDriver.stop()
            print "angle ok:", wp, angleToWp  # ##Debug.

            # Move to the angle to the next waypoint:
            robot.speed(fwSpeed, fwSpeed)
            while math.sqrt((center[0] - wp[0][0])**2 + (center[1] - wp[0][1])**2) > distanceTh:
                # print "not there yet"  # ##Debug.
                pass
            robot.positionDriver.stop()
            print "position ok:", wp, center  # ##Debug.
        robot.positionDriver.stop()  # Just in case.



def trackColor(imageIn, imageOut, lowerBound, upperBound, centerColor, boundsColor, drawCircles=False):
    # Convert image to HSV format:
    hsv = cv2.cvtColor(imageIn, cv2.COLOR_BGR2HSV)

    # Make a mask with the boundries and get rid of noise
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    # Find contours from first mask:
    dummyImage, ledsContours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    center = (0, 0)
    radius = 0
    addedContours = []
    if len(ledsContours) > 0:
        cv2.drawContours(imageOut, ledsContours, -1, boundsColor, 12)

        # Make a new mask from the previous contours to improve tracking:
        mask = cv2.inRange(imageOut, boundsColor, boundsColor)
        mask = cv2.dilate(mask, None, iterations=5)
        dummyImage, addedContours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Make circle around all contours and find center point:
        c = max(addedContours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        center = (x, y)
        if drawCircles:
            intCenter = (int(center[0]), int(center[1]))
            cv2.circle(imageOut, intCenter, 5, centerColor, -1)
            cv2.circle(imageOut, intCenter, int(radius), boundsColor, 2)

    return center, radius


# ##Temporal quick function, improve this:
def findWaypoints(imageIn, imageOut, lowerBound, upperBound, boundsColor, drawCircle=True):
    # Convert image to HSV format:
    hsv = cv2.cvtColor(imageIn, cv2.COLOR_BGR2HSV)

    # Make a mask with the boundries and get rid of noise
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    # Find contours from first mask:
    dummyImage, ledsContours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    waypoints = []
    addedContours = []
    if len(ledsContours) > 0:
        cv2.drawContours(imageOut, ledsContours, -1, boundsColor, 5)
        mask = cv2.inRange(imageOut, boundsColor, boundsColor)
        mask = cv2.dilate(mask, None, iterations=1)
        # cv2.imshow("debug", mask)  # ##Debug.
        dummyImage, addedContours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in addedContours:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        center = (x, y)
        intCenter = (int(center[0]), int(center[1]))
        waypoints.append((center, radius))
        if drawCircle:
            cv2.circle(imageOut, intCenter, int(radius), (128, 0, 128), 2)

    return waypoints


def drawTracking(imageOut, center, radius, points, values, displayColor):
    # Average past 2 points and update array
    if len(values) == 2:
        averageX = 0
        averageY = 0
        for i in range(len(values)):
            averageX += values[i][0]
            averageY += values[i][1]
        averageX = averageX / len(values)
        averageY = averageY / len(values)
        averageVal = (averageX, averageY)
        points.append(averageVal)
        values = []
    else:
        distance = 0
        if len(values) > 0:
            lastVal = values[len(values) - 1]
            distance = math.sqrt((center[0] - lastVal[0])**2 + (center[1] - lastVal[1])**2)
        if distance < radius * 4:
            values.append(center)

    for i in range(len(points) - 1):
        cv2.line(imageOut, (int(points[i][0]), int(points[i][1])), (int(points[i+1][0]), int(points[i+1][1])), displayColor, 5)

    return points, values


def traceMap(origin, outputImage, waypoints):
    # print "unsorted:", waypoints  # ##Debug.
    waypoints.sort(key=lambda waypoint: waypoint[1])
    origin = ((origin), 0)
    wps = waypoints[:]
    wps.insert(0, origin)
    # print "sorted  :", waypoints  # ##Debug.

    for i in range(len(wps) - 1):
        cv2.line(
            outputImage,
            (int(wps[i][0][0]), int(wps[i][0][1])),
            (int(wps[i+1][0][0]), int(wps[i+1][0][1])),
            (255, 0, 0), 5
        )


def makeMap(origin, inputImage, outputImage):
    waypoints = findWaypoints(inputImage, outputImage, redLower, redUpper, pointsContourColor)
    traceMap(origin, outputImage, waypoints)

    cv2.imshow("Waypoints", outputImage)
    cv2.moveWindow("Waypoints", 610, 10)  # ##Unhardcode.

    return waypoints


def getAngle(center, point):
    x0 = center[0]
    y0 = center[1]
    x1 = point[0]
    y1 = point[1]

    ref = (int(x0 + 60), int(y0))
    # cv2.line(outputImage, (int(x0), int(y0)), ref, (255, 128, 255), 5)  # ##Unhardcode color.
    # cv2.line(outputImage, (int(x0), int(y0)), ref, (0, 0, 255), 5)  # ##Unhardcode color.

    return math.degrees(math.atan2((y1 - y0), (x1 - x0)))


camera = cv2.VideoCapture(0)  # USB camera (faster).
#camera = cv2.VideoCapture(1)  # Builtin camera (easier to position, plus simultaneous on-screen visualization).

trackingColor = (0, 255, 0)
robotContourColor = (255, 0, 0)
noseColor = (0, 255, 255)
pointsContourColor = (0, 0, 255)

# Set boundries for green light (on the robot):
greenLower = np.array([40, 60, 60])
greenUpper = np.array([90, 255, 255])

# yellowLower = np.array([20, 85, 85])
# yellowUpper = np.array([25, 220, 220])
yellowLower = np.array([20, 80, 80])
yellowUpper = np.array([25, 220, 220])

redLower = np.array([0, 60, 60])
redUpper = np.array([10, 255, 255])

# Not used but probably useful in the future:
# humanHandLower = np.array([0, 60, 60])
# humanHandUpper = np.array([10, 255, 255])

# ##Improve these things in the future: don't use globals.

globalPoints = []
globalValues = []
waypoints = []

firstIteration = True

rotSpeed = 25
fwSpeed = 25
heading = 180
center = (0.0, 0.0)

# Starts the robot thread:
# ThreadDraw().start()

# Main application cycle:
while True:
    # Capture the current image from the camera, and resize it to improve processing speed:
    ret, inputImage = camera.read()
    # inputImage = imutils.resize(inputImage, width=600)  # Best FPS with the USB camera.
    # inputImage = imutils.resize(inputImage, width=900)
    inputImage = imutils.resize(inputImage, width=600)
    # inputImage = imutils.resize(inputImage, width=1200)
    outputImage = inputImage.copy()

    # Process image: if no copy of the images is used to draw, then the order here really matters:
    center, radius = trackColor(inputImage, outputImage, greenLower, greenUpper, trackingColor, robotContourColor)

    # if firstIteration:
    #     firstIteration = False
    #     waypoints = makeMap(center, inputImage, inputImage)
    noseCenter, noseRadius = trackColor(inputImage, outputImage, yellowLower, yellowUpper, noseColor, noseColor, False)
    globalPoints, globalValues = drawTracking(outputImage, center, radius, globalPoints, globalValues, trackingColor)

    heading = getAngle(center, noseCenter)
    # print "heading =", heading  # ##Debug.
    # ##Test:
    # if abs(heading) < 10:
    #    robot.positionDriver.stop()

    # Show images:
    # cv2.imshow("InputImage", inputImage)  # ##Debug.
    cv2.imshow("RootTracking", outputImage)
    cv2.moveWindow("RootTracking", 10, 10)  # ##Unhardcode.

    if cv2.waitKey(1) & 0xff == ord('m'):
        makeMap(center, inputImage, inputImage.copy())

    # Quits when q is pressed:
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release resources:
camera.release()
cv2.destroyWindow("RootTracking")
cv2.destroyWindow("Waypoints")
