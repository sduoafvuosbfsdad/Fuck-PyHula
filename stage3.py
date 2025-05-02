import pyhula
import time

from shihao.modules.hula_video import hula_video
from shihao.modules.tflite_detector import tflite_detector

import cv2
import numpy as np
tries = 0
successes = 0
#HorizontalMovementAfterTakeoffToGetToPositionToDetectBallAndCarryOutMLBeforeRAMMINGBallForward
horizontalmove = 30
#Movement to move drone forward to a distance where it can push ball with air value
frontbackmove = 80
#Forward movement to push all balls out of the cues
rammingmove = 200




def gothere(height):
    current=uapi.get_plane_distance()
    if int(height)>current:
        uapi.single_fly_up(height-current)
    elif current>int(height):
        uapi.single_fly_down(current-height)






def blue_hunter(frame):
    # Define HSV range for blue color
    Lblue = np.array([100, 150, 70])
    Ublue = np.array([140, 255, 255])
   
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   
    # Create a mask for blue color
    mask_blue = cv2.inRange(hsv, Lblue, Ublue)
   
    # Find contours in the mask
    contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   
    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        center_x = x + w // 2
        center_y = y + h // 2
       
        # Draw the detected contour and center
        cv2.drawContours(frame, [largest_contour], -1, (0, 0, 255), 3)  # Blue color
        cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)  # Green dot at center
       
        return True, center_x, center_y ,frame
    else:
        return False, None, None, frame




def red_hunter(frame):
    # Define HSV range for red color (Note: red spans both ends of HSV spectrum)
    Lred1 = np.array([0, 120, 70])
    Ured1 = np.array([10, 255, 255])
    Lred2 = np.array([170, 120, 70])
    Ured2 = np.array([180, 255, 255])
   
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   
    # Create masks for red color ranges
    mask_red1 = cv2.inRange(hsv, Lred1, Ured1)
    mask_red2 = cv2.inRange(hsv, Lred2, Ured2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
   
    # Find contours in the mask
    contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   
    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        center_x = x + w // 2
        center_y = y + h // 2
       
        # Draw the detected contour and center
        cv2.drawContours(frame, [largest_contour], -1, (0, 0, 255), 3)  # Red color
        cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)  # Green dot at center
       
        return True, center_x, center_y, frame
    else:
        return False, None, None, frame
   


uapi = pyhula.UserApi()




if not uapi.connect():
    print('connect error')
else:
    try:    
        print('success')
        video = hula_video(hula_api=uapi,display=True)
        #detector = tflite_detector(model="model.tflite",label="label.txt")
        video.video_mode_on()
        time.sleep(3)
        uapi.single_fly_takeoff()
        time.sleep(2)
        uapi.single_fly_right(horizontalmove)
        tries = 0
        successes = 0
        while tries < 500 and successes < 10:
            frame = video.get_video()
            request = red_hunter(frame)
            if request[0] == True:
                cv2.putText(frame, 'red ball', (request[1], request[2]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.imshow("window", frame)
                cv2.waitKey(1)
                time.sleep(0.3)
                successes+=1
                continue
            elif request[0]==False:
                cv2.putText(frame, 'NONE', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.imshow("window", frame)
                cv2.waitKey(1)
                time.sleep(0.3)
                tries+=1
                continue
        time.sleep(3)
        uapi.single_fly_forward(frontbackmove)
        time.sleep(4)
        uapi.single_fly_back(frontbackmove)
        time.sleep(1)
        uapi.single_fly_left(horizontalmove*2)
        tries = 0
        successes = 0
        while tries < 500 and successes < 10:
            frame = video.get_video()
            request = blue_hunter(frame)
            if request[0] == True:
                cv2.putText(frame, 'blue ball', (request[1], request[2]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.imshow("window", frame)
                cv2.waitKey(1)
                time.sleep(0.3)
                successes+=1
                continue
            elif request[0]==False:
                cv2.putText(frame, 'NONE', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.imshow("window", frame)
                cv2.waitKey(1)
                time.sleep(0.3)
                tries+=1
                continue
        time.sleep(3)
        uapi.single_fly_forward(frontbackmove)
        time.sleep(4)
        uapi.single_fly_back(frontbackmove)
        time.sleep(1)
        uapi.single_fly_right(horizontalmove)
        time.sleep(1)
        uapi.single_fly_forward(rammingmove)
        uapi.single_fly_touchdown()
        cv2.destroyAllWindows()
        video.close()
   
    except KeyboardInterrupt: #FAILSAFE
        uapi.single_fly_touchdown()
        cv2.destroyAllWindows()
        video.close()
















