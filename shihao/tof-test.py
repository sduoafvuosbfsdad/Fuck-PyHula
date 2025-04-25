from client import Client

client = Client(False)

while True:
    print(client.get_plane_distance())
    input()