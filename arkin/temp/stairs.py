from src.tflite_detector import tflite_detector
import pyhula
import time
from src.hula_video import hula_video
import cv2
import numpy as np


uapi = pyhula.UserApi()
detector = tflite_detector('src//model5.tflite', 'src//label.txt')


# Create a global flag
stop_flag = False
ok=False

def centreCross(frame, color=(0, 0, 255), size=20, thickness=2):
    h, w, _ = frame.shape
    global center_x
    global center_y
    center_x, center_y = w // 2, h // 2
    cv2.line(frame, (center_x - size, center_y), (center_x + size, center_y), color, thickness)
    cv2.line(frame, (center_x, center_y - size), (center_x, center_y + size), color, thickness)



def dih():
    global video
    global stop_flag
    global object_found
    ok=False
    video = hula_video(hula_api=uapi)
    video.video_mode_on()
    time.sleep(0.5)

    try:
        for i in range(30): #check how long you want to run it for
            frame = video.get_video()
            object_found, processed_frame = detector.detect(frame)
            if not object_found is None:
                print(object_found)
                detector.draw_center_cross(processed_frame, object_found['x'], object_found['y'])
                centreCross(processed_frame)
                cv2.imshow("VIDEO", processed_frame)

                    
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                stop_flag = True
                break

            else:
                centreCross(processed_frame)
                cv2.imshow("VIDEO", processed_frame)
            
    finally:
        # Clean up
        stop_flag=True
        cv2.destroyAllWindows()
        video.stoprecording()
        video.close()


if not uapi.connect('192.168.100.138'):
    print('NOT FUCKING CONNECTED')
else:
    print('CONNECTED')
    try:
        #ADD MOVEMENT HERE
        uapi.single_fly_takeoff()
        time.sleep(0.1)

        print('left DONE')
        time.sleep(0.1)
        dih()

        time.sleep(1)
        uapi.single_fly_touchdown()
        
    except KeyboardInterrupt:
        print("KeyboardInterrupt received, stopping...")
        stop_flag = True
        uapi.single_fly_touchdown()
