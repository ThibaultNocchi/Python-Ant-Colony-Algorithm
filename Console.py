from Model import *

width = 10
ScoutAnts = width
WorkerAnts = 10*width
DecreaseRate = 0.7

world = World(width, ScoutAnts, WorkerAnts, DecreaseRate)

while not world.pathFound:
	world.loop()

print("Food: {}".format(world.food))
print("Used path: {}".format(world.lastFoundPath))
print("Anthill: {}".format(world.anthill))

print("\nOptimal distance: {}".format(world.realOptimalDistance()))
print("Used distance: {}".format(len(world.lastFoundPath)+1))
