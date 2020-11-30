#!/usr/bin/env python3

import json
from read_aides import openCsv

# import calcul
# if len(calcul.a_proximite(adresse))>0


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
		print(" {:30} {} ".format(cle,valeur))

def prime_conversion(nombre, type_vehicule):
	# https://les-aides.fr/aide/apFqCHlGxv3UBGFIU1LH_Oh35XE1237dJE_P/asp/prime-a-la-conversion-aide-a-l-acquisition-ou-a-la-location-de-vehicules-peu-polluants.html
	if type_vehicule == "voiture":
		return nombre * 2500
	elif type_vehicule == "utilitaire":
		return nombre * 5000

def bonus_ecologique(nombre, prix):
	# https://les-aides.fr/aide/a5ZlDnhGxv3UBGFIU1LH_Oh35XE1237dJE_P/asp/bonus-ecologique-aide-a-l-acquisition-ou-la-location-de-vehicules-peu-polluants.html
	if prix > 45000:
		return nombre * 3000
	else :
		return nombre * 5000	

# cette fonction calcul les aides auquels est eligible l'entreprise à partir d'un fichier csv et des inforrmations sur l'entreprise
def calcul_cout(nb_voitures, nb_utilitaires):
	# aides = openCsv("aides_filtrees_nom.csv")

	# source https://www.renault.fr/vehicules-electriques/zoe.html
	prix_voiture_elec = 32300
	# source : https://professionnels.renault.fr/vehicules-electriques-et-hybrides/master-ze.html
	prix_utilitaire_elec = 55000

	return nb_voitures * prix_voiture_elec - prime_conversion(nb_voitures,"voiture") - bonus_ecologique(nb_voitures,prix_voiture_elec) \
			+ nb_utilitaires * prix_utilitaire_elec - prime_conversion(nb_utilitaires,"utilitaire") - bonus_ecologique(nb_utilitaires,prix_utilitaire_elec) 

def calcul_conversion_flotte(donnees_client):
	voit, util, capacite_investissement = donnees_client["Flotte"]["voitures_thermiques"],donnees_client["Flotte"]["utilitaires_thermiques"], donnees_client["Capacite investissement"]
	while calcul_cout(voit, util) > capacite_investissement:
		if calcul_cout(voit-1, util) < capacite_investissement:
			voit = voit - 1
		elif calcul_cout(voit, util-1) < capacite_investissement:
			util = util-1
		else :
			voit, util = voit -1, util-1
	return calcul_cout(voit, util), voit, util


# Cette fonction calcule les changements que l'entreprise peut effectuer sur sa flotte selon ses capacité d'investissment
# Elle retourne le nombre de véhicules qui peuvent être changé, les aides qui peuvent être perçus, et le retour sur investissement annuel

def calcul_roi(voitures, utilitaires, km):
	entretien_voitures ,entretien_utilitaires, km_voitures, km_utilitaires = (1314 - 1046, 0, 0.05, 0.05)
	roi_entretien = voitures * entretien_voitures + utilitaires * entretien_utilitaires
	roi_km = voitures * km * km_voitures + utilitaires * km * km_utilitaires
	return (roi_entretien, roi_km)


def main():

	file='donnees_client_example.json'
	donnees_client = openJson(file)
	afficher_dico(donnees_client)

	cout, conversion_voitures, conversion_utilitaires = calcul_conversion_flotte(donnees_client)

	roi = calcul_roi(conversion_voitures, conversion_utilitaires, donnees_client["km annuel"])

	# borne = calcul.a_proximite(adresse)
	borne = ""
	if borne=="":
		cout = cout +1500
		borne="borne à construire"

	print ("\nNouvelles voitures elec : {} \nNouveaux utilitaires elec : {} \nBorne : {} \nCout : {} € \nROI entretien: {} € \nROI km: {} € "\
		.format(conversion_voitures,conversion_utilitaires,borne,cout,roi[0],roi[1]))


if __name__ == "__main__":
    main()