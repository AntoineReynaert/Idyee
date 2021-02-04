#!/usr/bin/env python3
from pathlib import Path
import os
import sys
sys.path.append(str(Path(os.getcwd()).parent)+"\\bornes_utiles")
from PVGISapi import *
from autoConso import *
from trpPhoto import *
import coord_gps
from math import *

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
    
def prixTot(prixJson,pWc):
        nbrPanneau = ceil((pWc *1000)/265)
        nbrOndulateur = ceil(nbrPanneau/2)
        Prix = nbrPanneau * prixJson["Panneaux_solaire"]
        Prix += prixJson["Structure kit de pose"]
        Prix += prixJson["Passerelle de communication"]
        Prix += prixJson["Pose toiture"]
        Prix += prixJson["Etude"]
        if pWc > 6:
            Prix += nbrOndulateur * prixJson["Ondulateur triphase"]
            Prix += nbrOndulateur * prixJson["Cable ondulateur triphase"]
            Prix += prixJson["Coffret de protection PV AC Tri"]
            Prix += prixJson["PoseElectSup6"]
        else:
            Prix += nbrOndulateur * prixJson["Ondulateur mono"]
            Prix += nbrOndulateur * prixJson["Cable ondulateur mono"]
            Prix += prixJson["Coffret de protection PV AC Mono"]
            Prix += prixJson["PoseElectInf6"]
        Prix += prixJson["TVA"]*Prix
        return Prix
            
        
def aides(aideJson,pWc):
    if pWc <= 3:
        aideTot = aideJson["inf3"]*pWc
    else:
        aideTot = aideJson["sup3"]*pWc
    return aideTot
    
def resultRoi_Trp(fichier_client,fichier_aide,fichier_prix):
    donneesClient = openJson(fichier_client)
    aideJson = openJson(fichier_aide)
    prixJson = openJson(fichier_prix)
    prodDict = production(donneesClient)
    gainAnnuel = prixConso(prodDict["AnnualProd"])
    aideTot = aides(aideJson,prodDict["pWc"])
    coutTot = prixTot(prixJson,prodDict["pWc"]) - aideTot
    ROI = gainAnnuel/coutTot
    gainCO2 = gain_carbone(prodDict["MonthlyProd"],getConsommationParMois(prodDict["AnnualProd"]),dict(),donneesClient["Conso annuel"],"","")
    return {
    "Cout total": coutTot,
    "Aides": aideTot,
    "Gain Annuel": gainAnnuel,
    "CO2 économisé": aideTot
    }