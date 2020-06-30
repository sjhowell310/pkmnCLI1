import trainer
import json
import math
import string
import pokemon
import moveset


#Arena class for use in pkmnCLI1, contains Trainers, weather effects and other holistic battle mechanics (none of these classes extend one another)
class Arena():

	weather = "Clear"

	def __init__(self):
		#prompts user to decide how many pokemon each player is to have in their party (somewhat clunky but input is passed as string, this was easier to implement while also limiting numerical value)
		
		#first trainer is initialised and they're full party is reported after
		self.trainer1 = trainer.Trainer()
		
		#second trainer is initialised and they're full party is reported after
		self.trainer2 = trainer.Trainer()

	#function initiates actual battle protocol
	def startBattle(self):
		validPos = ["1", "2", "3", "4", "5", "6"]
		pokechoice = input("{tname}, which pokemon would you like to send into battle first?\nPlease enter either the pokemon's name or their current position in the party\n".format(tname = self.trainer1.name))
		pokechoice = pokechoice.lower()
		i = 0
		while pokechoice not in validPos and i == 0:
			i = 0
			for member in self.trainer1.party:
				if pokechoice == member.name.lower():
					break
				i += 1
			pokechoice = input("{tname}, which pokemon would you like to send into battle first?\nPlease enter either the pokemon's name or their current position in the party\n".format(tname = self.trainer1.name))
			pokechoice = pokechoice.lower()
		if pokechoice in validPos:
			i = int(pokechoice) - 1

		pokechoice = input("{tname}, which pokemon would you like to send into battle first?\nPlease enter either the pokemon's name or their current position in the party\n".format(tname = self.trainer2.name))
		pokechoice = pokechoice.lower()
		j = 0
		while pokechoice not in validPos and j == 0:
			j = 0
			for member in self.trainer2.party:
				if pokechoice == member.name.lower():
					break
				j += 1
			pokechoice = input("{tname}, which pokemon would you like to send into battle first?\nPlease enter either the pokemon's name or their current position in the party\n".format(tname = self.trainer2.name))
			pokechoice = pokechoice.lower()
		if pokechoice in validPos:
			j = int(pokechoice) - 1

		self.trainer1.switchIn(self.trainer1.party[i])
		self.trainer2.switchIn(self.trainer2.party[j])
		print("{tname} sent {current} into battle!".format(tname = self.trainer1.name, current = self.trainer1.activePokemon.name))
		print("{tname} sent {current} into battle!".format(tname = self.trainer2.name, current = self.trainer2.activePokemon.name))



# battle = Arena()
# battle.startBattle()
# print("TRAINER1")
# print(battle.trainer1.activePokemon.name)
# print("\n".join("{name: <15}{mtype: <10}".format(name = key.name, mtype = str(key.active)) for key in battle.trainer1.party))

# print("TRAINER2")
# print(battle.trainer2.activePokemon.name)
# print("\n".join("{name: <15}{mtype: <10}".format(name = key.name, mtype = str(key.active)) for key in battle.trainer2.party))




