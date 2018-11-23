from Model import *

width = 10
ScoutAnts = width
WorkerAnts = 10*width
DecreaseRate = 0.7

world = Monde(width, ScoutAnts, WorkerAnts, DecreaseRate)

while not world.cheminTrouve:
	world.effectuerTourProgramme()

print("Food: {}".format(world.nourriture))
print("Used path: {}".format(world.dernierCheminTrouve))
print("Anthill: {}".format(world.fourmiliere))

print("\nOptimal distance: {}".format(world.distanceCheminReellementOptimal()))
print("Used distance: {}".format(len(world.dernierCheminTrouve)+1))