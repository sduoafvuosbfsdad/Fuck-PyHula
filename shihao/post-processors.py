import cv2
from client import Client, PostProcessors

import time

client = Client()

_post_processors = [PostProcessors.Google_IMDA]

while True:
    start = time.time()
    for i in range(0, 10):
        cv2.imshow(
            'black',
            client.get_frame(PostProcessors.ContourRed)[0]
        )
        cv2.waitKey(1)

    frame = client.get_frame()[0]
    print(f'[FPS] {10/(time.time()-start)}fps')
