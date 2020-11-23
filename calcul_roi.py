#!/usr/bin/env python3

import json
from read_aides import openCsv

def openJson(file):
	with open(file) as json_data:
	    data_dict = json.load(json_data)
	    return data_dict

def afficher_donnes(dic):
	for titre_donnee, donnee in dic.items():
		print(" {:30} {} ".format(titre_donnee,donnee))


def main():
	file='donnees_client_example.json'
	aides = "aides_filtrees_nom.csv"

	donnees_client = openJson(file)
	afficher_donnes(donnees_client)

	print("\t ROI")

	roi = calcul_roi(donnees_client, aides)
	afficher_donnes(roi)

def calcul_aides(aides, voitures):
	total = 1000 * voitures
	return max(total,5000) 

def calcul_roi(donnees_client, aides_fichier):

	aides = openCsv(aides_fichier)
	borne_a_proximite=True
	prix_voiture_elec = 10000

	if borne_a_proximite:
		voitures=donnees_client["Flotte"]["voitures_thermiques"]
		cout = voitures*prix_voiture_elec - calcul_aides(aides, voitures)
		while cout > donnees_client["Capacite investissement"]:
			voitures = voitures - 1
			aides = calcul_aides(aides, voitures)
			cout = voitures  * prix_voiture_elec - aides

	return (
		{
			"voitures" : voitures, 
			"cout_total" : voitures * prix_voiture_elec,
			"aides" : aides,
			"cout_final" : cout,
			"flotte_final" : {
				"voitures_thermique" : donnees_client["Flotte"]["voitures_thermiques"] - voitures,
    			"voitures_electriques": donnees_client["Flotte"]["voitures_electriques"] + voitures
    		}
    	})





if __name__ == "__main__":
    main()