
is_rasperry_pi = True
try:
    from time import sleep
    from gpiozero import AngularServo

except ImportError:
    is_rasperry_pi = False


CLASS_I = 11
CLASS_II = 12

if is_rasperry_pi:
    class_i_servo = AngularServo(CLASS_I, min_pulse_width=0.0006, max_pulse_width=0.0023)
    class_ii_servo = AngularServo(CLASS_II, min_pulse_width=0.0006, max_pulse_width=0.0023)

def set_class_i():
    if is_rasperry_pi:
        class_i_servo.angle = 90
        sleep(1)
        class_i_servo.angle = 0
def set_class_ii():
    if is_rasperry_pi:
        class_ii_servo.angle = -90
        sleep(1)
        class_ii_servo.angle = 0