import Model
import pygame
from pygame.locals import *
from time import sleep
import argparse

class Screen: 	# Screen class to interact with the screen

	def __init__(self, L, antHill, food, elementSize = 30, borderSize = 1, margin = 40):
		"""
		Screen class to interact with the screen.

		Parameters
		-----------------------------------------
		L : int
			Size of the side of our world (number of cells on a side).
		antHill : list
			Coordinates of the anthill.
		food : list
			Coordinates of the food cell.
		elementSize : int
			Width in pixels of a cell.
		borderSize : int
			Width in pixels of the border of a cell.
		margin : int
			Width in pixels between the edge of the grid of the world and the edge of the window.
		"""

		self.L = L

		self.antHill = antHill
		self.food = food

		self.elementSize = elementSize
		self.borderSize = borderSize

		self.margin = margin
		# A cell measures its number of pixels + only a border (not two because when drawing cells, the next one will overwrite the common border instead of adding to it). So the screen needs to be the number of cells * the size of a cell + the left and right (or up and bottom) margins we want.
		self.ScreenLength = L*(self.elementSize + self.borderSize) + 2*self.margin
		self.XText = self.margin / 2 	# We display the text in the margin.
		self.YText = self.margin / 4
		self.SXText = 0 	# Attributes which will store the size on X and Y of the displayed text in order to clean it when refreshing it.
		self.SYText = 0

		self.window = None 	# Pygame window.

		# Drawing a pure black square the size of a cell with its borders.
		self.basicRect = pygame.Surface((self.elementSize+2*self.borderSize, self.elementSize+2*self.borderSize))
		self.basicRect.fill(Color("black"))

		# Drawing a pure white square the size of a cell without its borders, then we add it in the middle of the previous black square.
		# This way we have a cell to copy and paste everywhere.
		self.innerRect = pygame.Surface((self.elementSize, self.elementSize))
		self.innerRect.fill(Color("white"))
		self.basicRect.blit(self.innerRect, (self.borderSize, self.borderSize))

		pygame.init() 	# Starting the screen.

		self.opened = False 	# If the screen is opened.

		self.font = pygame.font.Font(pygame.font.get_default_font(), 14) 	# Initializing the font to print the brought back food.

	def drawText(self, text, X, Y, SX, SY):
		"""
		Draw a text at X and Y position, and returns the size it takes

		Parameters
		--------------------------------------------------------------
		text : string
			Text to display.
		X : int
			X coordinate to display the text.
		Y : int
			Y coordinate to display the text.
		SX : int
			X size of the rectangle from the X coordinate to erase to white before.
		SY : int
			Y size of the rectangle from the Y coordinate to erase to white before.

		Returns
		----------------------------------------------------------------
		list
			X and Y length of the newly displayed text.
		"""

		pygame.draw.rect(self.window, Color("white"), (X, Y, SX, SY)) 	# Erasing the previous location.
		self.window.blit(self.font.render(text, True, Color("black")), (X, Y)) 	# Renders the text and adds it to the window
		return self.font.size(text) 										# Returns the text size

	def startScreen(self):
		""" Starts the screen. """

		self.window = pygame.display.set_mode((self.ScreenLength, self.ScreenLength)) 	# Opens the window.
		pygame.display.set_caption("Ants GUI") 	# Names the window.

		self.window.fill(Color("white")) 	# Fills the window with white.

		X = self.margin 	# Puts the X cursor at a margin distance.
		
		for i in range(self.L): 	# For each X cell.
			for j in range(self.L): 	# For each Y cell.
				coords = self.getPygameCornerOfCell(i,j) 	# Gets the coordinates in pixels of the cell.
				self.window.blit(self.basicRect, coords) 	# Draws the cell with the borders (basicRect).

		antHillCoords = self.getPygameCornerOfCell(self.antHill[0], self.antHill[1]) 	# Get the coordinates in pixels of the cell where the anthill should be.
		self.changeInnerRectColor("brown") 	# We change the color of the inner part of the cells to be drawnq to brown.
		self.window.blit(self.basicRect, antHillCoords) 	# We display this new inner cell on the previous cell.

		foodCoords = self.getPygameCornerOfCell(self.food[0], self.food[1]) 	# Same method for the food cell, but with green color.
		self.changeInnerRectColor("green")
		self.window.blit(self.basicRect, foodCoords)


		pygame.display.update() 	# We refresh the screen.
		self.opened = True 	# We say the screen is now opened.

	def getPygameCornerOfCell(self, cellX, cellY):
		"""
		Calculates the coordinates of the edge of a cell.

		Parameters
		-------------------------------------------------
		cellX : int
			Cell's number on the X axis.
		cellY : int
			Cell's number on the Y axis.

		Returns
		-------------------------------------------------
		list
			X and Y positions of the cell in pixels.
		"""

		PosX = cellX*(self.elementSize+self.borderSize) + self.margin

		PosY = self.L - cellY - 1
		PosY = PosY*(self.elementSize+self.borderSize) + self.margin

		return (PosX, PosY)

	def changeInnerRectColor(self, color="white"):
		"""
		Changes the color of the inner part of a cell and updates the basic rect with the borders.
		It also blocks the RGB value into 0 and 255.

		Parameters
		color : string or list
			The name of a color or the RGB values.
		------------------------------------------------------------------------------------------
		"""
		if isinstance(color, tuple):
			if(color[0] > 255): color = (255, color[1], color[2])
			if(color[1] > 255): color = (color[0], 255, color[2])
			if(color[2] > 255): color = (color[0], color[1], 255)
			if(color[0] < 0): color = (0, color[1], color[2])
			if(color[1] < 0): color = (color[0], 0, color[2])
			if(color[2] < 0): color = (color[0], color[1], 0)
			self.innerRect.fill(Color(color[0], color[1], color[2], 255))
		else:
			self.innerRect.fill(Color(color))
		self.basicRect.blit(self.innerRect, (self.borderSize, self.borderSize))

	def updateScore(self, score):
		"""
		Updates the display of the number of food brought back. It also updates the X and Y length of the text.
		
		Parameters
		-------------------------------------------------------------------------------------------------------
		score : int
			Number of food brought back.
		"""
		pos = self.drawText("Round trip(s) : {}".format(score), self.XText, self.YText, self.SXText, self.SYText)
		self.SXText = pos[0]
		self.SYText = pos[1]

	def updatePheromones(self, pheromones):
		"""
		Displays the level of pheromones in each cell.

		Parameters
		----------------------------------------------
		pheromones : list
			2x2 matrix with pheromones in cell [X][Y].
		"""

		for i in range(len(pheromones)): 		# For each X cell.
			for j in range(len(pheromones)): 	# For each Y cell.

				if not ((i == self.antHill[0] and j == self.antHill[1]) or (i == self.food[0] and j == self.food[1])): 	# If the cell isn't the food or the anthill we will change its color.
					cellCoords = self.getPygameCornerOfCell(i, j) 	# Gets the coordinates of the cell.
					rgb = 255-round(pheromones[i][j]) 				# Calculates the RGB level in grey for the level of pheromones (more pheromones is darker).
					self.changeInnerRectColor((rgb, rgb, rgb)) 		# Changes the color of the inner part of the square.
					self.window.blit(self.basicRect, cellCoords) 	# Displays the new cell.

	def updateAnts(self, ants):
		"""
		Displays the number of ants in each cell in level of grey.

		Parameters
		----------------------------------------------------------
		ants : list
			2x2 matrix with the number of ants in cell [X][Y].
		"""

		for i in range(len(ants)): 		# For each X cell.
			for j in range(len(ants)): 	# For each Y cell.
				if not ((i == self.antHill[0] and j == self.antHill[1]) or (i == self.food[0] and j == self.food[1])): 	# If the cell isn't the food or the anthill we will change its color.
					cellCoords = self.getPygameCornerOfCell(i, j) 	# Gets the coordinates of the cell.
					rgb = 255-round(ants[i][j])*10 					# Calculates the RGB level in grey for the number of ants (more ants is darker).
					self.changeInnerRectColor((rgb, rgb, rgb)) 		# Changes the color of the inner part of the square.
					self.window.blit(self.basicRect, cellCoords) 	# Displays the new cell.


	def listen(self):
		""" Method to check for events (QUIT event or the escape key, to also quit). """
		for event in pygame.event.get(): 													# For each event in the queue
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 	# QUIT or Escape key.
				self.opened = False
				pygame.quit() 																# We stop the game



