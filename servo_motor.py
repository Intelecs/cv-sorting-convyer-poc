import RPi.GPIO as GPIO
import time

servoPIN = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(7.5) # Initialization
time.sleep(5)

val = 0
try:

  #block 
  p.ChangeDutyCycle(3.5)
  time.sleep(15)
  
  #come back to internet
  p.ChangeDutyCycle(7.5)
  time.sleep(5)

  
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()

