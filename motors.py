import RPi.GPIO as GPIO
import numpy as np
import time

# GPIO.setmode(GPIO.BOARD)  # Handled by door_animation.py, uncomment to run this main method


class Servo():
    def __init__(self, pin, angle_min=-15, angle_max=15, bias=0):
        self.pin = pin
        if angle_min < -210/2:
            angle_min = 210/2
        if angle_max > 210/2:
            # can techincally be a bit looser but +-20 or 30 deg should be standard for this bot
            angle_max = 210/2
        self.angle_min = angle_min
        self.angle_max = angle_max
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, True)
        pwm = GPIO.PWM(pin, 50)
        pwm.start(0)
        self.pwm = pwm
        self.angle = 0
        self.bias = bias
        self.set_angle(0)
        time.sleep(0.50)
        print("Servo object at GPIO pin #{} created with angle limits: ({}, {})".format(
            pin, angle_min, angle_max))

    def set_angle(self, angle):
        if angle < self.angle_min:
            angle = self.angle_min
        if angle > self.angle_max:
            angle = self.angle_max
        # angle: +100, -100
        duty = 1.5+(12.5-1.5) * (angle+self.bias+100)/200
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        # time.sleep(0.5)
        GPIO.output(self.pin, False)
        # self.pwm.ChangeDutyCycle(0)
        # time.sleep(0.050)
        self.angle = angle

    def shutdown(self):
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)
        self.pwm.stop()


