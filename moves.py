import json
import string
import math
import trainer
import pokemon

global g1moves
with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/g1movevals.json") as pdex:
	g1moves = json.load(pdex)

global allmoves
with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/moves.json") as pdex:
	allmoves = json.load(pdex)
	
class Move():

	def __init__(self, movename):
		physicals = ["Normal", "Fighting", "Flying", "Ground", "Rock", "Bug", "Ghost", "Poison"]
		specials = ["Water", "Grass", "Fire", "Ice", "Electric", "Psychic", "Dragon"]

		self.name = movename
		self.type = g1moves[movename]["type"]
		self.accuracy = g1moves[movename]["accuracy"]
		self.basePower = g1moves[movename]["basePower"]
		self.pp = g1moves[movename]["pp"] * (8/5)
		
		if allmoves[movename]["category"] == "status":
			self.category = "status"
		elif self.type in physicals:
			self.category = "physical"
		elif self.type in specials:
			self.category = "special"
		if "status" in allmoves[movename]:
			self.status = allmoves[movename]["status"]
		if "secondary" not in allmoves[movename]:
			self.statusp = 1
		elif "secondary" in allmoves[movename] and allmoves[movename]["secondary"] != None:
			self.status = allmoves[movename]["secondary"]["status"]
			self.statusp = self.status = allmoves[movename]["secondary"]["chance"]
		







# with open("data/gen1moves.json") as movedex1:
# 	dex1 = json.load(movedex1)

# 	with open("data/moves.json") as movedex:
# 		dex = json.load(movedex)
		
# 		mymove = Move("rockslide", dex, dex1)
# 		print(mymove.name, mymove.type)