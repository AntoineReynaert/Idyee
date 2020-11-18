
#determiner à partir de coordonnées GPS si un point (lieu)
#se trouve dans une région donnée


import json
from shapely.geometry import shape, GeometryCollection, Point,Polygon,MultiPolygon



def in_region(coord):
#Charger les contours géographiques des régions
    with open('contours-geographiques.json', 'r') as f:
        js = json.load(f)


    point = Point(coord[0], coord[1])

    for i in range(len(js)):

#Le fichier contient plusieurs types de formes géometriques pour chaque région
# #Cas polygon    
        if js[i]['fields']['geo_shape']["type"]=="Polygon":

            polygon = Polygon(js[i]['fields']['geo_shape']['coordinates'][0])

            if polygon.contains(point):
                return (js[i]['fields']['region_min'])
#Cas multipolygon
        if js[i]['fields']['geo_shape']["type"]=="MultiPolygon":
            aux=js[i]['fields']['geo_shape']['coordinates']
            aux=tuple(Polygon(x[0]) for x in aux)
            multipolygon = MultiPolygon(aux)

            if multipolygon.contains(point):
                return ( js[i]['fields']['region_min'])
        

