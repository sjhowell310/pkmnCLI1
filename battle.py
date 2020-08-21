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
		print("\n{name1: <30}{name2: >30}\n".format(name1 = self.t1.name, name2 = self.t2.name))
		print("{name1: <30}{name2: >30}\n".format(name1 = self.t1.activePokemon.name, name2 = self.t2.activePokemon.name))
		print("{hp: <3}{currhp1: >4}/{tothp1: <4}{status1: >7}{stat1: <4}{space: >14}{hp: >3}{currhp2: >4}/{tothp2: <4}{status1: >7}{stat2: >4}\n".format(hp = "HP:", currhp1 = str(self.t1.activePokemon.battHP), tothp1 = str(self.t1.activePokemon.statHP), status1 = "Status:", stat1 = str(self.t1.activePokemon.nonVolatileStatus), currhp2 = str(self.t2.activePokemon.battHP), tothp2 = str(self.t2.activePokemon.statHP), stat2 = str(self.t2.activePokemon.nonVolatileStatus), space = ""))
		print("{statone: <4}:{stat1: <3} {batt1: <16}{stat2: >16} {batt2: >3}:{stattwo: >4}\n".format(statone = "Atk", stat1 = self.t1.activePokemon.statAtk, batt1 = self.t1.activePokemon.battAtk, stattwo = "Atk", stat2 = self.t2.activePokemon.statAtk, batt2 = self.t2.activePokemon.battAtk))
		print("{statone: <4}:{stat1: <3} {batt1: <16}{stat2: >16} {batt2: >3}:{stattwo: >4}\n".format(statone = "Def", stat1 = self.t1.activePokemon.statDef, batt1 = self.t1.activePokemon.battDef, stattwo = "Def", stat2 = self.t2.activePokemon.statDef, batt2 = self.t2.activePokemon.battDef))
		print("{statone: <4}:{stat1: <3} {batt1: <16}{stat2: >16} {batt2: >3}:{stattwo: >4}\n".format(statone = "Spa", stat1 = self.t1.activePokemon.statSpa, batt1 = self.t1.activePokemon.battSpa, stattwo = "Spa", stat2 = self.t2.activePokemon.statSpa, batt2 = self.t2.activePokemon.battSpa))
		print("{statone: <4}:{stat1: <3} {batt1: <16}{stat2: >16} {batt2: >3}:{stattwo: >4}\n".format(statone = "Spe", stat1 = self.t1.activePokemon.statSpe, batt1 = self.t1.activePokemon.battSpe, stattwo = "Spe", stat2 = self.t2.activePokemon.statSpe, batt2 = self.t2.activePokemon.battSpe))
		print("{statone: <4}:{stat1: <3} {batt1: <16}{stat2: >16} {batt2: >3}:{stattwo: >4}\n".format(statone = "Acc", stat1 = self.t1.activePokemon.statAcc, batt1 = self.t1.activePokemon.battAcc, stattwo = "Acc", stat2 = self.t2.activePokemon.statAcc, batt2 = self.t2.activePokemon.battAcc))
		print("{statone: <4}:{stat1: <3} {batt1: <16}{stat2: >16} {batt2: >3}:{stattwo: >4}\n".format(statone = "Eva", stat1 = self.t1.activePokemon.statEva, batt1 = self.t1.activePokemon.battEva, stattwo = "Eva", stat2 = self.t2.activePokemon.statEva, batt2 = self.t2.activePokemon.battEva))



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
				self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2)
				if self.t1.activePokemon.battHP == 0:
					if not self.isWhiteOut():
						time.sleep(1)
						print("{pname} fainted!\n".format(self.t1.activePokemon.name))
						self.battleSwitch(self.t1)
					else:
						time.sleep(1)
						print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
						time.sleep(1)
						print("{name} whited out!\n".format(name = self.t1.name))
						return

			elif t1a == "attack" and t2a == "switch":		
				self.t2.switchIn(self.t2.party[t2c])
				self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 2)
				if self.t2.activePokemon.battHP == 0:
					if not self.isWhiteOut():
						time.sleep(1)
						print("{pname} fainted!\n".format(pname = self.t2.activePokemon.name))
						self.battleSwitch(self.t2)
					else:
						time.sleep(1)
						print("{pname} fainted!\n".format(pname = self.t2.activePokemon.name))
						time.sleep(1)
						print("{name} whited out!\n".format(name = self.t2.name))
						return
			elif t1a == "switch" and t2a == "switch":
				self.t1.switchIn(self.t1.party[t1c])
				self.t2.switchIn(self.t2.party[t2c])
		else:
			if self.t1.activePokemon.moves[t1c].priority > self.t2.activePokemon.moves[t2c].priority:				
				self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1)	
				if self.t2.activePokemon.battHP == 0:
					if not self.isWhiteOut():
						time.sleep(1)
						print("{pname} fainted!\n".format(pname = self.t2.activePokemon.name))
						self.battleSwitch(self.t2)
						return
					else:
						time.sleep(1)
						print("{pname} fainted!\n".format(pname = self.t2.activePokemon.name))
						time.sleep(1)
						print("{name} whited out!\n".format(name = self.t2.name))
						return
				self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2)
				if self.t1.activePokemon.battHP == 0:
					if not self.isWhiteOut():
						time.sleep(1)
						print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
						self.battleSwitch(self.t1)
						return
					else:
						time.sleep(1)
						print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
						time.sleep(1)
						print("{name} whited out!\n".format(name = self.t1.name))
						return

			elif self.t1.activePokemon.moves[t1c].priority < self.t2.activePokemon.moves[t2c].priority:				
				self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 1)
				if self.t1.activePokemon.battHP == 0:
					if not self.isWhiteOut():
						time.sleep(1)
						print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
						self.battleSwitch(self.t1)
						return
					else:
						time.sleep(1)
						print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
						time.sleep(1)
						print("{name} whited out!\n".format(name = self.t1.name))
						return
				self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 2)
				if self.t2.activePokemon.battHP == 0:
					if not self.isWhiteOut():
						time.sleep(1)
						print("{pname} fainted!\n".format(pname = self.t2.activePokemon.name))
						self.battleSwitch(self.t2)
						return					
					else:
						time.sleep(1)
						print("{pname} fainted!\n".format(pname = self.t2.activePokemon.name))
						time.sleep(1)
						print("{name} whited out!\n".format(name = self.t2.name))
						return

			elif self.t1.activePokemon.moves[t1c].priority == self.t2.activePokemon.moves[t2c].priority:
				if t1s > t2s:					
					self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1)	
					if self.t2.activePokemon.battHP == 0:
						if not self.isWhiteOut():
							time.sleep(1)
							print("{pname} fainted!\n".format(pname = self.t2.activePokemon.name))
							self.battleSwitch(self.t2)
							return
						else:
							time.sleep(1)
							print("{pname} fainted!\n".format(pname = self.t2.activePokemon.name))
							time.sleep(1)
							print("{name} whited out!\n".format(name = self.t2.name))
							return		
					self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2)
					if self.t1.activePokemon.battHP == 0:
						if not self.isWhiteOut():
							time.sleep(1)
							print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
							self.battleSwitch(self.t1)
							return
						else:
							time.sleep(1)
							print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
							time.sleep(1)
							print("{name} whited out!\n".format(name = self.t1.name))
							return

				elif t1s < t2s:					
					self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 1)	
					if self.t1.activePokemon.battHP == 0:
						if not self.isWhiteOut():
							time.sleep(1)
							print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
							self.battleSwitch(self.t1)
							return
						else:
							time.sleep(1)
							print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
							time.sleep(1)
							print("{name} whited out!\n".format(name = self.t1.name))
							return
					self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 2)
					if self.t2.activePokemon.battHP == 0:
						if not self.isWhiteOut():
							time.sleep(1)
							print("{pname} fainted!\n".format(pname = self.t2.activePokemon.name))
							self.battleSwitch(self.t2)
							return
						else:
							time.sleep(1)
							print("{pname} fainted!\n".format(pname = self.t2.activePokemon.name))
							time.sleep(1)
							print("{name} whited out!\n".format(name = self.t2.name))
							return

				elif t1s == t2s:
					rand = random.randint(0,256)
					if rand < 128:					
						self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 1)	
						if self.t2.activePokemon.battHP == 0:
							if not self.isWhiteOut():
								time.sleep(1)
								print("{pname} fainted!\n".format(pname = self.t2.activePokemon.name))
								self.battleSwitch(self.t2)
								return
							else:
								time.sleep(1)
								print("{pname} fainted!\n".format(pname = self.t2.activePokemon.name))
								time.sleep(1)
								print("{name} whited out!\n".format(name = self.t2.name))
								return			
						self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 2)
						if self.t1.activePokemon.battHP == 0:
							if not self.isWhiteOut():
								time.sleep(1)
								print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
								self.battleSwitch(self.t1)
								return
							else:
								time.sleep(1)
								print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
								time.sleep(1)
								print("{name} whited out!\n".format(name = self.t1.name))
								return
					else:
						self.attack(self.t2.activePokemon, self.t2.activePokemon.moves[t2c], self.t1.activePokemon, 1)
						if self.t1.activePokemon.battHP == 0:
							if not self.isWhiteOut():
								time.sleep(1)
								print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
								self.battleSwitch(self.t1)
								return
							else:
								time.sleep(1)
								print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
								time.sleep(1)
								print("{name} whited out!\n".format(name = self.t1.name))
								return				
						self.attack(self.t1.activePokemon, self.t1.activePokemon.moves[t1c], self.t2.activePokemon, 2)	
						if self.t2.activePokemon.battHP == 0:
							if not self.isWhiteOut():
								time.sleep(1)
								print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
								self.battleSwitch(self.t2)
								return
							else:
								time.sleep(1)
								print("{pname} fainted!\n".format(pname = self.t1.activePokemon.name))
								time.sleep(1)
								print("{name} whited out!\n".format(name = self.t1.name))
								return					


	def attack(self, off, att, dfn, firstorsecond):
		cantAttack = False

		if firstorsecond == 1:
			off.willFlinch = False
		elif firstorsecond == 2 and off.willFlinch:
			cantAttack = True
			off.willFlinch = False
			time.sleep(1)
			print("{name} flinched!\n".format(name = off.name))


		if not cantAttack:
			if off.nonVolatileStatus == "Frozen":
				time.sleep(1)
				print("{name} is frozen solid!\n".format(name = off.name))
				cantAttack = True
			elif off.nonVolatileStatus == "Asleep":
				off.nonVolatileCount -= 1
				if off.nonVolatileCount > 0:
					time.sleep(1)
					print("{name} is fast asleep!\n".format(name = off.name))
					cantAttack = True
				else:
					time.sleep(1)
					off.nonVolatileStatus = None
					off.nonVolatileCount = 0
					print("{name} woke up!\n".format(name = off.name))
					cantAttack = True
			elif off.isRecharging:
					time.sleep(1)
					print("{name} has to recharge!\n".format(name = off.name))
					cantAttack = True
					off.isRecharging = False
			elif off.disabledMove[0] > 0:
					off.disabledMove[0] -= 1
					if off.disabledMove[0] == 0:
						off.disabledMove[1] = 0
						time.sleep(1)
						print("{name}'s {movename} is no longer disabled!\n".format(name = off.name, movename = att.name))
					elif off.disabledMove[0] > 0 and off.disabledMove[1] == att.name:
						time.sleep(1)
						print("{name}'s {movename} is disabled!\n".format(name = off.name, movename = att.name))
			elif off.isConfused:
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
				elif off.nonVolatileStatus == "Paralyzed":
					rand = random.randint(0,256)
					if rand < 64:
						time.sleep(1)
						print("{name} is fully paralyzed and can't move!\n".format(name = off.name))
						cantAttack = True
				elif off.isConfusedCount > 0:
					rand = random.randint(0,256)
					if rand < 128:
						time.sleep(1)
						print("{name} hurt itself in its confusion!\n".format(name = off.name))
						self.takeConfusionDamage(off)
						cantAttack = True
						if off.battHP == 0:
							return
			elif off.nonVolatileStatus == "Paralyzed":
				rand = random.randint(0,256)
				if rand < 64:
					time.sleep(1)
					print("{name} is fully paralyzed and can't move!\n".format(name = off.name))
					cantAttack = True	

		if not cantAttack:					
			att.pp -= 1
			if att.name != "Swift" and att.movetype != "selfStat":
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
				if att.movetype == "dmgIfMiss" and "Ghost" not in dfn.type:
					time.sleep(1)
					print("{name} kept going and crashed, taking damage!\n".format(name = off.name))
					damage = self.takeHP(off, 1)
			else:
				if att.movetype == "selfStat":
					if "atk" in att.boosts.keys():
						mod = self.statMod(off, "atk", att.boosts["atk"])
						stat = "Attack"
					elif "def" in att.boosts.keys():
						mod = self.statMod(off, "def", att.boosts["def"])
						stat = "Defense"
					elif "spa" in att.boosts.keys():
						mod = self.statMod(off, "spa", att.boosts["spa"])
						stat = "Special"
					elif "spe" in att.boosts.keys():
						mod = self.statMod(off, "spe", att.boosts["spe"])
						stat = "Speed"
					elif "accuracy" in att.boosts.keys():
						mod = self.statMod(off, "accuracy", att.boosts["accuracy"])
						stat = "Accuracy"
					elif "evasion" in att.boosts.keys():
						mod = self.statMod(off, "evasion", att.boosts["evasion"])
						stat = "Evasion"
					if mod == 0:
						time.sleep(1)
						print("Nothing happened!\n")
					elif mod == 1:
						time.sleep(1)
						print("{pname}'s {stat} rose!\n".format(pname = off.name, stat = stat))
					elif mod == 2:
						time.sleep(1)
						print("{pname}'s {stat} greatly rose!\n".format(pname = off.name, stat = stat))
				elif att.movetype == "offStat":
					if "atk" in att.boosts.keys():
						mod = self.statMod(dfn, "atk", att.boosts["atk"])
						stat = "Attack"
					elif "def" in att.boosts.keys():
						mod = self.statMod(dfn, "def", att.boosts["def"])
						stat = "Defense"
					elif "spa" in att.boosts.keys():
						mod = self.statMod(dfn, "spa", att.boosts["spa"])
						stat = "Special"
					elif "spe" in att.boosts.keys():
						mod = self.statMod(dfn, "spe", att.boosts["spe"])
						stat = "Speed"
					elif "accuracy" in att.boosts.keys():
						mod = self.statMod(dfn, "accuracy", att.boosts["accuracy"])
						stat = "Accuracy"
					elif "evasion" in att.boosts.keys():
						mod = self.statMod(dfn, "evasion", att.boosts["evasion"])
						stat = "Evasion"
					if mod == 0:
						time.sleep(1)
						print("Nothing happened!\n")
					elif mod == -1:
						time.sleep(1)
						print("{pname}'s {stat} fell!\n".format(pname = dfn.name, stat = stat))
					elif mod == -2:
						time.sleep(1)
						print("{pname}'s {stat} greatly fell!\n".format(pname = dfn.name, stat = stat))
				elif att.movetype == "dmgOnly" or "dmgIfMiss":
					damage, crit, mult = self.getDamage(off, att, dfn)
				
					if damage == "failed":
						time.sleep(1)
						print("{movename} failed!\n".format(movename = att.name))
					elif damage == 65535:
						time.sleep(1)
						print("One Hit KO!\n")
					elif damage == "noEffect" or mult == 0:
						time.sleep(1)
						print("{movename} doesn't effect {opponent}!\n".format(movename = att.name, opponent = dfn.name))
					elif damage >= 0 and mult > 0:
						damage = self.takeHP(dfn, damage)
						if crit:
							time.sleep(1)
							print("Critical hit!\n")
						if mult > 10:
							time.sleep(1)
							print("It was super effective! {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						elif mult < 10:
							time.sleep(1)
							print("It wasn't very effective... {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						elif mult == 10:
							time.sleep(1)
							print("{hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						if dfn.battHP == 0:
							return
				elif att.movetype == "dmgStat":
					damage, crit, mult = self.getDamage(off, att, dfn)
				
					if damage == "failed":
						time.sleep(1)
						print("{movename} failed!\n".format(movename = att.name))
					elif damage == 65535:
						time.sleep(1)
						print("One Hit KO!\n")
					elif damage == "noEffect" or mult == 0:
						time.sleep(1)
						print("{movename} doesn't effect {opponent}!\n".format(movename = att.name, opponent = dfn.name))
					elif damage >= 0 and mult > 0:
						damage = self.takeHP(dfn, damage)
						if crit:
							time.sleep(1)
							print("Critical hit!\n")
						if mult > 10:
							time.sleep(1)
							print("It was super effective! {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						elif mult < 10:
							time.sleep(1)
							print("It wasn't very effective... {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						elif mult == 10:
							time.sleep(1)
							print("{hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						if dfn.battHP == 0:
							return
						rand = random.randint(0,256)
						if rand < math.floor(att.secondary["chance"] * 2.55):
							if "atk" in att.secondary["boosts"].keys():
								mod = self.statMod(dfn, "atk", att.secondary["boosts"]["atk"])
								stat = "Attack"
							elif "def" in att.secondary["boosts"].keys():
								mod = self.statMod(dfn, "def", att.secondary["boosts"]["def"])
								stat = "Defense"
							elif "spa" in att.secondary["boosts"].keys():
								mod = self.statMod(dfn, "spa", att.secondary["boosts"]["spa"])
								stat = "Special"
							elif "spe" in att.secondary["boosts"].keys():
								mod = self.statMod(dfn, "spe", att.secondary["boosts"]["spe"])
								stat = "Speed"
							elif "accuracy" in att.secondary["boosts"].keys():
								mod = self.statMod(dfn, "accuracy", att.secondary["boosts"]["accuracy"])
								stat = "Accuracy"
							elif "evasion" in att.secondary["boosts"].keys():
								mod = self.statMod(dfn, "evasion", att.secondary["boosts"]["evasion"])
								stat = "Evasion"
							if mod == -1:
								time.sleep(1)
								print("{pname}'s {stat} fell!\n".format(pname = dfn.name, stat = stat))
							elif mod == -2:
								time.sleep(1)
								print("{pname}'s {stat} greatly fell!\n".format(pname = dfn.name, stat = stat))
				elif att.movetype == "offStatus":
					if att.status:
						if dfn.nonVolatileStatus:
							time.sleep(1)
							print("But it failed!\n")
						else:
							if att.status == "par":
								if att.type == "Electric" and "Electric" in dfn.type:
									time.sleep(1)
									print("But it failed!\n")
								else:
									time.sleep(1)
									print("{pname} became Paralyzed! It may not attack!\n".format(pname = dfn.name))
									dfn.nonVolatileStatus = "Paralyzed"
							elif att.status == "psn":
								if "Poison" in dfn.type:
									time.sleep(1)
									print("But it failed!\n")
								else:
									time.sleep(1)
									print("{pname} was poisoned!\n".format(pname = dfn.name))
									dfn.nonVolatileStatus = "Poisoned"
							elif att.status == "slp":
								time.sleep(1)
								print("{pname} fell asleep!\n".format(pname = dfn.name))
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
									print("But it failed!\n")
								else:
									time.sleep(1)
									print("{pname} was badly poisoned!\n".format(pname = dfn.name))
									dfn.nonVolatileStatus = "Toxic"
					elif att.volatileStatus == "confusion":
						if dfn.isConfused:
							time.sleep(1)
							print("{pname} is already confused!\n".format(pname = dfn.name))
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
							dfn.isConfused = True
							print("{pname} became confused!\n".format(pname = dfn.name))
				elif att.movetype == "dmgStatus":
					damage, crit, mult = self.getDamage(off, att, dfn)
				
					if damage == "failed":
						time.sleep(1)
						print("{movename} failed!\n".format(movename = att.name))
					elif damage == 65535:
						time.sleep(1)
						print("One Hit KO!\n")
					elif damage == "noEffect" or mult == 0:
						time.sleep(1)
						print("{movename} doesn't effect {opponent}!\n".format(movename = att.name, opponent = dfn.name))
					elif damage >= 0 and mult > 0:
						damage = self.takeHP(dfn, damage)
						if crit:
							time.sleep(1)
							print("Critical hit!\n")
						if mult > 10:
							time.sleep(1)
							print("It was super effective! {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						elif mult < 10:
							time.sleep(1)
							print("It wasn't very effective... {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						elif mult == 10:
							time.sleep(1)
							print("{hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						if dfn.battHP == 0:
							return
						rand = random.randint(0, 256)
						# print("sampling, {sample}, suucess {success}".format(sample = rand, success = math.floor(att.secondary["chance"] * 2.55)))
						if rand < math.floor(att.secondary["chance"] * 2.55):
							if "status" in att.secondary.keys():
								if att.secondary["status"] == "par":
										if att.type == "Electric" and "Electric" in dfn.type:
											pass
										elif att.name == "Body Slam" and "Normal" in dfn.type:
											pass
										elif att.name == "Lick" and "Ghost" in dfn.type:
											pass
										else:
											time.sleep(1)
											print("{pname} became Paralyzed! It may not attack!\n".format(pname = dfn.name))
											dfn.nonVolatileStatus = "Paralyzed"
								elif att.secondary["status"] == "psn":
									if "Poison" in dfn.type:
										pass
									else:
										time.sleep(1)
										print("{pname} was poisoned!\n".format(pname = dfn.name))
										dfn.nonVolatileStatus = "Poisoned"
								elif att.secondary["status"] == "frz":
									if "Ice" in dfn.type:
										pass
									else:
										time.sleep(1)
										print("{pname} was frozen!\n".format(pname = dfn.name))
										dfn.nonVolatileStatus = "Frozen"
								elif att.secondary["status"] == "brn":
									if "Fire" in dfn.type:
										pass
									else:
										time.sleep(1)
										print("{pname} was burned!\n".format(pname = dfn.name))
										dfn.nonVolatileStatus = "Burned"
								elif att.secondary["status"] == "slp":
									time.sleep(1)
									print("{pname} fell asleep!\n".format(pname = dfn.name))
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
							elif "volatileStatus" in att.secondary.keys():
								if att.secondary["volatileStatus"] == "confusion":
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
										dfn.isConfused = True
										print("{pname} became confused!\n".format(pname = dfn.name))
								elif att.secondary["volatileStatus"] == "flinch":
									dfn.willFlinch = True
				elif att.movetype == "recoil":
						damage, crit, mult = self.getDamage(off, att, dfn)
					
						if damage == "failed":
							time.sleep(1)
							print("{movename} failed!\n".format(movename = att.name))
						elif damage == 65535:
							time.sleep(1)
							print("One Hit KO!\n")
						elif damage == "noEffect" or mult == 0:
							time.sleep(1)
							print("{movename} doesn't effect {opponent}!\n".format(movename = att.name, opponent = dfn.name))
						elif damage >= 0 and mult > 0:
							damage = self.takeHP(dfn, damage)
							if crit:
								time.sleep(1)
								print("Critical hit!\n")
							if mult > 10:
								time.sleep(1)
								print("It was super effective! {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
							elif mult < 10:
								time.sleep(1)
								print("It wasn't very effective... {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
							elif mult == 10:
								time.sleep(1)
								print("{hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
							damage = self.takeHP(off, math.floor((damage * att.recoil[0])/att.recoil[1]))
							print("{hplost} recoil damage taken by {pname}\n".format(hplost = str(damage), pname = off.name))
							if dfn.battHP == 0:
								return
				elif att.movetype == "drain":
					if att.name != "Dream Eater":
						damage, crit, mult = self.getDamage(off, att, dfn)
					elif att.name == "Dream Eater":
						if dfn.nonVolatileStatus == "Asleep":
							damage, crit, mult = self.getDamage(off, att, dfn)
						else:
							damage, crit, mult = "failed", False, 10
					if damage == "failed":
						time.sleep(1)
						print("{movename} failed!\n".format(movename = att.name))
					elif damage == 65535:
						time.sleep(1)
						print("One Hit KO!\n")
					elif damage == "noEffect" or mult == 0:
						time.sleep(1)
						print("{movename} doesn't effect {opponent}!\n".format(movename = att.name, opponent = dfn.name))
					elif damage >= 0 and mult > 0:
						damage = self.takeHP(dfn, damage)
						if crit:
							time.sleep(1)
							print("Critical hit!\n")
						if mult > 10:
							time.sleep(1)
							print("It was super effective! {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						elif mult < 10:
							time.sleep(1)
							print("It wasn't very effective... {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						elif mult == 10:
							time.sleep(1)
							print("{hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						damage = self.takeHP(off, -1 * max(1, math.floor(damage/2)))
						if damage > 0:
							print("{hplost} damage recovered by {pname}\n".format(hplost = str(damage), pname = off.name))
						if damage == 0:
							print("{pname}'s HP is already full!\n".format(pname = off.name))
						if dfn.battHP == 0:
							return
				elif att.movetype == "recharge":
					damage, crit, mult = self.getDamage(off, att, dfn)
					off.isRecharging = True
					if damage == "failed":
						time.sleep(1)
						print("{movename} failed!\n".format(movename = att.name))
					elif damage == 65535:
						time.sleep(1)
						print("One Hit KO!\n")
					elif damage == "noEffect" or mult == 0:
						time.sleep(1)
						print("{movename} doesn't effect {opponent}!\n".format(movename = att.name, opponent = dfn.name))
					elif damage >= 0 and mult > 0:
						damage = self.takeHP(dfn, damage)
						if crit:
							time.sleep(1)
							print("Critical hit!\n")
						if mult > 10:
							time.sleep(1)
							print("It was super effective! {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						elif mult < 10:
							time.sleep(1)
							print("It wasn't very effective... {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						elif mult == 10:
							time.sleep(1)
							print("{hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						if dfn.battHP == 0:
							return
				elif att.movetype == "multiHit":
					# FIX THIS PRINTING ISSUE AND CRITICAL HIT DAMAGE
					damage, crit, mult = self.getDamage(off, att, dfn)
					if damage == "failed":
						time.sleep(1)
						print("{movename} failed!\n".format(movename = att.name))
					elif damage == 65535:
						time.sleep(1)
						print("One Hit KO!\n")
					elif damage == "noEffect" or mult == 0:
						time.sleep(1)
						print("{movename} doesn't effect {opponent}!\n".format(movename = att.name, opponent = dfn.name))
					elif damage >= 0 and mult > 0:
						if crit:
							time.sleep(1)
							print("Critical hit!\n")
						if type(att.multihit) != int:
							rand = random.randint(0, 255)
							if rand < 96:
								hits = 2
							elif rand > 95 and rand < 192:
								hits = 3
							elif rand > 191 and rand < 224:
								hits = 4
							elif rand > 223 and rand < 256:
								hits = 5
						else:
							hits = 2
						j = 0
						for i in range(hits):
							damage = self.takeHP(dfn, damage)
							if mult > 10:
								time.sleep(1)
								print("It was super effective! {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
							elif mult < 10:
								time.sleep(1)
								print("It wasn't very effective... {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
							elif mult == 10:
								time.sleep(1)
								print("{hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
							if i == 1 and att.name == "Twineedle" and dfn.battHP > 0:
								rand = random.randint(0, 256)
								if rand < math.floor(att.secondary["chance"] * 2.55):
									if "Poison" not in dfn.type and not dfn.nonVolatileStatus:
										time.sleep(1)
										print("{pname} was poisoned!\n".format(pname = dfn.name))
										dfn.nonVolatileStatus = "Poisoned"
							if dfn.battHP == 0:
								time.sleep(1)
								print("Hit {pname} {hits} times!\n".format(pname = dfn.name, hits = str(j + 1)))
								return
							j += 1
						print("Hit {pname} {hits} times!\n".format(pname = dfn.name, hits = str(j)))

						# else:
						# 	if damage == "failed":
						# 		time.sleep(1)
						# 		print("{movename} failed!\n".format(movename = att.name))
						# 	elif damage == 65535:
						# 		time.sleep(1)
						# 		print("One Hit KO!\n")
						# 	elif damage == "noEffect" or mult == 0:
						# 		time.sleep(1)
						# 		print("{movename} doesn't effect {opponent}!\n".format(movename = att.name, opponent = dfn.name))
						# 	elif damage >= 0 and mult > 0:
						# 		if crit:
						# 			time.sleep(1)
						# 			print("Critical hit!\n")
						# 		rand = random.randint(0, 255)
						# 		if rand < 96:
						# 			hits = 2
						# 		elif rand > 95 and rand < 192:
						# 			hits = 3
						# 		elif rand > 191 and rand < 224:
						# 			hits = 4
						# 		elif rand > 223 and rand < 256:
						# 			hits = 5
						# 		j = 0
						# 		for i in range(hits):
						# 			damage = self.takeHP(dfn, damage)
						# 			if mult > 10:
						# 				time.sleep(1)
						# 				print("It was super effective! {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						# 			elif mult < 10:
						# 				time.sleep(1)
						# 				print("It wasn't very effective... {hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						# 			elif mult == 10:
						# 				time.sleep(1)
						# 				print("{hplost} damage taken by {pname}\n".format(hplost = str(damage), pname = dfn.name))
						# 			if dfn.battHP == 0:
						# 				time.sleep(1)
						# 				print("Hit {pname} {hits} times!\n".format(pname = dfn.name, hits = str(j + 1)))
						# 				return
						# 			j += 1
						# 		print("Hit {pname} {hits} times!\n".format(pname = dfn.name, hits = str(j)))
			
		
		if off.nonVolatileStatus:
			if off.nonVolatileStatus == "Burned":
				time.sleep(1)
				damage = max(1, math.floor(off.statHP/16))
				damage = self.takeHP(off, damage)
				print("{name} was hurt by it's burn!\n".format(name = off.name, dmg = damage))
			elif off.nonVolatileStatus == "Poisoned":
				time.sleep(1)
				damage = max(1, math.floor(off.statHP/16))
				damage = self.takeHP(off, damage)
				print("{name} was hurt by poison!\n".format(name = off.name))
			elif off.nonVolatileStatus == "Toxic":
				time.sleep(1)
				off.nonVolatileCount +=1
				damage = max(1, math.floor((off.nonVolatileCount * off.statHP)/16))
				damage = self.takeHP(off, damage)
				print("{name} was hurt by poison!\n".format(name = off.name))
		return



	def battleSwitch(self, trainer):
		madeChoice = False
		while not madeChoice:
			time.sleep(1)
			print("{name}! You must choose a member of your party to switch in:\n".format(name = trainer.name))
			trainer.battleShowParty()
			options = len(trainer.party)
			validChoices = ["a","b","c","d", "e", "f"]
			print("(Enter letter of desired option)\n")
			a1 = input()
			a1 = a1.lower()
			while a1 not in validChoices[:options]:
				print("\n(Enter letter of desired option, X to go back)\n")
				a1 = input()
				a1 = a1.lower()
			if a1 in validChoices and a1 != "x":
				if trainer.party[validChoices.index(a1)].battHP == 0:
					print("{name} doesn't have any energy left to battle!\n".format(name = trainer.party[validChoices.index(a1)].name))
				elif trainer.party[validChoices.index(a1)].active == True:
					print("{name} is already in battle!\n".format(name = trainer.activePokemon.name))
				else:
					isSure = ""
					while isSure.lower() != "y" and isSure.lower() != "n":
						isSure = input("You're about to switch {name} into battle. Are you sure? [y/n]\n".format(name = trainer.party[validChoices.index(a1)].name))
					isSure = isSure.lower()
					if isSure == "n":
						madeChoice = False
					elif isSure == "y":
						trainer.switchIn(trainer.party[validChoices.index(a1)])
						madeChoice = True
		
	def takeHP(self, dfn, damage):
		if damage < 0 and dfn.battHP == dfn.statHP:
			return 0
		elif damage < 0 and (dfn.battHP - damage) > dfn.statHP:
			dfn.battHP = dfn.statHP
			damage = (dfn.battHP - damage - dfn.statHP)
		elif damage > dfn.battHP:
			damage = dfn.battHP
			dfn.battHP = 0
		else:
			dfn.battHP -= damage
			if damage < 0:
				damage *= -1
		return damage


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
			return off.level, False, 10

		if att.name == "Psywave":
			return max(1, math.floor((off.level * (random.randint(0,151)))/100)), False, 10

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


	def statMod(self, poke, stat, mod):
		
		if stat == "atk":
			lvl = poke.Atklvl
		elif stat == "def":
			lvl = poke.Deflvl
		elif stat == "spa":
			lvl = poke.Spalvl
		elif stat == "spe":
			lvl = poke.Spelvl
		elif stat == "accuracy":
			lvl = poke.Acclvl
		elif stat == "evasion":
			lvl = poke.Evalvl

		if lvl + mod <= -6:
			mod = -6 - lvl
			lvl = -6
		elif lvl + mod >= 6:
			mod = 6 - lvl
			lvl = 6
		else:
			lvl += mod

		m = 100
		if lvl == -6:
			m = 25
		elif lvl == -5:
			m = 28
		elif lvl == -4:
			m = 33
		elif lvl == -3:
			m = 40
		elif lvl == -2:
			m = 50
		elif lvl == -1:
			m = 66
		elif lvl == 0:
			m = 100
		elif lvl == 1:
			m = 150
		elif lvl == 2:
			m = 200
		elif lvl == 3:
			m = 250
		elif lvl == 4:
			m = 300
		elif lvl == 5:
			m = 350
		elif lvl == 6:
			m = 400

		if stat == "atk":
			poke.battAtk = min(max(1, math.floor((poke.statAtk * m) / 100)), 999)
			poke.Atklvl += mod
		elif stat == "def":
			poke.battDef = min(max(1, math.floor((poke.statDef * m) / 100)), 999)
			poke.Deflvl += mod
		elif stat == "spa":
			poke.battSpa = min(max(1, math.floor((poke.statSpa * m) / 100)), 999)
			poke.Spalvl += mod
		elif stat == "spe":
			poke.battSpe = min(max(1, math.floor((poke.statSpe * m) / 100)), 999)
			poke.Spelvl += mod
		elif stat == "accuracy":
			poke.battAcc = min(max(1, math.floor((255 * m) / 100)), 999)
			poke.Acclvl += mod
		elif stat == "evasion":
			poke.battEva = min(max(1, math.floor((255 * m) / 100)), 999)
			poke.Evalvl += mod

		return mod


