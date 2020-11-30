#!/usr/bin/env python3

import json
from read_aides import openCsv

import Calcul

# # source : https://www.kelwatt.fr/guide/conso/voiture-electrique
# prix_km_thermique = 0.075
# prix_km_elec = 0.025
# # source https://lemobiliste.com/combien-coute-une-borne-de-recharge/
# prix_borne = 1500
# # source https://www.renault.fr/vehicules-electriques/zoe.html
# prix_voiture_elec = 32300
# # source : https://professionnels.renault.fr/vehicules-electriques-et-hybrides/master-ze.html
# prix_utilitaire_elec = 55000
# # pour une zoe et une clio source https://www.clubic.com/transport-electrique/article-888671-1-sr-cout-entretien-voiture-electrique.html
# entretien_annuel_voiture_elec = 1046
# entretien entretien_annuel_voiture_thermique = 1314 


# Cette fonction ourve un fichier et json et le renvoie sous forme de dictionnaire
def openJson(file):
	with open(file) as json_data:
	    data_dict = json.load(json_data)
	    return data_dict

# Cette fonction affiche les éléments d'un dictionnaire
def afficher_dico(dic):
	for cle, valeur in dic.items():
		try:
			afficher_dico(valeur)
		except AttributeError:
			print(" {:30} {} ".format(cle,valeur))

# Cette fonction calcul la prime à la conversion
def prime_conversion(nombre, type_vehicule):
	# https://les-aides.fr/aide/apFqCHlGxv3UBGFIU1LH_Oh35XE1237dJE_P/asp/prime-a-la-conversion-aide-a-l-acquisition-ou-a-la-location-de-vehicules-peu-polluants.html
	if type_vehicule == "voiture":
		return nombre * 2500
	elif type_vehicule == "utilitaire":
		return nombre * 5000

# Cette fonction calcul le bonus ecologique
def bonus_ecologique(nombre, prix):
	# https://les-aides.fr/aide/a5ZlDnhGxv3UBGFIU1LH_Oh35XE1237dJE_P/asp/bonus-ecologique-aide-a-l-acquisition-ou-la-location-de-vehicules-peu-polluants.html
	if prix > 45000:
		return nombre * 3000
	else :
		return nombre * 5000	

# cette fonction calcule le cout d'une flotte éléctrique en prenant en compte les aids financiéres disponibles
# elle retoure le cout de cette flotte
def calcul_cout(nb_voitures, nb_utilitaires):
	# source https://www.renault.fr/vehicules-electriques/zoe.html
	prix_voiture_elec = 32300
	# source : https://professionnels.renault.fr/vehicules-electriques-et-hybrides/master-ze.html
	prix_utilitaire_elec = 55000

	return nb_voitures * prix_voiture_elec - prime_conversion(nb_voitures,"voiture") - bonus_ecologique(nb_voitures,prix_voiture_elec) \
			+ nb_utilitaires * prix_utilitaire_elec - prime_conversion(nb_utilitaires,"utilitaire") - bonus_ecologique(nb_utilitaires,prix_utilitaire_elec) 

# cette fonction calcule la flotte éléctrique que peut acheter le client selon sa capacité d'investissement et la taille de sa follte thermique
# Elle retourne le nombre de véhicules éléctriques qui peuvent être achetées et leur cout 
def calcul_conversion_flotte(donnees_client):
	voit, util, capacite_investissement = donnees_client["Flotte"]["Voitures_thermiques"],donnees_client["Flotte"]["Utilitaires_thermiques"], donnees_client["Capacite investissement"]
	while calcul_cout(voit, util) > capacite_investissement:
		if calcul_cout(voit-1, util) < capacite_investissement:
			voit = voit - 1
		elif calcul_cout(voit, util-1) < capacite_investissement:
			util = util-1
		else :
			voit, util = voit -1, util-1
	return calcul_cout(voit, util), voit, util

# cette fonction calcul le retour sur investissement annuel sur l'entretien et sur les km parcourus
def calcul_roi(voitures, utilitaires, km):
	entretien_voitures ,entretien_utilitaires, km_voitures, km_utilitaires = (1314 - 1046, 0, 0.05, 0.05)
	roi_entretien = voitures * entretien_voitures + utilitaires * entretien_utilitaires
	roi_km = voitures * km * km_voitures + utilitaires * km * km_utilitaires
	return int(roi_entretien), int(roi_km)

# cette fonction lit le fichier json des donnes du client, affiche ces données, calcule la conversion possible de la flotte et le retour sur investissement de cette flotte.
# Elle affiche la nouvelle flotte électrique son cout et les retour sur investissement
def main():

	file='donnees_client_example.json'
	donnees_client = openJson(file)
	print( "\tDonnées client\n")
	afficher_dico(donnees_client)

	cout, conversion_voitures, conversion_utilitaires = calcul_conversion_flotte(donnees_client)

	roi = calcul_roi(conversion_voitures, conversion_utilitaires, donnees_client["Km annuel"])

	borne = Calcul.a_proximite(donnees_client["Numéro"] + donnees_client["Nom de rue"] + donnees_client["Code postal"] + donnees_client["Ville"])
	
	if not borne:
		cout = cout +1500
		borne="borne à construire"

	print ("\n\tNouvelle flotte\n \n{:30}{} \n{:30}{} \n{:30}{} \n{:30}{} € \n{:30}{} € \n{:30}{} €"\
		.format("Nouvelles voitures elec :",conversion_voitures,\
				"Nouveaux utilitaires elec :",conversion_utilitaires,\
				"Borne :",borne,\
				"Cout :",cout,\
				"ROI annuel sur l'entretien:",roi[0],\
				"ROI annuel sur les km : ",roi[1]\
		)
	)

if __name__ == "__main__":
    main()