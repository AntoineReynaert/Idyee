#!/usr/bin/env python3
import sys
import os
import json

try:
    sys.path.append(os.getcwd()+"/bornes_utiles")
    sys.path.append(os.getcwd()+"/bornes_rentabilite")
    sys.path.append(os.getcwd()+"/photovoltaique")
except (ModuleNotFoundError,ImportError):
    sys.path.append(os.getcwd()+"\\bornes_utiles")
    sys.path.append(os.getcwd()+"\\bornes_rentabilite")
    sys.path.append(os.getcwd()+"\\photovoltaique")

from bornes_rentabilite.calcul_roi_v2 import *
from bornes_rentabilite.pertinence import *
from photovoltaique.roiPhoto import *
import json

"""
Fonction permettant d'obtenir le rang d'une solution
"""
def getclerang(obj):
    return obj["Rang"]

"""
Fonction principale permettant de calculer la pertinence des solutions bas carbone.
On crée pour chaque use case une solution avec les paramètres du client et on
l'ajoute à une liste.
Pour finir on trie la liste en fonction du rang.
"""

def bestSolutions(donnees_client,donnees_aide,donnees_mobilite,donnees_autoconso):
    ranking = list()
    #Photovoltaïque (visibilité = 2)
    dict_flotte = calcul_solution_flotte(donnees_client, donnees_aide, donnees_mobilite)
    solution_flotte = rangSolution(dict_flotte["ROI annuel sur l'entretien"]+ \
    dict_flotte["ROI annuel sur les km"],dict_flotte["Cout final"],dict_flotte["Baisse emission co2"],2)
    dict_flotte["Rang"] = solution_flotte.getRang()
    ranking.append(dict_flotte)
    
    #Autoconsommation (visibilité = 1)
    dict_photo = resultRoi_Trp(donnees_client,donnees_aide,donnees_autoconso )
    solution_photo = rangSolution(dict_photo["Gain Annuel"], dict_photo["Cout total"],dict_photo["CO2 economise"],1)
    dict_photo["Rang"] = solution_photo.getRang()
    ranking.append(dict_photo)
    
    #Trie en fonction du rang
    ranking.sort(key = getclerang, reverse = True)
    return json.dumps(ranking)
    
    
print(bestSolutions("donnees_client_example.json", "fichier_aide.json", "prix_achat_entretien_km.json","prix_panneaux.json" ))