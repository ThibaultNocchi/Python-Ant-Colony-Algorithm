from math import *
from random import randint

class World: 	# Notre class pour englober notre monde

	def __init__(self, width, scoutAntsNumber, workerAntsNumber, decreaseRate): 	# Fonction appelée quand on créé un monde

		self.pheromones = [[0 for i in range(width)] for j in range(width)] 	# Création d'une matrice par défaut de taile LxL avec un tuple pour le taux de phéromones et la durée sans nouvelle fourmi
		# Position 0 du tuple : taux de phéromones
		# Position 1 du tuple : durée sans phéromones
		self.width = width 	# Largeur enregistrée pour future utilisation

		self.decreaseRate = decreaseRate 	# Taux de décrementation des phéromones entre 0 et 1

		self.workerAntsNumber = workerAntsNumber
		self.scoutAntsNumber = scoutAntsNumber 	# Nombre de fourmis enregistrées

		self.anthill = [0, 0]
		self.food = [0, 0] 	# Définition des coordonnées X et Y de la fourmilière et de la nourriture
		# Pour l'instant ils sont au même endroit car on est sûr que le while fonctionnera au moins une fois

		self.broughtFood = 0 	# Nombre d'allers retours

		self.letGoWorkerAnts = False 	# Booléen qui autorise le départ des fourmis ouvrières

		self.pathFound = False 	# Si un chemin commun a été trouvé par des fourmis
		self.lastFoundPath = [] 	# Enregistre le dernier chemin trouvé
		self.commonPathsNumber = 0 	# Nombre de chemins trouvés à la suite par les fourmis

		while (abs(self.anthill[0] - self.food[0]) + (abs(self.anthill[1] - self.food[1]))) < self.width: 	# On calcule la distance en X et en Y, on additionne et on veut que ce soit au moins aussi loin qu'une largeur

			self.anthill = (randint(0, self.width-1), randint(0, self.width-1))
			self.food = (randint(0, self.width-1), randint(0, self.width-1)) 	# Définition des coordonnées X et Y de la fourmilière et de la nourriture

		self.ants = [] 	# Création d'une liste vide qui contiendra toutes nos fourmis

		for i in range(self.workerAntsNumber):
			newAnt = Ant(1, self.anthill) 	# Création d'une fourmi ouvrière à la fourmilière
			self.ants.append(newAnt) 	# Ajout de la nouvelle fourmi à la liste des fourmis du monde

		for i in range(self.scoutAntsNumber):
			newAnt = Ant(0, self.anthill) 	# Création d'une fourmi éclaireuse à la fourmilière
			self.ants.append(newAnt) 	# Ajout de la nouvelle fourmi à la liste des fourmis du monde

	def realOptimalDistance(self):

		lengthRealOptimalDistance = 0
		position = [self.food[0], self.food[1]]
		finalPosition = [self.anthill[0], self.anthill[1]]

		while position != finalPosition:

			if position[0] != finalPosition[0]:
				if position[0] < finalPosition[0]:
					position[0] = position[0] + 1
				else:
					position[0] = position[0] - 1

			if position[1] != finalPosition[1]:
				if position[1] < finalPosition[1]:
					position[1] = position[1] + 1
				else:
					position[1] = position[1] - 1

			lengthRealOptimalDistance = lengthRealOptimalDistance + 1

		return lengthRealOptimalDistance

	def returningAntsNumberPerCell(self):

		antsNumber = [[0 for i in range(self.width)] for j in range(self.width)] 	# Liste 2D du nombre de fourmis dans chaque case de la grille.

		for i in range(len(self.ants)): 	# On parcourt toutes les fourmis
			if self.ants[i].returning: 	# Si c'est une fourmi qui rentre
				antsNumber[self.ants[i].X][self.ants[i].Y] = antsNumber[self.ants[i].X][self.ants[i].Y] + 1 	# On ajoute notre fourmi grâce à sa case

		return antsNumber

	def antsNumberPerCell(self): 	# Pareil qu'avant, mais on ajoute aussi les fourmis à l'aller

		antsNumber = [[0 for i in range(self.width)] for j in range(self.width)]

		for i in range(len(self.ants)):
			antsNumber[self.ants[i].X][self.ants[i].Y] = antsNumber[self.ants[i].X][self.ants[i].Y] + 1

		return antsNumber

	def listAuthorizedCellsAround(self, ant): 	# Renvoie la liste de cases autour d'une fourmi qu'elle peut légalement emprunter

		Fx = ant.X 	# On enregistre en variable local la position de la fourmi pour avoir moins de texte à écrire
		Fy = ant.Y

		returning = ant.returning 	# Pareil pour si elle est à l'aller ou au retour

		cellsList = [] 	# Liste des cases possibles que l'on renverra

		for i in range(-1, 2): 	# Pour les delta X possibles autour de nous (donc -1, 0, 1)
			newX = Fx + i 	# Renommage de l'emplacement X potentiel
			if newX >= 0 and newX < self.width: 	# Si le X potentiel est dans la grille
				for j in range(-1, 2): 	# Pareil pour Y
					newY = Fy + j
					if newY >= 0 and newY < self.width:
						if i != 0 or j != 0: 	# Si on se déplace d'au moins une case sur un axe, la case potentielle est bien différente de celle actuelle
							if (not returning and not (newX == self.anthill[0] and newY == self.anthill[1])) or (returning and not (newX == self.food[0] and newY == self.food[1])):
								# Ce if au dessus autorise l'ajout de la carte si :
								# La case potentielle n'est pas la fourmilière et que l'on est à l'aller (empêchant la fourmi de rentrer chez elle sans avoir eu de nourriture)
								# Ou la case potentielle n'est pas la nourriture et qu'on est au retour (empêchant la fourmi de retourner sur la nourriture sans avoir déposé celle qu'elle avait déjà prise)
								if not ([newX, newY] in ant.visitedCells): 	# Si la case potentielle n'est pas encore visitée on l'ajoute
									cellsList.append([newX, newY]) 	# On ajoute la case potentielle

		return cellsList


	def chooseInterestingCellAround(self, antNumber): 	# Choisis LA case à visiter au prochain pour la fourmi numeroFourmi

		ant = self.ants[antNumber] 	# On récupère toutes les infos de la fourmi

		decision = None 	# On initialise le futur choix
		pheromoneSum = 0 	# On initialise la somme des phéromones autour de la fourmi

		possibleDecisions = self.listAuthorizedCellsAround(ant) 	# On récupère la liste des cases légales autour de la fourmi
		if len(possibleDecisions) == 0: 	# Si jamais il n'y aucune case de disponible (généralement parce qu'on les a déjà toutes visitées)
			self.ants[antNumber].visitedCells = [] 	# On reset son historique de cases visitées
			possibleDecisions = self.listAuthorizedCellsAround(ant) 	# On redemande la liste des cases autour de la fourmi

		for i in range(len(possibleDecisions)): 	# Pour tous les choix possibles
			X = possibleDecisions[i][0] 	# On initialise le X et le Y de ce choix en variable locale de boucle
			Y = possibleDecisions[i][1]
			if (X == self.anthill[0] and Y == self.anthill[1] and ant.returning) or (X == self.food[0] and Y == self.food[1] and not ant.returning):
			# Si on est au retour et que le choix possible est la fourmilière
			# Ou que on est à l'aller et que le choix possible est la nourriture	
				decision = [X, Y] 	# On enregistre ce choix comme choix final directement
				break 	# On arrête la boucle car on se fiche des autres choix possibles
			else: 	# Si on est pas à côte de la nourriture ou de la fourmilière quand on veut y aller
				pheromoneSum = pheromoneSum + self.pheromones[X][Y] 	# On augmente la somme des phéromones autour avec celle de la case potentielle

		if decision != None: 	# Si le choix est différent de None, c'est qu'on a privilégié la fourmilière ou la nourriture dans la boucle précédente. On peut directement renvoyer ce choix.
			return decision 	# On retourne le choix et la fonction s'arrête ici

		probabilitiesList = [None for i in range(len(possibleDecisions))] 	# On initialise la liste des probabilités pour chaque choix possible

		if pheromoneSum == 0: 	# Si aucune case autour n'a de phéromones
			decisionNumber = randint(0, len(possibleDecisions)-1) 	# On en choisis une au hasard
			decision = possibleDecisions[decisionNumber] 	# On enregistre la case pour la retourner à la fin de la fonction

		else: 	# Si il y a des phéromones autour
			probability = 0 	# Proba utilisée pour la comparaison
			choosenProbability = randint(0, 99) / 100 	# Tirage entre 0 et 1
			for i in range(0, len(possibleDecisions)): 	# Pour tous les choix possibles
				X = possibleDecisions[i][0] 	# Renommage du X et du Y du choix actuel
				Y = possibleDecisions[i][1]
				pheromones = self.pheromones[X][Y] 	# On récupère le taux de phéromones de la case actuelle
				probability = (pheromones/pheromoneSum) + probability 	# On ajoute la proba de cette case à la somme des proba précédentes
				if probability > choosenProbability: 	# Si on a dépassé notre tirage, c'est cette case qu'on veut
					decision = possibleDecisions[i] 	# On l'enregistre
					break 	# On arrête la boucle car on a trouvé notre case

		return decision



	def moveAnts(self):

		for i in range(len(self.ants)): 	# On parcourt toutes les fourmis de notre monde
			
			if self.ants[i].antType == 1: 	# Si c'est une ouvrière
				
				if self.letGoWorkerAnts: 	# Et que on l'a autorisée à partir car au moins une fourmi éclaireuse est revenue
					newPosition = self.chooseInterestingCellAround(i) 	# On récupère sa nouvelle position
					
					self.ants[i].visitedCells.append([self.ants[i].X, self.ants[i].Y]) 	# On ajoute sa position actuelle dans la liste des cases déjà visitées
					self.ants[i].X = newPosition[0] 	# On met à jour sa position actuelle avec la nouvelle position
					self.ants[i].Y = newPosition[1]

			elif self.ants[i].antType == 0 and not (self.ants[i].X == self.anthill[0] and self.ants[i].Y == self.anthill[1] and self.ants[i].returning == True):
			# Ou si c'est une fourmi éclaireuse et que elle n'est pas encore rentrée

				moveX = 0 	# On initialise son delta de déplacement
				moveY = 0

				for j in range(-1, 2): 	# Pour tous les déplacements possibles en X
					newX = self.ants[i].X + j 	# Renommage
					for k in range(-1, 2): 	# Pareil Y
						newY = self.ants[i].Y + k
						if (self.ants[i].returning and newX == self.anthill[0] and newY == self.anthill[1]) or (not self.ants[i].returning and newX == self.food[0] and newY == self.food[1]):
						# Si on est à côte de la fourmilière au retour ou à côte de la nourriture à l'aller on y va sans hésiter
						# Vu qu'au moins une de ces valeurs sera différente de 0, on saute la boucle suivante et de cette façon notre fourmilière ou nourriture sera privilégiée	
							moveX = j
							moveY = k

				while (moveX == 0 and moveY == 0) or (self.ants[i].X + moveX) < 0 or (self.ants[i].Y + moveY) < 0 or (self.ants[i].X + moveX) >= self.width or (self.ants[i].Y + moveY) >= self.width:
				# On recalcule le delta de déplacement tant que au moins une de ces conditions est valide :
				# Tant que la fourmi ne bouge pas du tout
				# Tant que sa nouvelle position serait en dehors de la grille
					moveX = randint(-1, 1)
					moveY = randint(-1, 1)

				self.ants[i].visitedCells.append([self.ants[i].X, self.ants[i].Y]) 	# On ajoute sa position actuelle dans la liste des cases déjà visitées
				self.ants[i].X = self.ants[i].X + moveX 	# On enregistre la nouvelle position
				self.ants[i].Y = self.ants[i].Y + moveY

			self.changeAntState(i) 	# On met l'état de la fourmi à jour

	def changeAntState(self, antNumber):

		if self.ants[antNumber].X == self.food[0] and self.ants[antNumber].Y == self.food[1]: 	# Si la fourmi est sur la nourriture
			self.ants[antNumber].returning = True 	# On la met au retour
			self.ants[antNumber].visitedCells = [] 	# On reset ses cases déjà visitée

		elif self.ants[antNumber].X == self.anthill[0] and self.ants[antNumber].Y == self.anthill[1]: 	# Si on est à la fourmilière
			
			if self.ants[antNumber].returning: 	# Si notre furmi est au retour
				
				if self.ants[antNumber].antType == 0 and self.letGoWorkerAnts == False: 	# Si c'est une éclaireuse et que les ouvrières ne sont pas partis
					self.letGoWorkerAnts = True 	# On fait partir les ouvrières
				
				elif self.ants[antNumber].antType == 1: 	# Si c'est une ouvrière
					
					self.broughtFood = self.broughtFood + 1 	# On augmente le compteur d'allers / retours
					
					if self.ants[antNumber].visitedCells == self.lastFoundPath: 	# Si le chemin emprunté par cette fourmi est le même que celui d'avant
						self.commonPathsNumber = self.commonPathsNumber + 1 	# On augmente le nombre de chemins pareils
					else: 	# Si c'est pas le même que la fourmi précédente
						self.commonPathsNumber = 1 	# On reset le compteur de chemins
						self.lastFoundPath = self.ants[antNumber].visitedCells 	# On enregistre ce chemin comme étant le dernier trouvé
				
				self.ants[antNumber].returning = False 	# On la remet en position aller
				self.ants[antNumber].visitedCells = [] 	# On reset les cases visitées

	def leaveAllPheromones3(self):

		antsNumber = self.returningAntsNumberPerCell() 	# On récupère une liste 2D de la grille avec le nombre de fourmis en retour sur chaque case

		for i in range(self.width): 	# Pour tous les X
			for j in range(self.width): 	# Pour tous les Y
				self.pheromones[i][j] = ((1-self.decreaseRate)*self.pheromones[i][j]) + antsNumber[i][j]**(self.width)
				# pheromones[X][Y] = (1-tauxDecrementation)*pheromones[X][Y] + fourmisRetour[X][Y]^largeur

	def leaveAllPheromones4(self):

		addedPheromones = [[0 for i in range(self.width)] for j in range(self.width)]

		for i in range(len(self.ants)):
			# if self.fourmis[i].retour:
			if 1:
				addedPheromones[self.ants[i].X][self.ants[i].Y] = addedPheromones[self.ants[i].X][self.ants[i].Y] + (1/(len(self.ants[i].visitedCells)+1))**(self.width)

		for i in range(self.width):
			for j in range(self.width):
				self.pheromones[i][j] = ((1-self.decreaseRate)*self.pheromones[i][j]) + addedPheromones[i][j]**(self.width)


	def checkConvergence(self):
		if self.commonPathsNumber > self.workerAntsNumber/4:
			self.pathFound = True

	def loop(self): 	# La fonction qui fait un tour de programme
		self.moveAnts()
		self.leaveAllPheromones3()
		self.checkConvergence()


class Ant: 	# La classe des fourmis
	# 0 = fourmi éclaireuse
	# 1 = fourmi ouvrière
	def __init__(self, antType, anthillCoordinates):

		self.antType = antType

		if self.antType == 0:
			self.antName = "Scout"
		elif self.antType == 1:
			self.antName = "Worker"

		self.X = anthillCoordinates[0]
		self.Y = anthillCoordinates[1]

		self.returning = False 	# Vaut False si la fourmi cherche et True si la fourmi a trouvé (elle fait le chemin retour)

		self.visitedCells = []
