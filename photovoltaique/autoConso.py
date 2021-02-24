#!/usr/bin/env python3

def getConsommationParMois(conso_annuelle):
    conso={}
    ratios=[0.09896,0.08904,0.08912,0.08014,0.07796,0.07204,0.07058,0.07066,0.07516,0.08534,0.091,0.10036]
    for i in range(12):
        conso[i+1]=ratios[i]*conso_annuelle
    return conso

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

def autoconsommation(consoDict,prodDict):
    autoconso = 0
    for conso,prod in zip(consoDict.items(),prodDict.items()):
        if conso[1]>= prod[1]:
            autoconso += prod[1]
        else:
            autoconso += conso[1]
    return autoconso

def injection(consoDict,prodDict):
    injection = 0
    for conso,prod in zip(consoDict.items(),prodDict.items()):
        if prod[1]>= conso[1]:
            injection += prod[1]-conso[1]
    return injection
    
"""
Calcul réalisé en prenant arbitrairement 45% d'autoconsommation (55% d'injection)
"""
def prixConso(annualProd):
    autoconso = annualProd * (45/100) * 0.17
    injection = annualProd * (55/100) * 0.1
    return autoconso + injection
        