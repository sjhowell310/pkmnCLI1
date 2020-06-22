import json
import string
import math
setup party setup in trainer module
class Move():

	def __init__(self, movename, dex, dex1):
		self.name = movename
		if "type" in dex1[movename]:
			self.type = dex1[movename]["type"]
		else:
			self.type = dex[movename]["type"]

# with open("data/gen1moves.json") as movedex1:
# 	dex1 = json.load(movedex1)

# 	with open("data/moves.json") as movedex:
# 		dex = json.load(movedex)
		
# 		mymove = Move("rockslide", dex, dex1)
# 		print(mymove.name, mymove.type)