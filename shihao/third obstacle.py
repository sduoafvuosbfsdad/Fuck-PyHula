import client
from client import PostProcessors
import cv2
import threading

from PIL import Image

client = client.Client()

client.single_fly_takeoff()

while True:
    frame, results = client.get_frame(PostProcessors.ContourBlue)
    cv2.imshow('niga', frame)
    cv2.waitKey(1)
    if results is not (None, None):
        break
image = Image.fromarray(frame)
image.show()
while True:
    frame, results = client.get_frame(PostProcessors.ContourRed)
    cv2.imshow('niga', frame)
    cv2.waitKey(1)

    if results is not (None, None):
        break
image = Image.fromarray(frame)
image.show()
