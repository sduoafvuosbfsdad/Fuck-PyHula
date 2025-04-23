import threading
from client import Client, WorkerThread

client = Client(False)

#TOF threading
tof_thread = WorkerThread(client.get_plane_distance)
tof_thread.start()

client.single_fly_takeoff()
client.single_fly_forward(100)
client.single_fly_touchdown()

print(tof_thread.stop())



