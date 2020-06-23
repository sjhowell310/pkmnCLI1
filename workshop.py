import random
import math
import json

with open("data/g1movevals.json") as pdex:
	g1moves = json.load(pdex)

	with open("data/moves.json") as pdex:
		allmoves = json.load(pdex)
	out = []

	for moves in g1moves.keys():
		for keys in g1moves[moves]:
			if keys not in out:
				out.append(keys)
				out.append("b")
				
	for moves in allmoves.keys():
		for keys in allmoves[moves]:
			if keys not in out:
				out.append(keys)
				out.append("a")

	print(out, len(out))

	out2 = []
	for moves in allmoves.keys():
		if "secondary" in allmoves[moves] and allmoves[moves]["secondary"] != None:
			for keys in allmoves[moves]["secondary"].keys():
				if keys not in out2:
					out2.append(keys)

	print(sorted(out2), len(out2))

