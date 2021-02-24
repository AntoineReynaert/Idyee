#!/usr/bin/env python3

import requests, json

def getProduction(latitude,longitude,inclinaison,orientation,puissanceCrete):
    url = "https://re.jrc.ec.europa.eu/api/PVcalc?lat=" + str(latitude) + "&lon=" + str(longitude) + "&peakpower="+str(puissanceCrete) + "&loss=15&outputformat=json&angle=" + str(inclinaison) + "&aspect=" + str(orientation)
    r = requests.get(url).json()
    return r
    
def getMonthlyProd(jsonPVGIS):
    result = dict()
    for elem in jsonPVGIS["outputs"]["monthly"]["fixed"]:
        result[elem["month"]]=elem["E_m"]
    return result
    
def getAnnualProd(jsonPVGIS):
    return jsonPVGIS["outputs"]["totals"]["fixed"]["E_y"]