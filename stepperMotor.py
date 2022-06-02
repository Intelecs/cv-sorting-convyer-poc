# import RPi.GPIO as GPIO
# from RpiMotorLib import RpiMotorLib
# import time

# dir = 22
# step = 23
# en_pin = 24


# motor = RpiMotorLib.A4988Nema(dir, step, (21,21,21), "DRV8825")
# GPIO.setup(en_pin, GPIO.OUT)


# #Motor control
# GPIO.output(en_pin, GPIO.LOW) #pulled to low to enable motor
# i = 0
# while(i<100):
#     motor.motor_go(False, 
#                     "Full",
#                     200,
#                     0.0005,
#                     False,
#                     0.05)
#     i+=1

# GPIO.cleanup();

# from time import sleep
# import RPi.GPIO as GPIO

# DIR = 22   # Direction GPIO Pin
# STEP = 23  # Step GPIO Pin
# CW = 1     # Clockwise Rotation
# CCW = 0    # Counterclockwise Rotation
# SPR = 48   # Steps per Revolution (360 / 7.5)

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(DIR, GPIO.OUT)
# GPIO.setup(STEP, GPIO.OUT)
# GPIO.output(DIR, CW)

# step_count = SPR
# delay = .0208

# for x in range(step_count):
#     GPIO.output(STEP, GPIO.HIGH)
#     sleep(delay)
#     GPIO.output(STEP, GPIO.LOW)
#     sleep(delay)

# sleep(.5)
# GPIO.output(DIR, CCW)
# for x in range(step_count):
#     GPIO.output(STEP, GPIO.HIGH)
#     sleep(delay)
#     GPIO.output(STEP, GPIO.LOW)
#     sleep(delay)

# GPIO.cleanup()