import argparse
import os
import sys
from pathlib import Path
import time
import torch
import torch.backends.cudnn as cudnn
from threading import Thread

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_img_size, check_imshow, check_requirements, cv2,
                         non_max_suppression, print_args, scale_coords, strip_optimizer)
from utils.plots import Annotator, colors
from utils.torch_utils import select_device, time_sync

try:
    import RPi.GPIO as GPIO
    import pigpio 
    pi = pigpio.pi()


    triggerPin = 23
    echoPin = 24


    servo_pin = 13
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)
    # handle = GPIO.PWM(servo_pin, 50) # GPIO 17 for PWM with 50Hz
    # handle.start(0) # Initialization
    time.sleep(3)

    GPIO.setup(triggerPin,GPIO.OUT)
    GPIO.setup(echoPin,GPIO.IN)

    # handle.ChangeDutyCycle(7)
    # time.sleep(5)
    # handle.ChangeDutyCycle(4)
except ImportError:
    pass 

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 48   # Steps per Revolution (360 / 7.5)


try:
    pi.set_PWM_dutycycle(STEP, 128)
    pi.set_PWM_frequency(STEP, 800)
except Exception as e:
    pass

def open_servo():

    handle.ChangeDutyCycle(4)
    time.sleep(25)
    handle.ChangeDutyCycle(0)


    handle.ChangeDutyCycle(7)
    time.sleep(0.5)
    handle.ChangeDutyCycle(0)
    # GPIO.cleanup()

def run_conveyer():
    while True:
        pi.write(DIR, CCW)

def ultasonic():
    while True:
        GPIO.output(triggerPin, False)
        time.sleep(1)
    
        GPIO.output(triggerPin, True)
        time.sleep(0.00001)
        GPIO.output(triggerPin, False)
    
    
        while GPIO.input(echoPin)==0:
             pulseStart = time.time()
    
        while GPIO.input(echoPin)==1:
             pulseEnd = time.time()
    
        pulseDuration = pulseEnd - pulseStart
    
        distance = pulseDuration * 17150
    
    
        distance = round(distance, 2)
    
        print("Distance: %s cm")
        print(distance)

Thread(target=run_conveyer, daemon=True).start()
# Thread(target=ultasonic, daemon=True).start()

@torch.no_grad()
def run(
        weights=ROOT / 'yolov5s.pt',  # model.pt path(s)
        source=ROOT / 'data/images',  # file/dir/URL/glob, 0 for webcam
        data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
        imgsz=(320, 3200),  # inference size (height, width)
        conf_thres=0.7,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=100,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=True,  # show results
    save_txt=False,  # save results to *.txt
    save_conf=False,  # save confidences in --save-txt labels
    save_crop=False,  # save cropped prediction boxes
    nosave=False,  # do not save images/videos
          project=ROOT / "runs/detect",  # save results to project/name
    name="exp",  # save results to project/name
    exist_ok=False,
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
):
    source = str(source)
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)


    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Dataloader
    if webcam:
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt)
        bs = len(dataset)  # batch_size
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
        bs = 1  # batch_size
   
    # Run inference
    model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
    dt, seen = [0.0, 0.0, 0.0], 0
    
    predicted_labels = []
    for path, im, im0s, _, s in dataset:
        t1 = time_sync()
        im = torch.from_numpy(im).to(device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
    
        pred = model(im, augment=augment, visualize=visualize)
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        dt[2] += time_sync() - t3

        
        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            s += '%gx%g ' % im.shape[2:]  # print string

            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum() 
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  

                # Write results
                for *xyxy, conf, cls in reversed(det):

                    
                    predicted_labels.append(
                        {
                            "label": names[int(cls)],
                            "confidence": f"{conf:.2f}",
                            "inference_speed": f"{t3 - t2:.3f}",
                            "timestamp": int(time.time())
                        }
                    )

                    if names[int(cls)] == 'CLASS I':
                        LOGGER.info(f"Opening Servo for CLASS A")
                        # set_class_i()
                        
                        time.sleep(5)
                    
                    if names[int(cls)] == 'Class II':
                        LOGGER.info(f"Opening Servo for CLASS B")
                        # set_class_ii() with

                        # try:
                        #     duty = 4
                        #     handle.ChangeDutyCycle(7)
                        #     time.sleep(5)
                        #     handle.ChangeDutyCycle(4)
                        #     while duty <= 7:
                        #         handle.ChangeDutyCycle(duty)
                        #         time.sleep(0.01)
                        #         duty = duty + 0.033


                        # except Exception as e:
                        #     LOGGER.error(f"Error opening servo: {e}")
                    

                    c = int(cls)  # integer class
                    label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                    annotator.box_label(xyxy, label, color=colors(c, True))
    
            # Stream results
            im0 = annotator.result()
             
            cv2.imshow("Mangoes Sorting and Grading", im0)
            cv2.waitKey(1)  # 1 millisecond
            LOGGER.info(f'Total time: {sum(dt):.3f}s')
            t = tuple(x / seen * 1E3 for x in dt)  # speeds per image
            LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)

            LOGGER.info(
                        f"Predicted labels: {predicted_labels}"
                    )
        predicted_labels.clear()
    if update:
        strip_optimizer(weights)  # update model (to fix SourceChangeWarning)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'yolov5s.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default=ROOT / 'data/images', help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--data', type=str, default=ROOT / 'data/coco128.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[416], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default=ROOT / 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(vars(opt))
    return opt


def main(opt):
    check_requirements(exclude=('tensorboard', 'thop'))
    run(**vars(opt))


if __name__ == "__main__":
    try:
        opt = parse_opt()
        main(opt)
    except KeyboardInterrupt as e:
        handle.ChangeDutyCycle(7)
        time.sleep(0.5)
        handle.ChangeDutyCycle(0)
        handle.stop()
        GPIO.cleanup()

        pi.set_PWM_dutycycle(STEP,0) # off Pulse width modulation
        pi.stop()
        pass
