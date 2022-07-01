from yolov5.device.stepperMotor import run_conveyer
from threading import Thread
import subprocess

def run_inference():
    
    command = "python3 yolov5/detect.py --weights models/best.pt --source 0"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', universal_newlines=True)
    while True:
        realtime_output = process.stdout.readline()
        if realtime_output != '':
            print(realtime_output)


if __name__ == '__main__':
    Thread(target=run_conveyer, daemon=False).start()
    Thread(target=run_inference, daemon=False).start()
    



