import numpy as np
import threading
from client import Client, WorkerThread, PostProcessors

import cv2
from PIL import Image
from matplotlib import pyplot as plt

client = Client()

#TOF threading
tof_thread = WorkerThread(client.get_plane_distance)

#Camera Feed
def show_image():
    while True:
        frame, results = client.get_frame(PostProcessors.Google_IMDA)
        cv2.imshow('niga', frame)
        cv2.waitKey(1)
        imda = results[PostProcessors.Google_IMDA]
        if imda:
            if imda['label'] == 'IMDA' and imda['score'] > 0.5:
                break
    image = Image.fromarray(frame)
    image.show()

video_thread = threading.Thread(target=show_image)

client.single_fly_takeoff()
tof_thread.start()
client.single_fly_forward(120)#Change this value accordingly
video_thread.start()
heights = tof_thread.stop()
client.single_fly_touchdown()

plt.scatter(range(0, len(heights)), heights)
for i in range(2, len(heights), 3):
    gradient = (heights[i-2]-heights[i])/2
    if gradient > 10 or gradient < -10:
        print(f'Height of the first step{heights[i-2]-heights[i]}')
        break
plt.show()
