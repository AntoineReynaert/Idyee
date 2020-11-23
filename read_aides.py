#!/usr/bin/env python3

import csv

def openCsv(file):
    with open(file, newline='' , encoding="utf8", errors= "ignore") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        donnees = list()
        for row in spamreader:
            donnees.append(row)
    return donnees

def writeCsv(file, donnees):
    with open(file, 'w', newline='' , encoding="utf8", errors= "ignore") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        for row in donnees:
            spamwriter.writerow(row)

def filter_all(donnees):
    # ici on regarde la présence du mot véhicule dans au moins un des colonnes
    donnees_filtrees = [donnees[0]] #Ajout de l'entête
    for ligne in donnees:
        for elem in ligne:
            count = 0 # pour éviter de récupérer plusieurs fois la même ligne si il y a plusieurs fois le mot vehicule
            if "hicul" in elem and count ==0:
                donnees_filtrees.append(ligne)
                count += 1
    return donnees_filtrees

def filter_name(donnees):
    # ici on regarde la présence du mot véhicule uniquement dans la colonne aid_nom
    donnees_filtrees = [donnees[0]] #Ajout de l'entête
    for ligne in donnees:
        count=0
        if "hicul" in ligne[1] and count ==0:
            donnees_filtrees.append(ligne)
            count += 1
    return donnees_filtrees

def main():
    donnees = openCsv("aides.csv")
    filtered_all = filter_all(donnees) 
    filtered_name = filter_name(donnees)
    writeCsv('aides_filtrees_toutes_les_colonnes.csv', filtered_all)
    writeCsv('aides_filtrees_nom.csv', filtered_name)


if __name__ == "__main__":
    main()