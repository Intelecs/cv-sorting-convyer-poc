from stepper_motor import run_conveyer
from threading import Thread
import subprocess
import pigpio 

command = "sudo pigiod"
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', universal_newlines=True)

pi = pigpio.pi()
STEP = 21 


def run_inference():
    
    command = "python3 yolov5/detect.py --weights models/best.pt --source 0"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', universal_newlines=True)
    while True:
        realtime_output = process.stdout.readline()
        if realtime_output != '':
            print(realtime_output)


if __name__ == '__main__':
    # Thread(target=run_conveyer, daemon=True).start()
    
    
    try:
        Thread(target=run_inference, daemon=True).start()
        # Thread(target=run_conveyer, daemon=True).start()

    except KeyboardInterrupt:
        print("\nCtrl-C pressed. Stopping PIGPIo and exit")
    finally:
        pi.set_PWM_dutycycle(STEP,0) # off Pulse width modulation
        pi.stop()