import json
import string 
from collections import OrderedDict 
from operator import getitem 

def makedexwlearnsets(out, master, learnlist, movedex):
	for key in out.keys():
		out[key]["types"] = master[key]["types"]
		
		out[key]["name"] = master[key]["name"]
		out[key]["heightm"] = master[key]["heightm"]
		out[key]["weightkg"] = master[key]["weightkg"]
		out[key]["learnset"] = {}
		out[key]["id"] = master[key]["num"]

		for lkey in learnlist[key]["learnset"].keys():
			count = 0
			for genkey in learnlist[key]["learnset"][lkey]:
				if genkey[0] == "1":
					count += 1
			if count > 0:
				out[key]["learnset"][lkey] = movedex[lkey]["name"]

def makegenimovesetlib(gen1movevals, pokemonshowdowndata, masterlist):
	out = {}

	physicals = ["normal", "fighting", "flying", "ground", "rock", "bug", "ghost", "poison"]
	specials = ["water", "grass", "fire", "ice", "electric", "psychic", "dragon"]

	for key in gen1movevals.keys():
		if key not in out.keys():
			out[key] = gen1movevals[key]

		if key in pokemonshowdowndata.keys():
			for key2 in pokemonshowdowndata[key].keys():
				if key2 not in out[key].keys() and key2 != "zMove" and key2 != "contestType" and key2 != "inherit":
					out[key][key2] = pokemonshowdowndata[key][key2]

		if key in masterlist.keys():
			for key3 in masterlist[key].keys():
				if key3 not in out[key].keys() and key3 != "zMove" and key3 != "contestType" and key3 != "inherit":
					out[key][key3] = masterlist[key][key3]	

		if out[key]["type"] in physicals and out[key]["category"] != "Status":
			out[key]["category"] = "Physical"
		elif out[key]["type"] in specials:
			out[key]["category"] = "Special"

		out[key]["type"] = out[key]["type"].capitalize()

	for key in out.keys():
		if out[key]["accuracy"] == "na" or out[key]["accuracy"] == "n/a":
			out[key]["accuracy"] = 0
		if out[key]["basePower"] == "na" or out[key]["basePower"] == "n/a":
			out[key]["basePower"] = 0	

	return out



with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/gen1/moves.json") as g1m:
	gen1moves = json.load(g1m)

	with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/gen1/pokedex.json") as g1p:
		gen1pokedex = json.load(g1p)

		with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/gen1/learnsets.json") as learn:
			learnset = json.load(learn)

			with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/master/moves.json") as mvs:
				movevals = json.load(mvs)

				with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/master/pokedex.json") as pkdx:
					pokedex = json.load(pkdx)

					with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/gen1/movevals.json") as amvs:
						gen1movevals = json.load(amvs)

						movedex = makegenimovesetlib(gen1movevals, gen1moves, movevals)

						with open("../data/final/gen1moves.json", "w") as jsonout:
							json.dump(movedex, jsonout, sort_keys = True, indent = "\t")

						makedexwlearnsets(gen1pokedex, pokedex, learnset, movedex)

						with open("../data/final/pokedexwmoves.json", "w") as jsonout:
							json.dump(gen1pokedex, jsonout, sort_keys = True, indent = "\t")