import pokemon
import json
import math
import string
import moves

class Trainer():

	def __init__(self):
		name = input("Trainer, please enter your name:\n(up to 10 characters)\n")
		while(len(name) > 10):
			name = input("Trainer, please enter your name:\n(up to 10 characters)\n")
		self.name = name.capitalize()
		self.party = self.chooseParty()

		

	def chooseParty(self):
		with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/pokedexwmoves.json") as pdex:
			dex = json.load(pdex)
			print("Generation I Pokedex:\n")
			for keys in sorted(dex.keys()):
				print(keys.capitalize())
			out = []
			for i in range(6):
				pname = input("\n{name}, please enter your choice of pokemon #{number} for your party:\n".format(name = self.name, number=len(out)+1))
				pname = pname.lower()
				while(pname not in dex):
					pname = input("Trainer, please enter your choice of pokemon #{number} for your party:\n(Generation I)\n".format(number=len(out)+1))
					pname = pname.lower()
				out.append(pokemon.Pokemon(dex[pname], self.name))
		return out

