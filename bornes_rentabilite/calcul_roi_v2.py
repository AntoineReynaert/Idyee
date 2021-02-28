#!/usr/bin/env python3

from pathlib import Path
import os
import sys
sys.path.append(str(Path(os.getcwd()).parent)+"/bornes_utiles")
sys.path.append(str(Path(os.getcwd()).parent))
import json
from bornes_utiles import Calcul
from calcul_emission_co2 import calcul_baisse_emission
import CoutBorne
import OpenDataSoftAPI
import coord_gps

# Cette fonction ourve un fichier et json et le renvoie sous forme de dictionnaire
def openJson(file):
	if isinstance(file,str):
		with open(file) as json_data:
			data_dict = json.load(json_data)
			return data_dict
	else:
		return file


# Cette fonction affiche les éléments d'un dictionnaire
def afficher_dico(dic):
	for cle, valeur in dic.items():
		try:
			afficher_dico(valeur)
		except AttributeError:
			print(" {:30} {} ".format(cle,valeur))


# Cette fonction calcul la prime à la conversion
def prime_conversion(nombre,aideVehicule):
	# https://les-aides.fr/aide/apFqCHlGxv3UBGFIU1LH_Oh35XE1237dJE_P/asp/prime-a-la-conversion-aide-a-l-acquisition-ou-a-la-location-de-vehicules-peu-polluants.html
	return nombre * aideVehicule



# Cette fonction calcul le bonus ecologique
def bonus_ecologique(nombre, prix,bonus_sup_45k,bonus_inf_45k):
	# https://les-aides.fr/aide/a5ZlDnhGxv3UBGFIU1LH_Oh35XE1237dJE_P/asp/bonus-ecologique-aide-a-l-acquisition-ou-la-location-de-vehicules-peu-polluants.html
	if prix > 45000:
		return nombre * bonus_sup_45k
	else :
		return nombre * bonus_inf_45k	


# cette fonction calcule le cout d'une flotte éléctrique en prenant en compte les aids financiéres disponibles
# elle retoure le cout de cette flotte
def calcul_cout(nb_voitures, nb_utilitaires,fichier_prix, fichier_aide):
	prix_voiture_elec, prix_utilitaire_elec = fichier_prix["prix_voiture_elec"], fichier_prix["prix_utilitaire_elec"]

	prime_conversion_total = prime_conversion(nb_voitures,fichier_aide["prime_conversion_voiture"]) + prime_conversion(nb_utilitaires,fichier_aide["prime_conversion_utilitaire"])
	bonus_ecologique_total =  bonus_ecologique(nb_voitures,prix_voiture_elec,fichier_aide["bonus_eco_sup45k"],fichier_aide["bonus_eco_inf45k"]) + bonus_ecologique(nb_utilitaires,prix_utilitaire_elec,fichier_aide["bonus_eco_sup45k"],fichier_aide["bonus_eco_inf45k"]) 
	cout_initial = nb_voitures * prix_voiture_elec + nb_utilitaires * prix_utilitaire_elec 
	cout_final = cout_initial - prime_conversion_total - bonus_ecologique_total

	return [cout_final, cout_initial, prime_conversion_total, bonus_ecologique_total]

# cette fonction calcule la flotte éléctrique que peut acheter le client selon sa capacité d'investissement et la taille de sa follte thermique
# Elle retourne le nombre de véhicules éléctriques qui peuvent être achetées et leur cout 
def calcul_conversion_flotte(donnees_client,fichier_prix,fichier_aide):
	voit, util, capacite_investissement = donnees_client["Flotte"]["Voitures_thermiques"],donnees_client["Flotte"]["Utilitaires_thermiques"], donnees_client["Capacite investissement"]
	while calcul_cout(voit, util,fichier_prix,fichier_aide)[0] > capacite_investissement:
		if calcul_cout(max(0,voit -1), util,fichier_prix,fichier_aide)[0] < capacite_investissement:
			voit = voit - 1
		elif calcul_cout(voit, max(0,util-1),fichier_prix,fichier_aide)[0] < capacite_investissement:
			util = util-1
		else :
			voit, util = max(0,voit -1), max(0,util-1)
	if voit==0 and util ==0:
		voit = 1
	return [calcul_cout(voit, util,fichier_prix,fichier_aide), voit, util]


# cette fonction calcul le retour sur investissement annuel sur l'entretien et sur les km parcourus
def calcul_roi(nb_voitures, nb_utilitaires, km, pourcentage,prix):
	roi_entretien_voiture = prix["entretien_annuel_voiture_thermique"] - prix["entretien_annuel_voiture_elec"]
	roi_entretien_utilitaire = 0 #non determine pour le moment
	pvce, pvct, pvre, pvrt, puce, puct, pure, purt = prix["voiture_citadin_elec"], prix["voiture_citadin_thermique"],prix["voiture_rural_elec"], prix["voiture_rural_thermique"], prix["utilitaire_citadin_elec"], prix["utilitaire_citadin_thermique"], prix["utilitaire_rural_elec"], prix["utilitaire_rural_thermique"]

	roi_entretien = nb_voitures * roi_entretien_voiture + nb_utilitaires * roi_entretien_utilitaire
	# citadin + rural
	roi_citadin = ((nb_voitures * km * (pvct - pvce)) + (nb_utilitaires * km * (puct - puce))) * (pourcentage     *0.01)
	roi_rural = ((nb_voitures * km * (pvrt - pvre)) + (nb_utilitaires * km * (purt - pure))) * ((100-pourcentage) *0.01)
	roi_km = roi_citadin + roi_rural

	return [int(roi_entretien), int(roi_km)]


# cette fonction lit le fichier json des donnes du client, affiche ces données, calcule la conversion possible de la flotte et le retour sur investissement de cette flotte.
# Elle affiche la nouvelle flotte électrique son cout et les retour sur investissement
def calcul_solution_flotte(fichier_client,fichier_aide ,fichier_prix, verbose=False):
	donnees_client = openJson(fichier_client)
	donnees_prix = openJson(fichier_prix)
	donnees_aides = openJson(fichier_aide)
	if verbose : afficher_dico(donnees_client)
	coordonnees = coord_gps.get_coord(donnees_client["Numero"] +" "+ donnees_client["Nom de rue"] + " " + donnees_client["Code postal"] + " "+ donnees_client["Ville"])
	borne = OpenDataSoftAPI.getBornes(coordonnees[0],coordonnees[1])
	cout, conversion_voitures, conversion_utilitaires = calcul_conversion_flotte(donnees_client,donnees_prix,donnees_aides)
	roi = calcul_roi(conversion_voitures, conversion_utilitaires, donnees_client["Km annuel"], donnees_client["Parcours citadin % :"],donnees_prix)
	baisse_emission = calcul_baisse_emission(conversion_voitures, conversion_utilitaires, donnees_client["Km annuel"], donnees_client["Parcours citadin % :"],donnees_prix)
	
	if not borne:
		coutTotBorne = CoutBorne.resultCoutBorne(conversion_voitures+conversion_utilitaires,donnees_prix)
		borne="Borne à construire: " + str(CoutBorne.nombreBorne(conversion_voitures+conversion_utilitaires)) \
		+ " pour un cout de " + str(coutTotBorne) + "euros."
		cout[1] += coutTotBorne
		cout[0] += coutTotBorne
		cout[3] += CoutBorne.getAidesBornes(donnees_prix)


	return {"Solution bas carbone": "Mobilite verte",\
			"Nouvelles voitures elec" : conversion_voitures,\
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