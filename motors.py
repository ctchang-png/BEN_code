import RPi.GPIO as GPIO
import numpy as np
import time

GPIO.setmode(GPIO.BOARD)  # Handled by door_animation.py


class Servo():
    def __init__(self, pin, angle_min=-20, angle_max=20, bias=0):
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
        self.hl = Servo(2, angle_min=-20, angle_max=20, bias=0)
        self.al = Servo(3, angle_min=-20, angle_max=20, bias=0)
        self.hr = Servo(4, angle_min=-20, angle_max=20, bias=15)
        self.ar = Servo(14, angle_min=-20, angle_max=20, bias=25)

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
            else:
                self.set_animation("IDLE1")
        else:
            A = self.animation
            f = self.frame

            if A.shape[0] != 4:
                print("Animation should be array of shape (5xn)")
            self.hl.set_angle(A[0, f])
            self.al.set_angle(A[1, f])
            # print("Attempting to set angle {}".format(A[2,f]))
            self.hr.set_angle(-A[2, f])
            self.ar.set_angle(A[3, f])
            # self.jaw.set_angle(A[4,f])
            time.sleep(0.1)  # allow .1s to reach angle. Test and tune this

    def get_idle1_animation(self):
        n = 10
        hl_arr = np.concatenate([np.linspace(
            0, -20, n), np.linspace(-20, 20, 2*n), np.linspace(20, 0, n), np.zeros(4*n)])
        al_arr = np.concatenate([np.zeros(
            4*n), np.linspace(0, -20, n), np.linspace(-20, 20, 2*n), np.linspace(20, 0, n)])
        hr_arr = np.concatenate([np.linspace(
            0, -20, n), np.linspace(-20, 20, 2*n), np.linspace(20, 0, n), np.zeros(4*n)])
        ar_arr = np.concatenate([np.zeros(
            4*n), np.linspace(0, 20, n), np.linspace(20, -20, 2*n), np.linspace(-20, 0, n)])
        A = np.vstack([hl_arr, al_arr, hr_arr, ar_arr])
        return A, n*8

    # Go here when you press 2. Added by Len Huang
    def get_ACTIVATED_animation(self, freeze_time=4):
        n = 300
        # Left eyebrow raised
        hl_arr = -10 * np.ones(n)
        al_arr = -10 * np.ones(n)
        hr_arr = 10 * np.ones(n)
        ar_arr = 10 * np.ones(n)

        A = np.vstack([hl_arr, al_arr, hr_arr, ar_arr])
        return A, n

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
        if animation_name == "surprise":
            A, n = self.get_surprise_animation()
        self.animation = A
        self.max_frame = n
        self.frame = 0


if __name__ == "__main__":
    servo1 = Servo(3, angle_min=-20, angle_max=20, bias=0)
    servo2 = Servo(5, angle_min=-20, angle_max=20, bias=0)
    servo3 = Servo(7, angle_min=-100, angle_max=100, bias=15)
    servo4 = Servo(8, angle_min=-100, angle_max=100, bias=25)
    while True:
        # angle = input("enter angle for servo1 between {} and {}: ".format(-20, 20))
        # servo1.set_angle(-int(angle))
        # servo2.set_angle(int(angle))
        # servo3.set_angle(int(angle))
        # servo4.set_angle(-int(angle))

        print("")
        angle1 = input("enter servo1 angle btwn {} and {}: ".format(-20, 20))
        angle2 = input("enter servo2 angle btwn {} and {}: ".format(-20, 20))
        angle3 = input("enter servo3 angle btwn {} and {}: ".format(-20, 20))
        angle4 = input("enter servo4 angle btwn {} and {}: ".format(-20, 20))
        servo1.set_angle(-int(angle1))
        servo2.set_angle(int(angle2))
        servo3.set_angle(int(angle3))
        servo4.set_angle(-int(angle4))

'''
Eyebrows In (Angry) Neutral
enter servo1 angle btwn -20 and 20: -10
enter servo2 angle btwn -20 and 20: 10
enter servo3 angle btwn -20 and 20: 10
enter servo4 angle btwn -20 and 20: -10

Eyebrows In (Angry) High
enter servo1 angle btwn -20 and 20: -20
enter servo2 angle btwn -20 and 20: 20
enter servo3 angle btwn -20 and 20: 20
enter servo4 angle btwn -20 and 20: -20

Eyebrows Out (Concerned) Neutral
enter servo1 angle btwn -20 and 20: 10
enter servo2 angle btwn -20 and 20: -10
enter servo3 angle btwn -20 and 20: -10
enter servo4 angle btwn -20 and 20: 10
'''
