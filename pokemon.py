import random
import math
import moves
setup party setup in trainer module
class Pokemon():

	level = 100

	def __init__(self, poke):
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
		# self.moves = setMoves(poke, learnset)

			
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

	def setMoves(self, poke, learnset):
		pass

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

