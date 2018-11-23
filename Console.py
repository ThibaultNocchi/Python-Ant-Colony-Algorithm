from Model import *

largeur = 10
fourmisEclaireuses = largeur
fourmisOuvrieres = 10*largeur
tauxDecroissement = 0.7

monMonde = Monde(largeur, fourmisEclaireuses, fourmisOuvrieres, tauxDecroissement)

while not monMonde.cheminTrouve:
	monMonde.effectuerTourProgramme()

print("Nourriture : {}".format(monMonde.nourriture))
print("Chemin trouvé : {}".format(monMonde.dernierCheminTrouve))
print("Fourmilière : {}".format(monMonde.fourmiliere))

print("\nDistance réellement optimale : {}".format(monMonde.distanceCheminReellementOptimal()))
print("Distance trouvée : {}".format(len(monMonde.dernierCheminTrouve)+1))