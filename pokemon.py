import random
import math
import moves
import trainer
import json

#Pokemon class for use in pkmnCLI1, contained by Trainers, each Pokemon contains Moves (none of these classes extend one another)
class Pokemon():

	level = 100

	def __init__(self, pokemon, trainername, isRandom):
		#taking values rom passed in dictionary
		self.name = pokemon["name"]
		self.baseHP = pokemon["baseStats"]["hp"]
		self.baseAtk = pokemon["baseStats"]["atk"]
		self.baseDef = pokemon["baseStats"]["def"]
		self.baseSpa = pokemon["baseStats"]["spa"]
		self.baseSpe = pokemon["baseStats"]["spe"]
		self.type = pokemon["types"]
		self.height = pokemon["heightm"]
		self.weight = pokemon["weightkg"]

		#calculate IVs and EVs for stat calculation
		self.ivs = self.calcIVs()
		self.evs = self.calcEVs(isRandom)
		self.statHP , self.statAtk, self. statDef, self.statSpa, self.statSpe =  self.calcStats(self.ivs, self.evs)
		
		#choosing moves
		self.moves = []
		self.setMoves(pokemon, trainername, self.moves)
		
		#stat multipliers for use in battle
		self.Atklvl = 0
		self.Deflvl = 0
		self.Spalvl = 0
		self.Spelvl = 0

	#randomly samples a number between 0 and 15 for Atk, Def, Spa, and Spa. Takes final bit of binary representations of all 4 stats to form final binary representation of HP IV value 		
	def calcIVs(self):
		IVs = [int(15 * random.random()) for i in range(4)]
		hpiv  = ""
		for i in range(4):
			hpiv += str(bin(IVs[i]))[-1]
		HPiv = int(hpiv, 2)
		IVs.insert(0, HPiv)
		return IVs

	#calculates EV values for each of the stats, this can either be maxed out or randomly assigned
	def calcEVs(self, isRandom):
		EVs = [0,0,0,0,0]
		if isRandom == "y":
			for i in range(len(EVs)):
				EVs[i] = int(random.random() * 65535)
		else:
			for i in range(len(EVs)):
				EVs[i] = 65535
			# print(EVs)
		return EVs

	#takes IVs and EVs along with base stats and converts them into full stats 
	def calcStats(self, ivs, evs):

		hp = math.floor(((((self.baseHP + ivs[0]) * 2) + (math.floor((math.ceil(evs[0]**0.5))/(4))))*(self.level))/(100)) + self.level + 10

		attack = math.floor(((((self.baseAtk + ivs[1]) * 2) + (math.floor((math.ceil(evs[1]**0.5))/(4))))*(self.level))/(100)) + 5

		defense = math.floor(((((self.baseDef + ivs[2]) * 2) + (math.floor((math.ceil(evs[2]**0.5))/(4))))*(self.level))/(100)) + 5

		special = math.floor(((((self.baseSpa + ivs[3]) * 2) + (math.floor((math.ceil(evs[3]**0.5))/(4))))*(self.level))/(100)) + 5

		speed = math.floor(((((self.baseSpe + ivs[4]) * 2) + (math.floor((math.ceil(evs[4]**0.5))/(4))))*(self.level))/(100)) + 5

		return hp, attack, defense, special, speed

	#trainer makes choice of moves from pokemon's learnset
	def setMoves(self, pokemon, trainerName, out):
		#keeps list of movenames chosen so far, easier to keep track of than to examine instantiated Move objects
		names = []

		#reads in full list of moves available in Generation I
		with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/gen1moves.json") as pdex:
			g1moves = json.load(pdex)

			#check there are more than 4 moves to choose from (Magikarp I'm looking at YOU)
			if len(pokemon["learnset"]) > 4:

				#displays full list of moves pokemon can learn
				print("\nChoose 4 of the following moves from the learnset once each:")
				print("{name: <15}{mtype: <10}{base: <10}{acc: <7}{pp: <5}".format(name = "MOVENAME", mtype = "TYPE", base = "BASEPOWER", acc = "ACCURACY", pp = "PP"))
				print("\n".join("{name: <15}{mtype: <10}{power: <10}{accuracy: <7}{pp: <5}".format(name = str(g1moves[key]["name"]), mtype = str(g1moves[key]["type"]), power = str(g1moves[key]["basePower"]), accuracy = str(g1moves[key]["accuracy"]), pp = str(g1moves[key]["pp"])) for key in sorted(pokemon["learnset"].keys())))

				#trainer now makes 4 choices on moves
				while len(out) < 4:
					#trainer can input any combination of capitalisation spaces and hyphens, can input individually or as comma separated list in terminal
					movechoices = "buffer"	
					movechoices = input("\n{trainerName}, please complete your choice of moves for {name} (comma separated)\nYou have {places} moves left to choose:\n".format(trainerName = trainerName, name = self.name, places = 4 - len(out)))
					movechoices = movechoices.lower().split(",")
					movechoices = [move.replace(" ", "").replace("-", "") for move in movechoices]
					if len(out) != len(pokemon["learnset"]):
						for move in movechoices:
							if move in pokemon["learnset"].keys() and move not in names:
								if len(out) <4:
									if len(out) == 0:
										print("You chose {move} as {pkmn}'s first move!".format(move = pokemon["learnset"][move], pkmn = self.name))	
									elif len(out) == 1:
										print("You chose {move} as {pkmn}'s second move!".format(move = pokemon["learnset"][move], pkmn = self.name))
									elif len(out) == 2:
										print("You chose {move} as {pkmn}'s third move!".format(move = pokemon["learnset"][move], pkmn = self.name))
									elif len(out) == 3:
										print("You chose {move} as {pkmn}'s final move!".format(move = pokemon["learnset"][move], pkmn = self.name))
									out.append(moves.Move(move))
									names.append(move)
					#prints current moveset to remind trainer as moves can only be added to moveset once each
					print("\nCurrent moveset:")
					self.printMoves()				
			else:
				for key in pokemon["learnset"].keys():
					out.append(moves.Move(key))
					print("{name} has 4 or less moves in their moveset, you can have 'em all!\n".format(name = pokemon["name"]))
		return
	


	def getStats(self):
		return self.statHP, self.statAtk, self. statDef, self.statSpa, self.statSpe

	def getBase(self):
		return self.baseHP, self.baseAtk, self.baseDef, self.baseSpa, self.baseSpe

	#prints full list of moveset to terminal with headings
	def printMoves(self):
		header = "{pos: <6}{name: <15}{mtype: <10}{base: <10}{acc: <9}{pp: <8}\n".format(pos = "", name = "MOVENAME", mtype = "TYPE", base = "BASEPOWER", acc = "ACCURACY", pp = "PP")

		out = "\n".join("{pos: <6}{name: <15}{mtype: <10}{power: <10}{accuracy: <9}{pp: <8}".format(pos = "", name = move.name, mtype = move.type, power = str(move.basePower), accuracy = str(move.accuracy), pp = str(move.pp)) for move in self.moves)
		out = header + out
		print(out)

