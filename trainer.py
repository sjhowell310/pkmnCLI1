import pokemon
import json
import math
import string
setup party setup in trainer module
class Trainer():

	def __init__(self):
		name = input("Trainer, please enter your name:\n(up to 10 characters)\n")
		while(len(name) > 10):
			name = input("Trainer, please enter your name:\n(up to 10 characters)\n")
		self.name = name
		self.party = []
		return

	# def addToParty(self, pokemon):
	# 	with open("data/dexwithmovesandtypes.json") as dex:
	# 		pdex = json.load(dex)
	# 		if type(pokemon) == str:
	# 			if pokemon in pdex:
	# 				addPartyMember = Pokemon()

firsttrainer = Trainer()
print(firsttrainer.name)

