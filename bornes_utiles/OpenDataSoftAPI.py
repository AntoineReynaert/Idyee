#!/usr/bin/env python3

import requests, json

"""
Retourne un fichier JSON utilisant l'API d'opendatasoft sur le fichier consolidé 
des bornes de recharge pour véhicules électriques (IRVE).
L'url défini permet d'avoir accès aux bornes à moins de 1km des coordonnées latitude longitude  données en argument.
"""
def getBornes(latitude,longitude):
    url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve&q=&facet=n_enseigne&facet=nbre_pdc&facet=puiss_max&facet=accessibilite&facet=nom_epci&facet=commune&facet=nom_reg&facet=nom_dep&geofilter.distance=" + str(latitude) + "%2C" + str(longitude) + "%2C1000"
    r = requests.get(url).json()
    return r["records"]


"""
À partir du JSON retourner par la fonction getBornes(latitude,longitude), retourne
une liste de string représentant les bornes à proximité (inférieur à 1km) de l'adresse du client.
"""
def afficherBornes(jsonBornes):
    rst = list()
    for element in jsonBornes:
        rst.append(str(element["fields"]["ad_station"]) + " | " + str(element["fields"]["puiss_max"]) + " kW" + " | " + str(element["fields"]["coordonnees"]))

    