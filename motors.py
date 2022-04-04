import RPi.GPIO as GPIO
import numpy as np
import time

#GPIO.setmode(GPIO.BOARD) Handled by door_animation.py

class Servo():
    def __init__(self, pin, angle_min=-20, angle_max=20, bias=0):
        self.pin = pin
        if angle_min < -210/2:
            angle_min = 210/2
        if angle_max > 210/2:
            angle_max = 210/2 #can techincally be a bit looser but +-20 or 30 deg should be standard for this bot
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
        print("Servo object at GPIO pin #{} created with angle limits: ({}, {})".format(pin, angle_min, angle_max))
    
    def set_angle(self, angle):
        if angle < self.angle_min:
            angle = self.angle_min
        if angle > self.angle_max:
            angle = self.angle_max
        #angle: +100, -100
        if angle + self.bias < -100:
            angle = -100-self.bias
        if angle + self.bias > 100:
            angle = 100 - self.bias
        duty = 1.5+(12.5-1.5)* (angle+self.bias+100)/200
        print(duty)
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.15)
        GPIO.output(self.pin, False)
        #self.pwm.ChangeDutyCycle(0)
        #time.sleep(0.050)
        self.angle = angle


    def shutdown(self):
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)
        self.pwm.stop()



    
class Eyebrows():
    def __init__(self):
        #self.hl = Servo(pin, angle_min, angle_max)
        #self.al = Servo(pin, angle_min, angle_max)
        self.hr = Servo(2, -30, 30)
        #self.ar = Servo(pin, angle_min, angle_max)
        
        self.animation = None
        self.frame = 0
        self.max_frame = 0
        self.state = "IDLE"

    def advance_animation(self):
        self.frame = self.frame + 1
        if self.frame >= self.max_frame:
            #If animation is complete default to idling
            if self.state == "IDLE":
                self.set_animation("IDLE1")
            else:
                self.set_animation("IDLE1")
        else:
            A = self.animation
            f = self.frame

            if A.shape[0] != 4:
                print("Animation should be array of shape (5xn)")
            #self.hl.set_angle(A[0,f])
            #self.al.set_angle(A[1,f])
            #print("Attempting to set angle {}".format(A[2,f]))
            self.hr.set_angle(A[2,f])
            #self.ar.set_angle(A[3,f])
            #self.jaw.set_angle(A[4,f])
            #time.sleep(0.1) #allow .1s to reach angle. Test and tune this

    def get_idle1_animation(self):
        n = 100
        hr_arr = np.concatenate([np.linspace(-100,100, n), np.flip(np.linspace(-100,100,n)), np.zeros(n)])
        Z = np.zeros(3*n)
        A = np.vstack([Z,Z,hr_arr,Z])
        return A, n

    def set_state(self, state):
        self.state = state

    def set_animation(self, animation_name):
        if animation_name == "IDLE1":
            A, n = self.get_idle1_animation()
        self.animation = A
        self.max_frame = n
        self.frame = 0

    

if __name__ == "__main__":
    servo1 = Servo(3, angle_min=-20, angle_max=20, bias=10)
    while True:
        angle = input("enter angle between {} and {}".format(-20, 20)
        servo1.set_angle(int(angle))