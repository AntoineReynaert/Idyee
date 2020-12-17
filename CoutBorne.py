#!/usr/bin/env python3
from math import *
from calcul_roi_v2 import *
import datetime

#Coût moyen du raccordement d'une borne de 22kw Wallbox
def getPrixRaccordement():
    return 2000

#Coût moyen du d'une borne de 22kw Wallbox    
def getPrixBorne():
    return 1500

"""
Fonction permettant de calculer l'aide Advenir en prenant en hypothèse que 
le client souhaite loué sa borne au public
"""
def aideAdvenir(prixRaccordement,prixBorne):
    anneeCourante = datetime.datetime.now().year
    if anneeCourante == 2020 or anneeCourante == 2021:
        aide = 0.6*(prixRaccordement+prixBorne)
    elif anneeCourante == 2022 or anneeCourante == 2023:
        aide = 0.2*(prixRaccordement+prixBorne)
    if aide > 2700:
        aide = 2700
    return aide
    
    
"""
Fonction calculant le coût de construction d'une borne en s'appuyant sur les données
des Wallbox 22kw.
Prends en entrée :  - aidesBornes = list() des aides
                   - prixRaccordement = int() prix du raccordement d'une borne au
                     réseau électrique
                   - prixBorne = int() prix d'une borne électrique 
"""
def CoutConstructionBorne(aidesBornes,prixRaccordement,prixBorne):
    return prixRaccordement+prixBorne-sum(aidesBornes)


"""
Nombre de bornes à construire en fonction du nombre de nouveaux véhicules électriques
Prends en entrée: - nb_voiture = int()
"""
def nombreBorne(nb_voiture):
    return ceil(nb_voiture/2)
  
def resultCoutBorne(nb_voiture):
    return nombreBorne(nb_voiture)*CoutConstructionBorne([aideAdvenir(getPrixBorne(),getPrixRaccordement())],getPrixRaccordement(),getPrixBorne())

if __name__ == "__main__":
	print(CoutConstructionBorne([aideAdvenir(getPrixBorne(),getPrixRaccordement())],getPrixRaccordement(),getPrixBorne()))



    
    