class Eyebrows():
    def __init__(self):
        self.hl = Servo(2, angle_min=-15, angle_max=15, bias=0)
        self.al = Servo(3, angle_min=-15, angle_max=15, bias=0)
        self.hr = Servo(4, angle_min=-15, angle_max=15, bias=15)
        self.ar = Servo(14, angle_min=-15, angle_max=15, bias=25)

        self.animation = None
        self.frame = 0
        self.max_frame = 0
        self.state = "IDLE"

    def advance_animation(self):
        self.frame = self.frame + 1
        if self.frame >= self.max_frame:
            # If animation is complete default to idling
            if self.state == "IDLE":
                self.set_animation("IDLE1")
            elif self.state == "ACTIVATED":
                self.set_animation("IDLE2")
            elif self.state == "PORTAL":
                self.set_animation("IDLE1")
        else:
            A = self.animation
            f = self.frame

            if A.shape[0] != 4:
                print("Animation should be array of shape (5xn)")
            self.hl.set_angle(-A[0, f])
            self.al.set_angle(A[1, f])
            # print("Attempting to set angle {}".format(A[2,f]))
            self.hr.set_angle(A[2, f])
            self.ar.set_angle(-A[3, f])
            # self.jaw.set_angle(A[4,f])
            time.sleep(0.1)  # allow .1s to reach angle. Test and tune this

    def get_idle1_animation(self):
        # n = 10
        # hl_arr = np.concatenate([np.linspace(
        #     0, -20, n), np.linspace(-20, 20, 2*n), np.linspace(20, 0, n), np.zeros(4*n)])
        # al_arr = np.concatenate([np.zeros(
        #     4*n), np.linspace(0, -20, n), np.linspace(-20, 20, 2*n), np.linspace(20, 0, n)])
        # hr_arr = np.concatenate([np.linspace(
        #     0, -20, n), np.linspace(-20, 20, 2*n), np.linspace(20, 0, n), np.zeros(4*n)])
        # ar_arr = np.concatenate([np.zeros(
        #     4*n), np.linspace(0, 20, n), np.linspace(20, -20, 2*n), np.linspace(-20, 0, n)])
        # A = np.vstack([hl_arr, al_arr, hr_arr, ar_arr])
        # return A, n*8
        n = 20
        low = -20 * np.ones(n)
        A = np.vstack([low, low, low, low])
        return A, n

    # Helper for ACTIVATED
    def get_ACTIVATED_animation_awake(self):
        n = 20
        fullRange = np.linspace(-20, 20, n)
        posTwenty = 20 * np.ones(n)
        leftHeight = np.concatenate([fullRange, posTwenty])
        leftAngle = np.concatenate([fullRange, posTwenty])
        rightHeight = leftHeight
        rightAngle = leftAngle
        A = np.vstack([leftHeight, leftAngle, rightHeight, rightAngle])
        return A, 2 * n

    # Helper for ACTIVATED
    def get_ACTIVATED_animation_tilt(self):
        n = 20
        posTwenty = 20 * np.ones(n)
        leftHeight = np.concatenate([posTwenty, posTwenty])
        leftAngle = np.concatenate([posTwenty, -posTwenty])
        rightHeight = leftHeight
        rightAngle = -leftAngle
        A = np.vstack([leftHeight, leftAngle, rightHeight, rightAngle])
        return A, 2 * n

    # Helper for ACTIVATED
    def get_ACTIVATED_animation_down(self):
        n = 20
        leftHeight = np.linspace(20, 0, n)
        leftAngle = np.linspace(-20, 0, n)
        rightHeight = leftHeight
        rightAngle = -leftAngle
        A = np.vstack([leftHeight, leftAngle, rightHeight, rightAngle])
        return A, n

    # Helper for ACTIVATED
    def get_ACTIVATED_animation_raiseleft(self):
        n = 15
        leftHeight = np.concatenate([np.linspace(0, 15, n), 15 * np.ones(n)])
        leftAngle = np.concatenate([np.linspace(0, 15, n), 15 * np.ones(n)])
        rightHeight = np.concatenate([np.linspace(0, -5, n), -5 * np.ones(n)])
        rightAngle = np.concatenate([np.linspace(0, 10, n), 10 * np.ones(n)])
        A = np.vstack([leftHeight, leftAngle, rightHeight, rightAngle])
        return A, n

    # Helper for ACTIVATED
    def get_ACTIVATED_animation_glitch(self):
        jump1 = [-10, 10, 10, -10, -10, -15, -15, -10, -10, 15, 15, -10]
        jump2 = [-10, 10, 10, -10, -10, 15, 15, -10, -10, -15, -15, -10]
        wiper = [-10, -10, -5, 5, -5, 5]
        alte1 = [5, 15, 15, -15, -15, 5]
        alte2 = [5, -15, -15, 15, 15, 5]
        leftHeight = jump1 + jump2 + jump1
        leftAngle = alte1 + alte2 + wiper + wiper + alte1 + alte2
        rightHeight = jump2 + jump1 + jump2
        rightAngle = alte2 + alte1 + wiper + wiper + alte2 + alte1
        n = len(jump1)
        A = np.vstack([leftHeight, leftAngle, rightHeight, rightAngle])
        return A, 3 * n

    # Go here when you press 2. Added by Len Huang

    def get_ACTIVATED_animation(self):
        "Why hello there, it seems you've awakened me from something"
        A1, n1 = self.get_ACTIVATED_animation_awake()
        # "I'm looking around, at you all,"
        # A2, n2 = self.get_ACTIVATED_animation_tilt()
        # "Can you help me find something important?"
        # A3, n3 = self.get_ACTIVATED_animation_down()
        # "I'm forgetting what it was"
        # A4, n4 = self.get_ACTIVATED_animation_raiseleft()
        # "OH YES THE TREASURE MAP"
        # A5, n5 = self.get_ACTIVATED_animation_glitch()
        # N = [n1, n2, n3, n4, n5]
        # A = [A1, A2, A3, A4, A5]
        N = [n1]
        A = [A1]
        return np.hstack(A), np.sum(N)
        # return self.get_ACTIVATED_animation_glitch()

    # Look at the bottom left / map / portal button thing
    def get_idle2_animation(self):
        n = 20
        twelve = 15 * np.ones(n)
        A = np.vstack([-twelve, -twelve, -twelve, twelve])
        return A, n
        # return self.get_idle1_animation()

    # React to the portal
    def get_portal_animation(self):
        n = 12
        lookup = np.linspace(-15, 15, n)
        lookdown = np.linspace(15, -15, n)
        angleup = np.linspace(-2, -15, n)
        angledown = np.linspace(-15, -2, n)
        leftHeight = np.concatenate(
            [lookup, lookdown, lookup, lookdown,
             lookup, lookdown,  lookup, lookdown, (-15 * np.ones(n))]
        )
        leftAngle = np.concatenate(
            [angleup, angledown, angleup, angledown,
             angleup, angledown, angleup, angledown, angleup]
        )
        rightHeight = leftHeight
        rightAngle = leftAngle
        A = np.vstack([leftHeight, leftAngle, rightHeight, rightAngle])
        return A, 9 * n

    def get_surprise_animation(self):
        n_zero = 10
        n_up = 30
        hl_arr = np.concatenate([np.zeros(n_zero), 20*np.ones(n_up)])
        al_arr = np.zeros(n_zero+n_up)
        hr_arr = np.concatenate([np.zeros(n_zero), 20*np.ones(n_up)])
        ar_arr = np.zeros(n_zero+n_up)
        A = np.vstack([hl_arr, al_arr, hr_arr, ar_arr])
        return A, n_zero+n_up

    def set_state(self, state):
        self.state = state

    def set_animation(self, animation_name):
        if animation_name == "IDLE1":
            A, n = self.get_idle1_animation()
        if animation_name == "ACTIVATED":
            A, n = self.get_ACTIVATED_animation()
        if animation_name == "IDLE2":
            A, n = self.get_idle2_animation()
        if animation_name == "PORTAL":
            A, n = self.get_portal_animation()
        if animation_name == "surprise":
            A, n = self.get_surprise_animation()
        self.animation = A
        self.max_frame = n
        self.frame = 0


if __name__ == "__main__":
    servo1 = Servo(3, angle_min=-15, angle_max=15, bias=0)
    servo2 = Servo(5, angle_min=-15, angle_max=15, bias=0)
    servo3 = Servo(7, angle_min=-100, angle_max=100, bias=15)
    servo4 = Servo(8, angle_min=-100, angle_max=100, bias=25)
    while True:
        # angle = input("enter angle for servo1 between {} and {}: ".format(-20, 20))
        # servo1.set_angle(-int(angle))
        # servo2.set_angle(int(angle))
        # servo3.set_angle(int(angle))
        # servo4.set_angle(-int(angle))

        print("")
        angle1 = input("leftHeight btwn {} and {}:  ".format(-15, 15))
        angle2 = input("leftAngle btwn {} and {}:   ".format(-15, 15))
        angle3 = input("rightHeight btwn {} and {}: ".format(-15, 15))
        angle4 = input("rightAngle btwn {} and {}:  ".format(-15, 15))
        servo1.set_angle(-int(angle1))  # Bigger => Higher Up
        servo2.set_angle(int(angle2))  # Bigger => More Inward Angle
        servo3.set_angle(int(angle3))  # Bigger => Higher Up
        servo4.set_angle(-int(angle4))  # Bigger => More Inward Angle
