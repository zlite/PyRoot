import threading
import cv2
import numpy as np
import math
import imutils
from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()
robot.ledsEffect(ledsEffectSet, clGreen)

def drawSquare():
    distance = 5  # cm.

    # robot.penDown()
    robot.move(distance)
    robot.rotate(90)
    robot.move(distance)
    robot.rotate(90)
    robot.move(distance)
    robot.rotate(90)
    robot.move(distance)
    # robot.penAndEraserUp()
    # robot.stop()


class ThreadDraw (threading.Thread):
    def run(self):
        drawSquare()


def trackColor(imageIn, imageOut, lowerBound, upperBound, centerColor, boundsColor, drawCircles=True):
    # Convert image to HSV format:
    hsv = cv2.cvtColor(imageIn, cv2.COLOR_BGR2HSV)

    # Make a mask with the boundries and get rid of noise
    greenMask = cv2.inRange(hsv, lowerBound, upperBound)
    greenMask = cv2.erode(greenMask, None, iterations=1)
    greenMask = cv2.dilate(greenMask, None, iterations=1)

    # Find contours from first mask:
    dummyImage, ledsContours, hierarchy = cv2.findContours(greenMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    center = (0, 0)
    radius = 0
    if len(ledsContours) > 0:
        cv2.drawContours(imageOut, ledsContours, -1, boundsColor, 12)

        # Make a new mask from the previous contours to improve tracking:
        mask = cv2.inRange(imageOut, boundsColor, boundsColor)
        mask = cv2.dilate(mask, None, iterations=5)
        dummyImage, addedContours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Make circle around all contours and find center point:
        c = max(addedContours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))
        if drawCircles:
            cv2.circle(imageOut, center, 5, centerColor, -1)
            cv2.circle(imageOut, center, int(radius), boundsColor, 2)

    return center, radius


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

    for i in range(len(points)-1):
        cv2.line(imageOut, points[i], points[i+1], displayColor, 5)

    return points, values


camera = cv2.VideoCapture(0)  # USB camera (faster).
# camera = cv2.VideoCapture(1)  # Builtin camera (easier to position, plus simultaneous on-screen visualization).

globalPoints = []
globalValues = []

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

# Not used but probably useful in teh future:
# humanHandLower = np.array([0, 60, 60])
# humanHandUpper = np.array([10, 255, 255])

# Starts the robot thread:
ThreadDraw().start()

# Main application cycle:
while True:
    # Capture the current image from the camera, and resize it to improve processing speed:
    ret, inputImage = camera.read()
    inputImage = imutils.resize(inputImage, width=600)  # Best FPS with the USB camera.
    # inputImage = imutils.resize(image, width=900)
    # inputImage = imutils.resize(image, width=1200)
    outputImage = inputImage.copy()

    # Process image: if no copy of the images is used to draw, then the order here really matters:
    center, radius = trackColor(inputImage, outputImage, greenLower, greenUpper, trackingColor, robotContourColor)
    noseCenter, noseRadius = trackColor(inputImage, outputImage, yellowLower, yellowUpper, noseColor, noseColor)
    globalPoints, globalValues = drawTracking(outputImage, center, radius, globalPoints, globalValues, trackingColor)
    trackColor(inputImage, outputImage, redLower, redUpper, pointsContourColor, pointsContourColor, False)

    # Show image:
    cv2.imshow("RootTracking", outputImage)

    # Quits when q is pressed:
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release resources:
camera.release()
cv2.destroyWindow("RootTracking")
