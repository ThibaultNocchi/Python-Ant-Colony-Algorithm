from math import *
from random import randint

class World:

	def __init__(self, width, scoutAntsNumber, workerAntsNumber, decreaseRate): 	# Fonction appelée quand on créé un monde
		"""
		Initializes the world with all its parameters, its agents (the ants).

		Parameters
		---------------------------------------------------------------------
		width : int
			Size of a side of the world.
		scoutAntsNumber : int
			Number of scout ants who will roam the world.
		workerAntsNumber : int
			Number of worker ants who will roam the world.
		decreaseRate : float
			Decrease rate of the pheromones, between 0 and 1. A higher value means the pheromones will evaporate faster.
		"""

		self.pheromones = [[0 for i in range(width)] for j in range(width)] 	# 2x2 matrix to store the pheromones level in each cell, with X being the first dimension and Y the second.
		self.width = width 	# Saving size for later use.

		self.decreaseRate = decreaseRate 		# Decrease rate.

		self.workerAntsNumber = workerAntsNumber
		self.scoutAntsNumber = scoutAntsNumber 	# Number of each ants.

		self.anthill = [0, 0]
		self.food = [0, 0] 	# X and Y coordinates of the anthill and food locations.
		# They are set up at the same location so that the while placing them later will see them in the same cell and loop at least once.

		self.broughtFood = 0 			# Number of food brought back to the anthill, it is equivalent to the number of round trips.

		self.letGoWorkerAnts = False 	# Boolean to check whether worker ants can start looking for food and leave the anthill.

		self.pathFound = False 			# Boolean put to True when the algorithm decides a path has converged.
		self.lastFoundPath = [] 		# Saves the last found path.
		self.commonPathsNumber = 0 		# Number of consecutive identical successful paths made by the ants.

		# We want the distance between the food and the anthill to be at least the size of a side of the world.
		while (abs(self.anthill[0] - self.food[0]) + (abs(self.anthill[1] - self.food[1]))) < self.width:

			# Randomizing coordinates.
			self.anthill = (randint(0, self.width-1), randint(0, self.width-1))
			self.food = (randint(0, self.width-1), randint(0, self.width-1))

		self.ants = [] 	# Empty list which will contain all different ants.

		# Creating and adding to the ant list the required number of worker ants.
		for i in range(self.workerAntsNumber):
			newAnt = Ant(1, self.anthill)
			self.ants.append(newAnt)

		# Creating and adding to the ant list the required number of scout ants.
		for i in range(self.scoutAntsNumber):
			newAnt = Ant(0, self.anthill)
			self.ants.append(newAnt)

	def realOptimalDistance(self):
		"""
		Calculates the real optimal distance the ants could have taken.

		Returns
		---------------------------------------------------------------
		int
			Real optimal distance between the food and the anthill.
		"""

		lengthRealOptimalDistance = 0 						# Optimal distance to return.
		position = [self.food[0], self.food[1]] 			# We start our fake ant from the food.
		finalPosition = [self.anthill[0], self.anthill[1]] 	# It needs to reach the anthill.

		# While our fake ant hasn't reached the anthill, we make it walk the most straighter line by moving it one X and Y to the destination at the same time.
		# This is the longest move an ant can do in a turn.
		# If it is on one axis of the anthill, it only needs to walk along the other axis.
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
		"""
		Returns the number of ants going to the anthill on each cell.

		Returns
		-------------------------------------------------------------
		list
			2x2 matrix containing the number of returning ants in each cell, wuth X being the first dimension and Y the second.
		"""

		antsNumber = [[0 for i in range(self.width)] for j in range(self.width)] 								# Preparing the 2x2 matrix.

		for i in range(len(self.ants)): 																		# For each ant.
			if self.ants[i].returning: 																			# If this ant is coming home.
				antsNumber[self.ants[i].X][self.ants[i].Y] = antsNumber[self.ants[i].X][self.ants[i].Y] + 1 	# We increase the counter in its position.

		return antsNumber

	def antsNumberPerCell(self):
		"""
		Returns the number of ants on each cell.

		Returns
		----------------------------------------
		list
			2x2 matrix containing the number of ants in each cell, wuth X being the first dimension and Y the second.
		"""

		antsNumber = [[0 for i in range(self.width)] for j in range(self.width)] 							# Preparing the 2x2 matrix.

		for i in range(len(self.ants)): 																	# For each ant.
			antsNumber[self.ants[i].X][self.ants[i].Y] = antsNumber[self.ants[i].X][self.ants[i].Y] + 1 	# We increase the counter in its position.

		return antsNumber

	def listAuthorizedCellsAround(self, ant):
		"""
		Returns a list of cells directly around an ant she can move into next loop.

		Parameters
		---------------------------------------------------------------------------
		ant : Ant
			An ant we need to decide on.

		Returns
		---------------------------------------------------------------------------
		list
			List of coordinates the ant can move into the next loop. Coordinates are list with the first element being the X and the second the Y.
		"""

		Ax = ant.X 	# Reducing the variables name of the ant's position.
		Ay = ant.Y

		returning = ant.returning 	# Same for its returning state.

		cellsList = [] 	# List of available cells.

		for i in range(-1, 2): 						# For a range of movement on the X axis going from -1 to 1. (So a case to the left, the same one, on the right).
			newX = Ax + i 							# Naming the potential new X value.
			if newX >= 0 and newX < self.width: 	# If the newly calculated X isn't outside the world.
				for j in range(-1, 2): 				# We calculate a new Y the same way.
					newY = Ay + j
					if newY >= 0 and newY < self.width:
						if i != 0 or j != 0: 		# If the ant will at least move from its current cell next loop. (i and j are differences on X and Y from the current cell)
							if (not returning and not (newX == self.anthill[0] and newY == self.anthill[1])) or (returning and not (newX == self.food[0] and newY == self.food[1])):
								# This if statement only adds the newly found cell if :
								# The ant is seeking for food (not returning) and doesn't want to enter the anthill (blocking the ant from going home without food)
								# OR
								# The ant is seeking its home (returning) and doesn't want to enter the food cell (blocking the ant from getting another piece of food without dropping it at the anthill first)
								if not ([newX, newY] in ant.visitedCells): 	# Finally, if we didn't already visit this cell
									cellsList.append([newX, newY]) 			# We add it to the list of available cells.

		return cellsList


	def chooseInterestingCellAround(self, antNumber):
		"""
		Decides of the cell to visit next loop.

		Parameters
		---------------------------------------
		antNumber : int
			Index of the ant in our world.

		Returns
		---------------------------------------
		list
			A set of coordinates where the ant needs to go, with X being the first element and Y the second.
		"""

		ant = self.ants[antNumber] 	# Getting the ant "locally".

		decision = None 	# Initializing the future choice.
		pheromoneSum = 0 	# Pheromone sum of the available cells around.

		possibleDecisions = self.listAuthorizedCellsAround(ant) 		# Getting the legally available cells around.
		if len(possibleDecisions) == 0: 								# If no cell is available (usually because we already visited them all once).
			self.ants[antNumber].visitedCells = [] 						# We reset the history of visited cells.
			possibleDecisions = self.listAuthorizedCellsAround(ant) 	# We retry getting the list of available cells.

		for i in range(len(possibleDecisions)): 	# For every available cell.
			X = possibleDecisions[i][0] 	# We store its coordinates in local variables.
			Y = possibleDecisions[i][1]
			if (X == self.anthill[0] and Y == self.anthill[1] and ant.returning) or (X == self.food[0] and Y == self.food[1] and not ant.returning):
			# If the ant is returning to the anthill and the available cell is the anthill
			# OR
			# the ant is not returning (going for food) and the available cell is the food cell
				decision = [X, Y] 	# We directly save this choice.
				break 				# We stop the loop because we won't care about other available cells.
			else: 														# But if the ant isn't next to the food or the anthill when it needs to go to it.
				pheromoneSum = pheromoneSum + self.pheromones[X][Y] 	# We increase the counter of pheromones with the available cell value.

		if decision != None: 	# If the decision isn't None, it is because we already decided on the next cell.
			return decision 	# So we return the result.

		probabilitiesList = [None for i in range(len(possibleDecisions))] 	# Initializing a list of probabilities for each available cell.

		if pheromoneSum == 0: 	# If no available cell has pheromones.
			decisionNumber = randint(0, len(possibleDecisions)-1) 	# We randomly choose one.
			decision = possibleDecisions[decisionNumber] 			# And we save it to return it at the end.

		else: 	# But if available cells have pheromones.
			probability = 0 	# Probability used to compare with the picked probability.
			choosenProbability = randint(0, 99) / 100 	# Random pick between 0 and 1.
			for i in range(0, len(possibleDecisions)): 	# For every available cell.
				X = possibleDecisions[i][0] 	# We save its X and Y coordinate.
				Y = possibleDecisions[i][1]
				pheromones = self.pheromones[X][Y] 	#  We get its level of pheromones.
				probability += (pheromones/pheromoneSum) 	# We increase the moving probability with the cell probability.
				if probability > choosenProbability: 	# If the moving probability passed the picked probability, it means it is this cell we want.
					decision = possibleDecisions[i] 	# We save it.
					break 	# We stop the loop because we found our cell.
		# Let's explain how this moving probability was done.
		# Imagine we have 3 cells, with 20%, 50% and 30% chances of being picked.
		# We have repartition like this: C1 C1 C2 C2 C2 C2 C2 C3 C3 C3
		# We then pick a random number, let's say 0.82.
		# We start with a probability of 0.
		# We add the probability of picking the first cell: now probability is 0.2.
		# 0.2 isn't superior to 0.82.
		# We retry with the second cell: probability now is 0.7. But 0.7 < 0.82.
		# Finally probability is 1 and is superior to 0.82. We decide to pick C3.
		# This way, we can have probabilities attached to a list of elements, and we just need to pick a number and add the probabilities.
		# It is just like picking a random item among 100 by its position. Except here coordinates have frequencies attached to them.
		# I hope it was clear, if you need more explanation or think it is wrong, please contact me. :)

		return decision



	def moveAnts(self):
		""" Move all world's ants. """

		for i in range(len(self.ants)): 	# For each ant of our world.
			
			if self.ants[i].antType == 1: 	# If it is a worker.
				
				if self.letGoWorkerAnts: 	# And if workers are authorized to move around because at least one scout has come back.
					newPosition = self.chooseInterestingCellAround(i) 	# We get its new position.
					
					self.ants[i].visitedCells.append([self.ants[i].X, self.ants[i].Y]) 	# We add its current position to its list of visited cells.
					self.ants[i].X = newPosition[0] 	# And we move it into its new position.
					self.ants[i].Y = newPosition[1]

			# Or it is a scout ant and it hasn't returned yet.
			elif self.ants[i].antType == 0 and not (self.ants[i].X == self.anthill[0] and self.ants[i].Y == self.anthill[1] and self.ants[i].returning == True):

				moveX = 0 	# We intialize its movements.
				moveY = 0

				for j in range(-1, 2): 			# For each move available on the X axis.
					newX = self.ants[i].X + j 	# We save it.
					for k in range(-1, 2): 		# Same for Y.
						newY = self.ants[i].Y + k
						if (self.ants[i].returning and newX == self.anthill[0] and newY == self.anthill[1]) or (not self.ants[i].returning and newX == self.food[0] and newY == self.food[1]):
						# If we are next to the anthill when we are returning or next to the food when looking for it, we move into it.
						# We save those values, and as at least one of them will be different from 0, we will skip the next while.
							moveX = j
							moveY = k

				while (moveX == 0 and moveY == 0) or (self.ants[i].X + moveX) < 0 or (self.ants[i].Y + moveY) < 0 or (self.ants[i].X + moveX) >= self.width or (self.ants[i].Y + moveY) >= self.width:
				# We retry moving the and while one of these conditions is true:
				# The ant isn't moving (moves variables equal to 0)
				# The new position is outside the grid.
					moveX = randint(-1, 1) 	# We pick a random move on the X and Y axis.
					moveY = randint(-1, 1)

				self.ants[i].visitedCells.append([self.ants[i].X, self.ants[i].Y]) 	# We add the current position to the list of visited cells.
				self.ants[i].X = self.ants[i].X + moveX 	# We move the ant.
				self.ants[i].Y = self.ants[i].Y + moveY

			self.changeAntState(i) 	# We check the actions needed based on the new position of the ant.

	def changeAntState(self, antNumber):
		"""
		Checks the position of the ant and update different variables based on it. (returning, visited cells, number of food brought back...)

		Parameters
		-------------------------------------------------------------------------------------------------------------------------------------
		antNumber : int
			Number of the ant in the world's list of ants.
		"""

		if self.ants[antNumber].X == self.food[0] and self.ants[antNumber].Y == self.food[1]: 	# If the ant is on the food cell.
			self.ants[antNumber].returning = True 	# We put it in a returning state.
			self.ants[antNumber].visitedCells = [] 	# We reset its visited cells.

		elif self.ants[antNumber].X == self.anthill[0] and self.ants[antNumber].Y == self.anthill[1]: 	# If the ant is on the anthill.
			
			if self.ants[antNumber].returning: 	# If the ant was returning.
				
				if self.ants[antNumber].antType == 0 and self.letGoWorkerAnts == False: 	# If it is a scout and the workers haven't been released yet.
					self.letGoWorkerAnts = True 	# We let the workers go.
				
				elif self.ants[antNumber].antType == 1: 	# If it is a worker.
					
					self.broughtFood = self.broughtFood + 1 	# We increase by one the number of brought back food.
					
					if self.ants[antNumber].visitedCells == self.lastFoundPath: 	# If the path used by this ant was the same as the previous one.
						self.commonPathsNumber = self.commonPathsNumber + 1 	# We increase by one the number of consecutive common paths.
					else: 	# If it isn't the same path as the previous ant.
						self.commonPathsNumber = 1 	# We reset the counter of common paths.
						self.lastFoundPath = self.ants[antNumber].visitedCells 	# We erase the previous path with the ant's current one.
				
				self.ants[antNumber].returning = False 	# We put back the ant on the outward journey.
				self.ants[antNumber].visitedCells = [] 	# We reset its visited cells.

	def leaveAllPheromones3(self):
		""" Method which updates the number of pheromones on each cell based on the ants on it. """

		antsNumber = self.returningAntsNumberPerCell() 	# We get a 2x2 grid with the number of returning ant on each cell.

		for i in range(self.width): 	# For each X
			for j in range(self.width): 	# For each Y
				# First we apply the decreasing rate on the cell, then we add a certain number of pheromones based on the number of ants and the size of the world.
				# This is the subtle part of the algorithm, with the part of choosing the next cell for an ant.
				# To improve the algorithm, one would need to start from here.
				# Here is the current formula:
				# pheromones[X][Y] = (1-decreaseRate)*pheromones[X][Y] + returningAntsNumber[X][Y]^width
				self.pheromones[i][j] = ((1-self.decreaseRate)*self.pheromones[i][j]) + antsNumber[i][j]**(self.width)

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
		""" Checks whether we can assume a correct path was found. """
		if self.commonPathsNumber > self.workerAntsNumber/4: 	# If the number of same consecutive paths is a quarter of the number of ants, we assume it is at least a good one.
			self.pathFound = True

	def loop(self):
		""" The core of the program, the one which executes a round of our world. Moving the ants, updating the pheromones and checking if a path was found. """
		self.moveAnts()
		self.leaveAllPheromones3()
		self.checkConvergence()


class Ant:

	def __init__(self, antType, anthillCoordinates):
		"""
		Defines an ant.
		-----------------
		antType : int
			Type of the ant.
			0: Scount ant
			1: Worker ant
		anthillCoordinates : list
			List with at least 2 elements where the first represents the X coordinate and the second the Y coordinate of the anthill.
		"""

		self.antType = antType

		if self.antType == 0:
			self.antName = "Scout"
		elif self.antType == 1:
			self.antName = "Worker"

		self.X = anthillCoordinates[0]
		self.Y = anthillCoordinates[1]

		self.returning = False 	# False when the ant is looking for food, True when it is returning to its anthill.

		self.visitedCells = [] 	# On its way, the ant stores every cell it already visited.
