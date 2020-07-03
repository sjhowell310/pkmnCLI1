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
				self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2, self.t2)
			elif t1a == "attack" and t2a == "switch":		
				self.t2.switchIn(self.t2.party[t2c])
				self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 2, self.t1)
			elif t1a == "switch" and t2a == "switch":
				self.t1.switchIn(self.t1.party[t1c])
				self.t2.switchIn(self.t2.party[t2c])
		else:
			if self.t1.activePokemon.moves[t1c]["priority"] > self.t2.activePokemon.moves[t2c]["priority"]:				
				self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1, self.t1)	
				self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2, self.t2)

			elif self.t1.activePokemon.moves[t1c]["priority"] < self.t2.activePokemon.moves[t2c]["priority"]:				
				self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 1, self.t2)
				self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 2, self.t1)

			elif self.t1.activePokemon.moves[t1c]["priority"] == self.t2.activePokemon.moves[t2c]["priority"]:
				if self.t1.activePokemon.battSpe > self.t2.activePokemon.battSpe:					
					self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1, self.t1)				
					self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2, self.t2)

				elif self.t1.activePokemon.battSpe < self.t2.activePokemon.battSpe:					
					self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 1, self.t2)	
					self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 2, self.t1)

				elif self.t1.activePokemon.battSpe == self.t2.activePokemon.battSpe:
					rand = random.random()
					if rand < 0.5:						
						self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1)				
						self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2)
					else:
						self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1)				
						self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2)						


	def attack(self, off, att, dfn, firstorsecond, trainer):
		cantAttack = False

		if firstorsecond == 1:
			if off.nonVolatileStatus == "Frozen":
				time.sleep(1)
				print("{name} is frozen solid!\n".format(name = off.name))
				cantAttack = True
			else:
				if off.nonVolatileStatus == "Asleep":
					off.nonVolatileCount -= 1
					if off.nonVolatileCount > 0:
						time.sleep(1)
						print("{name} is fast asleep!\n".format(name = off.name))
						cantAttack = True
					else:
						time.sleep(1)
						off.nonVolatileStatus = "None"
						off.nonVolatileCount = 0
						print("{name} woke up!\n".format(name = off.name))
						cantAttack = True
						if off.isRecharging:
							time.sleep(1)
							print("{name} has to recharge!\n".format(name = off.name))
							cantAttack = True
							off.isRecharging = False
						else:
							if off.disabledMove[0] > 0:
								off.disabledMove[0] -= 1
								if off.disabledMove[0] == 0:
									off.disabledMove[1]
									time.sleep(1)
									print("{name}'s {movename} is no longer disabled!\n".format(name = off.name, movename = att.name))
							if off.isConfused:
								time.sleep(1)
								print("{name} is confused!\n".format(name = off.name))
								off.isConfusedCount -= 1
								if off.isConfusedCount == 0:
									time.sleep(1)
									print("{name} snapped out of it!\n".format(name = off.name))
									off.isConfused = False
									off.isConfusedCount = 0
									if off.nonVolatileStatus == "Paralyzed":
										rand = random.random()
										if rand < 0.25:
											time.sleep(1)
											print("{name} is fully paralyzed and can't move!\n".format(name = off.name))
											cantAttack = True
								else:
									if off.nonVolatileStatus == "Paralyzed":
										rand = random.random()
										if rand < 0.25:
											time.sleep(1)
											print("{name} is fully paralyzed and can't move!\n".format(name = off.name))
											cantAttack = True
									rand = random.random()
									if rand < 0.5:
										time.sleep(1)
										print("{name} hurt itself in its confusion!\n".format(name = off.name))
										off.takeConfusionDamage()
										cantAttack = True
										if off.battHP == 0:
											time.sleep(1)
											print("{name} fainted!".format(off.name))
											if isWhiteOut():
												return
											else:
												madeChoice = False
												while not madeChoice:
													print("Choose which member of your party to switch in:")
													trainer.battleShowParty()
													options = len(trainer.party)
													validChoices = ["a","b","c","d", "e", "f"]
													print("\n(Enter letter of desired option)\n")
													a1 = input()
													a1 = a1.lower()
													while a1 not in validChoices[:options+1]:
														print("\n(Enter letter of desired option)\n")
														a1 = input()
														a1 = a1.lower()
													if a1 == "a":
														if trainer.activePokemon.idtag == trainer.party[validChoices.index(a1)].idtag and trainer.activePokemon.battHP == trainer.party[validChoices.index(a1)].battHP:
															print("{name} is already in battle!\n".format(name = trainer.activePokemon.name))
														elif trainer.party[validChoices.index(a1)].battHP == 0:
															print("{name} doesn't have any energy left to battle!\n".format(name = trainer.activePokemon.name))
														else:
															trainer.switchIn(trainer.party[validChoices.index(a1)])
															madeChoice = True
															return
													elif a1 == "b":
														if trainer.activePokemon.idtag == trainer.party[validChoices.index(a1)].idtag and trainer.activePokemon.battHP == trainer.party[validChoices.index(a1)].battHP:
															print("{name} is already in battle!\n".format(name = trainer.activePokemon.name))
														elif trainer.party[validChoices.index(a1)].battHP == 0:
															print("{name} doesn't have any energy left to battle!\n".format(name = trainer.activePokemon.name))
														else:
															trainer.switchIn(trainer.party[validChoices.index(a1)])
															madeChoice = True
															return
													elif a1 == "c":
														if trainer.activePokemon.idtag == trainer.party[validChoices.index(a1)].idtag and trainer.activePokemon.battHP == trainer.party[validChoices.index(a1)].battHP:
															print("{name} is already in battle!\n".format(name = trainer.activePokemon.name))	
														elif trainer.party[validChoices.index(a1)].battHP == 0:
															print("{name} doesn't have any energy left to battle!\n".format(name = trainer.activePokemon.name))
														else:
															trainer.switchIn(trainer.party[validChoices.index(a1)])
															madeChoice = True
															return
													elif a1 == "d":
														if trainer.activePokemon.idtag == trainer.party[validChoices.index(a1)].idtag and trainer.activePokemon.battHP == trainer.party[validChoices.index(a1)].battHP:
															print("{name} is already in battle!\n".format(name = trainer.activePokemon.name))						
														elif trainer.party[validChoices.index(a1)].battHP == 0:
															print("{name} doesn't have any energy left to battle!\n".format(name = trainer.activePokemon.name))
														else:
															trainer.switchIn(trainer.party[validChoices.index(a1)])
															madeChoice = True
															return
													elif a1 == "e":
														if trainer.activePokemon.idtag == trainer.party[validChoices.index(a1)].idtag and trainer.activePokemon.battHP == trainer.party[validChoices.index(a1)].battHP:
															print("{name} is already in battle!\n".format(name = trainer.activePokemon.name))						
														elif trainer.party[validChoices.index(a1)].battHP == 0:
															print("{name} doesn't have any energy left to battle!\n".format(name = trainer.activePokemon.name))
														else:
															trainer.switchIn(trainer.party[validChoices.index(a1)])
															madeChoice = True
															return
													elif a1 == "f":
														if trainer.activePokemon.idtag == trainer.party[validChoices.index(a1)].idtag and trainer.activePokemon.battHP == trainer.party[validChoices.index(a1)].battHP:
															print("{name} is already in battle!\n".format(name = trainer.activePokemon.name))						
														elif trainer.party[validChoices.index(a1)].battHP == 0:
															print("{name} doesn't have any energy left to battle!\n".format(name = trainer.activePokemon.name))
														else:
															trainer.switchIn(trainer.party[validChoices.index(a1)])
															madeChoice = True
															return
							
			if not cantAttack:					
				att.pp -= 1
				if att.name != "Swift":
					willHit = self.isHit(off, att, dfn)
				else:
					willHit = True
				if not willHit:
					time.sleep(1)
					print("{name} used {movename}!\n".format(name = off.name, movename = att.name))
					if off.Acclvl >= dfn.Evalvl:
					time.sleep(1)
					print("{name} missed!\n".format(name = off.name))
				else:
					time.sleep(1)
					print("{name} used {movename}!\n".format(name = off.name, movename = att.name))
					results = self.useAttack(off, att, dfn)

					self.takeHP(dfn, results[0])
					if results[1]:
						time.sleep(1)
						print("Critical hit!")
					if results[2] > 10:
						time.sleep(1)
						print("It was super effective!")
					elif results[2] < 10:
						print("It wasn't very effective...")

