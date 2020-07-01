import trainer
import json
import math
import string
import pokemon
import moveset
import time
import random


#Battle class for use in pkmnCLI1, contains Trainers, weather effects and other holistic battle mechanics (none of these classes extend one another)
class Battle():

	weather = "Clear"

	#trainer objects are mounted to the battle object, they contain parties of pokemon with full stats and movesets
	def __init__(self, t1, t2):
		self.t1 = t1
		self.t2 = t2


	#function prints the name of each trainer, their in battle pokemon, and their hp to terminal before moves are decided upon
	def printBattle(self):
		print("\n{name1: <30}{name2: >30}".format(name1 = self.t1.name, name2 = self.t2.name))
		print("{name1: <30}{name2: >30}".format(name1 = self.t1.activePokemon.name, name2 = self.t2.activePokemon.name))
		print("{hp: <3}{currhp1: >4}/{tothp1: <4}{status1: >7}{stat1: <4}{space: >14}{hp: >3}{currhp2: >4}/{tothp2: <4}{status1: >7}{stat2: >4}".format(hp = "HP:", currhp1 = str(self.t1.activePokemon.battHP), tothp1 = str(self.t1.activePokemon.statHP), status1 = "Status:", stat1 = str(self.t1.activePokemon.status), currhp2 = str(self.t2.activePokemon.battHP), tothp2 = str(self.t2.activePokemon.statHP), stat2 = str(self.t2.activePokemon.status), space = ""))


	#function that checks through each party and counted number of fainted pokemon, if all pokemon of either party are fainted, this is white out and the player with the whited out party loses
	def isWhiteOut(self):
		count1 = len(self.t1.party)
		count2 = len(self.t2.party)
		for member in self.t1.party:
			if member.battHP == 0:
				count1 -= 1
		for member in self.t2.party:
			if member.battHP == 0:
				count2 -= 1
		if count1 == 0 or count2 == 0:
			return True
		else:
			return False

	#function which delegates what actions happen in what order after trainers have made their choices
	def action(self, t1action, t2action):
		t1action = t1action.split("-")
		t2action = t2action.split("-")
		t1a = t1action[0]
		t1c = int(t1action[1])
		t2a = t2action[0]
		t2c = int(t2action[1])
		if t1a == "switch" or t2a == "switch":
			if t1a == "switch" and t2a == "attack":			
				self.t1.switchIn(self.t1.party[t1c])		
				self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2)
			elif t1a == "attack" and t2a == "switch":		
				self.t2.switchIn(self.t2.party[t2c])
				self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 2)
			elif t1a == "switch" and t2a == "switch":
				self.t1.switchIn(self.t1.party[t1c])
				self.t2.switchIn(self.t2.party[t2c])
		else:
			if self.t1.activePokemon.moves[t1c]["priority"] > self.t2.activePokemon.moves[t2c]["priority"]:				
				self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1)				
				self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2)
			elif self.t1.activePokemon.moves[t1c]["priority"] < self.t2.activePokemon.moves[t2c]["priority"]:				
				self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 1)
				
				self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 2)
			elif self.t1.activePokemon.moves[t1c]["priority"] == self.t2.activePokemon.moves[t2c]["priority"] 
				if self.t1.activePokemon.battSpe > self.t2.activePokemon.battSpe:					
					self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1)					
					self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2)
				elif self.t1.activePokemon.battSpe < self.t2.activePokemon.battSpe:					
					self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 1)					
					self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 2)
				elif self.t1.activePokemon.battSpe == self.t2.activePokemon.battSpe:
					rand = random.random()
					if rand < 0.5:						
						self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1)				
						self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2)
					else:
						self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1)				
						self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2)						


	def attack(off, att, dfn, firstorsecond):
		if off.nonVolatileStatus == "Asleep" or off.nonVolatileStatus == "Frozen":
			off.nonVolatileStatus -= 1
			if off.nonVolatileCount == 0:
				if off.nonVolatileStatus == "Asleep":
					time.sleep(1)
					print("{name} woke up!\n".format(name = off.name))
				if off.nonVolatileStatus == "Frozen":
					time.sleep(1)
					print("{name} thawed!\n".format(name = off.name))
		if off.isRecharging:
			isRecharging = False
			time.sleep(1)
			print("{name} has to recharge!\n".format(name = off.name))
			return
		if firstorsecond == 2:
			if willFlinch == True:
				print("{name} flinched!!\n".format(name = off.name))
				return
		if off.disabledMove[0] > 0:
			off.disabledMove[0] -= 1
			
