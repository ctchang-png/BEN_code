import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
gpio.setup(3, gpio.OUT)
pwm = gpio.PWM(3, 50)
pwm.start(0)

def SetAngle(angle):
	duty = angle / 18 + 2
	gpio.output(3, True)
	pwm.ChangeDutyCycle(duty)
	time.sleep(1)
	gpio.output(3, False)
	pwm.ChangeDutyCycle(0)

SetAngle(90)
pwm.stop()
gpio.cleanup()