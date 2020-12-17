#!/usr/bin/env python3

import json
import Calcul
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
def calcul_roi(nb_voitures, nb_utilitaires, km,borne):
	prix=openJson("prix_achat_entretien_km.json")
	donnees=openJson("donnees_client_example.json")
	#Instanciation des frais de gestion et de carburant de l'utilisateur
	frais=donnees["Frais"]
	prix_carburant_voiture_t=frais["Total_voiture_carburant"]
	prix_carburant_utilitaire_t=frais["Total_utilitaire_carburant"]
	if frais["Aggregat"]==0:
		prix_entretien_voiture_t=frais["Total_voiture_entretien"]
		prix_entretien_utilitaire_t=frais["Total_utilitaire_entretien"]
	if frais["Aggregat"]==1:
		prix_entretien_voiture_t=frais["Assurance_voiture"]+frais["Maintenance_voiture"]+frais["Taxe_voiture"]+frais["Divers_voiture"]
		prix_entretien_utilitaire_t=frais["Assurance_utilitaire"]+frais["Maintenance_utilitaire"]+frais["Taxe_utilitaire"]+frais["Divers_utilitaire"]

	#Le prix de recharge d'une voiture électrique varie en rechargeant sur une borne publique et privée
	if not borne:
		prix_carburant_voiture_e=prix["prix_km_elec_borne_priv"]
		prix_carburant_utilitaire_e=prix["prix_km_elec_borne_priv"]
	else:
		prix_carburant_voiture_e=prix["prix_km_elec_borne_pub"]
		prix_carburant_utilitaire_e=prix["prix_km_elec_borne_pub"]

	roi_entretien_voiture = prix_entretien_voiture_t - prix["entretien_annuel_voiture_elec"]
	roi_entretien_utilitaire = prix_entretien_utilitaire_t- prix["entretien_annuel_utilitaire_elec"]
	roi_km_voiture, roi_km_utilitaire = prix_carburant_voiture_t/km- prix_carburant_voiture_e, prix_carburant_utilitaire_t/km- prix_carburant_utilitaire_e
	# il faudra ajouter les prix pour un utilitaire

	roi_entretien = nb_voitures * roi_entretien_voiture + nb_utilitaires * roi_entretien_utilitaire
	roi_km = nb_voitures * km * roi_km_voiture + nb_utilitaires * km * roi_km_utilitaire
	return [int(roi_entretien), int(roi_km)]

# Calcul à partir de combien de temps l'investissement devient rentable
def seuilRentabilite(RoiAnnuel,CoutTotal):
	seuil = CoutTotal/RoiAnnuel
	nbAnnee = round(seuil)
	nbMois = round((seuil%1)*12)
	return "Rentable après " + str(nbAnnee) + " année(s) et " + str(nbMois) + "mois"


# cette fonction lit le fichier json des donnes du client, affiche ces données, calcule la conversion possible de la flotte et le retour sur investissement de cette flotte.
# Elle affiche la nouvelle flotte électrique son cout et les retour sur investissement
def calcul_solution(fichier_client, verbose=True):
	donnees_client = openJson(fichier_client)
	if verbose : afficher_dico(donnees_client)

	borne = Calcul.a_proximite(donnees_client["Numero"] +" " + donnees_client["Nom de rue"] + " " + donnees_client["Code postal"] + " " + donnees_client["Ville"])
	
	cout, conversion_voitures, conversion_utilitaires = calcul_conversion_flotte(donnees_client)
	roi = calcul_roi(conversion_voitures, conversion_utilitaires, donnees_client["Km annuel"],borne)
	
	if not borne: 
		coutBorne = CoutBorne.resultCoutBorne(conversion_voitures+conversion_utilitaires)
		borne="Borne à construire: " + str(CoutBorne.nombreBorne(conversion_voitures+conversion_utilitaires)) \
		+ " pour un coût de " + str(coutBorne) + "€ avec "
		cout[1] += coutBorne
		cout[0] += coutBorne
		cout[3] += CoutBorne.aideAdvenir(CoutBorne.getPrixBorne(),CoutBorne.getPrixRaccordement())

	return {"Nouvelles voitures elec" : conversion_voitures,\
			"Nouveaux utilitaires elec" : conversion_utilitaires,\
			"Borne" : borne,\
			"Cout initial" : cout[1],\
			"Prime a la conversion":cout[2],\
			"Bonus ecologique":cout[3],\
			"Cout final":cout[0],\
			"ROI annuel sur l'entretien":roi[0],\
			"ROI annuel sur les km":roi[1],\
			"Seuil de rentabilité":seuilRentabilite(sum(roi),cout[0])\
			}


if __name__ == "__main__":
	solution = calcul_solution("donnees_client_example.json")
	print("\n\n 		Solution Proposé \n")
	afficher_dico(solution)