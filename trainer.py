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
		with open("data/dexwithmovesandtypes.json") as pdex:
			dex = json.load(pdex)
			for keys in sorted(dex.keys()):
				print(keys.capitalize())
			out = []
			for i in range(6):
				pname = input("{name}, please enter your choice of pokemon #{number} for your party:\n(Generation I)\n".format(name = self.name, number=len(out)+1))
				pname = pname.lower()
				while(pname not in dex):
					pname = input("Trainer, please enter your choice of pokemon #{number} for your party:\n(Generation I)\n".format(number=len(out)+1))
					pname = pname.lower()
				out.append(pokemon.Pokemon(dex[pname]))
		return out

