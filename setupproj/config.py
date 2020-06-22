import json
import string 

def makebattledex(gen1dex, dex, learnset, gen1moves):
	moves = gen1moves.keys()
	for key in gen1dex.keys():
		gen1dex[key]["types"] = dex[key]["types"]
		gen1dex[key]["name"] = dex[key]["name"]
		gen1dex[key]["heightm"] = dex[key]["heightm"]
		gen1dex[key]["weightkg"] = dex[key]["weightkg"]
		gen1dex[key]["learnset"] = []
		for lkey in learnset[key]["learnset"].keys():
			if lkey in moves:
				gen1dex[key]["learnset"].append(lkey)




with open("data/gen1moves.json") as g1m:
	gen1moves = json.load(g1m)

with open("data/gen1pokedex.json") as g1p:
	gen1dex = json.load(g1p)

with open("data/gen1typechart.json") as g1t:
	gen1typechart = json.load(g1t)

with open("data/learnsets.json") as learn:
	learnset = json.load(learn)

with open("data/moves.json") as mvs:
	moves = json.load(mvs)

with open("data/pokedex.json") as pkdx:
	dex = json.load(pkdx)

makebattledex(gen1dex, dex, learnset, gen1moves)

with open("data/dexwithmovesandtypes.json", "w") as jsonout:
	json.dump(gen1dex, jsonout, sort_keys = True, indent = "\t")