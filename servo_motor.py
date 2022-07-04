
import time
import RPi.GPIO as GPIO

servoPIN = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

pin = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
# pin.start(2.5) # Initialization
# pin.start(0) # Initialization
pin.start(0)
time.sleep(5)

try:

  # #block on CLASS A
  pin.ChangeDutyCycle(4)
  time.sleep(5)
  pin.ChangeDutyCycle(0)
  
  # #come back to internet
  pin.ChangeDutyCycle(7)
  time.sleep(0.5)
  pin.ChangeDutyCycle(0)


  # pin.ChangeDutyCycle(10.5)
  time.sleep(5)

  
except KeyboardInterrupt:
  pin.stop()
  GPIO.cleanup()

