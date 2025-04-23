from client import Client

client = Client(False)
client.single_fly_takeoff()
client.single_fly_forward(50)
client.single_fly_touchdown()