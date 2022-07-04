
import time
import RPi.GPIO as GPIO

servoPIN = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

pin = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
pin.start(2.5) # Initialization
time.sleep(5)

try:

  #block 
  # pin.ChangeDutyCycle(3.5)
  # time.sleep(5)
  
  #come back to internet
  pin.ChangeDutyCycle(6.5)


  # pin.ChangeDutyCycle(10.5)
  time.sleep(5)

  
except KeyboardInterrupt:
  pin.stop()
  GPIO.cleanup()

