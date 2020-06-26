import pokemon
import json
import math
import string
import moves

#Trainer class for use in pkmnCLI1, contained by Arena class, contains Pokemon in party (none of these classes extend one another)
class Trainer():

	#declare init for instantiation
	def __init__(self, partySize, isRandom):
		#take name as in put from command line
		name = input("\nTrainer, please enter your name:\n(up to 10 characters)\n")

		#check input is valid, if not, prompt again until valid
		while(len(name) >10):
			name = input("\nTrainer, please enter your name:\n(up to 10 characters)\n")
		self.name = name.capitalize()
		self.party = []
		self.chooseParty(partySize, self.party, isRandom)

		
	#function to handle selection of pokemon in trainers party
	def chooseParty(self, partySize, party, isRandom):
		#read in pokedex json file which includes learnsets for each pokemon
		with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/pokedexwmoves.json") as pdex:
			dex = json.load(pdex)

			#print pokedex out in index order (i.e. the order of the original pokedex)
			print("Gen I Pokedex:\n")
			print("{index: <5}{name: <12}{type: <18}{hp: <4}{atk: <8}{dfn: <8}{spa: <8}{spe: <8}".format(index = "#", name = "NAME", type = "TYPE(s)", hp = "HP", atk = "ATTACK", dfn = "DEFENCE", spa = "SPECIAL", spe = "SPEED"))

			#cycle through index numbers
			for i in range(1, len(dex.keys())):
				#finds key which contains next index number (this is clunky but it works, efficiency is not of the essence)
				for key in dex.keys():
					if dex[key]["id"] == i:
						print("{index: <5}{name: <12}{type: <18}{hp: <4}{atk: <8}{dfn: <8}{spa: <8}{spe: <8}".format(index = str(dex[key]["id"]), name = dex[key]["name"], type = ", ".join(dex[key]["types"]), hp = str(dex[key]["baseStats"]["hp"]), atk = str(dex[key]["baseStats"]["atk"]), dfn = str(dex[key]["baseStats"]["def"]), spa = str(dex[key]["baseStats"]["spa"]), spe = str(dex[key]["baseStats"]["spe"])))
			#select predetermined number of pokemon to add to party (limited to 6 in Arena object)
			for i in range(partySize):
				#prompt user for name of pokemon they'd like to add, if not contained in pokedex, reprompt until valid input is passed
				pname = input("\n{name}, please enter your choice of pokemon #{number} for your party:\n".format(name = self.name, number=len(party)+1))
				pname = pname.lower()
				while(pname not in dex):
					pname = input("\n{name}, please enter your choice of pokemon #{number} for your party:\n".format(name = self.name, number=len(party)+1))
					pname = pname.lower()
				#selected pokemon is added to trainers party
				party.append(pokemon.Pokemon(dex[pname], self.name, isRandom))
		return

	#function which prints entire party to terminal along with each members moveset
	def showPartywMoves(self):
		print("\n{name}'s party and their movesets:".format(name = self.name))
		i = 0
		for pokemon in self.party:
			i +=1
			print("\n{pos: <5} {name: <12}{type: <18}{hp: <4}{atk: <7}{dfn: <8}{spa: <8}{spe: <8}".format(pos = str(i) + ")", name = "NAME", type = "TYPE(s)", hp = "HP", atk = "ATTACK", dfn = "DEFENCE", spa = "SPECIAL", spe = "SPEED"))
			print("{pos: <6}{name: <12}{type: <18}{hp: <4}{atk: <7}{dfn: <8}{spa: <8}{spe: <8}\n".format(pos= "", name = pokemon.name, type = ", ".join(pokemon.type), hp = str(pokemon.statHP), atk = str(pokemon.statAtk), dfn = str(pokemon.statDef), spa = str(pokemon.statSpa), spe = str(pokemon.statSpe)))
			pokemon.printMoves()
