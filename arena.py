import trainer
import json
import math
import string
import pokemon
import moves

#Arena class for use in pkmnCLI1, contains Trainers, weather effects and other holistic battle mechanics (none of these classes extend one another)
class Arena():

	weather = "Clear"

	def __init__(self):
		#prompts user to decide how many pokemon each player is to have in their party (somewhat clunky but input is passed as string, this was easier to implement while also limiting numerical value)
		partySize = 7
		validsizes = ["1", "2", "3", "4", "5", "6"]
		while partySize not in validsizes:
			partySize = input("Contestants, decide and enter how many Pokemon you will both have in your parties\n")
		isRandom = ""
		while isRandom.lower() != "y" and isRandom.lower() != "n":
			isRandom = input("EVs are set to be randomised by default, would you like them to be randomised instead? [y/n]")
		isRandom = isRandom.lower()
		#first trainer is initialised and they're full party is reported after
		self.trainer1 = trainer.Trainer(int(partySize), isRandom)
		self.trainer1.showPartywMoves()
		
		#second trainer is initialised and they're full party is reported after
		self.trainer2 = trainer.Trainer(int(partySize), isRandom)
		self.trainer2.showPartywMoves()

battle = Arena()