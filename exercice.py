#!/usr/bin/env python3

import json
from read_aides import openCsv

def openJson(file):
	with open(file) as json_data:
	    data_dict = json.load(json_data)
	    return data_dict

def afficher_dico(dic):
	for cle, valeur in dic.items():
		print(" {:30} {} ".format(cle,valeur))

def main():
	fichier='donnees_client_example.json'
	donnees_client = openJson(fichier)

	afficher_dico(donnees_client)

#1  Afficher la capcite d'investissment la societe
#2 Afficher le nombre de voitures thermiques
#3 Calculer le nombre de voitures electriques que peut acheter l'entrerpise avec sa capacite d'investissment si une voiture electrique coute 10 000€ 

if __name__ == "__main__":
    main()
