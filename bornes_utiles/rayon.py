import math
from coord_gps import get_adr


"""
L'objectif de cette fonction est de créer un cercle de rayon 1 km autour d'un point gps donné
Ensuite, la fonction retournera les coordonnées gps d'un carré se basant sur les différents points
constituant le cercle. (Le carré englobera notre cercle)


"""
def findpoints(lon, lat):
    radius = 1
    N = 360 

    # generate points
    
    #liste des latitudes
    pointlat=[]
    #liste des longitudes
    pointlon=[]
    for k in range(N):
        angle = math.pi*2*k/N
        dx = radius*math.cos(angle)
        dy = radius*math.sin(angle)


        pointlat.append(lat + (180/math.pi)*(dy/6371)) #Earth Radius
        pointlon.append(lon + (180/math.pi)*(dx/6371)/math.cos(lon*math.pi/180)) #Earth Radius
    #retourne les coordonnées d'un carré
    return [min(pointlat),max(pointlat),min(pointlon),max(pointlon)]

