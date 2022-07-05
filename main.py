from threading import Thread
import subprocess



def run_inference():
    command = "python yolov5/detect.py --weights models/best.pt --source 0 --conf-thres 0.05 --imgsz 640"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', universal_newlines=True)
    while True:
        realtime_output = process.stdout.readline()
        if realtime_output != '':
            print(realtime_output)


if __name__ == '__main__':
    # Thread(target=run_conveyer, daemon=True).start()
    Thread(target=run_inference, daemon=False).start()
        # Thread(target=run_conveyer, daemon=True).start()
    