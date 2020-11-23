#!/usr/bin/env python3

import csv

"""
 Fonction permettant de lire un fichier CSV et de récupérer les données dans une liste.
 Arguments: 
   - str file: nom d'un fichier csv dans le répertoire
"""
def openCsv(file):
    with open(file, newline='' , encoding="utf8", errors= "ignore") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        donnees = list()
        for row in spamreader:
            donnees.append(row)
    return donnees

def main():
	donnes = openCsv("aides.csv")
	donnes_filtrees=list()
	donnes_filtrees.append(donnes[0]) #Ajout de l'entête
	for ligne in donnes[:10]:
		for elem in ligne:
			count = 0
			if "hicul" in elem and count ==0:
				print("\r",ligne)
				donnes_filtrees.append(ligne)

	print("\r\r")

	with open('aides_filtrees.csv', 'w', newline='') as csvfile:

	    spamwriter = csv.writer(csvfile, delimiter=' ',
	                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

	    for row in donnes_filtrees:
	    	print("\r", donnes_filtrees)
	    	# spamwriter.writerow(donnes_filtrees)


if __name__ == "__main__":
    main()