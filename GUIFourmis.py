import Model
import pygame
from pygame.locals import *
from time import sleep

class Screen: 	# Screen class to interact with the screen

	def __init__(self, L, fourmiliere, nourriture, elementSize = 30, borderSize = 1, margin = 100):

		self.L = L

		self.fourmiliere = fourmiliere
		self.nourriture = nourriture

		self.elementSize = elementSize
		self.borderSize = borderSize

		self.margin = margin
		self.ScreenL = L*(self.elementSize + self.borderSize) + self.margin

		self.XText = self.margin / 4
		self.YText = self.margin / 8
		self.SXText = 0
		self.SYText = 0

		self.grid = [[0 for i in range(self.L)] for j in range(self.L)]

		self.window = None

		self.basicRect = pygame.Surface((self.elementSize+2*self.borderSize, self.elementSize+2*self.borderSize))
		self.basicRect.fill(Color("black"))

		self.innerRect = pygame.Surface((self.elementSize, self.elementSize))
		self.innerRect.fill(Color("white"))
		self.basicRect.blit(self.innerRect, (self.borderSize, self.borderSize))

		pygame.init()

		self.opened = False

		self.font = pygame.font.Font(pygame.font.get_default_font(), 14)

	def drawText(self, text, X, Y, SX, SY): # Draw a text at X and Y position, and returns the size it takes

		pygame.draw.rect(self.window, Color("white"), (X, Y, SX, SY))
		self.window.blit(self.font.render(text, True, Color("black")), (X, Y)) 	# Renders the text and adds it to the window
		return self.font.size(text) 										# Returns the text size

	def startScreen(self):
		self.window = pygame.display.set_mode((self.ScreenL, self.ScreenL))
		pygame.display.set_caption("GUI Fourmis")

		self.window.fill(Color("white"))

		X = self.margin / 2
		

		for i in range(self.L):
			Y = self.margin / 2
			for j in range(self.L):
				self.window.blit(self.basicRect, (X, Y))
				Y += self.elementSize + self.borderSize
			X += self.elementSize + self.borderSize

		fourmiliereCoords = self.getPygameCornerOfCell(self.fourmiliere[0], self.fourmiliere[1])
		self.changeInnerRectColor("brown")
		self.window.blit(self.basicRect, fourmiliereCoords)

		nourritureCoords = self.getPygameCornerOfCell(self.nourriture[0], self.nourriture[1])
		self.changeInnerRectColor("green")
		self.window.blit(self.basicRect, nourritureCoords)


		pygame.display.update()
		self.opened = True

	def getPygameCornerOfCell(self, cellX, cellY):

		PosX = cellX*(self.elementSize+self.borderSize) + self.margin/2

		PosY = self.L - cellY - 1
		PosY = PosY*(self.elementSize+self.borderSize) + self.margin/2

		return (PosX, PosY)

	def changeInnerRectColor(self, color="white"):
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
		pos = self.drawText("A/R : {}".format(score), self.XText, self.YText, self.SXText, self.SYText)
		self.SXText = pos[0]
		self.SYText = pos[1]

	def updatePheromones(self, pheromones):

		for i in range(len(pheromones)):
			for j in range(len(pheromones)):

				if not ((i == self.fourmiliere[0] and j == self.fourmiliere[1]) or (i == self.nourriture[0] and j == self.nourriture[1])):
					cellCoords = self.getPygameCornerOfCell(i, j)
					rgb = 255-round(pheromones[i][j])
					self.changeInnerRectColor((rgb, rgb, rgb))
					self.window.blit(self.basicRect, cellCoords)

	def updateAnts(self, ants):

		for i in range(len(ants)):
			for j in range(len(ants)):
				if not ((i == self.fourmiliere[0] and j == self.fourmiliere[1]) or (i == self.nourriture[0] and j == self.nourriture[1])):
					cellCoords = self.getPygameCornerOfCell(i, j)
					rgb = 255-round(ants[i][j])*10
					self.changeInnerRectColor((rgb, rgb, rgb))
					self.window.blit(self.basicRect, cellCoords)


	def listen(self):
		for event in pygame.event.get(): 	# For each event in the queue
			if event.type == QUIT: 	# QUIT
				self.opened = False
				pygame.quit() 	# We stop the game


largeur = 10
fourmisEclaireuses = largeur
fourmisOuvrieres = 10*largeur
tauxDecroissement = 0.7

monMonde = Model.Monde(largeur, fourmisEclaireuses, fourmisOuvrieres, tauxDecroissement)
myScreen = Screen(monMonde.largeur, monMonde.fourmiliere, monMonde.nourriture)
myScreen.startScreen()

while myScreen.opened:
	monMonde.effectuerTourProgramme()
	myScreen.updateAnts(monMonde.nombreFourmisParPosition())
	myScreen.updateScore(monMonde.nourritureApportee)
	pygame.display.update()
	myScreen.listen()
	sleep(0.016)

print(monMonde.dernierCheminTrouve)