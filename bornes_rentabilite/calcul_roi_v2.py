#!/usr/bin/env python3

from pathlib import Path
import os
import sys
sys.path.append(str(Path(os.getcwd()).parent)+"\\bornes_utiles")
sys.path.append(str(Path(os.getcwd()).parent))
print(sys.path)
import json
from bornes_utiles import Calcul
from calcul_emission_co2 import calcul_baisse_emission
import CoutBorne

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
	prix=openJson("prix_achat_entretien_km.json")
	prix_voiture_elec, prix_utilitaire_elec = prix["prix_voiture_elec"], prix["prix_utilitaire_elec"]

	prime_conversion_total = prime_conversion(nb_voitures,"voiture") + prime_conversion(nb_utilitaires,"utilitaire")
	bonus_ecologique_total =  bonus_ecologique(nb_voitures,prix_voiture_elec) + bonus_ecologique(nb_utilitaires,prix_utilitaire_elec) 
	cout_initial = nb_voitures * prix_voiture_elec + nb_utilitaires * prix_utilitaire_elec 
	cout_final = cout_initial - prime_conversion_total - bonus_ecologique_total

	return [cout_final, cout_initial, prime_conversion_total, bonus_ecologique_total]

# cette fonction calcule la flotte éléctrique que peut acheter le client selon sa capacité d'investissement et la taille de sa follte thermique
# Elle retourne le nombre de véhicules éléctriques qui peuvent être achetées et leur cout 
def calcul_conversion_flotte(donnees_client):
	voit, util, capacite_investissement = donnees_client["Flotte"]["Voitures_thermiques"],donnees_client["Flotte"]["Utilitaires_thermiques"], donnees_client["Capacite investissement"]
	while calcul_cout(voit, util)[0] > capacite_investissement:
		if calcul_cout(voit-1, util)[0] < capacite_investissement:
			voit = voit - 1
		elif calcul_cout(voit, util-1)[0] < capacite_investissement:
			util = util-1
		else :
			voit, util = voit -1, util-1
	return [calcul_cout(voit, util), voit, util]


# cette fonction calcul le retour sur investissement annuel sur l'entretien et sur les km parcourus
def calcul_roi(nb_voitures, nb_utilitaires, km, pourcentage):
	prix=openJson("prix_achat_entretien_km.json")
	roi_entretien_voiture = prix["entretien_annuel_voiture_thermique"] - prix["entretien_annuel_voiture_elec"]
	roi_entretien_utilitaire = 0 #non determine pour le moment
	pvce, pvct, pvre, pvrt, puce, puct, pure, purt = prix["voiture_citadin_elec"], prix["voiture_citadin_thermique"],prix["voiture_rural_elec"], prix["voiture_rural_thermique"], prix["utilitaire_citadin_elec"], prix["utilitaire_citadin_thermique"], prix["utilitaire_rural_elec"], prix["utilitaire_rural_thermique"]

	roi_entretien = nb_voitures * roi_entretien_voiture + nb_utilitaires * roi_entretien_utilitaire
	# citadin + rural
	roi_km = (nb_voitures * km * (pvct - pvce) + nb_utilitaires * km * (puct - puce)) * pourcentage     *0.01 \
			+(nb_voitures * km * (pvrt - pvre) + nb_utilitaires * km * (purt - pure)) * (1-pourcentage) *0.01

	return [int(roi_entretien), int(roi_km)]


# cette fonction lit le fichier json des donnes du client, affiche ces données, calcule la conversion possible de la flotte et le retour sur investissement de cette flotte.
# Elle affiche la nouvelle flotte électrique son cout et les retour sur investissement
def calcul_solution_flotte(fichier_client, verbose=True):
	donnees_client = openJson(fichier_client)
	donnees_borne = openJson("construction_borne.json")
	if verbose : afficher_dico(donnees_client)

	borne = Calcul.a_proximite(donnees_client["Numero"] + donnees_client["Nom de rue"] + donnees_client["Code postal"] + donnees_client["Ville"])
	cout, conversion_voitures, conversion_utilitaires = calcul_conversion_flotte(donnees_client)
	roi = calcul_roi(conversion_voitures, conversion_utilitaires, donnees_client["Km annuel"], donnees_client["Parcours citadin % :"])
	baisse_emission = calcul_baisse_emission(conversion_voitures, conversion_utilitaires, donnees_client["Km annuel"], donnees_client["Parcours citadin % :"])
	
	if not borne:
		coutTotBorne = CoutBorne.resultCoutBorne(conversion_voitures+conversion_utilitaires,donnees_borne)
		borne="Borne à construire: " + str(CoutBorne.nombreBorne(conversion_voitures+conversion_utilitaires)) \
		+ " pour un coût de " + str(coutTotBorne) + "€."
		cout[1] += coutTotBorne
		cout[0] += coutTotBorne
		cout[3] += CoutBorne.getAidesBornes(donnees_borne)


	return {"Nouvelles voitures elec" : conversion_voitures,\
			"Nouveaux utilitaires elec" : conversion_utilitaires,\
			"Borne" : borne,\
			"Cout initial" : cout[1],\
			"Prime a la conversion":cout[2],\
			"Bonus ecologique":cout[3],\
			"Cout final":cout[0],\
			"ROI annuel sur l'entretien":roi[0],\
			"ROI annuel sur les km":roi[1],\
			"Baisse emission co2":baisse_emission,\
			}


if __name__ == "__main__":
	solution = calcul_solution_flotte("donnees_client_example.json")
	print("\n\n 		Solution Proposé \n")
	afficher_dico(solution)