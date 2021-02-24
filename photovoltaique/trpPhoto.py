#!/usr/bin/env python3


"""
Fonction permettant de calculer le gain en carbone grâce à la mise en place 
des panneaux photovoltaïques.
Calcul basé sur le fichier excel de Mr. Marchand
"""
def gain_carbone(prod_moyenne_mois,conso_moyenne_mois,injection_moyenne_mois,kwh,conso_euro,tranche):
    mois=[31,28,31,30,31,30,31,31,30,31,30,31]
    
    if kwh!="":
        kwh_annuel=kwh
    else:
        if conso_euro!="":
            conso_ann_euro=conso_euro
        else:
            if tranche=="< 1500":
                conso_ann_euro=1250
            else:
                if tranche=="> 2500":
                    conso_ann_euro=3000
                else:
                    conso_ann_euro=2000
        
        kwh_annuel=conso_ann_euro*100/(15.57*1.02)
    conso_totale=0
    prod_reelle=0
    for i in range (12):
        conso_totale=conso_totale+mois[i]*conso_moyenne_mois[i+1]
        prod_reelle=prod_reelle+mois[i]*prod_moyenne_mois[i+1]
    correctif=kwh_annuel/conso_totale
    prod_totale=prod_reelle*correctif
    if not injection_moyenne_mois:
        inject_reelle=(prod_reelle*(55/100))
    else:
        inject_reelle=inject_reelle+mois[i]*injection_moyenne_mois[i+1]
    inject_totale=inject_reelle*correctif

    diff=prod_totale-inject_totale
    carbone=(round(diff,0)*37.81)/1000
    return carbone


