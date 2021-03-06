# import RPi.GPIO as GPIO
# from RpiMotorLib import RpiMotorLib
# import time

# dir = 20
# step = 21
# en_pin = 26


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

from time import sleep
try:
    import pigpio 
except:
    print("pigpio not installed")

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 48   # Steps per Revolution (360 / 7.5)

try:
    #connecting the pigpio daemon
    pi = pigpio.pi()

    #cycle and frequency
    pi.set_PWM_dutycycle(STEP, 128)
    pi.set_PWM_frequency(STEP, 500)
except Exception as e:
    print(f"[ERROR] {e}")

def run_conveyer():
    while 1:
        print("moving")
        sleep(1)
    try:
        while True:
            try:
                pi.write(DIR, 1) # direction of the motor to clockwise
                sleep(.1)
            except Exception as e:
                print(f"[ERROR] {e}")

    except KeyboardInterrupt:
        print("\nCtrl-C pressed. Stopping PIGPIo and exit")

    finally:
        try:
            pi.set_PWM_dutycycle(STEP,0) # off Pulse width modulation
            pi.stop()
        except Exception as e:
            print(f"[ERROR] {e}")

