
import time
import RPi.GPIO as GPIO

servoPIN = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

pin = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
# pin.start(2.5) # Initialization
# pin.start(0) # Initialization
pin.start(4)
# time.sleep(1)

try:

  # #block on CLASS A
  # pin.ChangeDutyCycle(4)
  # time.sleep(20)
  
  # #come back to internet
  # pin.ChangeDutyCycle(7)


  # pin.ChangeDutyCycle(10.5)
  time.sleep(5)

  
except KeyboardInterrupt:
  pin.stop()
  GPIO.cleanup()

