import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)


class Servo():
    def __init__(self, pin, angle_min=30, angle_max=30):
        self.pin = pin
        self.angle_min = angle_min
        self.angle_max = angle_max
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, True)
        pwm = GPIO.PWM(pin, 50)
        pwm.start(0)
        self.pwm = pwm
        self.angle = 0
        self.set_angle(0)
    
    def set_angle(self, angle):
        angle = angle % 360 #Stupid dumbass servo behavior here
        if angle < self.angle_min:
            #print("Angle {:0.2f} exceeds angle limits of ({:0.2f},{:0.2f}) [degrees]".format(angle, self.angle_min, self.angle_max))
            #angle = self.angle_min
            None
        if angle > self.angle_max:
            #print("Angle {:0.2f} exceeds angle limits of ({:0.2f},{:0.2f}) [degrees]".format(angle, self.angle_min, self.angle_max))
            #angle = self.angle_max
            None
        duty = (angle / 18 + 2) % (360/18)
        self.pwm.ChangeDutyCycle(duty)
        self.angle = angle

    def shutdown(self):
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)

#servo1 = Servo(3, angle_min=-30, angle_max=30)
angle = 0
GPIO.setup(3, GPIO.OUT)
GPIO.output(3, True)
pwm = GPIO.PWM(3, 50)
while True:
    angle += 1
    pwm.ChangeDutyCycle(angle)
    print(angle)
    
    

