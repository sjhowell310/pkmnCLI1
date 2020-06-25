import pokemon
import json
import math
import string
import moves

class Trainer():

	def __init__(self, partySize):
		name = input("\nTrainer, please enter your name:\n(up to 10 characters)\n")
		while(len(name) >10):
			name = input("\nTrainer, please enter your name:\n(up to 10 characters)\n")
		self.name = name.capitalize()
		self.party = []
		self.chooseParty(partySize, self.party)

		

	def chooseParty(self, partySize, party):
		with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/pokedexwmoves.json") as pdex:
			dex = json.load(pdex)
			print("Gen I Pokedex:\n")
			# dex = sorted(dex.items() ,  key=lambda x: x[1]["id"])
			# print(dex)
			# for key in dex[1:]:
			# 	# 
			print("{index: <5}{name: <12}{type: <18}{hp: <4}{atk: <8}{dfn: <8}{spa: <8}{spe: <8}".format(index = "#", name = "NAME", type = "TYPE(s)", hp = "HP", atk = "ATTACK", dfn = "DEFENCE", spa = "SPECIAL", spe = "SPEED"))
			for i in range(1, len(dex.keys())):
				for key in dex.keys():
					if dex[key]["id"] == i:
						# print(i, key.capitalize())
						print("{index: <5}{name: <12}{type: <18}{hp: <4}{atk: <8}{dfn: <8}{spa: <8}{spe: <8}".format(index = str(dex[key]["id"]), name = dex[key]["name"], type = ", ".join(dex[key]["types"]), hp = str(dex[key]["baseStats"]["hp"]), atk = str(dex[key]["baseStats"]["atk"]), dfn = str(dex[key]["baseStats"]["def"]), spa = str(dex[key]["baseStats"]["spa"]), spe = str(dex[key]["baseStats"]["spe"])))
			# 	print(key[0])
			for i in range(partySize):
				pname = input("\n{name}, please enter your choice of pokemon #{number} for your party:\n".format(name = self.name, number=len(party)+1))
				pname = pname.lower()
				while(pname not in dex):
					pname = input("\n{name}, please enter your choice of pokemon #{number} for your party:\n".format(name = self.name, number=len(party)+1))
					pname = pname.lower()
				party.append(pokemon.Pokemon(dex[pname], self.name))
		return

	def showPartywMoves(self):
		print("\n{name}'s party and their movesets:".format(name = self.name))
		i = 0
		for pokemon in self.party:
			i +=1
			print("\n{pos: <5} {name: <12}{type: <18}{hp: <4}{atk: <7}{dfn: <8}{spa: <8}{spe: <8}".format(pos = str(i) + ")", name = "NAME", type = "TYPE(s)", hp = "HP", atk = "ATTACK", dfn = "DEFENCE", spa = "SPECIAL", spe = "SPEED"))
			print("{pos: <6}{name: <12}{type: <18}{hp: <4}{atk: <7}{dfn: <8}{spa: <8}{spe: <8}\n".format(pos= "", name = pokemon.name, type = ", ".join(pokemon.type), hp = str(pokemon.statHP), atk = str(pokemon.statAtk), dfn = str(pokemon.statDef), spa = str(pokemon.statSpa), spe = str(pokemon.statSpe)))
			pokemon.printMoves()
