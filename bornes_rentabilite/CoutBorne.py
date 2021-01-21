#!/usr/bin/env python3
import json
from math import *
import datetime

"""
Cette fonction ourve un fichier et json et le renvoie sous forme de dictionnaire
"""
def openJson(file):
    with open(file) as json_data:
        data_dict = json.load(json_data)
        return data_dict

"""
Retoune la somme des aides pour la construction des bornes.
"""
def getAidesBornes(dict):
    return sum(dict["aides_bornes"])
  

"""
Fonction calculant le coût de construction d'une borne en s'appuyant sur les données
des Wallbox 22kw.
Prends en entrée :  - aidesBornes = list() des aides
                   - prixRaccordement = int() prix du raccordement d'une borne au
                     réseau électrique
                   - prixBorne = int() prix d'une borne électrique 
"""
def CoutConstructionBorne(dict):
    aides = sum(dict["aides_bornes"])
    prix = dict["prix_raccordement"] + dict["prix_borne"]
    return prix - aides


"""
Nombre de bornes à construire en fonction du nombre de nouveaux véhicules électriques
Prends en entrée: - nb_voiture = int()
"""
def nombreBorne(nb_voiture):
    return ceil(nb_voiture/2)
  
"""
Coût total de la construction des bornes
"""
def resultCoutBorne(nb_voiture,dict):
    return nombreBorne(nb_voiture)*CoutConstructionBorne(dict)


if __name__ == "__main__":
	print(CoutConstructionBorne(openJson("construction_borne.json")))

