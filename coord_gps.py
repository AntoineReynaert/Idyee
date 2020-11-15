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

def main():
    numero=input("Veuillez saisir le numéro: ")
    nom_rue=input("Veuillez saisir le nom de la rue/voie/avenue: ")
    code_postal=input("Veuillez saisir le code postal: ")
    ville=input("Veuillez saisir la ville: ")
    
    adr= numero +','+nom_rue+','+code_postal+','+ville
    print(adr)
    print(get_coord(adr))
        

main()