BASIC FRAMEWORK TO GO IN FOR BASIC ATTACKING MOVES

	def useAttack(self, off, att, dfn):
		return self.getDamage(off, att, dfn)

	def takeHP(self, dfn, damage):
		if damage > dfn.battHP:
			dfn.battHP = 0
		else
			dfn.battHP -= damage
		return

	def isHit(self, off, att, dfn):
		accmove = math.floor(2.55 * att.accuracy)
		accuser = off.Acclvl
		evatarg = dfn.Evalvl
		T = min(max(1, accmove * accuser * evatarg), 255)
		R = random.randint(0, 256)
		if R < T:
			return True
		else:
			return False


	def takeConfusionDamage(self, off):

		A = off.battAtk
		D = off.battDef

		if A > 255 or D > 255:
			A = math.floor(A/2)
			A = math.floor(A/2)
			D = math.floor(D/2)
			D = math.floor(D/2)
		
		lvl = off.level

		damage = (min(math.floor(math.floor((((math.floor((2*lvl)/5) + 2)*A*40)/max(1, D)))/50), 997) + 2)

		if off.battHP - damage < 0:
			off.battHP = 0
		else:
			off.battHP -= damage
		return


	def getDamage(self, off, att, dfn):
		lvl = off.level
		
		if att.category == "Physical":
			A = off.battAtk
			D = dfn.battDef
			if off.nonVolatileStatus == "Burned":
				A = math.floor(A/2) 
		if att.category == "Special":
			A = off.battSpa
			D = dfn.battSpa
		isCritical = self.isCritical(off, att)
		if isCritical
			lvl *= 2
			if att.category == "Physical":
				A = off.statAtk
				D = dfn.statDef
			if att.category == "Special":
				A = off.statSpa
				D = dfn.statSpa

		if A > 255 or D > 255:
			A = math.floor(A/2)
			A = math.floor(A/2)
			D = math.floor(D/2)
			D = math.floor(D/2)

		P = att.basePower
		S = self.getStab(off, att)
		T = self.getTypeMult(dfn, att.type)
		R = random.randint(217, 256)

		return math.floor((math.floor((((min(math.floor(math.floor((((math.floor((2*lvl)/5) + 2)*A*P)/max(1, D)))/50), 997) + 2)*S)*T)/10)*R)/255), isCritical, T

	def getTypeMult(self, dfn, atype):
		with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/typechart.json") as tchartjson:
			tchart = json.load(tchartjson)
		out = 10
		for ptype in dfn.type:
			out *= tchart[atype]["damageTaken"][ptype]
		return math.floor(out)

	def getStab(self, off, att):
		stab = 1
		for ptype in off.type:
			if ptype == att.type:
				stab = 1.5
		return stab

	def isCritical(self, off, att):
		rand = math.floor(256 * random.random())
		threshold = math.floor(off.baseSpe / 2)
		if off.isFocusEnergy:
			threshold = math.floor(off.baseSpe / 8)
		if att.critRatio:
			if att.critRatio == 2:
				threshold *= 4
		if rand < threshold:
			return True
		else:
			return False


