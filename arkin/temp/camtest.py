import pyhula
import time
uapi=pyhula.UserApi()

uapi.connect('192.168.100.138')
print('connect ok')

def moveCoordinate(x,y,z):
    pos=uapi.get_coordinate()
    x=x-int(pos[0])
    y=y-int(pos[1])
    z=z-int(pos[2])
    if x>0:
        uapi.single_fly_right(x)
    elif x<0:
        x=abs(x)
        uapi.single_fly_left(x)
    

    if y>0:
        uapi.single_fly_forward(y)
    elif y<0:
        y=abs(y)
        uapi.single_fly_back(y)
    

    if z>0:
        uapi.single_fly_up(z)
    elif z<0:
        z=abs(z)
        uapi.single_fly_down(z)

    
print(uapi.get_coordinate())
uapi.single_fly_takeoff()
print(uapi.get_coordinate())
print(uapi.get_plane_distance())
uapi.single_fly_back(45,0)
print(uapi.get_coordinate())
moveCoordinate(0,0,100)
print(uapi.get_coordinate())
moveCoordinate(0,0,100)
print(uapi.get_coordinate())
moveCoordinate(0,30,100)
print(uapi.get_coordinate())
uapi.single_fly_touchdown()
uapi.get_coordinate()