from Model import *
import argparse

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError("argument needs to be positive")
    return ivalue

def check_0_1(value):
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

world = World(width, scoutAnts, workerAnts, decreaseRate)

while not world.pathFound:
	world.loop()

print("Food: {}".format(world.food))
print("Used path: {}".format(world.lastFoundPath))
print("Anthill: {}".format(world.anthill))

print("\nOptimal distance: {}".format(world.realOptimalDistance()))
print("Used distance: {}".format(len(world.lastFoundPath)+1))
