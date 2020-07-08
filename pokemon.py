import random
import math
import moveset
import trainer
import json
import sys

#Pokemon class for use in pkmnCLI1, contained by Trainers, each Pokemon contains Moves (none of these classes extend one another)
class Pokemon():

	def __init__(self, pokemon, isRandom):
		#taking values from passed in dictionary value
		self.level = 100
		self.name = pokemon["name"]
		self.baseHP = pokemon["baseStats"]["hp"]
		self.baseAtk = pokemon["baseStats"]["atk"]
		self.baseDef = pokemon["baseStats"]["def"]
		self.baseSpa = pokemon["baseStats"]["spa"]
		self.baseSpe = pokemon["baseStats"]["spe"]
		self.type = pokemon["types"]
		self.height = pokemon["heightm"]
		self.weight = pokemon["weightkg"]
		self.active = False
		self.idtag = random.randint(0, 100000000)
		#calculate IVs and EVs for stat calculation, battStats are for manipulation with move multipliers during battle
		self.ivs = self.calcIVs()
		self.evs = self.calcEVs(isRandom)
		self.statHP , self.statAtk, self. statDef, self.statSpa, self.statSpe =  self.calcStats(self.ivs, self.evs)
		self.battHP, self.battAtk, self.battDef, self.battSpa, self.battSpe = self.statHP , self.statAtk, self. statDef, self.statSpa, self.statSpe
		self.statAcc = -1
		self.statEva = -1
		self.battAcc = 255
		self.battEva = 255
		self.nonVolatileStatus = None
		self.nonVolatileCount = 0
		self.volatileStatus = "None"
		self.volatileCount = 0
		self.isRecharging = False
		self.isCharging = False
		self.isConfused = False
		self.isConfusedCount = 0
		self.willFlinch = False
		self.disabledMove = [0, 0]
		self.isFocusEnergy = False

		#choosing moves
		self.moves = []
		
		#stat multipliers for use in battle
		self.Atklvl = 0
		self.Deflvl = 0
		self.Spalvl = 0
		self.Spelvl = 0
		self.Acclvl = 0
		self.Evalvl = 0


	#randomly samples a number between 0 and 15 for Atk, Def, Spa, and Spa. Takes final bit of binary representations of all 4 stats to form final binary representation of HP IV value 		
	def calcIVs(self):
		IVs = [random.randint(0, 16) for i in range(4)]
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
				EVs[i] = random.randint(0, 65535)
		else:
			for i in range(len(EVs)):
				EVs[i] = 65535
			# print(EVs)
		return EVs


	#takes IVs and EVs along with base stats and converts them into full stats 
	def calcStats(self, ivs, evs):

		hp = math.floor(((((self.baseHP + ivs[0]) * 2) + (math.floor((math.ceil(evs[0]**0.5))/(4))))*(self.level))/(100)) + self.level + 10
		if hp > 888:
			hp = 888

		attack = math.floor(((((self.baseAtk + ivs[1]) * 2) + (math.floor((math.ceil(evs[1]**0.5))/(4))))*(self.level))/(100)) + 5
		if attack > 888:
			attack = 888

		defense = math.floor(((((self.baseDef + ivs[2]) * 2) + (math.floor((math.ceil(evs[2]**0.5))/(4))))*(self.level))/(100)) + 5
		if defense > 888:
			defense = 888

		special = math.floor(((((self.baseSpa + ivs[3]) * 2) + (math.floor((math.ceil(evs[3]**0.5))/(4))))*(self.level))/(100)) + 5
		if special > 888:
			special = 888
		
		speed = math.floor(((((self.baseSpe + ivs[4]) * 2) + (math.floor((math.ceil(evs[4]**0.5))/(4))))*(self.level))/(100)) + 5
		if speed > 888:
			speed = 888
		
		return hp, attack, defense, special, speed


	def getStats(self):
		return self.statHP, self.statAtk, self. statDef, self.statSpa, self.statSpe


	def getBase(self):
		return self.baseHP, self.baseAtk, self.baseDef, self.baseSpa, self.baseSpe


	#prints full list of moveset to terminal with headings
	def printMoves(self):
		header = "{pos: <9}{name: <15}{mtype: <10}{base: <10}{acc: <9}{pp: <8}\n".format(pos = "", name = "MOVENAME", mtype = "TYPE", base = "BASEPOWER", acc = "ACCURACY", pp = "PP")

		out = "\n".join("{pos: <9}{name: <15}{mtype: <10}{power: <10}{accuracy: <9}{pp: <8}".format(pos = "", name = move.name, mtype = move.type, power = str(move.basePower), accuracy = str(move.accuracy), pp = str(move.pp)) for move in self.moves)
		out = header + out
		print(out)


	def battlePrintMoves(self):
		letters = validChoices = ["a","b","c","d"]
		header = "{pos: <9}{name: <15}{mtype: <10}{pp: <8}\n".format(pos = "", name = "MOVENAME", mtype = "TYPE", pp = "PP")

		out = "\n".join("{pos: <9}{name: <15}{mtype: <10}{pp: <8}".format(pos = letters[i] + ")", name = self.moves[i].name, mtype = self.moves[i].type, pp = str(self.moves[i].pp)) for i in range(len(self.moves)))
		out = header + out
		print(out)


