#!/usr/bin/env python3

import requests, json

def getProduction(latitude,longitude,inclinaison,orientation):
    url = "https://re.jrc.ec.europa.eu/api/PVcalc?lat=" + str(latitude) + "&lon=" + str(longitude) + "&peakpower=6&loss=16&outputformat=json&angle=" + str(inclinaison) + "&aspect=" + str(orientation)
    r = requests.get(url).json()
    return r
    
def getMonthlyProd(jsonPVGIS):
    result = dict()
    for elem in jsonPVGIS["outputs"]["monthly"]["fixed"]:
        result[elem["month"]]=elem["E_m"]
    return result
    
def getAnnualProd(jsonPVGIS):
    return jsonPVGIS["outputs"]["totals"]["fixed"]["E_m"]

jsonProd = getProduction(45,8,20,-45) 
print(getMonthlyProd(jsonProd))
print(getAnnualProd(jsonProd))