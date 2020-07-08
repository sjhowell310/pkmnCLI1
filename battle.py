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
		if t1.activePokemon.nonVolatileStatus == "Paralyzed":
			t1s = math.floor(self.t1.activePokemon.battSpe/4)
		else:
			t1s = self.t1.activePokemon.battSpe

		if t2.activePokemon.nonVolatileStatus == "Paralyzed":
			t2s = math.floor(self.t2.activePokemon.battSpe/4)
		else:
			t2s = self.t2.activePokemon.battSpe 

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
				if t1s > t2s:					
					self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1, self.t1)				
					self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2, self.t2)

				elif t1s < t2s:					
					self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 1, self.t2)	
					self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 2, self.t1)

				elif t1s == t2s:
					rand = random.randint(0,256)
					if rand < 128:						
						self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1)				
						self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2)
					else:
						self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1)				
						self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2)						


	def attack(self, off, att, dfn, firstorsecond, trainer):
		cantAttack = False

		if firstorsecond == 1:
			off.willFlinch = False
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
				else:
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
									rand = random.randint(0,256)
									if rand < 64:
										time.sleep(1)
										print("{name} is fully paralyzed and can't move!\n".format(name = off.name))
										cantAttack = True
							else:
								if off.nonVolatileStatus == "Paralyzed":
									rand = random.randint(0,256)
									if rand < 64:
										time.sleep(1)
										print("{name} is fully paralyzed and can't move!\n".format(name = off.name))
										cantAttack = True
								rand = random.randint(0,256)
								if rand < 128:
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
						else:
							if off.nonVolatileStatus == "Paralyzed":
									rand = random.randint(0,256)
									if rand < 64:
										time.sleep(1)
										print("{name} is fully paralyzed and can't move!\n".format(name = off.name))
										cantAttack = True	
			if not cantAttack:					
				att.pp -= 1
				if att.name != "Swift":
					willHit = self.isHit(off, att, dfn)
				else:
					willHit = True

				time.sleep(1)
				print("{name} used {movename}!\n".format(name = off.name, movename = att.name))
				
				if not willHit:
					if off.Acclvl >= dfn.Evalvl:
						time.sleep(1)
						print("{name} missed!\n".format(name = off.name))
					elif dfn.Evalvl > off.Acclvl:
						time.sleep(1)
						print("{name} evaded the attack!\n".format(name = dfn.name))
				else:
					results = self.useAttack(off, att, dfn)

					if results[0] == "failed":
						time.sleep(1)
						print("{movename} failed!".format(movename = att.name))
					elif results[0] == "noEffect" or results[2] == 0:
						time.sleep(1)
						print("{movename} doesn't effect {opponent}!".format(movename = att.name, opponent = dfn.name))
					elif results[0] > 0 and results[2] > 0:
						self.takeHP(dfn, results[0])
						if results[1]:
							time.sleep(1)
							print("Critical hit!, {hplost} damage taken by {pname}".format(hplost = results[0], pname = dfn.name))
						if results[2] > 10:
							time.sleep(1)
							print("It was super effective!, {hplost} damage taken by {pname}".format(hplost = results[0], pname = dfn.name))
						elif results[2] < 10:
							print("It wasn't very effective..., {hplost} damage taken by {pname}".format(hplost = results[0], pname = dfn.name))
					if results[3]:
						pass




	def useAttack(self, off, att, dfn):
		statBuffs = []
		if att.basePower != 0 and att.target == "normal":
			damage, isCrit, tmult = self.getDamage(off, att, dfn)
			if att.secondary:
				if "status" in att.secondary:
					rand = random.randint(0, 256)
					if rand < math.floor(att.secondary["chance"] * 2.55):
						if "status" in att.secondary.keys():
							if att.secondary["status"] == "brn" and dfn.nonVolatileStatus == None and "Fire" not in dfn.type:
								dfn.nonVolatileStatus == "Burned"
								statusEffects = "burned"

							if att.secondary["status"] == "frz" and dfn.nonVolatileStatus == None and "Ice" not in dfn.type:
								dfn.nonVolatileStatus == "Frozen"
								statusEffects = "frozen"

							if att.secondary["status"] == "par" and dfn.nonVolatileStatus == None:
								if att.type == "Electric" and "Electric" in dfn.type:
									pass
								if att.name == "Body Slam" and "Normal" in dfn.type:
									pass
								if att.name == "Lick" and "Ghost" in dfn.type:
									pass
								else:
									dfn.nonVolatileStatus == "Paralyzed"
									statusEffects = "paralyzed"
							if att.secondary["status"] == "psn" and dfn.nonVolatileStatus == None and "Poison" not in dfn.type:
								dfn.nonVolatileStatus = "Poisoned"
								statusEffects = "poisoned"
				if att.secondary["volatileStatus"] in att.secondary.keys():
					if att.secondary["volatileStatus"] == "flinch":
						rand = random.randint(0, 256)
						if rand < math.floor(att.secondary["chance"] * 2.55):
							dfn.willFlinch = True
					if att.secondary["volatileStatus"] == "confusion":
						rand = random.randint(0, 256)
						if rand < math.floor(att.secondary["chance"] * 2.55):
							dfn.isConfused = True
							statusEffects = "Confused"
							rand = random.randint(0, 256)
							if rand < 64:
								dfn.isConfusedCount = 2
							elif rand > 63 and rand < 128:
								dfn.isConfusedCount = 3
							elif rand > 127 and rand < 192:
								dfn.isConfusedCount = 4
							elif rand > 191 and rand < 256:
								dfn.isConfusedCount = 5
				else:
					statusEffects = None
				if "boosts" in att.secondary:
					rand = random.randint(0, 256)
					if rand < math.floor(att.secondary["chance"] * 2.55):
						for key in att.secondary["boosts"].keys():
							if key == "atk":
								self.statMod(dfn.statAtk, dfn.battAtk, dfn.Atklvl, att.secondary["boosts"]["atk"])
							elif key == "def":
								self.statMod(dfn.statDef, dfn.battDef, dfn.Deflvl, att.secondary["boosts"]["def"])
							elif key == "spa":
								self.statMod(dfn.statSpa, dfn.battSpa, dfn.Spalvl, att.secondary["boosts"]["spa"])
							elif key == "spe":
								self.statMod(dfn.statSpe, dfn.battSpe, dfn.Spelvl, att.secondary["boosts"]["spe"])
