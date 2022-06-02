import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time

dir = 22
step = 23
en_pin = 24


motor = RpiMotorLib.A4988Nema(dir, step, (21,21,21), "DRV8825")
GPIO.setup(en_pin, GPIO.OUT)


#Motor control
GPIO.output(en_pin, GPIO.LOW) #pulled to low to enable motor
i = 0
while(i<100):
    motor.motor_go(False, 
                    "Full",
                    200,
                    0.0005,
                    False,
                    0.05)
    i+=1

GPIO.cleanup();