def check_positive(value):
	""" Checks if the given value is positive. Used for the command line. """
	ivalue = int(value)
	if ivalue <= 0:
		raise argparse.ArgumentTypeError("argument needs to be positive")
	return ivalue


def check_0_1(value):
	""" Checks if the given value is between 0 and 1. Used for the command line. """
	fvalue = float(value)
	if fvalue < 0 or fvalue > 1:
		raise argparse.ArgumentTypeError("argument needs to be between 0 and 1")
	return fvalue


parser = argparse.ArgumentParser("Console.py", description="Runs a simulation of the algorithm and displays the resulted path.")
parser.add_argument("--width", help="Side size of the world. (Default: 10)", type=check_positive)
parser.add_argument("-s", "--scouts", help="Number of scout ants. (Default: width)", type=check_positive)
parser.add_argument("-w", "--workers", help="Number of worker ants. (Default: 10*width)", type=check_positive)
parser.add_argument("-r", "--rate", help="Pheromones decrease rate between 0 and 1. (Default: 0.7)", type=check_0_1)
args = parser.parse_args()

if args.width:
	width = args.width
else:
	width = 10

if args.scouts:
	scoutAnts = args.scouts
else:
	scoutAnts = width

if args.workers:
	workerAnts = args.workers
else:
	workerAnts = 10*width

if(args.rate):
	decreaseRate = args.rate
else:
	decreaseRate = 0.7

world = Model.World(width, scoutAnts, workerAnts, decreaseRate)
screen = Screen(world.width, world.anthill, world.food)
screen.startScreen()

while screen.opened:
	world.loop() 									# Does a world's loop.
	screen.updateAnts(world.antsNumberPerCell()) 	# Update the ants number in displayed cells.
	screen.updateScore(world.broughtFood) 			# Update the number of brought back food.
	pygame.display.update() 						# Refresh the screen.
	screen.listen() 								# Check for events.
	sleep(0.016) 									# Waits for 0.016s. (to display at 60 fps).
