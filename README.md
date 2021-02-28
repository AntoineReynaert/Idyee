# Idyee

Développement d'un algorithme de ranking de solutions éco-responsables.

# Lancement du programme

Pour lancer le programme de décarbonation des activités, il faut pour cela lancer la fonction
bestSolutions() provenant du fichier "main.py". Pour cela, il faut quatre paramètres en entrée
devant être fourni au format JSON. La description des fichiers JSON est donnée dans une partie
suivante.

# Résultat de l'algorithme

L'algorithme retourne un JSON représentant les solutions optimales concernant la mobilité electrique
et l'autoconsommation. On y trouve des informations général sur les solutions, d'autres informations
portant sur le coût total de chaque solution, le gain  écologique de la transition ainsi qu'un rang
représentant la pertinence de la solution pour  l'utilisateur. Plus le rang est élevé, plus la 
solution est intéressante fiancièrement et  écologiquement pour l'utilisateur. Attention cependant:
ce score n'a aucune valeure autre que le classement d'une solution en fonction d'une autre, la 
différence entre les solutions ne doit donc pas être pris à la lettre.

#Explication des fichiers JSON
    ## Donnees_client.json
		Ce fichier est un fichier de données concernant l'utilisateur de l'application. Ces informations
		doivent être recueillies dans un formulaire dédié.
		
		"Nom_societe": Nom de la société de l'utilisateur
		"Numero" : numéro de rue
		"Nom de rue" : nom de la rue
		"Code postal": code postale de l'adresse de l'utilisateur
		"Ville": ville de l'utilisateur
		"Flotte" : {
			"Voitures_thermiques": Nbr de voiture thermique possédé par l'utilisateur
			"Voitures_electriques": Nbr de voiture electrique possédé par l'utilisateur
			"Utilitaires_thermiques":Nbr d'utilitaire thermique possédé par l'utilisateur
			"Utilitaires_electriques": Nbr d'utilitaire electrique possédé par l'utilisateur
			},
		"Frais":{
			"Aggregat": si l'agrégat est à 0 on ne prend pas en compte ces données sinon si l'agrégat est à 1 on prend en compte les données ci dessous
			"Assurance_utilitaire":
			"Maintenance_utilitaire":
			"Taxe_utilitaire":
			"Divers_utilitaire":
			"Assurance_voiture":
			"Maintenance_voiture":
			"Taxe_voiture":
			"Divers_voiture":
			"Total_voiture_entretien":
			"Total_utilitaire_entretien":
			"Total_voiture_carburant":
			"Total_utilitaire_carburant":

		},
		"Km annuel" : moyenne annuelle d'ulitsation pour chaque voiture de la flotte de l'utilisateur
		"Capacite investissement" : capacité d'investissement de l'utilisateur
		"Location 0, Achat 1 " : si 0 alors location, si 1 alors achat des véhicules
		"Parcours citadin % :" : Valeur compris entre 0-100: si 0 alors aucun parcours citadin, si 100 alors 100% de parcours citadin
		
		"Surface toit": Surface de toiture disponible par l'utilisateur pour installer des panneaux solaires
		"Conso annuel": consommation électrique annuelle de l'utilisateur
		"Inclinaison": inclinaison du toit en degré
		"Orientation": Valeur comprise entre -90 et 90. -90 représente l'Est, 0 le Sud et 90 l'Ouest
		
	## prix_panneaux.json
		Fichier JSON permettant d'accéder à des informations concernant des prix sur les panneaux
		solaires. Ce fichier devra être mis à jour régulièrement pour tenir compte des avancées 
		technologiques et sociétales.
		
		"Panneaux_solaire": prix moyen d'un panneau solaire
		"Puissance panneaux_solaire": puissance en kwh d'un panneau solaire    
		"PoseElectSup6": prix supérieur d'une pose de panneau
		"PoseElectInf6": prix inférieur d'une pose de panneau
		"Pose toiture": prix de la pose sur une toiture
		"Etude": prix de l'étude de faisabilité par un prestataire
		"Structure kit de pose": prix d'un kit de pose
		"Ondulateur mono": prix d'un ondulateur monophasé
		"Cable ondulateur mono": prix d'un cable monophasé
		"Ondulateur triphase": prix d'un ondulateur triphasé
		"Cable ondulateur triphase": prix d'un cable triphasé
		"Coffret de protection PV AC Mono": prix d'un coffret de protection PV AC Monophasé
		"Coffret de protection PV AC Tri": prix d'un coffret de protection PV AC Triphsé
		"Passerelle de communication":  prix d'une passerelle de communication
		"TVA": pourcentage compris entre 0 et 1 de TVA
		
		"empreinte_carbone_kwh_g": empreinte carbone moyen sur le réseau électrique français en g de c02 par kwh
	
	##fichier aide.json
		Ce fichier repertorie l'ensemble des aides pour la mobilité et l'autoconsommation suceptible de faire
		baisser le coût des investissements. Ce fichier devra être mis à jour régulièrement pour tenir compte des avancées 
		sociétales.
		
		"prime_conversion_voiture": prime pour la conversion à l'électrique d'une voiture
		"prime_conversion_utilitaire": prime pour la conversion à l'électrique d'un utilitaire
		"bonus_eco_sup45k": prime si le véhicule coûte plus de 45000 euros
		"bonus_eco_inf45k": prime si le véhicule coûte moins de 45000 euros
		
		"inf3": prime solaire si le kwcrête est inférieur à 3
		"sup3": prime solaire si le kwcrête est supérieur à 3
		
	##prix_achat_entretien_km.json
		"prix_voiture_elec" : prix à l'achat d'une voiture électrique
		"prix_utilitaire_elec" : prix à l'achat d'un utilitaire électrique
		"entretien_annuel_voiture_elec" : entretien d'une voiture électrique
		"entretien_annuel_voiture_thermique" : entretien d'un utilitaire électrique
		
		"voiture_citadin_elec": prix en voiture citadin de l'électrique pour 1 km parcouru
		"voiture_citadin_thermique": prix en voiture citadin du thermique pour 1 km parcouru 
		"voiture_rural_elec": prix en voiture rural de l'électrique pour 1 km parcouru
		"voiture_rural_thermique": prix en voiture rural du thermique pour 1 km parcouru
		"utilitaire_citadin_elec": prix en utilitaire citadin de l'électrique pour 1 km parcouru
		"utilitaire_citadin_thermique": prix en utilitaire citadin thermique pour 1 km parcouru
		"utilitaire_rural_elec": prix en utilitaire rural de l'électrique pour 1 km parcouru
		"utilitaire_rural_thermique": prix en utilitaire rural thermique pour 1 km parcouru
		
		---> même chose ici pour l'émission de C02 pour 1 km parcouru
		"voiture_citadin_elec_conso": 0.0,
		"voiture_citadin_thermique_conso": 0.186,
		"voiture_rural_elec_conso": 0.0,
		"voiture_rural_thermique_conso": 0.147,
		"utilitaire_citadin_elec_conso": 0.0,
		"utilitaire_citadin_thermique_conso": 0.265,
		"utilitaire_rural_elec_conso": 0.0,
		"utilitaire_rural_thermique_conso": 0.225,
		
		"aides_bornes" : liste des aides pour l'achat et l'installation de bornes
		"prix_raccordement" : prix du raccordement d'une borne
		"prix_borne" : prix d'une borne de recharge
		
# APIfication du code

Le développement d'une API devra se baser sur la fonction bestSolutions() provenant du fichier
"main.py". Les paramètres de cette fonction devront être récupérer par l'API grâce à des requêtes
à des bases de données ainsi que la récupération des données clients via un formulaire.
L'API devra renvoyé simplement l'objet JSON retourner par la fonction bestSolutions().
Cette dernière étape de développement permettra d'utiliser l'algorithme à son plein potentiel via
la plateforme en ligne GreenRoom.

