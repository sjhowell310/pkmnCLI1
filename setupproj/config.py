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
			count = 0
			for genkey in learnset[key]["learnset"][lkey]:
				if genkey[0] == "1":
					count += 1
			if count > 0:
				gen1dex[key]["learnset"].append(lkey)




with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/gen1moves.json") as g1m:
	gen1moves = json.load(g1m)

with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/gen1pokedex.json") as g1p:
	gen1dex = json.load(g1p)

with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/gen1typechart.json") as g1t:
	gen1typechart = json.load(g1t)

with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/learnsets.json") as learn:
	learnset = json.load(learn)

with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/moves.json") as mvs:
	moves = json.load(mvs)

with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/pokedex.json") as pkdx:
	dex = json.load(pkdx)

makebattledex(gen1dex, dex, learnset, gen1moves)

with open("../data/dexwithmovesandtypes.json", "w") as jsonout:
	json.dump(gen1dex, jsonout, sort_keys = True, indent = "\t")