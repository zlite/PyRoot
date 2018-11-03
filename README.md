# PyRoot
Python control of Root Robot via BLE
Open Source Licence: BSD

This example will allow you to control a Root Robot via Python on a Bluetooth-equipped Raspberry Pi (or any other Linux computer with Bluetooth). 


Instructions: 

1) Clone Gatt-Python: https://github.com/getsenic/gatt-python
2) If you're using a RasperryPi 3 or Zero W, you've already got Bluetooth Low Energy (BLE) built in, along with the necessary BlueZ library. If not follow the Gatt instructions: https://github.com/getsenic/gatt-python
3) Clone this repo into your Gatt-Python folder. 
4) Run the example by typing "Python3 drive-root.py" and then, after it finds your Root, typing in command letters followed by the enter key

"l" = Left
"r" = Right
"f" = Forward
"b" = Back
"s" = Stop
"u" = Pen Up
"d" = Pen Down
"q" = Quit
