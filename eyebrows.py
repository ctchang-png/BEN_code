import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)


class Servo():
    def __init__(self, pin, angle_min=20, angle_max=20):
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
        time.sleep(0.50)
        print("Servo object at PIN {} created".format(pin))
    
    def set_angle(self, angle):
        #angle: scale from 0-100 from angle_min to angle_max
        #measured angle range is 0-210
        #measured duty range is  0-12.5
        if angle < self.angle_min:
            #print("Angle {:0.2f} exceeds angle limits of ({:0.2f},{:0.2f}) [degrees]".format(angle, self.angle_min, self.angle_max))
            #angle = self.angle_min
            None
        if angle > self.angle_max:
            #print("Angle {:0.2f} exceeds angle limits of ({:0.2f},{:0.2f}) [degrees]".format(angle, self.angle_min, self.angle_max))
            #angle = self.angle_max
            None
        angle_degrees = angle *0.01*(self.angle_max-self.angle_min) + self.angle_min
        angle_offset = angle_degrees + 210/2
        duty = angle_offset * (12.5/210)
        #print(duty)
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.050)
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)
        time.sleep(0.050)
        self.angle = angle

    def shutdown(self):
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)
        self.pwm.stop()


servo1 = Servo(3, angle_min=-30, angle_max=30)
for angle in range(-30, 31, 5):
    print(angle)
    servo1.set_angle(angle)
    
