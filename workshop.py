import random
import math

def calcHPStat(poke, hpiv, basetotal):
	level = 100
	ev = poke["baseStats"]["hp"]*65535 / basetotal
	hp = math.floor(((((poke["baseStats"]["hp"] + hpiv) * 2) + (math.floor((math.ceil(ev**0.5))/(4))))*(level))/(100)) + level + 10
	return hp

poke = {
		"baseStats": {
			"atk": 20,
			"def": 15,
			"hp": 25,
			"spa": 105,
			"spd": 105,
			"spe": 90
		},
		"heightm": 0.9,
		"inherit": True,
		"learnset": [
			"mimic",
			"bide",
			"rest",
			"rage",
			"counter",
			"dreameater",
			"skullbash",
			"lightscreen",
			"metronome",
			"doubleedge",
			"submission",
			"psywave",
			"takedown",
			"psychic",
			"swift",
			"seismictoss",
			"thunderwave",
			"reflect",
			"substitute",
			"triattack"
		],
		"name": "Abra",
		"types": [
			"Psychic"
		],
		"weightkg": 19.5
	}

IVs = [int(15 * random.random()) for i in range(4)]
hpiv  = ""
for i in range(4):
	hpiv += str(bin(IVs[i]))[-1]
print(IVs, int(hpiv, 2))
HPiv = int(hpiv, 2)
totalBase = 0
for key in poke["baseStats"].keys():
	if key != "spd":
		totalBase += poke["baseStats"][key]
		print(totalBase)





print(calcHPStat(poke, HPiv, totalBase))