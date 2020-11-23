from ElecTerminals import openCsv,terminalsCoordinates

from coord_gps import *
from Classes import Point as pt
import numpy
import math
from math import radians
from math import acos
from math import cos
from math import sin
from rayon import findpoints

#creation d'un dictionnaire de bornes
bornes=dict()
for idx ,terminal in enumerate(terminalsCoordinates(openCsv("bornes-irve-20200920.csv"))):
    
    bornes[terminal]=idx



"""
La fonction suivante prend comme input une adresse texte et la convertit en coordonnées gps.
Ensuite, ces coordonnées GPS sont utilisées pour tracer un carré de cote 1 km
LA fonction ensuite parcourt toutes les bornes que nous utilisons, et verifient celle qui sont présentes dans notre carré.
Si une borne se trouve dans le carré, nous calculons la distance et nous retenons que la borne avec une ditance inférieure
ou égale à 1km de notre adresse de départ.
"""

def a_proximite(adr):
    k=0

    #Convertir l'adresse en coordonnées
    adrCoord=get_coord(adr)
    if not adrCoord:
        print("Nous n'arrivons pas à trouver l'adresse que vous avez renseignée")
        print("Veuillez saisir une adresse correcte de la forme : Numéro,Nom de rue,Code Postal,Ville")
    else:
    #récupere les coordonnées constituant notre carré
        aux=findpoints(adrCoord[0],adrCoord[1])
        proche=[]
        #parcourir les bornes:
        for cle,valeur in bornes.items():
            #verifier que la borne se trouve dans le carré
            if float(cle.getX())<=aux[3] and float(cle.getX())>=aux[2] and float(cle.getY())<=aux[1] and float(cle.getY())>=aux[0]:
                #calculer la distance
                distance=pt(adrCoord[0],adrCoord[1]).distancePoint(pt(float(cle.getX()),float(cle.getY())))
                #retenir que les bornes avec une distance inférieure ou égale à 1km
                if distance <=1:
                    proche.append([get_adr([float(cle.getX()),float(cle.getY())]), distance])
        if not proche:
            print("Aucune borne n'a été trouvé à proximité")
        else:
            return proche                    

         


        
def main():
    adresse=input("Veuillez saisir une adresse")
    calcul=a_proximite(adresse)
    if calcul:
        for element in calcul:
            print(element[0], " ", element[1])

main()

