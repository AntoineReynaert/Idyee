#!/usr/bin/env python3

### Class Point

"""
Classe permettant d'initialiser une structure de point. L'objet possède un attribut X et Y.
Arguments:
    - float x: longitude d'une coordonnée
    - float y: latitude d'une coordonnée

Méthodes:
    - getX(self): permet de récupérer la longitude du point
    - getY(self): permet de récupérer la latitude du point
    - setX(self,x): permet de modifier la longitude du point par la nouvelle valeur x
    - setY(self,y): permet de modifier la latitude du point par la nouvelle valeur y
    - distancePoint(self,pointB): calcule la distance entre le point self et le pointB. Retourne
        un résultat en km.
"""

class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        
    def __str__(self):
        return "(" + str(self.getX()) + "," + str(self.getY()) + ")"

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y

    def distancePoint(self,pointB):
        selfLong = radians(self.getX())
        selfLat = radians(self.getY())
        pointBLong = radians(pointB.getX())
        pointBLat = radians(pointB.getY())
        return 6371.01 * acos(sin(selfLat)*sin(pointBLat) + cos(selfLat)*cos(pointBLat)*cos(selfLong - pointBLong))