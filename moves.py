import json
import string
import math
import trainer
import pokemon


# global allmoves
# with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/moves.json") as pdex:
# 	allmoves = json.load(pdex)
	
class Move():

	def __init__(self, movename):
		#importing moves library
		with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/gen1moves.json") as pdex:
			g1moves = json.load(pdex)

			#harvesting the many required flags and such for each move
			self.accuracy = g1moves[movename]["accuracy"]

			self.basePower = g1moves[movename]["basePower"]

			if "boosts" in g1moves[movename]:
				self.boosts = g1moves[movename]["boosts"]
			elif "boosts" not in g1moves[movename]:
				self.boosts = None

			self.category = g1moves[movename]["category"]

			if "critRatio" in g1moves[movename]:
				self.critRatio = g1moves[movename]["critRatio"]
			elif "critRatio" not in g1moves[movename]:
				self.critRatio = None

			if "damage" in g1moves[movename]:
				self.damage = g1moves[movename]["damage"]
			elif "damage" not in g1moves[movename]:
				self.damage = None

			if "drain" in g1moves[movename]:
				self.drain = g1moves[movename]["drain"]
			elif "drain" not in g1moves[movename]:
				self.drain = None

			if "flags" in g1moves[movename]:
				self.flags = g1moves[movename]["flags"]
			elif "flags" not in g1moves[movename]:
				self.flags = None

			if "forceSwitch" in g1moves[movename]:
				self.forceSwitch = g1moves[movename]["forceSwitch"]
			elif "forceSwitch" not in g1moves[movename]:
				self.forceSwitch = None

			if "hasCrashDamage" in g1moves[movename]:
				self.hasCrashDamage = g1moves[movename]["hasCrashDamage"]
			elif "hasCrashDamage" not in g1moves[movename]:
				self.hasCrashDamage = None

			if "heal" in g1moves[movename]:
				self.heal = g1moves[movename]["heal"]
			elif "heal" not in g1moves[movename]:
				self.heal = None

			if "ignoreEvasion" in g1moves[movename]:
				self.ignoreEvasion = g1moves[movename]["ignoreEvasion"]
			elif "ignoreEvasion" not in g1moves[movename]:
				self.ignoreEvasion = None

			if "ignoreImmunity" in g1moves[movename]:
				self.ignoreImmunity = g1moves[movename]["ignoreImmunity"]
			elif "ignoreImmunity" not in g1moves[movename]:
				self.ignoreImmunity = None

			if "isNonstandard" in g1moves[movename]:
				self.isNonstandard = g1moves[movename]["isNonstandard"]
			elif "isNonstandard" not in g1moves[movename]:
				self.isNonstandard = None

			if "maxMove" in g1moves[movename]:
				self.maxMove = g1moves[movename]["maxMove"]
			elif "maxMove" not in g1moves[movename]:
				self.maxMove = None

			if "multihit" in g1moves[movename]:
				self.multihit = g1moves[movename]["multihit"]
			elif "multihit" not in g1moves[movename]:
				self.multihit = None

			self.name = g1moves[movename]["name"]

			if "noMetronome" in g1moves[movename]:
				self.noMetronome = g1moves[movename]["noMetronome"]
			elif "noMetronome" not in g1moves[movename]:
				self.noMetronome = None

			if "noPPBoosts" in g1moves[movename]:
				self.noPPBoosts = g1moves[movename]["noPPBoosts"]
			elif "noPPBoosts" not in g1moves[movename]:
				self.noPPBoosts = None

			if "noSketch" in g1moves[movename]:
				self.noSketch = g1moves[movename]["noSketch"]
			elif "noSketch" not in g1moves[movename]:
				self.noSketch = None

			if "num" in g1moves[movename]:
				self.num = g1moves[movename]["num"]
			elif "num" not in g1moves[movename]:
				self.num = None

			if "ohko" in g1moves[movename]:
				self.ohko = g1moves[movename]["ohko"]
			elif "ohko" not in g1moves[movename]:
				self.ohko = None	

			if "onTryHit" in g1moves[movename]:
				self.onTryHit = g1moves[movename]["onTryHit"]
			elif "onTryHit" not in g1moves[movename]:
				self.onTryHit = None		
			self.pp = g1moves[movename]["pp"] * (8/5)
			
			self.priority = g1moves[movename]["priority"]

			if "recoil" in g1moves[movename]:
				self.recoil = g1moves[movename]["recoil"]
			elif "recoil" not in g1moves[movename]:
				self.recoil = None

			if "secondary" in g1moves[movename]:
				self.secondary = g1moves[movename]["secondary"]
			elif "secondary" not in g1moves[movename]:
				self.secondary = None

			if "self" in g1moves[movename]:
				self.self = g1moves[movename]["self"]
			elif "self" not in g1moves[movename]:
				self.self = None

			if "selfSwitch" in g1moves[movename]:
				self.selfSwitch = g1moves[movename]["selfSwitch"]
			elif "selfSwitch" not in g1moves[movename]:
				self.selfSwitch = None

			if "selfdestruct" in g1moves[movename]:
				self.selfdestruct = g1moves[movename]["selfdestruct"]
			elif "selfdestruct" not in g1moves[movename]:
				self.selfdestruct = None

			if "sideCondition" in g1moves[movename]:
				self.sideCondition = g1moves[movename]["sideCondition"]
			elif "sideCondition" not in g1moves[movename]:
				self.sideCondition = None

			if "status" in g1moves[movename]:
				self.status = g1moves[movename]["status"]
			elif "status" not in g1moves[movename]:
				self.status = None

			if "struggleRecoil" in g1moves[movename]:
				self.struggleRecoil = g1moves[movename]["struggleRecoil"]
			elif "struggleRecoil" not in g1moves[movename]:
				self.struggleRecoil = None

			if "target" in g1moves[movename]:
				self.target = g1moves[movename]["target"]
			elif "target" not in g1moves[movename]:
				self.target = None
			
			self.type = g1moves[movename]["type"]

			if "volatileStatus" in g1moves[movename]:
				self.volatileStatus = g1moves[movename]["volatileStatus"]
			elif "volatileStatus" not in g1moves[movename]:
				self.volatileStatus = None

			if "willCrit" in g1moves[movename]:
				self.willCrit = g1moves[movename]["willCrit"]
			elif "willCrit" not in g1moves[movename]:
				self.willCrit = None
	


		









# with open("data/gen1moves.json") as movedex1:
# 	dex1 = json.load(movedex1)

# 	with open("data/moves.json") as movedex:
# 		dex = json.load(movedex)
		
# 		mymove = Move("rockslide", dex, dex1)
# 		print(mymove.name, mymove.type)