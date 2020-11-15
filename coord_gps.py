#!/usr/bin/env python3

import requests, json
import urllib.parse
import sys
from sys import argv

def get_coord(adresse):
    api_url = "https://api-adresse.data.gouv.fr/search/?q="
    r = requests.get(api_url + urllib.parse.quote(adresse)).json()
    if not r["features"]:
        print("Nous n'arrivons pas à trouver l'adresse que vous avez renseignée")
        print("Veuillez saisir une adresse correcte de la forme : Numéro,Nom de rue,Code Postal,Ville")
    else:

        return (r["features"][0]["geometry"]["coordinates"])



