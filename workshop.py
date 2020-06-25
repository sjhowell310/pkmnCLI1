import random
import math
import json
import moves

with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/gen1moves.json") as pdex:
	g1moves = json.load(pdex)

	with open("data/master/moves.json") as pdex:
		allmoves = json.load(pdex)
		with open("data/final/pokedexwmoves.json") as pdex:
			allpokemon = json.load(pdex)
			out = []
			print(len(g1moves.keys()))
			# for move in g1moves.keys():
			# 	testmove = moves.Move(move)
			# 	print(testmove.getMove())
test_dict = {'Nikhil' : { 'roll' : 24, 'marks' : 17}, 
             'Akshat' : {'roll' : 54, 'marks' : 12},  
             'Akash' : { 'roll' : 12, 'marks' : 15}} 
  
# printing original dict 
print("The original dictionary : " + str(test_dict)) 
  
# using sorted() 
# Sort nested dictionary by key 
res = sorted(test_dict.items(), key = lambda x: x[1]['marks']) 
  
# print result 
print("The sorted dictionary by marks is : " + str(res)) 
			

	# for moves in g1moves.keys():
	# 	for keys in g1moves[moves]:
	# 		if keys not in out:
	# 			out.append(keys)
	# # 			out.append("b")
				
	# # for moves in allmoves.keys():
	# # 	for keys in allmoves[moves]:
	# # 		if keys not in out:
	# # 			out.append(keys)
	# # 			out.append("a")

	# print(sorted(out), len(out))

	# out2 = []
	# for moves in allmoves.keys():
	# 	if "secondary" in allmoves[moves] and allmoves[moves]["secondary"] != None:
	# 		for keys in allmoves[moves]["secondary"].keys():
	# 			if keys not in out2:
	# 				out2.append(keys)

	# print(sorted(out2), len(out2))
	
# ['xaccuracy', 'xbasePower', 'xboosts', 'xcategory', 'xcritRatio', 'xdamage', 'xdesc', 'xdrain', 'xeffect', 'xflags', 'xforceSwitch', 'xhasCrashDamage', 'xheal', 'xignoreEvasion', 'xignoreImmunity', 'xisNonstandard', 'xmaxMove', 'xmultihit', 'xname', 'xnoMetronome', 'xnoPPBoosts', 'xnoSketch', 'xnum', 'xohko', 'xonTryHit', 'xpp', 'xpriority', 'xrecoil', 'xsecondary', 'xself', 'xselfSwitch', 'xselfdestruct', 'xshortDesc', 'xsideCondition', 'xstatus', 'xstruggleRecoil', 'xtarget', 'xtype', 'xvolatileStatus', 'xwillCrit'] 40