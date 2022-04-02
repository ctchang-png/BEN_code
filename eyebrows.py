import RPi.GPIO as GPIO
import time

GPIO.setmode(gpio.BOARD)


class Servo():
    def __init__(self, pin, angle_min=30, angle_max=30):
        self.pin = pin
        self.angle_min = angle_min
        self.angle_max = angle_max
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, 50)
        pwm.start(0
        self.pwm = pwm)
        self.angle = 0
        self.set_angle(0)
    
    def set_angle(self, angle):
        if angle < self.angle_min:
            angle = self.angle_min
            print("Angle {:0.2f} exceeds angle limits of ({:0.2f},{:0.2f}) [degrees]".format(angle, self.angle_min, self.angle_max))
        if angle > self.angle_max:
            angle = self.angle_max
            print("Angle {:0.2f} exceeds angle limits of ({:0.2f},{:0.2f}) [degrees]".format(angle, self.angle_min, self.angle_max))
        duty = angle / 18 + 2
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)     

servo1 = Servo(3, angle_min=-30, angle_max=30)
while True:
    #rotate by increments of 90 degrees
    angle = (servo1.angle + 90) % 360
    servo1.set_angle(angle)
    time.sleep(1.0)

