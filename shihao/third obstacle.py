import client
from client import PostProcessors
import cv2
import threading

from PIL import Image

client = client.Client()

client.single_fly_takeoff()
client.single_fly_forward(120)
client.single_fly_right(20)

for i in range(0, 900):
    frame, results = client.get_frame(PostProcessors.ContourRed)
    cv2.imshow('niga', frame)
    cv2.waitKey(1)

client.single_fly_left(40)
for i in range(0, 900):
    frame, results = client.get_frame(PostProcessors.ContourBlue)
    cv2.imshow('niga', frame)
    cv2.waitKey(1)

client.single_fly_right(20)
client.single_fly_forward(20)
client.single_fly_down(
    client.get_plane_distance()-20
)

client.single_fly_forward(120)
client.single_fly_up(80)
client.single_fly_back(120)
client.single_fly_right(20)
client.single_fly_down(
    client.get_plane_distance()-20
)
client.single_fly_forward(120)
client.single_fly_up(80)
client.single_fly_back(120)


client.single_fly_left(40)
client.single_fly_down(
    client.get_plane_distance()-20
)
client.single_fly_forward(120)

client.single_fly_forward(40)
client.single_fly_touchdown()
