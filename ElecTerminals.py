#!/usr/bin/env python3
import numpy
from math import *
import matplotlib.pyplot as plt
import csv
from Classes import *


### 1st Use Case: Electrical Terminals

"""
 Fonction permettant de lire un fichier CSV et de récupérer les données dans une liste.
 Arguments: 
   - str file: nom d'un fichier csv dans le répertoire
"""
def openCsv(file):
    with open(file, newline='' , encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        donnees = list()
        for row in spamreader:
            donnees.append(row)
    return donnees

"""      
 Fonction permettant de récupérer les coordonnées des bornes électriques 
 du fichier de données "bornes-irve-20200920.csv"
 Arguments: 
   - list donnees: liste python portant sur les données du fichier "bornes-irve-20200920.csv"
"""
def terminalsCoordinates(donnees):
    indexLongitude = 7
    indexLatitude = 8
    memory = list()
    for row in donnees:
        memory.append(Point(row[indexLongitude],row[indexLatitude]))
    return memory
    

"""
Fonction principale pour lancer l'algorithme
"""
def main():
    reader = openCsv("bornes-irve-20200920.csv")
    for element in terminalsCoordinates(reader):
        print(element)

main()