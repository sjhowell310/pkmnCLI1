import trainer
import battle
import json
import math
import string
import pokemon
import moveset
import sys
import os
import time

# #enables program to read inputs from file, makes testing a lot easier
sys.stdin


def printDex():
	#print pokedex out in index order (i.e. the order of the original pokedex)
	print("GEN I POKEDEX:\n")
	print("{index: <5}{name: <12}{type: <18}{hp: <4}{atk: <8}{dfn: <8}{spa: <8}{spe: <8}\n".format(index = "#", name = "NAME", type = "TYPE(s)", hp = "HP", atk = "ATTACK", dfn = "DEFENCE", spa = "SPECIAL", spe = "SPEED"))
	#cycle through index numbers
	for i in range(1, len(dex.keys())):
		#finds key which contains next index number (this is clunky but it works, efficiency is not of the essence)
		for key in dex.keys():
			if dex[key]["id"] == i:
				print("{index: <5}{name: <12}{type: <18}{hp: <4}{atk: <8}{dfn: <8}{spa: <8}{spe: <8}".format(index = str(dex[key]["id"]), name = dex[key]["name"], type = ", ".join(dex[key]["types"]), hp = str(dex[key]["baseStats"]["hp"]), atk = str(dex[key]["baseStats"]["atk"]), dfn = str(dex[key]["baseStats"]["def"]), spa = str(dex[key]["baseStats"]["spa"]), spe = str(dex[key]["baseStats"]["spe"])))


