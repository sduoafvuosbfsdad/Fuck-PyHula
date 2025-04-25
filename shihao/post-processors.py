import cv2
from client import Client, PostProcessors

client = Client()

_post_processors = [PostProcessors.Google_IMDA]

while True:
    cv2.imshow(
        'black',
        client.get_frame(*_post_processors)[0]
    )
    cv2.waitKey(1)