HANDLE PURE STATMOD MOVES THEN TEST
		return damage, isCrit, tmult, statBuffs, statusEffects


	def takeHP(self, dfn, damage):
		if damage > dfn.battHP:
			dfn.battHP = 0
		else:
			dfn.battHP -= damage
		return


	def isHit(self, off, att, dfn):
		accmove = math.floor(2.56 * att.accuracy)
		accuser = off.battAcc
		evatarg = dfn.battEva
		T = min(max(1, math.floor((accmove * accuser) / evatarg)), 255)
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
		P = att.basePower
		S = self.getStab(off, att)
		T = self.getTypeMult(dfn, att.type)
		R = random.randint(217, 256)

		if att.basePower == "set" or att.basePower == "var dmg" or att.basePower == "ko":
			if att.name == "Dragon Rage":
				if T != 0:
					return 40, False, 10
				else:
					return "noEffect", False, 0

			if att.name == "Sonic Boom":
				return 20, False, 10

			if att.name == "Night Shade":
				P = off.level

			if att.name == "Psywave":
				return max(1, math.floor((off.level * (random.randint(0,101) + 50))/100)), False, 10

			if att.name == "Seismic Toss":
				return off.level, False, 10

			if att.name == "superfang":
				return max(1, math.floor(dfn.battHP/2)), False, 10

			if att.name == "Fissure" or att.name == "Guillotine" or att.name == "Horn Drill":
				if dfn.battSpe > att.battSpe:
					return "failed", False, 10
				else:
					return 65535, False, 10


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
		if isCritical:
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
		rand = random.randint(0,256)
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


	def statMod(self, stat, batt, lvl, mod):
		if lvl + mod < -6:
			mod = 6 + lvl
			lvl = -6
		elif lvl + mod > 6:
			mod = 6 - lvl
			lvl = 6
		else:
			lvl += mod

		if stat == -1:
			if lvl == -6:
				batt = math.floor((255 * 25) / 100)
			elif lvl == -5:
				batt = math.floor((255 * 28) / 100)
			elif lvl == -4:
				batt = math.floor((255 * 33) / 100)
			elif lvl == -3:
				batt = math.floor((255 * 40) / 100)
			elif lvl == -2:
				batt = math.floor((255 * 50) / 100)
			elif lvl == -1:
				batt = math.floor((255 * 66) / 100)
			elif lvl == 0:
				batt = math.floor((255 * 100) / 100)
			elif lvl == 1:
				batt = math.floor((255 * 150) / 100)
			elif lvl == 2:
				batt = math.floor((255 * 200) / 100)
			elif lvl == 3:
				batt = math.floor((255 * 250) / 100)
			elif lvl == 4:
				batt = math.floor((255 * 300) / 100)
			elif lvl == 5:
				batt = math.floor((255 * 350) / 100)
			elif lvl == 6:
				batt = math.floor((255 * 400) / 100)
		else:
			if lvl == -6:
				batt = min(max(1, math.floor((stat * 25) / 100), 999))
			elif lvl == -5:
				batt = min(max(1, math.floor((stat * 28) / 100), 999))
			elif lvl == -4:
				batt = min(max(1, math.floor((stat * 33) / 100), 999))
			elif lvl == -3:
				batt = min(max(1, math.floor((stat * 40) / 100), 999))
			elif lvl == -2:
				batt = min(max(1, math.floor((stat * 50) / 100), 999))
			elif lvl == -1:
				batt = min(max(1, math.floor((stat * 66) / 100), 999))
			elif lvl == 0:
				batt = min(max(1, math.floor((stat * 100) / 100), 999))
			elif lvl == 1:
				batt = min(max(1, math.floor((stat * 150) / 100), 999))
			elif lvl == 2:
				batt = min(max(1, math.floor((stat * 200) / 100), 999))
			elif lvl == 3:
				batt = min(max(1, math.floor((stat * 250) / 100), 999))
			elif lvl == 4:
				batt = min(max(1, math.floor((stat * 300) / 100), 999))
			elif lvl == 5:
				batt = min(max(1, math.floor((stat * 350) / 100), 999))
			elif lvl == 6:
				batt = min(max(1, math.floor((stat * 400) / 100), 999))

		return mod


