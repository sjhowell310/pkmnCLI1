import trainer
import json
import math
import string
import pokemon
import moves

class Arena():

	weather = "Clear"

	def __init__(self):
		partySize = 7
		validsizes = ["1", "2", "3", "4", "5", "6"]
		while partySize not in validsizes:
			partySize = input("Contestants, decide and enter how many Pokemon you will both have in your parties\n")

		self.trainer1 = trainer.Trainer(int(partySize))
		self.trainer1.showPartywMoves()
		self.trainer2 = trainer.Trainer(int(partySize))
		self.trainer2.showPartywMoves() 
battle = Arena()