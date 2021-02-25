#!/usr/bin/env python3


"""
Fonction permettant de calculer le gain en carbone grâce à la mise en place 
des panneaux photovoltaïques.
Calcul basé sur les chiffres de l'OCDE. L'empreinte carbone par kwh est exprimé
en gramme et le résultat est divisé par 1000 pour obtenir le nombre de kg de CO2
économisé.
"""
def gain_carbone(prod_annuelle,donnees_panneaux):
    return (prod_annuelle*(45/100)*donnees_panneaux["empreinte_carbone_kwh_g"])/1000


