#!/usr/bin/env python3

import requests, json
import urllib.parse
import sys
from sys import argv

def get_coord(adresse):
    api_url = "https://api-adresse.data.gouv.fr/search/?q="
    r = requests.get(api_url + urllib.parse.quote(adresse)).json()
    if not r["features"]:
        return []
    else:
        return (r["features"][0]["geometry"]["coordinates"])
        
def get_adr(coord):
    api_url="https://api-adresse.data.gouv.fr/reverse/?"
    query='lon='+str(coord[0])+'&lat='+str(coord[1])
    
    r = requests.get(api_url + query).json()
    return r["features"][0]["properties"]["label"]

def get_city(coord):
    api_url="https://api-adresse.data.gouv.fr/reverse/?"
    query='lon='+str(coord[0])+'&lat='+str(coord[1])
    r = requests.get(api_url + query).json()
    if not r["features"]:
        return ""
    else:
        return r["features"][0]["properties"]["postcode"]


