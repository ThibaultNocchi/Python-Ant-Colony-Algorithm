from Model import *

width = 10
scoutAnts = width
workerAnts = 10*width
decreaseRate = 0.7

world = World(width, scoutAnts, workerAnts, decreaseRate)

while not world.pathFound:
	world.loop()

print("Food: {}".format(world.food))
print("Used path: {}".format(world.lastFoundPath))
print("Anthill: {}".format(world.anthill))

print("\nOptimal distance: {}".format(world.realOptimalDistance()))
print("Used distance: {}".format(len(world.lastFoundPath)+1))
