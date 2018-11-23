from math import *
from random import randint

class Monde: 	# Notre class pour englober notre monde

	def __init__(self, largeur, nombreFourmisEclaireuses, nombreFourmisOuvrieres, tauxDecrementation): 	# Fonction appelée quand on créé un monde

		self.pheromones = [[0 for i in range(largeur)] for j in range(largeur)] 	# Création d'une matrice par défaut de taile LxL avec un tuple pour le taux de phéromones et la durée sans nouvelle fourmi
		# Position 0 du tuple : taux de phéromones
		# Position 1 du tuple : durée sans phéromones
		self.largeur = largeur 	# Largeur enregistrée pour future utilisation

		self.tauxDecrementation = tauxDecrementation 	# Taux de décrementation des phéromones entre 0 et 1

		self.nombreFourmisOuvrieres = nombreFourmisOuvrieres
		self.nombreFourmisEclaireuses = nombreFourmisEclaireuses 	# Nombre de fourmis enregistrées

		self.fourmiliere = [0, 0]
		self.nourriture = [0, 0] 	# Définition des coordonnées X et Y de la fourmilière et de la nourriture
		# Pour l'instant ils sont au même endroit car on est sûr que le while fonctionnera au moins une fois

		self.nourritureApportee = 0 	# Nombre d'allers retours

		self.fourmisOuvrieresPeuventPartir = False 	# Booléen qui autorise le départ des fourmis ouvrières

		self.cheminTrouve = False 	# Si un chemin commun a été trouvé par des fourmis
		self.dernierCheminTrouve = [] 	# Enregistre le dernier chemin trouvé
		self.nombreCheminsCommuns = 0 	# Nombre de chemins trouvés à la suite par les fourmis

		while (abs(self.fourmiliere[0] - self.nourriture[0]) + (abs(self.fourmiliere[1] - self.nourriture[1]))) < self.largeur: 	# On calcule la distance en X et en Y, on additionne et on veut que ce soit au moins aussi loin qu'une largeur

			self.fourmiliere = (randint(0, self.largeur-1), randint(0, self.largeur-1))
			self.nourriture = (randint(0, self.largeur-1), randint(0, self.largeur-1)) 	# Définition des coordonnées X et Y de la fourmilière et de la nourriture

		self.fourmis = [] 	# Création d'une liste vide qui contiendra toutes nos fourmis

		for i in range(self.nombreFourmisOuvrieres):
			nouvelleFourmi = Fourmi(1, self.fourmiliere) 	# Création d'une fourmi ouvrière à la fourmilière
			self.fourmis.append(nouvelleFourmi) 	# Ajout de la nouvelle fourmi à la liste des fourmis du monde

		for i in range(self.nombreFourmisEclaireuses):
			nouvelleFourmi = Fourmi(0, self.fourmiliere) 	# Création d'une fourmi éclaireuse à la fourmilière
			self.fourmis.append(nouvelleFourmi) 	# Ajout de la nouvelle fourmi à la liste des fourmis du monde

	def distanceCheminReellementOptimal(self):

		longueurCheminReellementOptimal = 0
		position = [self.nourriture[0], self.nourriture[1]]
		positionFinale = [self.fourmiliere[0], self.fourmiliere[1]]

		while position != positionFinale:

			if position[0] != positionFinale[0]:
				if position[0] < positionFinale[0]:
					position[0] = position[0] + 1
				else:
					position[0] = position[0] - 1

			if position[1] != positionFinale[1]:
				if position[1] < positionFinale[1]:
					position[1] = position[1] + 1
				else:
					position[1] = position[1] - 1

			longueurCheminReellementOptimal = longueurCheminReellementOptimal + 1

		return longueurCheminReellementOptimal

	def nombreFourmisRetourParPosition(self):

		nombreFourmis = [[0 for i in range(self.largeur)] for j in range(self.largeur)] 	# Liste 2D du nombre de fourmis dans chaque case de la grille.

		for i in range(len(self.fourmis)): 	# On parcourt toutes les fourmis
			if self.fourmis[i].retour: 	# Si c'est une fourmi qui rentre
				nombreFourmis[self.fourmis[i].X][self.fourmis[i].Y] = nombreFourmis[self.fourmis[i].X][self.fourmis[i].Y] + 1 	# On ajoute notre fourmi grâce à sa case

		return nombreFourmis

	def nombreFourmisParPosition(self): 	# Pareil qu'avant, mais on ajoute aussi les fourmis à l'aller

		nombreFourmis = [[0 for i in range(self.largeur)] for j in range(self.largeur)]

		for i in range(len(self.fourmis)):
			nombreFourmis[self.fourmis[i].X][self.fourmis[i].Y] = nombreFourmis[self.fourmis[i].X][self.fourmis[i].Y] + 1

		return nombreFourmis

	def listeCasesAutoriseesAutour(self, fourmi): 	# Renvoie la liste de cases autour d'une fourmi qu'elle peut légalement emprunter

		Fx = fourmi.X 	# On enregistre en variable local la position de la fourmi pour avoir moins de texte à écrire
		Fy = fourmi.Y

		retour = fourmi.retour 	# Pareil pour si elle est à l'aller ou au retour

		listeCases = [] 	# Liste des cases possibles que l'on renverra

		for i in range(-1, 2): 	# Pour les delta X possibles autour de nous (donc -1, 0, 1)
			nouveauX = Fx + i 	# Renommage de l'emplacement X potentiel
			if nouveauX >= 0 and nouveauX < self.largeur: 	# Si le X potentiel est dans la grille
				for j in range(-1, 2): 	# Pareil pour Y
					nouveauY = Fy + j
					if nouveauY >= 0 and nouveauY < self.largeur:
						if i != 0 or j != 0: 	# Si on se déplace d'au moins une case sur un axe, la case potentielle est bien différente de celle actuelle
							if (not retour and not (nouveauX == self.fourmiliere[0] and nouveauY == self.fourmiliere[1])) or (retour and not (nouveauX == self.nourriture[0] and nouveauY == self.nourriture[1])):
								# Ce if au dessus autorise l'ajout de la carte si :
								# La case potentielle n'est pas la fourmilière et que l'on est à l'aller (empêchant la fourmi de rentrer chez elle sans avoir eu de nourriture)
								# Ou la case potentielle n'est pas la nourriture et qu'on est au retour (empêchant la fourmi de retourner sur la nourriture sans avoir déposé celle qu'elle avait déjà prise)
								if not ([nouveauX, nouveauY] in fourmi.casesVisitees): 	# Si la case potentielle n'est pas encore visitée on l'ajoute
									listeCases.append([nouveauX, nouveauY]) 	# On ajoute la case potentielle

		return listeCases


	def choisirCaseInteressanteAutour(self, numeroFourmi): 	# Choisis LA case à visiter au prochain pour la fourmi numeroFourmi

		fourmi = self.fourmis[numeroFourmi] 	# On récupère toutes les infos de la fourmi

		choix = None 	# On initialise le futur choix
		sommePheromones = 0 	# On initialise la somme des phéromones autour de la fourmi

		choixPossibles = self.listeCasesAutoriseesAutour(fourmi) 	# On récupère la liste des cases légales autour de la fourmi
		if len(choixPossibles) == 0: 	# Si jamais il n'y aucune case de disponible (généralement parce qu'on les a déjà toutes visitées)
			self.fourmis[numeroFourmi].casesVisitees = [] 	# On reset son historique de cases visitées
			choixPossibles = self.listeCasesAutoriseesAutour(fourmi) 	# On redemande la liste des cases autour de la fourmi

		for i in range(len(choixPossibles)): 	# Pour tous les choix possibles
			X = choixPossibles[i][0] 	# On initialise le X et le Y de ce choix en variable locale de boucle
			Y = choixPossibles[i][1]
			if (X == self.fourmiliere[0] and Y == self.fourmiliere[1] and fourmi.retour) or (X == self.nourriture[0] and Y == self.nourriture[1] and not fourmi.retour):
			# Si on est au retour et que le choix possible est la fourmilière
			# Ou que on est à l'aller et que le choix possible est la nourriture	
				choix = [X, Y] 	# On enregistre ce choix comme choix final directement
				break 	# On arrête la boucle car on se fiche des autres choix possibles
			else: 	# Si on est pas à côte de la nourriture ou de la fourmilière quand on veut y aller
				sommePheromones = sommePheromones + self.pheromones[X][Y] 	# On augmente la somme des phéromones autour avec celle de la case potentielle

		if choix != None: 	# Si le choix est différent de None, c'est qu'on a privilégié la fourmilière ou la nourriture dans la boucle précédente. On peut directement renvoyer ce choix.
			return choix 	# On retourne le choix et la fonction s'arrête ici

		listeProbabilites = [None for i in range(len(choixPossibles))] 	# On initialise la liste des probabilités pour chaque choix possible

		if sommePheromones == 0: 	# Si aucune case autour n'a de phéromones
			numeroChoix = randint(0, len(choixPossibles)-1) 	# On en choisis une au hasard
			choix = choixPossibles[numeroChoix] 	# On enregistre la case pour la retourner à la fin de la fonction

		else: 	# Si il y a des phéromones autour
			proba = 0 	# Proba utilisée pour la comparaison
			probaTiree = randint(0, 99) / 100 	# Tirage entre 0 et 1
			for i in range(0, len(choixPossibles)): 	# Pour tous les choix possibles
				X = choixPossibles[i][0] 	# Renommage du X et du Y du choix actuel
				Y = choixPossibles[i][1]
				pheromones = self.pheromones[X][Y] 	# On récupère le taux de phéromones de la case actuelle
				proba = (pheromones/sommePheromones) + proba 	# On ajoute la proba de cette case à la somme des proba précédentes
				if proba > probaTiree: 	# Si on a dépassé notre tirage, c'est cette case qu'on veut
					choix = choixPossibles[i] 	# On l'enregistre
					break 	# On arrête la boucle car on a trouvé notre case

		return choix



	def deplacerFourmis(self):

		for i in range(len(self.fourmis)): 	# On parcourt toutes les fourmis de notre monde
			
			if self.fourmis[i].typeFourmi == 1: 	# Si c'est une ouvrière
				
				if self.fourmisOuvrieresPeuventPartir: 	# Et que on l'a autorisée à partir car au moins une fourmi éclaireuse est revenue
					nouvellePosition = self.choisirCaseInteressanteAutour(i) 	# On récupère sa nouvelle position
					
					self.fourmis[i].casesVisitees.append([self.fourmis[i].X, self.fourmis[i].Y]) 	# On ajoute sa position actuelle dans la liste des cases déjà visitées
					self.fourmis[i].X = nouvellePosition[0] 	# On met à jour sa position actuelle avec la nouvelle position
					self.fourmis[i].Y = nouvellePosition[1]

			elif self.fourmis[i].typeFourmi == 0 and not (self.fourmis[i].X == self.fourmiliere[0] and self.fourmis[i].Y == self.fourmiliere[1] and self.fourmis[i].retour == True):
			# Ou si c'est une fourmi éclaireuse et que elle n'est pas encore rentrée

				deplacementX = 0 	# On initialise son delta de déplacement
				deplacementY = 0

				for j in range(-1, 2): 	# Pour tous les déplacements possibles en X
					nouveauX = self.fourmis[i].X + j 	# Renommage
					for k in range(-1, 2): 	# Pareil Y
						nouveauY = self.fourmis[i].Y + k
						if (self.fourmis[i].retour and nouveauX == self.fourmiliere[0] and nouveauY == self.fourmiliere[1]) or (not self.fourmis[i].retour and nouveauX == self.nourriture[0] and nouveauY == self.nourriture[1]):
						# Si on est à côte de la fourmilière au retour ou à côte de la nourriture à l'aller on y va sans hésiter
						# Vu qu'au moins une de ces valeurs sera différente de 0, on saute la boucle suivante et de cette façon notre fourmilière ou nourriture sera privilégiée	
							deplacementX = j
							deplacementY = k

				while (deplacementX == 0 and deplacementY == 0) or (self.fourmis[i].X + deplacementX) < 0 or (self.fourmis[i].Y + deplacementY) < 0 or (self.fourmis[i].X + deplacementX) >= self.largeur or (self.fourmis[i].Y + deplacementY) >= self.largeur:
				# On recalcule le delta de déplacement tant que au moins une de ces conditions est valide :
				# Tant que la fourmi ne bouge pas du tout
				# Tant que sa nouvelle position serait en dehors de la grille
					deplacementX = randint(-1, 1)
					deplacementY = randint(-1, 1)

				self.fourmis[i].casesVisitees.append([self.fourmis[i].X, self.fourmis[i].Y]) 	# On ajoute sa position actuelle dans la liste des cases déjà visitées
				self.fourmis[i].X = self.fourmis[i].X + deplacementX 	# On enregistre la nouvelle position
				self.fourmis[i].Y = self.fourmis[i].Y + deplacementY

			self.changerEtatFourmi(i) 	# On met l'état de la fourmi à jour

	def changerEtatFourmi(self, numeroFourmi):

		if self.fourmis[numeroFourmi].X == self.nourriture[0] and self.fourmis[numeroFourmi].Y == self.nourriture[1]: 	# Si la fourmi est sur la nourriture
			self.fourmis[numeroFourmi].retour = True 	# On la met au retour
			self.fourmis[numeroFourmi].casesVisitees = [] 	# On reset ses cases déjà visitée

		elif self.fourmis[numeroFourmi].X == self.fourmiliere[0] and self.fourmis[numeroFourmi].Y == self.fourmiliere[1]: 	# Si on est à la fourmilière
			
			if self.fourmis[numeroFourmi].retour: 	# Si notre furmi est au retour
				
				if self.fourmis[numeroFourmi].typeFourmi == 0 and self.fourmisOuvrieresPeuventPartir == False: 	# Si c'est une éclaireuse et que les ouvrières ne sont pas partis
					self.fourmisOuvrieresPeuventPartir = True 	# On fait partir les ouvrières
				
				elif self.fourmis[numeroFourmi].typeFourmi == 1: 	# Si c'est une ouvrière
					
					self.nourritureApportee = self.nourritureApportee + 1 	# On augmente le compteur d'allers / retours
					
					if self.fourmis[numeroFourmi].casesVisitees == self.dernierCheminTrouve: 	# Si le chemin emprunté par cette fourmi est le même que celui d'avant
						self.nombreCheminsCommuns = self.nombreCheminsCommuns + 1 	# On augmente le nombre de chemins pareils
					else: 	# Si c'est pas le même que la fourmi précédente
						self.nombreCheminsCommuns = 1 	# On reset le compteur de chemins
						self.dernierCheminTrouve = self.fourmis[numeroFourmi].casesVisitees 	# On enregistre ce chemin comme étant le dernier trouvé
				
				self.fourmis[numeroFourmi].retour = False 	# On la remet en position aller
				self.fourmis[numeroFourmi].casesVisitees = [] 	# On reset les cases visitées

	def deposerToutesPheromones3(self):

		nombreFourmis = self.nombreFourmisRetourParPosition() 	# On récupère une liste 2D de la grille avec le nombre de fourmis en retour sur chaque case

		for i in range(self.largeur): 	# Pour tous les X
			for j in range(self.largeur): 	# Pour tous les Y
				self.pheromones[i][j] = ((1-self.tauxDecrementation)*self.pheromones[i][j]) + nombreFourmis[i][j]**(self.largeur)
				# pheromones[X][Y] = (1-tauxDecrementation)*pheromones[X][Y] + fourmisRetour[X][Y]^largeur

	def deposerToutesPheromones4(self):

		ajoutPheromones = [[0 for i in range(self.largeur)] for j in range(self.largeur)]

		for i in range(len(self.fourmis)):
			# if self.fourmis[i].retour:
			if 1:
				ajoutPheromones[self.fourmis[i].X][self.fourmis[i].Y] = ajoutPheromones[self.fourmis[i].X][self.fourmis[i].Y] + (1/(len(self.fourmis[i].casesVisitees)+1))**(self.largeur)

		for i in range(self.largeur):
			for j in range(self.largeur):
				self.pheromones[i][j] = ((1-self.tauxDecrementation)*self.pheromones[i][j]) + ajoutPheromones[i][j]**(self.largeur)


	def verifierConvergence(self):
		if self.nombreCheminsCommuns > self.nombreFourmisOuvrieres/4:
			self.cheminTrouve = True

	def effectuerTourProgramme(self): 	# La fonction qui fait un tour de programme
		self.deplacerFourmis()
		self.deposerToutesPheromones3()
		self.verifierConvergence()


class Fourmi: 	# La classe des fourmis
	# 0 = fourmi éclaireuse
	# 1 = fourmi ouvrière
	def __init__(self, typeFourmi, coordonneesFourmiliere):

		self.typeFourmi = typeFourmi

		if self.typeFourmi == 0:
			self.nomFourmi = "Eclaireuse"
		elif self.typeFourmi == 1:
			self.nomFourmi = "Ouvrière"

		self.X = coordonneesFourmiliere[0]
		self.Y = coordonneesFourmiliere[1]

		self.retour = False 	# Vaut False si la fourmi cherche et True si la fourmi a trouvé (elle fait le chemin retour)

		self.casesVisitees = []