import random
import math
import moves
import trainer
import json

class Pokemon():

	level = 100

	def __init__(self, poke, tname):
		self.name = poke["name"]
		self.baseHP = poke["baseStats"]["hp"]
		self.baseAtk = poke["baseStats"]["atk"]
		self.baseDef = poke["baseStats"]["def"]
		self.baseSpa = poke["baseStats"]["spa"]
		self.baseSpe = poke["baseStats"]["spe"]
		self.baseTot = self.baseHP + self.baseAtk + self.baseDef + self.baseSpa + self.baseSpe
		self.ivs = self.calcIVs()
		self.evs = self.calcEVs()
		self.statHP , self.statAtk, self. statDef, self.statSpa, self.statSpe =  self.calcStats(self.ivs, self.evs)
		self.moves = self.setMoves(poke, tname)
		self.Atklvl = 0
		self.Deflvl = 0
		self.Spalvl = 0
		self.Spelvl = 0

			
	def calcIVs(self):
		IVs = [int(15 * random.random()) for i in range(4)]
		hpiv  = ""
		for i in range(4):
			hpiv += str(bin(IVs[i]))[-1]
		HPiv = int(hpiv, 2)
		IVs.insert(0, HPiv)
		return IVs

	def calcEVs(self):
		EVs = [0,0,0,0,0]
		for i in range(len(EVs)):
			EVs[i] = int(random.random() * 65535)
		# print(EVs)
		return EVs

	def calcStats(self, ivs, evs):

		hp = math.floor(((((self.baseHP + ivs[0]) * 2) + (math.floor((math.ceil(evs[0]**0.5))/(4))))*(self.level))/(100)) + self.level + 10

		attack = math.floor(((((self.baseAtk + ivs[1]) * 2) + (math.floor((math.ceil(evs[1]**0.5))/(4))))*(self.level))/(100)) + 5

		defense = math.floor(((((self.baseDef + ivs[2]) * 2) + (math.floor((math.ceil(evs[2]**0.5))/(4))))*(self.level))/(100)) + 5

		special = math.floor(((((self.baseSpa + ivs[3]) * 2) + (math.floor((math.ceil(evs[3]**0.5))/(4))))*(self.level))/(100)) + 5

		speed = math.floor(((((self.baseSpe + ivs[4]) * 2) + (math.floor((math.ceil(evs[4]**0.5))/(4))))*(self.level))/(100)) + 5

		return hp, attack, defense, special, speed

	def setMoves(self, pokemon, trainerName):
		out = []
		names = []
		with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/gen1moves.json") as pdex:
			g1moves = json.load(pdex)
			if len(pokemon["learnset"]) > 4:
				print("\nChoose 4 of the following moves from the learnset once each:")
				# for key in sorted(pokemon["learnset"].keys()):
				print("\n".join("{name: >15}{mtype: >10}{pwr: >10}{power: >8}{acc: >10}{accuracy: >8}{PP: >10}{pp: >8}".format(name = str(g1moves[key]["name"]), mtype = str(g1moves[key]["type"]), pwr = "Pwr:", acc = "Acc:", PP = "PP:" , power = str(g1moves[key]["basePower"]), accuracy = str(g1moves[key]["accuracy"]), pp = str(g1moves[key]["pp"])) for key in sorted(pokemon["learnset"].keys())))
				for i in range(4):
					move = "buffer"	
					if len(out) != len(pokemon["learnset"]):
						while move not in pokemon["learnset"].keys() or move in names or move == "buffer":
							move = input("{trainerName}, please enter your choice of move for {name}\n".format(trainerName = trainerName, name = self.name))
							move = move.lower().replace(" ", "").replace("-", "")
						print("\nYou chose {move} as {pkmn}'s #{num} move!".format(move = pokemon["learnset"][move], pkmn = self.name, num = len(out) + 1))
						out.append(moves.Move(move))
						names.append(move)
						print("Moves selected so far:", names)
			else:
				for key in pokemon["learnset"].keys():
					out.append(moves.Move(key))
					print("{name} has 4 or less moves in their moveset, you can have 'em all!\n".format(name = pokemon["name"]))
		return out
	


	def getStats(self):
		return self.statHP, self.statAtk, self. statDef, self.statSpa, self.statSpe

	def getBase(self):
		return self.baseHP, self.baseAtk, self.baseDef, self.baseSpa, self.baseSpe



		



# poke = {
# 		"baseStats": {
# 			"atk": 20,
# 			"def": 15,
# 			"hp": 25,
# 			"spa": 105,
# 			"spd": 105,
# 			"spe": 90
# 		},
# 		"heightm": 0.9,
# 		"inherit": True,
# 		"learnset": [
# 			"mimic",
# 			"bide",
# 			"rest",
# 			"rage",
# 			"counter",
# 			"dreameater",
# 			"skullbash",
# 			"lightscreen",
# 			"metronome",
# 			"doubleedge",
# 			"submission",
# 			"psywave",
# 			"takedown",
# 			"psychic",
# 			"swift",
# 			"seismictoss",
# 			"thunderwave",
# 			"reflect",
# 			"substitute",
# 			"triattack"
# 		],
# 		"name": "Abra",
# 		"types": [
# 			"Psychic"
# 		],
# 		"weightkg": 19.5
# 	}

# abra = Pokemon(poke)

# print(abra.getStats(), abra.getBase())

