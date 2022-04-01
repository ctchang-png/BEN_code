import numpy as np
import time
from math import pi

serPort = 'COM7'
serPort = '/dev/ttyACM0'
baudRate = 115200

from pyduinobridge import Bridge_py


class Eyes():
    def __init__(self, verbosity=0):
        myBridge = Bridge_py()
        myBridge.begin(serPort, baudRate, numIntValues_FromPy=4, numFloatValues_FromPy=0)
        myBridge.setSleepTime(0)
        myBridge.setVerbosity(verbosity)
        self.bridge = myBridge
        self.width = 240
        self.height = 320
        self.animation = None #numpy array of [PX_arr; PY_arr; PS_arr; PC_arr] (4xmax_frame)
        self.frame = 0
        self.max_frame = 0
        self.px = int(self.width/2)
        self.py = int(self.height/2)
        self.state = "IDLE" #BEN_state

    def advance_animation(self):
        self.frame = self.frame + 1
        if self.frame >= self.max_frame:
            #If animation is completed default to idling
            if self.state == "IDLE":
                self.set_animation("IDLE1")
            elif self.state == "ACTIVATED":
                self.set_animation("IDLE2")
        else:
            A = self.animation
            f = self.frame
            #                           ... A[2,f], A[3,f], ...
            # Implement color and size into animations later
            if A.shape[0] != 2:
                print("Animation should be array of shape (2xn)")
            self.bridge.writeAndRead_HeaderAndTwoLists("HEADER", [int(A[0,f]), int(A[1,f]), int(2), int(0xFFFF)], [])
            self.px = A[0,f]
            self.py = A[1,f]

    def get_idle1_animation(self):
        "look around periodically and pause"
        n_move = 10
        n_idle = 40
        x = np.random.randint(0, self.width)
        y = np.random.randint(0, self.height)
        x_arr = np.linspace(self.px, x, n_move)
        x_arr = np.concatenate((x_arr, x*np.ones(n_idle)))
        y_arr = np.linspace(self.py, y, n_move)
        y_arr = np.concatenate((y_arr, y*np.ones(n_idle)))
        A = np.vstack([x_arr, y_arr])
        return A, A.shape[1]

    def get_idle2_animation(self):
        "Slight pupil motions while looking towards map of treasure planet"
        n_move = 5
        n_idle = 40
        x = int(self.width*(4/5)) + np.random.randint(-self.width/10, self.width/10)
        y = int(self.height/2) + np.random.randint(-self.width/10, self.width/10)
        x_arr = np.linspace(self.px, x, n_move)
        x_arr = np.concatenate((x_arr, x*np.ones(n_idle)))
        y_arr = np.linspace(self.py, y, n_move)
        y_arr = np.concatenate((y_arr, y*np.ones(n_idle)))
        A = np.vstack([x_arr, y_arr])
        return A, A.shape[1]


    def get_center_animation(self, freeze_time=1):
        n_move = 10
        TIME_TO_FRAMES = 50
        n_idle = freeze_time * TIME_TO_FRAMES
        x = int(self.width/2)
        y = int(self.height/2)
        x_arr = np.linspace(self.px, x, n_move)
        x_arr = np.concatenate((x_arr, x*np.ones(n_idle)))
        y_arr = np.linspace(self.py, y, n_move)
        y_arr = np.concatenate((y_arr, y*np.ones(n_idle)))
        A = np.vstack([x_arr, y_arr])
        return A, A.shape[1]

    def get_ACTIVATED_animation(self, freeze_time=4):
        # Animation when robot enters 'activated' state following a button press
        # Look up towards user's eyes
        n_move = 10
        TIME_TO_FRAMES = 50
        n_idle = freeze_time * TIME_TO_FRAMES
        x = int(self.width*(1/5))
        y = int(self.height/2)
        x_arr = np.linspace(self.px, x, n_move)
        x_arr = np.concatenate((x_arr, x*np.ones(n_idle)))
        y_arr = np.linspace(self.py, y, n_move)
        y_arr = np.concatenate((y_arr, y*np.ones(n_idle)))
        A = np.vstack([x_arr, y_arr])

        #Look around
        n_move = 10
        n_idle = 40
        x, y = A[0,-1], A[1,-1]
        x_arr = np.ones(4*n_move+2*n_idle) * int(self.width*(1/5))
        y_arr = np.concatenate( (np.linspace(y, int(self.height*(1/5)), n_move),
                                 np.ones(n_idle)*int(self.height*(1/5)),
                                 np.linspace(int(self.height*(1/5)), int(self.height*(4/5)), 2*n_move),
                                 np.ones(n_idle)*int(self.height*(4/5)),
                                 np.linspace(int(self.height*(4/5)), y, n_move)))
        B = np.vstack([x_arr, y_arr])

        #Glitch
        n_pts = 15
        n_pause = 10
        x_pts = np.random.randint(0, self.width, n_pts)
        y_pts = np.random.randint(0, self.height, n_pts)
        x_arr = np.repeat(x_pts, n_pause)
        y_arr = np.repeat(y_pts, n_pause)
        C = np.vstack([x_arr, y_arr])


        #Look at treasure map

        #Idle at treasure map
        animation = np.concatenate((A, B, C), axis=1)
        return animation, animation.shape[1]

    def set_state(self, state):
        self.state = state

    def shutdown(self):
        self.bridge.close()

    def set_animation(self, animation_name):
        if animation_name == "IDLE1":
            A, n = self.get_idle1_animation()
        if animation_name == "CENTER":
            A, n = self.get_center_animation()
        if animation_name == "ACTIVATED":
            A, n = self.get_ACTIVATED_animation()
        if animation_name == "IDLE2":
            A, n = self.get_idle2_animation()
        self.animation = A
        self.max_frame = n
        self.frame = 0
        
