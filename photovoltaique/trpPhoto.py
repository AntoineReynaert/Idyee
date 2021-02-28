#!/usr/bin/env python3


"""
Fonction permettant de calculer le gain en carbone grâce à la mise en place 
des panneaux photovoltaïques.
Calcul basé sur les chiffres de l'OCDE et de RTE. L'empreinte carbone par kwh est exprimé
en gramme et le résultat est divisé par 1000 pour obtenir le nombre de kg de CO2
économisé. Nous avons ici pris la décision de valorisé aussi bien les kwh autoconsommés
qu'injectés dans le réseau.
"""
def gain_carbone(prod_annuelle,donnees_panneaux):
    return (prod_annuelle*donnees_panneaux["empreinte_carbone_kwh_g"])/1000


