#!/usr/bin/env python3
from calcul_roi_v2 import *
from pertinence import *
import json

"""
"""

def main():
    dict_flotte = calcul_solution_flotte("donnees_client_example.json")
    print(dict_flotte)
    solution_flotte = rangSolution(dict_flotte["ROI annuel sur l'entretien"]+ \
    dict_flotte["ROI annuel sur les km"],dict_flotte["Cout final"],dict_flotte["Baisse emission co2"])
    print(solution_flotte.getTRP())
    print(solution_flotte.getRang())
    
main()