import json
import string

def runsetup():
	trainer1name = input("Trainer 1, please enter your name:\n(up to 10 characters in length)\n")
	while(len(trainer1name) > 10):
		trainer1name = input("Trainer 1, please enter your name:\n(up to 10 characters in length)\n")


	with open("data/dexwithmovesandtypes.json") as dex:
		pdex = json.load(dex)
	print("Please choose your party from the pokedex:\n(Up to 6 pokemon)\n")
	for pkmn in pdex.keys():
		print(pdex[pkmn]["name"], pdex[pkmn]["types"])
