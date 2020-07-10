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
		with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/typechart.json") as tchartjson:
			self.tchart = json.load(tchartjson)


	#function prints the name of each trainer, their in battle pokemon, and their hp to terminal before moves are decided upon
	def printBattle(self):
		print("\n{name1: <30}{name2: >30}".format(name1 = self.t1.name, name2 = self.t2.name))
		print("{name1: <30}{name2: >30}".format(name1 = self.t1.activePokemon.name, name2 = self.t2.activePokemon.name))
		print("{hp: <3}{currhp1: >4}/{tothp1: <4}{status1: >7}{stat1: <4}{space: >14}{hp: >3}{currhp2: >4}/{tothp2: <4}{status1: >7}{stat2: >4}".format(hp = "HP:", currhp1 = str(self.t1.activePokemon.battHP), tothp1 = str(self.t1.activePokemon.statHP), status1 = "Status:", stat1 = str(self.t1.activePokemon.nonVolatileStatus), currhp2 = str(self.t2.activePokemon.battHP), tothp2 = str(self.t2.activePokemon.statHP), stat2 = str(self.t2.activePokemon.nonVolatileStatus), space = ""))


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
		if self.t1.activePokemon.nonVolatileStatus == "Paralyzed":
			t1s = math.floor(self.t1.activePokemon.battSpe/4)
		else:
			t1s = self.t1.activePokemon.battSpe

		if self.t2.activePokemon.nonVolatileStatus == "Paralyzed":
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
			if self.t1.activePokemon.moves[t1c].priority > self.t2.activePokemon.moves[t2c].priority:				
				self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1, self.t1)	
				self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2, self.t2)

			elif self.t1.activePokemon.moves[t1c].priority < self.t2.activePokemon.moves[t2c].priority:				
				self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 1, self.t2)
				self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 2, self.t1)

			elif self.t1.activePokemon.moves[t1c].priority == self.t2.activePokemon.moves[t2c].priority:
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
				if att.name != "Swift" or att.movetype != "selfStat":
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
					if att.movetype == "selfStat":
						if "atk" in att.boosts.keys():
							mod = self.statMod(off.statAtk, off.battAtk, off.Atklvl, att.boosts["atk"])
							stat = "Attack"
						elif "def" in att.boosts.keys():
							mod = self.statMod(off.statDef, off.battDef, off.Deflvl, att.boosts["def"])
							stat = "Defense"
						elif "spa" in att.boosts.keys():
							mod = self.statMod(off.statSpa, off.battSpa, off.Spalvl, att.boosts["spa"])
							stat = "Special"
						elif "spe" in att.boosts.keys():
							mod = self.statMod(off.statSpe, off.battSpe, off.Spelvl, att.boosts["spe"])
							stat = "Special"
						elif "accuracy" in att.boosts.keys():
							mod = self.statMod(off.statAcc, off.battAcc, off.Acclvl, att.boosts["accuracy"])
							stat = "Accuracy"
						elif "evasion" in att.boosts.keys():
							mod = self.statMod(off.statEva, off.battEva, off.Evalvl, att.boosts["evasion"])
							stat = "Evasion"
						if mod == 0:
							time.sleep(1)
							print("Nothing happened!")
						elif mod == 1:
							time.sleep(1)
							print("{pname}'s {stat} rose!".format(pname = off.name, stat = stat))
						elif mod == 2:
							time.sleep(1)
							print("{pname}'s {stat} greatly rose!".format(pname = off.name, stat = stat))
					elif att.movetype == "offStat":
						if "atk" in att.boosts.keys():
							mod = self.statMod(dfn.statAtk, dfn.battAtk, dfn.Atklvl, att.boosts["atk"])
							stat = "Attack"
						elif "def" in att.boosts.keys():
							mod = self.statMod(dfn.statDef, dfn.battDef, dfn.Deflvl, att.boosts["def"])
							stat = "Defense"
						elif "spa" in att.boosts.keys():
							mod = self.statMod(dfn.statSpa, dfn.battSpa, dfn.Spalvl, att.boosts["spa"])
							stat = "Special"
						elif "spe" in att.boosts.keys():
							mod = self.statMod(dfn.statSpe, dfn.battSpe, dfn.Spelvl, att.boosts["spe"])
							stat = "Special"
						elif "accuracy" in att.boosts.keys():
							mod = self.statMod(dfn.statAcc, dfn.battAcc, dfn.Acclvl, att.boosts["accuracy"])
							stat = "Accuracy"
						elif "evasion" in att.boosts.keys():
							mod = self.statMod(dfn.statEva, dfn.battEva, dfn.Evalvl, att.boosts["evasion"])
							stat = "Evasion"
						if mod == 0:
							time.sleep(1)
							print("Nothing happened!")
						elif mod == 1:
							time.sleep(1)
							print("{pname}'s {stat} fell!".format(pname = dfn.name, stat = stat))
						elif mod == 2:
							time.sleep(1)
							print("{pname}'s {stat} greatly fell!".format(pname = dfn.name, stat = stat))
					elif att.movetype == "dmgOnly":
						damage, crit, mult = self.getDamage(off, att, dfn)
					
						if damage == "failed":
							time.sleep(1)
							print("{movename} failed!".format(movename = att.name))
						elif damage == 65535:
							time.sleep(1)
							print("One Hit KO!")
						elif damage == "noEffect" or mult == 0:
							time.sleep(1)
							print("{movename} doesn't effect {opponent}!".format(movename = att.name, opponent = dfn.name))
						elif damage >= 0 and mult > 0:
							self.takeHP(dfn, damage)
							if crit:
								time.sleep(1)
								print("Critical hit!")
							if mult > 10:
								time.sleep(1)
								print("It was super effective! {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
							elif mult < 10:
								time.sleep(1)
								print("It wasn't very effective... {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
							elif mult == 10:
								time.sleep(1)
								print("{hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
					elif att.movetype == "dmgStat":
						damage, crit, mult = self.getDamage(off, att, dfn)
					
						if damage == "failed":
							time.sleep(1)
							print("{movename} failed!".format(movename = att.name))
						elif damage == 65535:
							time.sleep(1)
							print("One Hit KO!")
						elif damage == "noEffect" or mult == 0:
							time.sleep(1)
							print("{movename} doesn't effect {opponent}!".format(movename = att.name, opponent = dfn.name))
						elif damage >= 0 and mult > 0:
							self.takeHP(dfn, damage)
							if crit:
								time.sleep(1)
								print("Critical hit!")
							if mult > 10:
								time.sleep(1)
								print("It was super effective! {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
							elif mult < 10:
								time.sleep(1)
								print("It wasn't very effective... {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
							elif mult == 10:
								time.sleep(1)
								print("{hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))

						rand = random.randint(0,101)
						if rand < att.secondary["chance"]:
							if "atk" in att.secondary["boosts"].keys():
								mod = self.statMod(dfn.statAtk, dfn.battAtk, dfn.Atklvl, att.secondary["boosts"]["atk"])
								stat = "Attack"
							elif "def" in att.secondary["boosts"].keys():
								mod = self.statMod(dfn.statDef, dfn.battDef, dfn.Deflvl, att.secondary["boosts"]["def"])
								stat = "Defense"
							elif "spa" in att.secondary["boosts"].keys():
								mod = self.statMod(dfn.statSpa, dfn.battSpa, dfn.Spalvl, att.secondary["boosts"]["spa"])
								stat = "Special"
							elif "spe" in att.secondary["boosts"].keys():
								mod = self.statMod(dfn.statSpe, dfn.battSpe, dfn.Spelvl, att.secondary["boosts"]["spe"])
								stat = "Special"
							elif "accuracy" in att.secondary["boosts"].keys():
								mod = self.statMod(dfn.statAcc, dfn.battAcc, dfn.Acclvl, att.secondary["boosts"]["accuracy"])
								stat = "Accuracy"
							elif "evasion" in att.secondary["boosts"].keys():
								mod = self.statMod(dfn.statEva, dfn.battEva, dfn.Evalvl, att.secondary["boosts"]["evasion"])
								stat = "Evasion"
							if mod == 0:
								time.sleep(1)
								print("Nothing happened!")
							elif mod == 1:
								time.sleep(1)
								print("{pname}'s {stat} fell!".format(pname = dfn.name, stat = stat))
							elif mod == 2:
								time.sleep(1)
								print("{pname}'s {stat} greatly fell!".format(pname = dfn.name, stat = stat))
					elif att.movetype == "offStatus":
						if att.status:
							if dfn.nonVolatileStatus:
								time.sleep(1)
								print("But it failed!")
							else:
								if att.status == "par":
									if att.type == "Electric" and "Electric" in dfn.type:
										time.sleep(1)
										print("But it failed!")
									else:
										time.sleep(1)
										print("{pname} became Paralyzed! It may not attack!".format(pname = dfn.name))
										dfn.nonVolatileStatus = "Paralyzed"
								elif att.status == "psn":
									if "Poison" in dfn.type:
										time.sleep(1)
										print("But it failed!")
									else:
										time.sleep(1)
										print("{pname} was poisoned!".format(pname = dfn.name))
										dfn.nonVolatileStatus = "Poisoned"
								elif att.status == "slp":
									time.sleep(1)
									print("{pname} fell asleep!".format(pname = dfn.name))
									dfn.nonVolatileStatus = "Asleep"
									rand = random.randint(0,7)
									if rand == 0:
										dfn.nonVolatileCount = 1
									elif rand == 1:
										dfn.nonVolatileCount = 2
									elif rand == 2:
										dfn.nonVolatileCount = 3
									elif rand == 3:
										dfn.nonVolatileCount = 4
									elif rand == 4:
										dfn.nonVolatileCount = 5
									elif rand == 5:
										dfn.nonVolatileCount = 6
									elif rand == 6:
										dfn.nonVolatileCount = 7
								elif att.status == "tox":
									if "Poison" in dfn.type:
										time.sleep(1)
										print("But it failed!")
									else:
										time.sleep(1)
										print("{pname} was badly poisoned!".format(pname = dfn.name))
										dfn.nonVolatileStatus = "Toxic"
						elif att.volatileStatus == "confusion":
							if dfn.isConfused:
								time.sleep(1)
								print("{pname} is already confused!".format(pname = dfn.name))
							else:
								rand = random.randint(0, 256)
								if rand < 64:
									dfn.isConfusedCount = 2
								elif rand > 63 and rand < 128:
									dfn.isConfusedCount = 3
								elif rand > 127 and rand < 192:
									dfn.isConfusedCount = 4
								elif rand > 191 and rand < 256:
									dfn.isConfusedCount = 5
								time.sleep(1)
								print("{pname} became confused!")
					elif att.movetype == "dmgStatus":
						damage, crit, mult = self.getDamage(off, att, dfn)
					
						if damage == "failed":
							time.sleep(1)
							print("{movename} failed!".format(movename = att.name))
						elif damage == 65535:
							time.sleep(1)
							print("One Hit KO!")
						elif damage == "noEffect" or mult == 0:
							time.sleep(1)
							print("{movename} doesn't effect {opponent}!".format(movename = att.name, opponent = dfn.name))
						elif damage >= 0 and mult > 0:
							self.takeHP(dfn, damage)
							if crit:
								time.sleep(1)
								print("Critical hit!")
							if mult > 10:
								time.sleep(1)
								print("It was super effective! {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
							elif mult < 10:
								time.sleep(1)
								print("It wasn't very effective... {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
							elif mult == 10:
								time.sleep(1)
								print("{hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
						rand = random.randint(0, 255)
						if rand < math.floor(att.secondary["chance"]):
							if att.secondary["status"] == "par":
									if att.type == "Electric" and "Electric" in dfn.type:
										pass
									elif att.name == "Body Slam" and "Normal" in dfn.type:
										pass
									elif att.name == "Lick" and "Ghost" in dfn.type:
										pass
									else:
										time.sleep(1)
										print("{pname} became Paralyzed! It may not attack!".format(pname = dfn.name))
										dfn.nonVolatileStatus = "Paralyzed"
							elif att.secondary["status"] == "psn":
								if "Poison" in dfn.type:
									pass
								else:
									time.sleep(1)
									print("{pname} was poisoned!".format(pname = dfn.name))
									dfn.nonVolatileStatus = "Poisoned"
							elif att.secondary["status"] == "frz":
								if "Ice" in dfn.type:
									pass
								else:
									time.sleep(1)
									print("{pname} was frozen!".format(pname = dfn.name))
									dfn.nonVolatileStatus = "Frozen"
							elif att.secondary["status"] == "brn":
								if "Fire" in dfn.type:
									pass
								else:
									time.sleep(1)
									print("{pname} was burned!".format(pname = dfn.name))
									dfn.nonVolatileStatus = "Burned"
							elif att.secondary["status"] == "slp":
								time.sleep(1)
								print("{pname} fell asleep!".format(pname = dfn.name))
								dfn.nonVolatileStatus = "Asleep"
								rand = random.randint(0,7)
								if rand == 0:
									dfn.nonVolatileCount = 1
								elif rand == 1:
									dfn.nonVolatileCount = 2
								elif rand == 2:
									dfn.nonVolatileCount = 3
								elif rand == 3:
									dfn.nonVolatileCount = 4
								elif rand == 4:
									dfn.nonVolatileCount = 5
								elif rand == 5:
									dfn.nonVolatileCount = 6
								elif rand == 6:
									dfn.nonVolatileCount = 7
							elif att.secondary["volatileStatus"] == "confusion":
								if dfn.isConfused:
									pass
								else:
									rand = random.randint(0, 256)
									if rand < 64:
										dfn.isConfusedCount = 2
									elif rand > 63 and rand < 128:
										dfn.isConfusedCount = 3
									elif rand > 127 and rand < 192:
										dfn.isConfusedCount = 4
									elif rand > 191 and rand < 256:
										dfn.isConfusedCount = 5
									time.sleep(1)
									print("{pname} became confused!".format(pname = dfn.name))
							elif att.secondary["volatileStatus"] == "flinch":
								dfn.willFlinch = True
					elif att.movetype == "recoil":
						damage, crit, mult = self.getDamage(off, att, dfn)
					
						if damage == "failed":
							time.sleep(1)
							print("{movename} failed!".format(movename = att.name))
						elif damage == 65535:
							time.sleep(1)
							print("One Hit KO!")
						elif damage == "noEffect" or mult == 0:
							time.sleep(1)
							print("{movename} doesn't effect {opponent}!".format(movename = att.name, opponent = dfn.name))
						elif damage >= 0 and mult > 0:
							self.takeHP(dfn, damage)
							if crit:
								time.sleep(1)
								print("Critical hit!")
							if mult > 10:
								time.sleep(1)
								print("It was super effective! {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
							elif mult < 10:
								time.sleep(1)
								print("It wasn't very effective... {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
							elif mult == 10:
								time.sleep(1)
								print("{hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
							self.takeHP(off, math.floor((damage * att.recoil[0])/att.recoil[1]))
							print("{hplost} recoil damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))

		if firstorsecond == 2:
			if off.willFlinch:
				time.sleep(1)
				print("{name} flinched!\n".format(name = off.name))
				off.willFlinch = False
			else:
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
					if att.name != "Swift" or att.movetype != "selfStat":
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
						if att.movetype == "selfStat":
							if "atk" in att.boosts.keys():
								mod = self.statMod(off.statAtk, off.battAtk, off.Atklvl, att.boosts["atk"])
								stat = "Attack"
							elif "def" in att.boosts.keys():
								mod = self.statMod(off.statDef, off.battDef, off.Deflvl, att.boosts["def"])
								stat = "Defense"
							elif "spa" in att.boosts.keys():
								mod = self.statMod(off.statSpa, off.battSpa, off.Spalvl, att.boosts["spa"])
								stat = "Special"
							elif "spe" in att.boosts.keys():
								mod = self.statMod(off.statSpe, off.battSpe, off.Spelvl, att.boosts["spe"])
								stat = "Special"
							elif "accuracy" in att.boosts.keys():
								mod = self.statMod(off.statAcc, off.battAcc, off.Acclvl, att.boosts["accuracy"])
								stat = "Accuracy"
							elif "evasion" in att.boosts.keys():
								mod = self.statMod(off.statEva, off.battEva, off.Evalvl, att.boosts["evasion"])
								stat = "Evasion"
							if mod == 0:
								time.sleep(1)
								print("Nothing happened!")
							elif mod == 1:
								time.sleep(1)
								print("{pname}'s {stat} rose!".format(pname = off.name, stat = stat))
							elif mod == 2:
								time.sleep(1)
								print("{pname}'s {stat} greatly rose!".format(pname = off.name, stat = stat))
						elif att.movetype == "offStat":
							if "atk" in att.boosts.keys():
								mod = self.statMod(dfn.statAtk, dfn.battAtk, dfn.Atklvl, att.boosts["atk"])
								stat = "Attack"
							elif "def" in att.boosts.keys():
								mod = self.statMod(dfn.statDef, dfn.battDef, dfn.Deflvl, att.boosts["def"])
								stat = "Defense"
							elif "spa" in att.boosts.keys():
								mod = self.statMod(dfn.statSpa, dfn.battSpa, dfn.Spalvl, att.boosts["spa"])
								stat = "Special"
							elif "spe" in att.boosts.keys():
								mod = self.statMod(dfn.statSpe, dfn.battSpe, dfn.Spelvl, att.boosts["spe"])
								stat = "Special"
							elif "accuracy" in att.boosts.keys():
								mod = self.statMod(dfn.statAcc, dfn.battAcc, dfn.Acclvl, att.boosts["accuracy"])
								stat = "Accuracy"
							elif "evasion" in att.boosts.keys():
								mod = self.statMod(dfn.statEva, dfn.battEva, dfn.Evalvl, att.boosts["evasion"])
								stat = "Evasion"
							if mod == 0:
								time.sleep(1)
								print("Nothing happened!")
							elif mod == 1:
								time.sleep(1)
								print("{pname}'s {stat} fell!".format(pname = dfn.name, stat = stat))
							elif mod == 2:
								time.sleep(1)
								print("{pname}'s {stat} greatly fell!".format(pname = dfn.name, stat = stat))
						elif att.movetype == "dmgOnly":
							damage, crit, mult = self.getDamage(off, att, dfn)
						
							if damage == "failed":
								time.sleep(1)
								print("{movename} failed!".format(movename = att.name))
							elif damage == 65535:
								time.sleep(1)
								print("One Hit KO!")
							elif damage == "noEffect" or mult == 0:
								time.sleep(1)
								print("{movename} doesn't effect {opponent}!".format(movename = att.name, opponent = dfn.name))
							elif damage >= 0 and mult > 0:
								self.takeHP(dfn, damage)
								if crit:
									time.sleep(1)
									print("Critical hit!")
								if mult > 10:
									time.sleep(1)
									print("It was super effective! {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
								elif mult < 10:
									time.sleep(1)
									print("It wasn't very effective... {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
								elif mult == 10:
									time.sleep(1)
									print("{hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
						elif att.movetype == "dmgStat":
							damage, crit, mult = self.getDamage(off, att, dfn)
						
							if damage == "failed":
								time.sleep(1)
								print("{movename} failed!".format(movename = att.name))
							elif damage == 65535:
								time.sleep(1)
								print("One Hit KO!")
							elif damage == "noEffect" or mult == 0:
								time.sleep(1)
								print("{movename} doesn't effect {opponent}!".format(movename = att.name, opponent = dfn.name))
							elif damage >= 0 and mult > 0:
								self.takeHP(dfn, damage)
								if crit:
									time.sleep(1)
									print("Critical hit!")
								if mult > 10:
									time.sleep(1)
									print("It was super effective! {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
								elif mult < 10:
									time.sleep(1)
									print("It wasn't very effective... {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
								elif mult == 10:
									time.sleep(1)
									print("{hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))

							rand = random.randint(0,101)
							if rand < att.secondary["chance"]:
								if "atk" in att.secondary["boosts"].keys():
									mod = self.statMod(dfn.statAtk, dfn.battAtk, dfn.Atklvl, att.secondary["boosts"]["atk"])
									stat = "Attack"
								elif "def" in att.secondary["boosts"].keys():
									mod = self.statMod(dfn.statDef, dfn.battDef, dfn.Deflvl, att.secondary["boosts"]["def"])
									stat = "Defense"
								elif "spa" in att.secondary["boosts"].keys():
									mod = self.statMod(dfn.statSpa, dfn.battSpa, dfn.Spalvl, att.secondary["boosts"]["spa"])
									stat = "Special"
								elif "spe" in att.secondary["boosts"].keys():
									mod = self.statMod(dfn.statSpe, dfn.battSpe, dfn.Spelvl, att.secondary["boosts"]["spe"])
									stat = "Special"
								elif "accuracy" in att.secondary["boosts"].keys():
									mod = self.statMod(dfn.statAcc, dfn.battAcc, dfn.Acclvl, att.secondary["boosts"]["accuracy"])
									stat = "Accuracy"
								elif "evasion" in att.secondary["boosts"].keys():
									mod = self.statMod(dfn.statEva, dfn.battEva, dfn.Evalvl, att.secondary["boosts"]["evasion"])
									stat = "Evasion"
								if mod == 0:
									time.sleep(1)
									print("Nothing happened!")
								elif mod == 1:
									time.sleep(1)
									print("{pname}'s {stat} fell!".format(pname = dfn.name, stat = stat))
								elif mod == 2:
									time.sleep(1)
									print("{pname}'s {stat} greatly fell!".format(pname = dfn.name, stat = stat))
						elif att.movetype == "offStatus":
							if att.status:
								if dfn.nonVolatileStatus:
									time.sleep(1)
									print("But it failed!")
								else:
									if att.status == "par":
										if att.type == "Electric" and "Electric" in dfn.type:
											time.sleep(1)
											print("But it failed!")
										else:
											time.sleep(1)
											print("{pname} became Paralyzed! It may not attack!".format(pname = dfn.name))
											dfn.nonVolatileStatus = "Paralyzed"
									elif att.status == "psn":
										if "Poison" in dfn.type:
											time.sleep(1)
											print("But it failed!")
										else:
											time.sleep(1)
											print("{pname} was poisoned!".format(pname = dfn.name))
											dfn.nonVolatileStatus = "Poisoned"
									elif att.status == "slp":
										time.sleep(1)
										print("{pname} fell asleep!".format(pname = dfn.name))
										dfn.nonVolatileStatus = "Asleep"
										rand = random.randint(0,7)
										if rand == 0:
											dfn.nonVolatileCount = 1
										elif rand == 1:
											dfn.nonVolatileCount = 2
										elif rand == 2:
											dfn.nonVolatileCount = 3
										elif rand == 3:
											dfn.nonVolatileCount = 4
										elif rand == 4:
											dfn.nonVolatileCount = 5
										elif rand == 5:
											dfn.nonVolatileCount = 6
										elif rand == 6:
											dfn.nonVolatileCount = 7
									elif att.status == "tox":
										if "Poison" in dfn.type:
											time.sleep(1)
											print("But it failed!")
										else:
											time.sleep(1)
											print("{pname} was badly poisoned!".format(pname = dfn.name))
											dfn.nonVolatileStatus = "Toxic"
							elif att.volatileStatus == "confusion":
								if dfn.isConfused:
									time.sleep(1)
									print("{pname} is already confused!".format(pname = dfn.name))
								else:
									rand = random.randint(0, 256)
									if rand < 64:
										dfn.isConfusedCount = 2
									elif rand > 63 and rand < 128:
										dfn.isConfusedCount = 3
									elif rand > 127 and rand < 192:
										dfn.isConfusedCount = 4
									elif rand > 191 and rand < 256:
										dfn.isConfusedCount = 5
									time.sleep(1)
									print("{pname} became confused!".format(pname = dfn.name))
						elif att.movetype == "dmgStatus":
							damage, crit, mult = self.getDamage(off, att, dfn)
						
							if damage == "failed":
								time.sleep(1)
								print("{movename} failed!".format(movename = att.name))
							elif damage == 65535:
								time.sleep(1)
								print("One Hit KO!")
							elif damage == "noEffect" or mult == 0:
								time.sleep(1)
								print("{movename} doesn't effect {opponent}!".format(movename = att.name, opponent = dfn.name))
							elif damage >= 0 and mult > 0:
								self.takeHP(dfn, damage)
								if crit:
									time.sleep(1)
									print("Critical hit!")
								if mult > 10:
									time.sleep(1)
									print("It was super effective! {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
								elif mult < 10:
									time.sleep(1)
									print("It wasn't very effective... {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
								elif mult == 10:
									time.sleep(1)
									print("{hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
							rand = random.randint(0, 255)
							if rand < math.floor(att.secondary["chance"]):
								if att.secondary["status"] == "par":
										if att.type == "Electric" and "Electric" in dfn.type:
											pass
										elif att.name == "Body Slam" and "Normal" in dfn.type:
											pass
										elif att.name == "Lick" and "Ghost" in dfn.type:
											pass
										else:
											time.sleep(1)
											print("{pname} became Paralyzed! It may not attack!".format(pname = dfn.name))
											dfn.nonVolatileStatus = "Paralyzed"
								elif att.secondary["status"] == "psn":
									if "Poison" in dfn.type:
										pass
									else:
										time.sleep(1)
										print("{pname} was poisoned!".format(pname = dfn.name))
										dfn.nonVolatileStatus = "Poisoned"
								elif att.secondary["status"] == "frz":
									if "Ice" in dfn.type:
										pass
									else:
										time.sleep(1)
										print("{pname} was frozen!".format(pname = dfn.name))
										dfn.nonVolatileStatus = "Frozen"
								elif att.secondary["status"] == "brn":
									if "Fire" in dfn.type:
										pass
									else:
										time.sleep(1)
										print("{pname} was burned!".format(pname = dfn.name))
										dfn.nonVolatileStatus = "Burned"
								elif att.secondary["status"] == "slp":
									time.sleep(1)
									print("{pname} fell asleep!".format(pname = dfn.name))
									dfn.nonVolatileStatus = "Asleep"
									rand = random.randint(0,7)
									if rand == 0:
										dfn.nonVolatileCount = 1
									elif rand == 1:
										dfn.nonVolatileCount = 2
									elif rand == 2:
										dfn.nonVolatileCount = 3
									elif rand == 3:
										dfn.nonVolatileCount = 4
									elif rand == 4:
										dfn.nonVolatileCount = 5
									elif rand == 5:
										dfn.nonVolatileCount = 6
									elif rand == 6:
										dfn.nonVolatileCount = 7
								elif att.secondary["volatileStatus"] == "confusion":
									if dfn.isConfused:
										pass
									else:
										rand = random.randint(0, 256)
										if rand < 64:
											dfn.isConfusedCount = 2
										elif rand > 63 and rand < 128:
											dfn.isConfusedCount = 3
										elif rand > 127 and rand < 192:
											dfn.isConfusedCount = 4
										elif rand > 191 and rand < 256:
											dfn.isConfusedCount = 5
										time.sleep(1)
										print("{pname} became confused!".format(pname = dfn.name))
						elif att.movetype == "recoil":
							damage, crit, mult = self.getDamage(off, att, dfn)
						
							if damage == "failed":
								time.sleep(1)
								print("{movename} failed!".format(movename = att.name))
							elif damage == 65535:
								time.sleep(1)
								print("One Hit KO!")
							elif damage == "noEffect" or mult == 0:
								time.sleep(1)
								print("{movename} doesn't effect {opponent}!".format(movename = att.name, opponent = dfn.name))
							elif damage >= 0 and mult > 0:
								self.takeHP(dfn, damage)
								if crit:
									time.sleep(1)
									print("Critical hit!")
								if mult > 10:
									time.sleep(1)
									print("It was super effective! {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
								elif mult < 10:
									time.sleep(1)
									print("It wasn't very effective... {hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
								elif mult == 10:
									time.sleep(1)
									print("{hplost} damage taken by {pname}".format(hplost = str(damage), pname = dfn.name))
								self.takeHP(off, math.floor((damage * att.recoil[0])/att.recoil[1]))
								print("{hplost} recoil damage taken by {pname}".format(hplost = str(damage), pname = off.name))



						




	def useAttack(self, off, att, dfn):
		results = {}
		nothandledyet = ["Absorb", "Barrage", "Bide", "Bind", "Bonemerang", "Clamp", "Comet Punch", "Conversion", "Counter", "Dig", "Disable", "Double Kick", "Double Slap", "Dream Eater", "Explosion", "Fire Spin", "Fly", "Focus Energy", "Fury Attack", "Fury Swipes", "Haze", "High Jump Kick", "Hyper Beam", "Jump Kick", "Leech Life", "Leech Seed", "Light Screen", "Mega Drain", "Metronome", "Mimic", "Mirror Move", "Mist", "Petal Dance", "Pin Missile", "Rage", "Razor Wind", "Recover", "Reflect", "Rest", "Roar", "Self-Destruct", "Skull Bash", "Sky Attack", "Soft-Boiled", "Solar Beam", "Spike Cannon", "Splash", "Struggle", "Submission", "Substitute", "Take Down", "Teleport", "Thrash", "Toxic", "Transform", "Twin Needle", "Whirlwind", "Wrap"]
		if att.movetype == "other":
			print("lol not yet implemented sorry")
			results["damage"] = None
			results["isCrit"] = False
			results["tmult"] = 10
			results["statusEffects"] = None
			results["flinchorconfuse"] = False
			results["offStatMods"] = None
			results["dfnStatMods"] = None
			return results

		results["statMods"] = []
		if att.basePower != 0 and att.target == "normal":
			results["damage"], results["isCrit"], results["tmult"] = self.getDamage(off, att, dfn)
			if att.secondary:
				if "status" in att.secondary:
					rand = random.randint(0, 256)
					if rand < math.floor(att.secondary["chance"] * 2.55):
						if "status" in att.secondary.keys():
							if att.secondary["status"] == "brn" and dfn.nonVolatileStatus == None and "Fire" not in dfn.type:
								dfn.nonVolatileStatus == "Burned"
								results["statusEffects"] = "burned"

							if att.secondary["status"] == "frz" and dfn.nonVolatileStatus == None and "Ice" not in dfn.type:
								dfn.nonVolatileStatus == "Frozen"
								results["statusEffects"] = "frozen"

							if att.secondary["status"] == "par" and dfn.nonVolatileStatus == None:
								if att.type == "Electric" and "Electric" in dfn.type:
									pass
								if att.name == "Body Slam" and "Normal" in dfn.type:
									pass
								if att.name == "Lick" and "Ghost" in dfn.type:
									pass
								else:
									dfn.nonVolatileStatus == "Paralyzed"
									results["statusEffects"] = "paralyzed"
							if att.secondary["status"] == "psn" and dfn.nonVolatileStatus == None and "Poison" not in dfn.type:
								dfn.nonVolatileStatus = "Poisoned"
								results["statusEffects"] = "poisoned"
				if att.secondary["volatileStatus"] in att.secondary.keys():
					if att.secondary["volatileStatus"] == "flinch":
						rand = random.randint(0, 256)
						if rand < math.floor(att.secondary["chance"] * 2.55):
							dfn.willFlinch = True
							results["flinchorconfuse"] = "flinch"
					if att.secondary["volatileStatus"] == "confusion" and not dfn.isConfused:
						rand = random.randint(0, 256)
						if rand < math.floor(att.secondary["chance"] * 2.55):
							dfn.isConfused = True
							results["flinchorconfuse"] = "confused"
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
								results["dfnStatMods"].append("Attack")
								results["dfnStatMods"][-1].append(self.statMod(dfn.statAtk, dfn.battAtk, dfn.Atklvl, att.secondary["boosts"]["atk"]))
							elif key == "def":
								results["dfnStatMods"].append("Defense")	
								results["dfnStatMods"][-1].append(self.statMod(dfn.statDef, dfn.battDef, dfn.Deflvl, att.secondary["boosts"]["def"]))
							elif key == "spa":
								results["dfnStatMods"].append("Special")
								results["dfnStatMods"][-1].append(self.statMod(dfn.statSpa, dfn.battSpa, dfn.Spalvl, att.secondary["boosts"]["spa"]))
							elif key == "spe":
								results["dfnStatMods"].append("Speed")
								results["dfnStatMods"][-1].append(self.statMod(dfn.statSpe, dfn.battSpe, dfn.Spelvl, att.secondary["boosts"]["spe"]))


		if att.target == "self":
			for key in att.boosts.keys():
				if key == "atk":
					results["offStatMods"].append("Attack")
					results["offStatMods"][-1].append(self.statMod(off.statAtk, off.battAtk, off.Atklvl, att.secondary["boosts"]["atk"]))
				elif key == "def":
					results["offStatMods"].append("Defense")	
					results["offStatMods"][-1].append(self.statMod(off.statDef, off.battDef, off.Deflvl, att.secondary["boosts"]["def"]))
				elif key == "spa":
					results["offStatMods"].append("Special")
					results["offStatMods"][-1].append(self.statMod(off.statSpa, off.battSpa, off.Spalvl, att.secondary["boosts"]["spa"]))
				elif key == "spe":
					results["offStatMods"].append("Speed")
					results["offStatMods"][-1].append(self.statMod(off.statSpe, off.battSpe, off.Spelvl, att.secondary["boosts"]["spe"]))
		if att.target == "normal" and att.basePower == 0 and att.boosts:
			for key in att.boosts.keys():
				if key == "atk":
					results["dfnStatMods"].append("Attack")
					results["dfnStatMods"][-1].append(self.statMod(dfn.statAtk, dfn.battAtk, dfn.Atklvl, att.secondary["boosts"]["atk"]))
				elif key == "def":
					results["dfnStatMods"].append("Defense")	
					results["dfnStatMods"][-1].append(self.statMod(dfn.statDef, dfn.battDef, dfn.Deflvl, att.secondary["boosts"]["def"]))
				elif key == "spa":
					results["dfnStatMods"].append("Special")
					results["dfnStatMods"][-1].append(self.statMod(dfn.statSpa, dfn.battSpa, dfn.Spalvl, att.secondary["boosts"]["spa"]))
				elif key == "spe":
					results["dfnStatMods"].append("Speed")
					results["dfnStatMods"][-1].append(self.statMod(dfn.statSpe, dfn.battSpe, dfn.Spelvl, att.secondary["boosts"]["spe"]))
		if att.target == "normal" and att.basePower == 0 and (att.status or att.volatileStatus):
			if att.volatileStatus == "confusion" and not dfn.isConfused:
				rand = random.randint(0, 256)
				dfn.isConfused = True
				results["flinchorconfuse"] = "confused"
				if rand < 64:
					dfn.isConfusedCount = 2
				elif rand > 63 and rand < 128:
					dfn.isConfusedCount = 3
				elif rand > 127 and rand < 192:
					dfn.isConfusedCount = 4
				elif rand > 191 and rand < 256:
					dfn.isConfusedCount = 5
			if att.status == "brn" and dfn.nonVolatileStatus == None and "Fire" not in dfn.type:
				dfn.nonVolatileStatus == "Burned"
				results["statusEffects"] = "burned"

			if att.status == "frz" and dfn.nonVolatileStatus == None and "Ice" not in dfn.type:
				dfn.nonVolatileStatus == "Frozen"
				results["statusEffects"] = "frozen"

			if att.status == "par" and dfn.nonVolatileStatus == None:
				if att.type == "Electric" and "Electric" in dfn.type:
					pass
				if att.name == "Body Slam" and "Normal" in dfn.type:
					pass
				if att.name == "Lick" and "Ghost" in dfn.type:
					pass
				else:
					dfn.nonVolatileStatus == "Paralyzed"
					results["statusEffects"] = "paralyzed"


			if att.status == "psn" and dfn.nonVolatileStatus == None and "Poison" not in dfn.type:
				dfn.nonVolatileStatus = "Poisoned"
				results["statusEffects"] = "poisoned"

# HANDLE PURE STATMOD MOVES THEN TEST
		return results


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

		if att.name == "Dragon Rage":
			if T != 0:
				return 40, False, 10
			else:
				return "noEffect", False, 0

		if att.name == "Sonic Boom":
			return 20, False, 10

		if att.name == "Night Shade":
			P = off.level
			if T == 0:
				T = 10

		if att.name == "Psywave":
			return max(1, math.floor((off.level * (random.randint(0,101) + 50))/100)), False, 10

		if att.name == "Seismic Toss":
			return off.level, False, 10

		if att.name == "superfang":
			return max(1, math.floor(dfn.battHP/2)), False, 10

		if att.name == "Fissure" or att.name == "Guillotine" or att.name == "Horn Drill":
			if dfn.battSpe > off.battSpe:
				return "failed", False, 10
			else:
				return 65535, False, 10

		if att.name == "Quick Attack":
			if T == 0:
				T = 10


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
		
		out = 10
		for ptype in dfn.type:
			out *= self.tchart[atype]["damageTaken"][ptype]
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


