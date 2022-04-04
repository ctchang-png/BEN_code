import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

def do_servo_animation():
    return None

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
        self.set_angle(50)
        tic = time.time()
        time.sleep(0.50)
        print(time.time() - tic)
        print("Servo object at PIN {} created".format(pin))
    
    def set_angle(self, angle):
        #angle: scale from 0-100 from angle_min to angle_max
        #measured angle range is 0-210
        #measured duty range is  0-12.5
        if angle < 0:
            angle = 0
        if angle > 100:
            angle = 100
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



    
class Motors():
    def __init__(self):
        self.hl = Servo(pin, angle_min, angle_max)
        self.al = Servo(pin, angle_min, angle_max)
        self.hr = Servo(pin, angle_min, angle_max)
        self.ar = Servo(pin, angle_min, angle_max)
        self.jaw = Servo(pin, angle_min, angle_max)
        
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

        if A.shape[0] !=1:
            print("Animation should be array of shape (1xn)")
        self.hl.set_angle(A[0,f])

    def get_idle1_animation(self):
        n = 100
        hl_arr = np.linspace(0,100, n)
        return hl_arr, n

if __name__ == "__main__":
    servo1 = Servo(3, angle_min=-30, angle_max=30)
    while True:
        angle = input("enter angle between {} and {}".format(-30, 30))
        servo1.set_angle(int(angle))