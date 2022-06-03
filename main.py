from yolov5.device.stepperMotor import run_conveyer
from threading import Thread
from time import sleep


if __name__ == '__main__':
    
    
    Thread(target=run_conveyer, daemon=False).start()
    