try:
	with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/gen1moves.json") as g1mdex:
		g1moves = json.load(g1mdex)

	with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/pokedexwmoves.json") as pdex:
		dex = json.load(pdex)

	partySize = 7
	validsizes = ["1", "2", "3", "4", "5", "6"]
	while partySize not in validsizes:
		partySize = input("Contestants, decide and enter how many Pokemon you will both have in your parties\n")

	partySize = int(partySize)
	isRandom = ""
	while isRandom.lower() != "y" and isRandom.lower() != "n":
		isRandom = input("EVs are set to be maxed by default, would you like them to be randomised instead? [y/n]\n")
	isRandom = isRandom.lower()


	name = input("Trainer #1, please enter your name:\n(up to 10 characters)\n")
	#check input is valid, if not, prompt again until valid
	while(len(name) >10):
		name = input("Trainer#1, please enter your name:\n(up to 10 characters)\n")
	t1 = trainer.Trainer(name)

	name = input("Trainer #2, please enter your name:\n(up to 10 characters)\n")
	#check input is valid, if not, prompt again until valid
	while(len(name) >10):
		name = input("Trainer#2, please enter your name:\n(up to 10 characters)\n")
	t2 = trainer.Trainer(name)

	trainers = [t1, t2]
	battle = battle.Battle(t1, t2)
	

	for player in trainers:
		printDex()
		for i in range(partySize):
			#prompt user for name of pokemon they'd like to add, if not contained in pokedex, reprompt until valid input is passed
			pname = input("{name}, please enter your choice of pokemon #{number} for your party:\n".format(name = player.name, number=len(player.party)+1))
			pname = pname.lower()
			while(pname not in dex):
				pname = input("{name}, please enter your choice of pokemon #{number} for your party:\n".format(name = player.name, number=len(player.party)+1))
				pname = pname.lower()
			player.party.append(pokemon.Pokemon(dex[pname], isRandom))
			names = []
			#check there are more than 4 moves to choose from (Magikarp I'm looking at YOU)
			if len(dex[pname]["learnset"]) > 4:

				#displays full list of moves pname can learn
				print("Choose 4 of the following moves from the learnset once each:\n")
				print("{name: <15}{mtype: <10}{base: <10}{acc: <7}{pp: <5}\n".format(name = "MOVENAME", mtype = "TYPE", base = "BASEPOWER", acc = "ACCURACY", pp = "PP"))
				print("\n".join("{name: <15}{mtype: <10}{power: <10}{accuracy: <7}{pp: <5}".format(name = str(g1moves[key]["name"]), mtype = str(g1moves[key]["type"]), power = str(g1moves[key]["basePower"]), accuracy = str(g1moves[key]["accuracy"]), pp = str(g1moves[key]["pp"])) for key in sorted(dex[pname]["learnset"].keys())))
				poke = player.party[-1]
				#trainer now makes 4 choices on moves
				while len(poke.moves) < 4:
					#trainer can input any combination of capitalisation spaces and hyphens, can input individually or as comma separated list in terminal
					movechoices = "buffer"	
					movechoices = input("\n{trainerName}, please complete your choice of moves for {name} (comma separated)\nYou have {places} moves left to choose:\n".format(trainerName = player.name, name = poke.name, places = 4 - len(poke.moves)))
					movechoices = movechoices.lower().split(",")
					movechoices = [move.replace(" ", "").replace("-", "") for move in movechoices]
					if len(poke.moves) != len(dex[pname]["learnset"]):
						for move in movechoices:
							if move in dex[pname]["learnset"].keys() and move not in names:
								if len(poke.moves) <4:
									if len(poke.moves) == 0:
										print("{name} chose {move} as {pkmn}'s first move!".format(name = player.name, move = dex[pname]["learnset"][move], pkmn = poke.name))	
									elif len(poke.moves) == 1:
										print("{name} chose {move} as {pkmn}'s second move!".format(name = player.name, move = dex[pname]["learnset"][move], pkmn = poke.name))
									elif len(poke.moves) == 2:
										print("{name} chose {move} as {pkmn}'s third move!".format(name = player.name, move = dex[pname]["learnset"][move], pkmn = poke.name))
									elif len(poke.moves) == 3:
										print("{name} chose {move} as {pkmn}'s final move!".format(name = player.name, move = dex[pname]["learnset"][move], pkmn = poke.name))
									poke.moves.append(moveset.Move(move))
									names.append(move)
					#prints current moveset to remind trainer as moves can only be added to moveset once each
					print("Current moveset:\n")
					poke.printMoves()				
			else:
				for key in dex[pname]["learnset"].keys():
					poke.moves.append(moveset.Move(key))
				print("{name} has 4 or less moves in their moveset, you can have 'em all!\n".format(name = dex[pname]["name"]))
			pname = ""
			movechoices = "buffer"


	# name2 = input("Trainer #2, please enter your name:\n(up to 10 characters)\n")

	# #check input is valid, if not, prompt again until valid
	# while(len(name2) >10):
	# 	name2 = input("Trainer#2, please enter your name:\n(up to 10 characters)\n")

	# t2 = trainer.Trainer(name2)
	
	# printDex()

	# for i in range(partySize):
	# 	#prompt user for name of pokemon they'd like to add, if not contained in pokedex, reprompt until valid input is passed
	# 	pname = input("{name}, please enter your choice of pokemon #{number} for your party:\n".format(name = t2.name, number=len(t2.party)+1))
	# 	pname = pname.lower()
	# 	while(pname not in dex):
	# 		pname = input("{name}, please enter your choice of pokemon #{number} for your party:\n".format(name = t2.name, number=len(t2.party)+1))
	# 		pname = pname.lower()
	# 	t2.party.append(pokemon.Pokemon(dex[pname], isRandom))
	# 	names = []
	# 	#check there are more than 4 moves to choose from (Magikarp I'm looking at YOU)
	# 	if len(dex[pname]["learnset"]) > 4:

	# 		#displays full list of moves pname can learn
	# 		print("Choose 4 of the following moves from the learnset once each:\n")
	# 		print("{name: <15}{mtype: <10}{base: <10}{acc: <7}{pp: <5}".format(name = "MOVENAME", mtype = "TYPE", base = "BASEPOWER", acc = "ACCURACY", pp = "PP"))
	# 		print("\n".join("{name: <15}{mtype: <10}{power: <10}{accuracy: <7}{pp: <5}".format(name = str(g1moves[key]["name"]), mtype = str(g1moves[key]["type"]), power = str(g1moves[key]["basePower"]), accuracy = str(g1moves[key]["accuracy"]), pp = str(g1moves[key]["pp"])) for key in sorted(dex[pname]["learnset"].keys())))
	# 		poke = t2.party[-1]
	# 		#trainer now makes 4 choices on moves
	# 		while len(poke.moves) < 4:
	# 			#trainer can input any combination of capitalisation spaces and hyphens, can input individually or as comma separated list in terminal
	# 			movechoices = "buffer"	
	# 			movechoices = input("\n{trainerName}, please complete your choice of moves for {name} (comma separated)\nYou have {places} moves left to choose:\n".format(trainerName = t2.name, name = poke.name, places = 4 - len(poke.moves)))
	# 			movechoices = movechoices.lower().split(",")
	# 			movechoices = [move.replace(" ", "").replace("-", "") for move in movechoices]
	# 			print("")
	# 			if len(poke.moves) != len(dex[pname]["learnset"]):
	# 				for move in movechoices:
	# 					if move in dex[pname]["learnset"].keys() and move not in names:
	# 						if len(poke.moves) <4:
	# 							if len(poke.moves) == 0:
	# 								print("{name} chose {move} as {pkmn}'s first move!".format(name = t2.name, move = dex[pname]["learnset"][move], pkmn = poke.name))	
	# 							elif len(poke.moves) == 1:
	# 								print("{name} chose {move} as {pkmn}'s second move!".format(name = t2.name, move = dex[pname]["learnset"][move], pkmn = poke.name))
	# 							elif len(poke.moves) == 2:
	# 								print("{name} chose {move} as {pkmn}'s third move!".format(name = t2.name, move = dex[pname]["learnset"][move], pkmn = poke.name))
	# 							elif len(poke.moves) == 3:
	# 								print("{name} chose {move} as {pkmn}'s final move!".format(name = t2.name, move = dex[pname]["learnset"][move], pkmn = poke.name))
	# 							poke.moves.append(moveset.Move(move))
	# 							names.append(move)
	# 			#prints current moveset to remind trainer as moves can only be added to moveset once each
	# 			print("Current moveset:\n")
	# 			poke.printMoves()				
	# 	else:
	# 		for key in dex[pname]["learnset"].keys():
	# 			poke.moves.append(moveset.Move(key))
	# 			print("{name} has 4 or less moves in their moveset, you can have 'em all!\n".format(name = dex[pname]["name"]))
	# 	pname = ""
	# 	movechoices = "buffer"

	for player in trainers:
		if partySize > 1:
			player.showParty()
			validPos = [str(i) for i in range(1, partySize + 1)]
			pokechoice = input("{tname}, which pokemon would you like to send into battle first?\nPlease enter the pokemon's current position in the party\n".format(tname = player.name))
			pokechoice = pokechoice.capitalize()
			while pokechoice not in validPos:
				pokechoice = input("{tname}, which pokemon would you like to send into battle first?\nPlease enter the pokemon's current position in the party\n".format(tname = player.name))
			if pokechoice in validPos:
				i = int(pokechoice) - 1
			player.switchIn(player.party[i])
		else:
			player.switchIn(player.party[0])

	for player in trainers:
		time.sleep(1)
		print("{tname} sent {current} into battle!\n".format(tname = player.name, current = player.activePokemon.name))

	# cease input from stdin, idk why this works but it does, took me ages to find it...
	sys.stdin.close()
	sys.stdin = os.fdopen(1)
	choices = ["a", "a"]
	while not battle.isWhiteOut():
		time.sleep(1)
		battle.printBattle()
		time.sleep(1)
		for player in trainers:
			isFinished = False
			while not isFinished:
				r1 = input("{name}, what would you like to do?\n(Enter number of desired option)\n1)Attack\n2)Switch Pok\u00e9mon\n".format(name = player.name))
				while (r1 != "1" and r1 != "2") or r1 == "x":
					r1 = input("{name}, what would you like to do?\n(Enter number of desired option)\n1)Attack\n2)Switch Pok\u00e9mon\n".format(name = player.name))
				if r1 == "1":
					print("Choose an attack to use:\n")
					player.activePokemon.battlePrintMoves()
					options = len(player.activePokemon.moves)
					validChoices = ["x", "a","b","c","d"]
					print("(Enter letter of desired option, X to go back)\n")
					a1 = input()
					a1 = a1.lower()
					while a1 not in validChoices[:options + 1]:
						print("(Enter letter of desired option, X to go back)\n")
						a1 = input()
						a1 = a1.lower()
					if a1 in validChoices and a1 != "x":
						if player.activePokemon.moves[validChoices.index(a1) - 1].pp > 0:
							playeraction = "attack-"
							playeraction += str(validChoices.index(a1) - 1)
							choices[trainers.index(player)] = playeraction 
							isFinished = True
					else:
						pass
				if r1 == "2":
					madeChoice = False
					while not madeChoice:
						print("Choose a member of your party to switch in:\n")
						player.battleShowParty()
						options = len(player.party)
						validChoices = ["x", "a","b","c","d", "e", "f"]
						print("(Enter letter of desired option, X to go back)\n")
						a1 = input()
						a1 = a1.lower()
						while a1 not in validChoices[:options + 1]:
							print("(Enter letter of desired option, X to go back)\n")
							a1 = input()
							a1 = a1.lower()
						if a1 in validChoices and a1 != "x":
							if player.party[validChoices.index(a1) - 1].battHP == 0:
								print("{name} doesn't have any energy left to battle!\n".format(name = player.party[validChoices.index(a1) - 1].name))
							elif player.party[validChoices.index(a1) - 1].active == True:
								print("{name} is already in battle!\n".format(name = player.activePokemon.name))
							else:
								isSure = ""
								while isSure.lower() != "y" and isSure.lower() != "n":
									isSure = input("You're about to switch {name} into battle. Are you sure? [y/n]\n".format(name = player.party[validChoices.index(a1) - 1].name))
								isSure = isSure.lower()
								if isSure == "n":
									madeChoice = True
								elif isSure == "y":
									playeraction = "switch-"
									playeraction += str(validChoices.index(a1) - 1)
									choices[trainers.index(player)] = playeraction 
									madeChoice = True
									isFinished = True
						else:
							madeChoice = True
		battle.action(choices[0], choices[1])

		# time.sleep(1)
		# isFinished = False
		# while not isFinished:
		# 	r1 = input("{name}, what would you like to do?\n(Enter number of desired option)\n1)Attack\n2)Switch Pok\u00e9mon\n".format(name = t2.name))
		# 	while (r1 != "1" and r1 != "2") or r1 == "x":
		# 		r1 = input("{name}, what would you like to do?\n(Enter number of desired option)\n1)Attack\n2)Switch Pok\u00e9mon\n")
		# 	if r1 == "1":
		# 		print("Choose an attack to use:\n")
		# 		t2.activePokemon.battlePrintMoves()
		# 		options = len(t2.activePokemon.moves)
		# 		validChoices = ["x", "a","b","c","d"]
		# 		print("(Enter letter of desired option, X to go back)\n")
		# 		a1 = input()
		# 		a1 = a1.lower()
		# 		while a1 not in validChoices[:options + 1]:
		# 			print("(Enter letter of desired option, X to go back)\n")
		# 			a1 = input()
		# 			a1 = a1.lower()
		# 		if a1 in validChoices and a1 != "x":
		# 			if t2.activePokemon.moves[validChoices.index(a1) - 1].pp > 0:
		# 				t2action = "attack-"
		# 				t2action += str(validChoices.index(a1) - 1)
		# 				isFinished = True
		# 		else:
		# 			pass
		# 	if r1 == "2":
		# 		madeChoice = False
		# 		while not madeChoice:
		# 			print("Choose a member of your party to switch in:\n")
		# 			t2.battleShowParty()
		# 			options = len(t2.party)
		# 			validChoices = ["x", "a","b","c","d", "e", "f"]
		# 			print("(Enter letter of desired option, X to go back)\n")
		# 			a1 = input()
		# 			a1 = a1.lower()
		# 			while a1 not in validChoices[:options + 1]:
		# 				print("(Enter letter of desired option, X to go back)\n")
		# 				a1 = input()
		# 				a1 = a1.lower()
		# 			if a1 in validChoices and a1 != "x":
		# 				if t2.party[validChoices.index(a1) - 1].battHP == 0:
		# 					print("{name} doesn't have any energy left to battle!\n".format(name = t2.party[validChoices.index(a1) - 1].name))
		# 				elif t2.party[validChoices.index(a1) - 1].active == True:
		# 					print("{name} is already in battle!\n".format(name = t2.activePokemon.name))
		# 				else:
		# 					isSure = ""
		# 					while isSure.lower() != "y" and isSure.lower() != "n":
		# 						isSure = input("You're about to switch {name} into battle. Are you sure? [y/n]\n".format(name = t2.party[validChoices.index(a1) - 1].name))
		# 					isSure = isSure.lower()
		# 					if isSure == "n":
		# 						madeChoice = True
		# 					elif isSure == "y":
		# 						t2action = "switch-"
		# 						t2action += str(validChoices.index(a1) - 1) 
		# 						madeChoice = True
		# 						isFinished = True
		# 			else:
		# 				madeChoice = True
		



	

except EOFError:
	pass



