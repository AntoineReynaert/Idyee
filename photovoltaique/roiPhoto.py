#!/usr/bin/env python3
from pathlib import Path
import os
import sys
sys.path.append(str(Path(os.getcwd()).parent)+"\\bornes_utiles")
from PVGISapi import *
from autoConso import *
import coord_gps

# Cette fonction ourve un fichier et json et le renvoie sous forme de dictionnaire
def openJson(file):
    if isinstance(file,str):
        with open(file) as json_data:
            data_dict = json.load(json_data)
            return data_dict
    else:
        return file
        
def production(donneesClient):
    result = dict()
    pWc = calculCrete(donneesClient["Surface toit"],donneesClient["Conso annuel"])
    coordonnees = coord_gps.get_coord(donneesClient["Numero"] + donneesClient["Nom de rue"] + donneesClient["Code postal"] + donneesClient["Ville"])
    production = getProduction(coordonnees[0],coordonnees[1],donneesClient["Inclinaison"],donneesClient["Orientation"],pWc)
    result["MonthlyProd"] = getMonthlyProd(production)
    result["AnnualProd"] = getAnnualProd(production)
    result["pWc"] = pWc
    return result
    
def prixTot(coutJson,pWc):
        nbrPanneau = puissancePhoto / (pWc *1000)
        Prix = nbrPanneau * prixPanneau
        Prix += (nbrPanneau//2) * prixOnduleur
        Prix += kitIntegration + Pose + raccordement + etude
        
def aides(aideJson,pWc):
    if pWc <= 3:
        aideTot = aideJson["inf3"]*pWc
    else:
        aideTot = aideJson["sup3"]*pWc
    return aideTot
    
def roi(fichier_client,fichier_aide,fichier_prix,puissancePhoto, pWc):
    donneesClient = openJson(fichier_client)
    aideJson = openJson(fichier_aide)
    prodDict = production(donneesClient)
    gainAnnuel = prixConso(prodDict["AnnualProd"])
    aideTot = aides(aideJson,pWc)
    coutTot = 10000 - aideTot
    ROI = gainAnnuel/coutTot
    return ROI  

        
    

print(roi("donnees_client_example.json","fichier_aide.json","prix_panneau.json",200,7))