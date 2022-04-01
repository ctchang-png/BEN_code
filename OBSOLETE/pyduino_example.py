import numpy as np
import time
from math import pi

serPort = 'COM7'
baudRate = 115200

from pyduinobridge import Bridge_py
myBridge = Bridge_py()
myBridge.begin(serPort, baudRate, numIntValues_FromPy=4, numFloatValues_FromPy=0)
myBridge.setSleepTime(0)
#numIntVals_fromPy = 4
#numFloatVals_fromPy = 1
WIDTH = 240
HEIGHT = 320

# circular motion
n = 50 #number of frames
t = np.linspace(0, 2*pi, n)
x = (120 + 60*np.cos(t)).astype(int)
y = (160 + 60*np.sin(t)).astype(int)
#           Note: color must be uint16_t
testData = [(str(i), [int(x[i]), int(y[i]), int(2), int(0xFFFF)], []) for i in range(n)]
#header: frame number
#int_arr: [px, py, pr, pc]
#float_arr: [] (Empty)
# When using this function, the program sends a list of strings and receives a list of strings.
for header, int_arr, float_arr in testData:
    myBridge.writeAndRead_HeaderAndTwoLists(header, int_arr, float_arr)
    #header_fromArdu, int_arr, float_arr, millis = myBridge.writeAndRead_HeaderAndTwoLists("",[0,0,0,0],[])


# To hide the transmitted and received messages from the Python terminal:
myBridge.setVerbosity(0)

time.sleep(1.0)
#Idling motion
_, int_arr_old, float_arr_old = testData[-1]
x_old, y_old = int_arr_old[0], int_arr_old[1]
n_move = 30 #Fixed number of frames to reach goal
n_idle = 100 #Fixed number of frames to idle at position
while True:
    x = np.random.randint(0, WIDTH)
    y = np.random.randint(0, HEIGHT)
    x_arr = np.linspace(x_old, x, n_move)
    x_arr = np.concatenate((x_arr, x*np.ones(n_idle)))
    y_arr = np.linspace(y_old, y, n_move)
    y_arr = np.concatenate((y_arr, y*np.ones(n_idle)))
    data = [("HEADER", [int(x_arr[i]), int(y_arr[i]), int(2), int(0xFFFF)], []) for i in range(x_arr.size)]
    for header, int_arr, float_arr in data:
        myBridge.writeAndRead_HeaderAndTwoLists(header, int_arr, float_arr)
    x_old, y_old = x, y


myBridge.close()