import numpy as np
import threading
from client import Client, WorkerThread, PostProcessors

import cv2
from PIL import Image
from matplotlib import pyplot as plt

client = Client()

def show_image():
    while True:
        frame, results = client.get_frame(PostProcessors.Google_IMDA)
        cv2.imshow('niga', frame)
        cv2.waitKey(1)
        imda = results[PostProcessors.Google_IMDA]
        if imda:
            if imda['label'] == 'Google' and imda['score'] > 0.5:
                pass
    image = Image.fromarray(frame)
    image.show()

video_thread = threading.Thread(target=show_image)

client.single_fly_takeoff()
#Adjust the height
height = int(client.get_plane_distance()/2)
client.single_fly_down(height)
client.single_fly_forward(10)
client.single_fly_radius_around(70)
client.single_fly_up(height-10)
video_thread.start()
client.single_fly_radius_around(70)

client.single_fly_up(60)
client.single_fly_forward(20)
client.single_fly_Qrcode_align(0, 0)
client.single_fly_touchdown()

