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
        time.sleep(0.50)
        print("Servo object at PIN {} created".format(pin))
    
    def set_angle(self, angle):
        angle = angle % 180 #approximate 180 deg range
        if angle < self.angle_min:
            #print("Angle {:0.2f} exceeds angle limits of ({:0.2f},{:0.2f}) [degrees]".format(angle, self.angle_min, self.angle_max))
            #angle = self.angle_min
            None
        if angle > self.angle_max:
            #print("Angle {:0.2f} exceeds angle limits of ({:0.2f},{:0.2f}) [degrees]".format(angle, self.angle_min, self.angle_max))
            #angle = self.angle_max
            None
        #duty = angle * (100/360)
        #duty range (5, 34) * 100/360 = (1.5, 9.5)
        duty = angle/18 + 2
        print(duty)
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(1.0)
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)
        self.angle = angle

    def shutdown(self):
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)
        self.pwm.stop()

'''
servo1 = Servo(3, angle_min=-30, angle_max=30)
angle = 0
while True:
    try:
        angle += 10
        print(angle)
        servo1.set_angle(angle)
        time.sleep(1.0)
    except KeyboardInterrupt:
        servo1.shutdown()
        GPIO.cleanup()
    
    
'''
pin = 3
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, True)
pwm = GPIO.PWM(pin, 50)
pwm.start(0)

for duty in range(0, 100, 10):
    print(duty)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1.0)