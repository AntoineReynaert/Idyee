#!/usr/bin/env python3
import sys
import os

sys.path.append(os.getcwd()+"\\bornes_utiles")
sys.path.append(os.getcwd()+"\\bornes_rentabilite")

from bornes_rentabilite.calcul_roi_v2 import *
from bornes_rentabilite.pertinence import *
import json


"""
Fonction principale permettant de calculer la pertinence des solutions bas carbone.
"""

def main():
    dict_flotte = calcul_solution_flotte("donnees_client_example.json")
    solution_flotte = rangSolution(dict_flotte["ROI annuel sur l'entretien"]+ \
    dict_flotte["ROI annuel sur les km"],dict_flotte["Cout final"],dict_flotte["Baisse emission co2"])
    dict_flotte["Rang"] = solution_flotte.getRang()
    return dict_flotte
    
print(main())