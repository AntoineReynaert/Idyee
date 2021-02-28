#!/usr/bin/env python3

import requests, json

"""
Fonction permettant de récupérer un fichier JSON provenant de l'API européenne PVGIS.
La documentation est disponible suivant ce lien: https://ec.europa.eu/jrc/en/PVGIS/docs/noninteractive
La requête utilisée concerne la partie "Grid-connected & Tracking PV systems"
"""
def getProduction(latitude,longitude,inclinaison,orientation,puissanceCrete):
    url = "https://re.jrc.ec.europa.eu/api/PVcalc?lat=" + str(latitude) + "&lon=" + str(longitude) + "&peakpower="+str(puissanceCrete) + "&loss=15&outputformat=json&angle=" + str(inclinaison) + "&aspect=" + str(orientation)
    r = requests.get(url).json()
    return r

"""
À partir du JSON extrait de PVGIS, on récupère la production calculée par mois.
La fonction retourne un dictionnaire possédant comme clé un token allant de 1 à 12 
représentant le mois, et la valeur représente la production estimée ce même mois.
"""
def getMonthlyProd(jsonPVGIS):
    result = dict()
    for elem in jsonPVGIS["outputs"]["monthly"]["fixed"]:
        result[elem["month"]]=elem["E_m"]
    return result

"""
À partir du JSON extrait de PVGIS, on récupère la production calculée par an
"""    
def getAnnualProd(jsonPVGIS):
    return jsonPVGIS["outputs"]["totals"]["fixed"]["E_y"]