#!/usr/bin/env python3

import json

# Cette fonction ourve un fichier et json et le renvoie sous forme de dictionnaire
def openJson(file):
	with open(file) as json_data:
	    data_dict = json.load(json_data)
	    return data_dict

# calcul la baisse d'emission co2 du au passage de la flotte en éléctrique (en kg CO2 par €)
def calcul_baisse_emission(nb_voitures, nb_utilitaires, km, pourcentage,emission):
	vce, vct, vre, vrt, uce, uct, ure, urt = emission["voiture_citadin_elec_conso"], emission["voiture_citadin_thermique_conso"],emission["voiture_rural_elec_conso"], emission["voiture_rural_thermique_conso"], emission["utilitaire_citadin_elec_conso"], emission["utilitaire_citadin_thermique_conso"], emission["utilitaire_rural_elec_conso"], emission["utilitaire_rural_thermique_conso"]

	# citadin + rural
	baisse = ((nb_voitures * km * (vct - vce)) + (nb_utilitaires * km * (uct - uce))) * (pourcentage     *0.01) \
	+((nb_voitures * km * (vrt - vre)) + (nb_utilitaires * km * (urt - ure))) * ((100-pourcentage) *0.01)

	return baisse