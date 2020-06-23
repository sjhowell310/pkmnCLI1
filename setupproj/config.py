import json
import string 

def makedexwlearnsets(gen1dex, dex, learnset, gen1moves):
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

def makegenimovesetlib(g1m, psm, mmv):
	out = {}
	for key in g1m.keys():
		if g1m[key] == "n/a" or g1m[key] == "na":
			out[key] = 0
		else:
			out[key] = g1m[key]
		if key in psm.keys():
			for key2 in psm[key].keys():
				if key2 not in out[key].keys():
					out[key][key2] = psm[key][key2]
		for key3 in mmv[key].keys():
			if key3 not in out[key].keys():
				out[key][key3] = mmv[key][key3]		
		# for key2 in psm[key].keys():
		# 	if key2 not in g1m[key].keys():
		# 		out[key][key2] = psm[key][key2]
		# for key3 in mmv[key].keys():
		# 	if key3 not in g1m[key].keys():
		# 		out[key][key3] = mmv[key][key3]
	return out



with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/gen1moves.json") as g1m:
	gen1moves = json.load(g1m)
	with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/gen1pokedex.json") as g1p:
		gen1dex = json.load(g1p)
		with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/learnsets.json") as learn:
			learnset = json.load(learn)
			with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/moves.json") as mvs:
				moves = json.load(mvs)
				with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/pokedex.json") as pkdx:
					dex = json.load(pkdx)
					with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/g1movevals.json") as amvs:
						accmvs = json.load(amvs)

						makedexwlearnsets(gen1dex, dex, learnset, gen1moves)

						with open("../data/dexwithmovesandtypes.json", "w") as jsonout:
							json.dump(gen1dex, jsonout, sort_keys = True, indent = "\t")

						movedex = makegenimovesetlib(accmvs, gen1moves, moves)

						with open("../data/accurateg1moves.json", "w") as jsonout:
							json.dump(movedex, jsonout, sort_keys = True, indent = "\t")