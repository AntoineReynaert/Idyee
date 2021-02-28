#!/usr/bin/env python3

"""
Fonction permettant de calculer la consommation par mois d'un français en fonction
de sa consommation annuelle. Pour cela on utilise des ratios fournis par Enedis 
nous permettant d'évaluer la tendance de consommation d'un français au courant de l'année.
La fonction retourne un dictionnaire possédant comme clé un token allant de 1 à 12 
représentant le mois, et la valeur représente la production estimée ce même mois.
"""
def getConsommationParMois(conso_annuelle):
    conso={}
    ratios=[0.09896,0.08904,0.08912,0.08014,0.07796,0.07204,0.07058,0.07066,0.07516,0.08534,0.091,0.10036]
    for i in range(12):
        conso[i+1]=ratios[i]*conso_annuelle
    return conso
    
"""
Fonction permettant de calculer une approximation de la puissance crête chez un 
utilisateur en fonction de sa surface de toiture disponible et de sa consommation
annuelle en électricité.
Ce calcul ce base sur le fichier excel fourni par Mr. Marchand.
"""

def calculCrete(surface,consoAnnuel):
    crete = 0
    if consoAnnuel<1500:
        crete = 4000
    elif consoAnnuel>2500:
        crete = 7000
    else:
        crete = 5400    
    if surface < 20:
        surface_ind = 20
    elif surface >= 20 and surface <= 40:
        surface_ind = 30
    elif surface > 40 and surface < 60:
        surface_ind = 50
    else:
        surface_ind = 60
    diffcrete = round(((crete*1.7)/300),0)
    if diffcrete > surface_ind:
        coeffsurface = surface_ind/diffcrete
    else:
        coeffsurface = 1
    return crete*(coeffsurface/1000)

"""
À partir de la consommation et de la production estimée, on calcule la part
d'autoconsommation.
"""
def autoconsommation(consoDict,prodDict):
    autoconso = 0
    for conso,prod in zip(consoDict.items(),prodDict.items()):
        if conso[1]>= prod[1]:
            autoconso += prod[1]
        else:
            autoconso += conso[1]
    return autoconso

"""
À partir de la consommation et de la production estimée, on calcule la part
d'injection.
"""
def injection(consoDict,prodDict):
    injection = 0
    for conso,prod in zip(consoDict.items(),prodDict.items()):
        if prod[1]>= conso[1]:
            injection += prod[1]-conso[1]
    return injection
    
"""
Calcul réalisé en prenant arbitrairement 45% d'autoconsommation (donc 55% d'injection)
L'utilisation des fonctions autoconsommation() et injection() avec les données actuelles
ne permettant d'approximer correctement la part d'autoconsommation et d'injection.
En effet il faudrait avoir des données qui soient beaucoup plus précis, càd qui 
présentent la consommation et la production au jour le jour et non pas une moyenne
au mois.
"""
def prixConso(annualProd):
    #Le kWh d'autoconsommation est évalué à 17 centimes
    autoconso = annualProd * (45/100) * 0.17
    #Le kWh d'injection est évalué à 10 centimes
    injection = annualProd * (55/100) * 0.1
    return autoconso + injection
        