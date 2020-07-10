import trainer
import battle
import json
import math
import string
import pokemon
import moveset
import sys
import os

# #enables program to read inputs from file, makes testing a lot easier
sys.stdin


def printDex():
	#print pokedex out in index order (i.e. the order of the original pokedex)
	print("\nGEN I POKEDEX:")
	print("{index: <5}{name: <12}{type: <18}{hp: <4}{atk: <8}{dfn: <8}{spa: <8}{spe: <8}".format(index = "#", name = "NAME", type = "TYPE(s)", hp = "HP", atk = "ATTACK", dfn = "DEFENCE", spa = "SPECIAL", spe = "SPEED"))
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
		isRandom = input("EVs are set to be maxed by default, would you like them to be randomised instead? [y/n]")
	isRandom = isRandom.lower()


	name1 = input("\nTrainer #1, please enter your name:\n(up to 10 characters)\n")
	#check input is valid, if not, prompt again until valid
	while(len(name1) >10):
		name1 = input("\nTrainer#1, please enter your name:\n(up to 10 characters)\n")
	t1 = trainer.Trainer(name1)

	
	printDex()


	for i in range(partySize):
		#prompt user for name of pokemon they'd like to add, if not contained in pokedex, reprompt until valid input is passed
		pname = input("\n{name}, please enter your choice of pokemon #{number} for your party:\n".format(name = t1.name, number=len(t1.party)+1))
		pname = pname.lower()
		while(pname not in dex):
			pname = input("\n{name}, please enter your choice of pokemon #{number} for your party:\n".format(name = t1.name, number=len(t1.party)+1))
			pname = pname.lower()
		t1.party.append(pokemon.Pokemon(dex[pname], isRandom))
		names = []
		#check there are more than 4 moves to choose from (Magikarp I'm looking at YOU)
		if len(dex[pname]["learnset"]) > 4:

			#displays full list of moves pname can learn
			print("\nChoose 4 of the following moves from the learnset once each:")
			print("{name: <15}{mtype: <10}{base: <10}{acc: <7}{pp: <5}".format(name = "MOVENAME", mtype = "TYPE", base = "BASEPOWER", acc = "ACCURACY", pp = "PP"))
			print("\n".join("{name: <15}{mtype: <10}{power: <10}{accuracy: <7}{pp: <5}".format(name = str(g1moves[key]["name"]), mtype = str(g1moves[key]["type"]), power = str(g1moves[key]["basePower"]), accuracy = str(g1moves[key]["accuracy"]), pp = str(g1moves[key]["pp"])) for key in sorted(dex[pname]["learnset"].keys())))
			poke = t1.party[-1]
			#trainer now makes 4 choices on moves
			while len(poke.moves) < 4:
				#trainer can input any combination of capitalisation spaces and hyphens, can input individually or as comma separated list in terminal
				movechoices = "buffer"	
				movechoices = input("\n{trainerName}, please complete your choice of moves for {name} (comma separated)\nYou have {places} moves left to choose:\n".format(trainerName = t1.name, name = poke.name, places = 4 - len(poke.moves)))
				movechoices = movechoices.lower().split(",")
				movechoices = [move.replace(" ", "").replace("-", "") for move in movechoices]
				if len(poke.moves) != len(dex[pname]["learnset"]):
					for move in movechoices:
						if move in dex[pname]["learnset"].keys() and move not in names:
							if len(poke.moves) <4:
								if len(poke.moves) == 0:
									print("You chose {move} as {pkmn}'s first move!".format(move = dex[pname]["learnset"][move], pkmn = poke.name))	
								elif len(poke.moves) == 1:
									print("You chose {move} as {pkmn}'s second move!".format(move = dex[pname]["learnset"][move], pkmn = poke.name))
								elif len(poke.moves) == 2:
									print("You chose {move} as {pkmn}'s third move!".format(move = dex[pname]["learnset"][move], pkmn = poke.name))
								elif len(poke.moves) == 3:
									print("You chose {move} as {pkmn}'s final move!".format(move = dex[pname]["learnset"][move], pkmn = poke.name))
								poke.moves.append(moveset.Move(move))
								names.append(move)
				#prints current moveset to remind trainer as moves can only be added to moveset once each
				print("\nCurrent moveset:")
				poke.printMoves()				
		else:
			for key in dex[pname]["learnset"].keys():
				poke.moves.append(moveset.Move(key))
				print("{name} has 4 or less moves in their moveset, you can have 'em all!\n".format(name = dex[pname]["name"]))
		pname = ""
		movechoices = "buffer"


	name2 = input("\nTrainer #2, please enter your name:\n(up to 10 characters)\n")

	#check input is valid, if not, prompt again until valid
	while(len(name2) >10):
		name2 = input("\nTrainer#2, please enter your name:\n(up to 10 characters)\n")

	t2 = trainer.Trainer(name2)
	battle = battle.Battle(t1, t2)
	printDex()

	for i in range(partySize):
		#prompt user for name of pokemon they'd like to add, if not contained in pokedex, reprompt until valid input is passed
		pname = input("\n{name}, please enter your choice of pokemon #{number} for your party:\n".format(name = t2.name, number=len(t2.party)+1))
		pname = pname.lower()
		while(pname not in dex):
			pname = input("\n{name}, please enter your choice of pokemon #{number} for your party:\n".format(name = t2.name, number=len(t2.party)+1))
			pname = pname.lower()
		t2.party.append(pokemon.Pokemon(dex[pname], isRandom))
		names = []
		#check there are more than 4 moves to choose from (Magikarp I'm looking at YOU)
		if len(dex[pname]["learnset"]) > 4:

			#displays full list of moves pname can learn
			print("\nChoose 4 of the following moves from the learnset once each:")
			print("{name: <15}{mtype: <10}{base: <10}{acc: <7}{pp: <5}".format(name = "MOVENAME", mtype = "TYPE", base = "BASEPOWER", acc = "ACCURACY", pp = "PP"))
			print("\n".join("{name: <15}{mtype: <10}{power: <10}{accuracy: <7}{pp: <5}".format(name = str(g1moves[key]["name"]), mtype = str(g1moves[key]["type"]), power = str(g1moves[key]["basePower"]), accuracy = str(g1moves[key]["accuracy"]), pp = str(g1moves[key]["pp"])) for key in sorted(dex[pname]["learnset"].keys())))
			poke = t2.party[-1]
			#trainer now makes 4 choices on moves
			while len(poke.moves) < 4:
				#trainer can input any combination of capitalisation spaces and hyphens, can input individually or as comma separated list in terminal
				movechoices = "buffer"	
				movechoices = input("\n{trainerName}, please complete your choice of moves for {name} (comma separated)\nYou have {places} moves left to choose:\n".format(trainerName = t2.name, name = poke.name, places = 4 - len(poke.moves)))
				movechoices = movechoices.lower().split(",")
				movechoices = [move.replace(" ", "").replace("-", "") for move in movechoices]
				if len(poke.moves) != len(dex[pname]["learnset"]):
					for move in movechoices:
						if move in dex[pname]["learnset"].keys() and move not in names:
							if len(poke.moves) <4:
								if len(poke.moves) == 0:
									print("You chose {move} as {pkmn}'s first move!".format(move = dex[pname]["learnset"][move], pkmn = poke.name))	
								elif len(poke.moves) == 1:
									print("You chose {move} as {pkmn}'s second move!".format(move = dex[pname]["learnset"][move], pkmn = poke.name))
								elif len(poke.moves) == 2:
									print("You chose {move} as {pkmn}'s third move!".format(move = dex[pname]["learnset"][move], pkmn = poke.name))
								elif len(poke.moves) == 3:
									print("You chose {move} as {pkmn}'s final move!".format(move = dex[pname]["learnset"][move], pkmn = poke.name))
								poke.moves.append(moveset.Move(move))
								names.append(move)
				#prints current moveset to remind trainer as moves can only be added to moveset once each
				print("\nCurrent moveset:")
				poke.printMoves()				
		else:
			for key in dex[pname]["learnset"].keys():
				poke.moves.append(moveset.Move(key))
				print("{name} has 4 or less moves in their moveset, you can have 'em all!\n".format(name = dex[pname]["name"]))
		pname = ""
		movechoices = "buffer"


	t1.showParty()
	validPos = [str(i) for i in range(1, partySize + 1)]
	pokechoice = input("{tname}, which pokemon would you like to send into battle first?\nPlease enter the pokemon's current position in the party\n".format(tname = t1.name))
	pokechoice = pokechoice.capitalize()
	while pokechoice not in validPos:
		pokechoice = input("{tname}, which pokemon would you like to send into battle first?\nPlease enter the pokemon's current position in the party\n".format(tname = t1.name))
	if pokechoice in validPos:
		i = int(pokechoice) - 1
	t1.switchIn(t1.party[i])
	
	t2.showParty()
	pokechoice = input("{tname}, which pokemon would you like to send into battle first?\nPlease enter the pokemon's current position in the party\n".format(tname = t2.name))
	pokechoice = pokechoice.capitalize()
	while pokechoice not in validPos:
		pokechoice = input("{tname}, which pokemon would you like to send into battle first?\nPlease enter the pokemon's current position in the party\n".format(tname = t2.name))
	if pokechoice in validPos:
		j = int(pokechoice) - 1
	t2.switchIn(t2.party[j])
	print("{tname} sent {current} into battle!".format(tname = t1.name, current = t1.activePokemon.name))
	print("{tname} sent {current} into battle!".format(tname = t2.name, current = t2.activePokemon.name))

	# cease input from stdin, idk why this works but it does, took me ages to find it...
	# sys.stdin.close()
	# sys.stdin = os.fdopen(1)
	while not battle.isWhiteOut():
		battle.printBattle()
		isFinished = False
		while not isFinished:
			r1 = input("\n{name}, what would you like to do?\n(Enter number of desired option)\n1)Attack\n2)Switch Pok\u00e9mon\n".format(name = t1.name))
			while (r1 != "1" and r1 != "2") or r1 == "x":
				r1 = input("{name}, what would you like to do?\n(Enter number of desired option)\n1)Attack\n2)Switch Pok\u00e9mon\n")
			if r1 == "1":
				print("Choose an attack to use:")
				t1.activePokemon.battlePrintMoves()
				options = len(t1.activePokemon.moves)
				validChoices = ["x", "a","b","c","d"]
				print("\n(Enter letter of desired option, X to go back)\n")
				a1 = input()
				a1 = a1.lower()
				while a1 not in validChoices[:options+1]:
					print("\n(Enter letter of desired option, X to go back)\n")
					a1 = input()
					a1 = a1.lower()
				if a1 == "a":
					if t1.activePokemon.moves[0].pp > 0:
						t1action = "attack-0"
						isFinished = True
				elif a1 == "b":
					if t1.activePokemon.moves[1].pp > 0:
						t1action = "attack-1"
						isFinished = True
				elif a1 == "c":
					if t1.activePokemon.moves[2].pp > 0:
						t1action = "attack-2"
						isFinished = True
				elif a1 == "d":
					if t1.activePokemon.moves[2].pp > 0:
						t1action = "attack-3"
						isFinished = True
				else:
					pass
			if r1 == "2":
				madeChoice = False
				while not madeChoice:
					print("Choose which member of your party to switch in:")
					t1.battleShowParty()
					options = len(t1.party)
					validChoices = ["x", "a","b","c","d", "e", "f"]
					print("\n(Enter letter of desired option, X to go back)\n")
					a1 = input()
					a1 = a1.lower()
					while a1 not in validChoices[:options+1]:
						print("\n(Enter letter of desired option, X to go back)\n")
						a1 = input()
						a1 = a1.lower()
					if a1 == "a":
						if t1.activePokemon.idtag == t1.party[validChoices.index(a1)-1].idtag and t1.activePokemon.battHP == t1.party[validChoices.index(a1)-1].battHP:
							print("{name} is already in battle!\n".format(name = t1.activePokemon.name))
						else:
							t1action = "switch-0"
							isFinished = True
							madeChoice = True
					elif a1 == "b":
						if t1.activePokemon.idtag == t1.party[validChoices.index(a1)-1].idtag and t1.activePokemon.battHP == t1.party[validChoices.index(a1)-1].battHP:
							print("{name} is already in battle!\n".format(name = t1.activePokemon.name))
						else:
							t1action = "switch-1"
							isFinished = True
							madeChoice = True
					elif a1 == "c":
						if t1.activePokemon.idtag == t1.party[validChoices.index(a1)-1].idtag and t1.activePokemon.battHP == t1.party[validChoices.index(a1)-1].battHP:
							print("{name} is already in battle!\n".format(name = t1.activePokemon.name))	
						else:
							t1action = "switch-2"
							isFinished = True
							madeChoice = True
					elif a1 == "d":
						if t1.activePokemon.idtag == t1.party[validChoices.index(a1)-1].idtag and t1.activePokemon.battHP == t1.party[validChoices.index(a1)-1].battHP:
							print("{name} is already in battle!\n".format(name = t1.activePokemon.name))						
						else:
							t1action = "switch-3"
							isFinished = True
							madeChoice = True
					elif a1 == "e":
						if t1.activePokemon.idtag == t1.party[validChoices.index(a1)-1].idtag and t1.activePokemon.battHP == t1.party[validChoices.index(a1)-1].battHP:
							print("{name} is already in battle!\n".format(name = t1.activePokemon.name))						
						else:
							t1action = "switch-4"
							isFinished = True
							madeChoice = True
					elif a1 == "f":
						if t1.activePokemon.idtag == t1.party[validChoices.index(a1)-1].idtag and t1.activePokemon.battHP == t1.party[validChoices.index(a1)-1].battHP:
							print("{name} is already in battle!\n".format(name = t1.activePokemon.name))						
						else:
							t1action = "switch-5"
							isFinished = True
							madeChoice = True
					elif a1 == "x":
						madeChoice = True
		isFinished = False
		while not isFinished:
			r1 = input("\n{name}, what would you like to do?\n(Enter number of desired option)\n1)Attack\n2)Switch Pok\u00e9mon\n".format(name = t2.name))
			while (r1 != "1" and r1 != "2") or r1 == "x":
				r1 = input("{name}, what would you like to do?\n(Enter number of desired option)\n1)Attack\n2)Switch Pok\u00e9mon\n")
			if r1 == "1":
				print("Choose an attack to use:")
				t2.activePokemon.battlePrintMoves()
				options = len(t2.activePokemon.moves)
				validChoices = ["x", "a","b","c","d"]
				print("\n(Enter letter of desired option, X to go back)\n")
				a1 = input()
				a1 = a1.lower()
				while a1 not in validChoices[:options+1]:
					print("\n(Enter letter of desired option, X to go back)\n")
					a1 = input()
					a1 = a1.lower()
				if a1 == "a":
					if t2.activePokemon.moves[0].pp > 0:
						t2action = "attack-0"
						isFinished = True
				elif a1 == "b":
					if t2.activePokemon.moves[1].pp > 0:
						t2action = "attack-1"
						isFinished = True
				elif a1 == "c":
					if t2.activePokemon.moves[2].pp > 0:
						t2action = "attack-2"
						isFinished = True
				elif a1 == "d":
					if t2.activePokemon.moves[2].pp > 0:
						t1action = "attack-3"
						isFinished = True
				else:
					pass
			if r1 == "2":
				madeChoice = False
				while not madeChoice:
					print("Choose which member of your party to switch in:")
					t2.battleShowParty()
					options = len(t2.party)
					validChoices = ["x", "a","b","c","d", "e", "f"]
					print("\n(Enter letter of desired option, X to go back)\n")
					a1 = input()
					a1 = a1.lower()
					while a1 not in validChoices[:options+1]:
						print("\n(Enter letter of desired option, X to go back)\n")
						a1 = input()
						a1 = a1.lower()
					if a1 == "a":
						if t2.activePokemon.idtag == t2.party[validChoices.index(a1)-1].idtag and t2.activePokemon.battHP == t2.party[validChoices.index(a1)-1].battHP:
							print("{name} is already in battle!\n".format(name = t2.activePokemon.name))
						else:
							t2action = "switch-0"
							isFinished = True
							madeChoice = True
					elif a1 == "b":
						if t2.activePokemon.idtag == t2.party[validChoices.index(a1)-1].idtag and t2.activePokemon.battHP == t2.party[validChoices.index(a1)-1].battHP:
							print("{name} is already in battle!\n".format(name = t2.activePokemon.name))
						else:
							t2action = "switch-1"
							isFinished = True
							madeChoice = True
					elif a1 == "c":
						if t2.activePokemon.idtag == t2.party[validChoices.index(a1)-1].idtag and t2.activePokemon.battHP == t2.party[validChoices.index(a1)-1].battHP:
							print("{name} is already in battle!\n".format(name = t2.activePokemon.name))	
						else:
							t2action = "switch-2"
							isFinished = True
							madeChoice = True
					elif a1 == "d":
						if t2.activePokemon.idtag == t2.party[validChoices.index(a1)-1].idtag and t2.activePokemon.battHP == t2.party[validChoices.index(a1)-1].battHP:
							print("{name} is already in battle!\n".format(name = t2.activePokemon.name))						
						else:
							t2action = "switch-3"
							isFinished = True
							madeChoice = True
					elif a1 == "e":
						if t2.activePokemon.idtag == t2.party[validChoices.index(a1)-1].idtag and t2.activePokemon.battHP == t2.party[validChoices.index(a1)-1].battHP:
							print("{name} is already in battle!\n".format(name = t2.activePokemon.name))						
						else:
							t2action = "switch-4"
							isFinished = True
							madeChoice = True
					elif a1 == "f":
						if t2.activePokemon.idtag == t2.party[validChoices.index(a1)-1].idtag and t2.activePokemon.battHP == t2.party[validChoices.index(a1)-1].battHP:
							print("{name} is already in battle!\n".format(name = t2.activePokemon.name))						
						else:
							t2action = "switch-5"
							isFinished = True
							madeChoice = True
					elif a1 == "x":
						madeChoice = True
		battle.action(t1action, t2action)



	

except EOFError:
	pass



