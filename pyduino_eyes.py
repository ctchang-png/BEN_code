from pyduinobridge import Bridge_py
import numpy as np
from math import pi
import time

serPort = 'COM7'  # laptop
serPort = '/dev/ttyACM0'  # pi
baudRate = 115200


class Eyes():
    def __init__(self, verbosity=0):
        myBridge = Bridge_py()
        myBridge.begin(serPort, baudRate, numIntValues_FromPy=4,
                       numFloatValues_FromPy=0)
        myBridge.setSleepTime(0)
        myBridge.setVerbosity(verbosity)
        self.bridge = myBridge
        self.width = 240
        self.height = 320
        # numpy array of [PX_arr; PY_arr; PS_arr; PC_arr] (4xmax_frame)
        self.animation = None
        self.frame = 0
        self.max_frame = 0
        self.px = int(self.width/2)
        self.py = int(self.height/2)
        self.state = "IDLE"  # BEN_state

    '''
    From button press, notify the user that the robot is missing something very important!
    Wake up startled, look around, and direct them to the map.
    Portal is to his left, map will be right in front of him (bottom right).
    '''

    def advance_animation(self):
        self.frame = self.frame + 1
        if self.frame >= self.max_frame:
            # If animation is completed default to idling
            if self.state == "IDLE":
                self.set_animation("IDLE1")
            elif self.state == "ACTIVATED":
                self.set_animation("IDLE2")
            elif self.state == "PORTAL":
                self.set_animation("IDLE3")
        else:
            A = self.animation
            f = self.frame
            #                           ... A[2,f], A[3,f], ...
            # Implement color and size into animations later
            if A.shape[0] != 2:
                print("Animation should be array of shape (2xn)")
            self.bridge.writeAndRead_HeaderAndTwoLists(
                "HEADER", [int(A[0, f]), int(A[1, f]), int(2), int(0xFFFF)], [])
            self.px = A[0, f]
            self.py = A[1, f]

    def get_idle1_animation(self):
        "look around periodically and pause"
        n_move = 10
        n_idle = 40
        b = 20
        x = np.random.randint(0+b, self.width-b)
        ymin = self.height/2 - self.width/2 + b + abs(self.width/2 - b - x)
        ymax = self.height/2 + self.width/2 - b - abs(self.width/2 - b - x)
        if ymin >= ymax:
            ymin = self.height/2
            ymax = self.height/2 + 1
        y = np.random.randint(ymin, ymax)
        x_arr = np.linspace(self.px, x, n_move)
        x_arr = np.concatenate((x_arr, x*np.ones(n_idle)))
        y_arr = np.linspace(self.py, y, n_move)
        y_arr = np.concatenate((y_arr, y*np.ones(n_idle)))
        A = np.vstack([x_arr, y_arr])
        return A, A.shape[1]

    # Len focus on this
    def get_idle2_animation(self):
        "Slight pupil motions while looking towards map of treasure planet"
        # X is height, Y is horizontal
        n_move = 5
        n_idle = 40
        # change to 1/5 for more to the down
        x = int((1/5) * self.width) + \
            np.random.randint(-self.width/10, self.width/10)
        # change to 2/3 for more to the bottom?
        y = int((self.height/2 + (1/8)*self.height)) + \
            np.random.randint(-self.width/10, self.width/10)
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

    def get_ACTIVATED_animation_chris(self, freeze_time=4):
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

        # Look around
        n_move = 10
        n_idle = 40
        x, y = A[0, -1], A[1, -1]
        x_arr = np.ones(4*n_move+2*n_idle) * int(self.width*(1/5))
        y_arr = np.concatenate((np.linspace(y, int(self.height*(1/5)), n_move),
                                np.ones(n_idle)*int(self.height*(1/5)),
                                np.linspace(int(self.height*(1/5)),
                                            int(self.height*(4/5)), 2*n_move),
                                np.ones(n_idle)*int(self.height*(4/5)),
                                np.linspace(int(self.height*(4/5)), y, n_move)))
        B = np.vstack([x_arr, y_arr])

        # Glitch
        n_pts = 20
        n_pause = 5
        x_pts = np.random.randint(0, self.width, n_pts)
        y_pts = np.random.randint(0, self.height, n_pts)
        x_arr = np.repeat(x_pts, n_pause)
        y_arr = np.repeat(y_pts, n_pause)
        C = np.vstack([x_arr, y_arr])

        # Look at treasure map

        # Idle at treasure map
        # handled by advance_animation
        animation = np.concatenate((A, B, C), axis=1)
        return animation, animation.shape[1]

    # Helper FN, look up at the user
    def get_ACTIVATED_animation_awake(self):
        n = 20
        height = np.linspace(int(1/5 * self.height), int(4/5 * self.height), n)
        width = int(1/2 * self.width) * np.ones(n)
        A = np.vstack([height, width])
        return A, A.shape[1]

    # Helper FN, look to sides with tilt
    def get_ACTIVATED_animation_tilt(self):
        n = 10
        height = np.concatenate(
            [np.linspace(int(4/5 * self.height), int(2/5 * self.height), n),
             int(2/5 * self.height) * np.ones(n + 2 * (n // 2))]
        )
        seeleft = np.linspace(int(2/5 * self.width),
                              int(4/5 * self.width), n)
        stayleft = int(4/5 * self.width) * np.ones(n // 2)
        seeright = np.linspace(int(4/5 * self.width),
                               int(1/5 * self.width), n)
        stayright = int(1/5 * self.width) * np.ones(n // 2)
        width = np.concatenate([seeleft, stayleft, seeright, stayright])
        A = np.vstack([height, width])
        return A, A.shape[1]

    # Helper FN, look to sides with down
    def get_ACTIVATED_animation_down(self, freeze_time=4):
        n = 20
        height = int(2/5 * self.height) * np.ones(n)
        left2mid = np.linspace(int(1/5 * self.width),
                               int(2/5 * self.width), n // 2)
        staymid = int(2/5 * self.width) * np.ones(n - (n // 2))
        width = np.concatenate([left2mid, staymid])
        A = np.vstack([height, width])
        return A, A.shape[1]

    # Helper FN, look up left
    def get_ACTIVATED_animation_raiseleft(self):
        n = 15
        height = np.linspace(int(2/5 * self.height), int(4/5 * self.height), n)
        width = int(1/2 * self.width) * np.ones(n)
        A = np.vstack([height, width])
        return A, A.shape[1]

    # Helper FN, look everywhere
    def get_ACTIVATED_animation_glitch(self, freeze_time=4):
        '''
        n = 36
        midH = int(3/5 * self.height)
        midW = int(3/5 * self.width)
        height = midH + (10 * np.sin(np.linspace(0, 2 * np.pi, n)))
        width = midW + (10 * np.cos(np.linspace(0, 2 * np.pi, n)))
        height = np.concatenate([height, height, height, height, height])
        width = np.concatenate([width, width, width, width, width])
        A = np.vstack([height, width])
        '''

        n_pts = 6
        n_pause = 6
        x_pts = np.random.randint(0, self.width, n_pts)
        y_pts = np.random.randint(self.height/2 - self.width/2, self.height/2 + self.width/2, n_pts)
        x_arr = np.repeat(x_pts, n_pause)
        y_arr = np.repeat(y_pts, n_pause)
        A = np.vstack([x_arr, y_arr])
        return A, A.shape[1]

    def get_ACTIVATED_animation(self, freeze_time=4):
        A1, n1 = self.get_ACTIVATED_animation_awake()  # Look Up At User
        A2, n2 = self.get_ACTIVATED_animation_tilt()  # Look To Sides with Tilt
        A3, n3 = self.get_ACTIVATED_animation_down()  # Look Back at Neutral
        A4, n4 = self.get_ACTIVATED_animation_raiseleft()  # Raise Eyebrow
        A5, n5 = self.get_ACTIVATED_animation_glitch()  # Glitch
        N = [n1, n2, n3, n4, n5]
        A = [A1, A2, A3, A4, A5]
        print("pyduino_eyes.py: get_ACTIVATED_animation produced animation of length {}".format(sum(N)))
        return np.hstack(A), np.sum(N)

    def get_portal_animation(self):
        '''
        n = 20
        sinn = 10 * np.sin(np.linspace(0, 2 * np.pi, n))
        coss = 10 * np.cos(np.linspace(0, 2 * np.pi, n))
        midH1 = int(3/5 * self.height)
        midW1 = int(3/5 * self.width)
        midH2 = int(1/2 * self.height)
        midW2 = int(1/2 * self.width)
        midH3 = int(2/5 * self.height)
        midW3 = int(2/5 * self.width)
        height1 = midH1 + sinn
        height2 = midH2 + sinn
        height3 = midH3 + sinn
        width1 = midW1 + coss
        width2 = midW2 + coss
        width3 = midW3 + coss
        height = np.concatenate([height1, height2, height3])
        width = np.concatenate([width1, width2, width3])
        height = np.concatenate([height, height, height, height1])
        width = np.concatenate([width, width, width, width1])
        A = np.vstack([height, width])
        '''
        n = 10
        x, y = self.px, self.py
        xf = self.width/2
        yf = self.height/2 - self.width/2 * 0.6
        x_arr = np.concatenate([np.linspace(x, xf, n), xf*np.ones(n)])
        y_arr = np.concatenate([np.linspace(y, yf, n), yf*np.ones(n)]) #hopefully minus is right
        A = np.vstack([x_arr, y_arr])
        return A, A.shape[1]

    def get_idle3_animation(self):
        n = 10
        x, y = self.px, self.py
        cx, cy = self.width/2, self.height/2 - (self.width/2 * 0.6) #match end points of portal animation
        x_arr = np.linspace(x, cx+np.random.randint(-self.width/20, self.width/20), n)
        y_arr = np.linspace(y, cy+np.random.randint(-self.width/20, self.width/20), n)
        A = np.vstack([x_arr, y_arr])
        return A, A.shape[1]

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
        if animation_name == "IDLE3":
            A, n = self.get_idle3_animation()
        if animation_name == "PORTAL":
            A, n = self.get_portal_animation()
        self.animation = A
        self.max_frame = n
        self.frame = 0
