import trainer
import arena
import json
import math
import string
import pokemon
import moves
import sys
data = sys.stdin.readlines()
def printDex():
	#print pokedex out in index order (i.e. the order of the original pokedex)
	print("Gen I Pokedex:\n")
	print("{index: <5}{name: <12}{type: <18}{hp: <4}{atk: <8}{dfn: <8}{spa: <8}{spe: <8}".format(index = "#", name = "NAME", type = "TYPE(s)", hp = "HP", atk = "ATTACK", dfn = "DEFENCE", spa = "SPECIAL", spe = "SPEED"))
	#cycle through index numbers
	for i in range(1, len(dex.keys())):
		#finds key which contains next index number (this is clunky but it works, efficiency is not of the essence)
		for key in dex.keys():
			if dex[key]["id"] == i:
				print("{index: <5}{name: <12}{type: <18}{hp: <4}{atk: <8}{dfn: <8}{spa: <8}{spe: <8}".format(index = str(dex[key]["id"]), name = dex[key]["name"], type = ", ".join(dex[key]["types"]), hp = str(dex[key]["baseStats"]["hp"]), atk = str(dex[key]["baseStats"]["atk"]), dfn = str(dex[key]["baseStats"]["def"]), spa = str(dex[key]["baseStats"]["spa"]), spe = str(dex[key]["baseStats"]["spe"])))
try:
	with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/gen1moves.json") as pdex:
		g1moves = json.load(pdex)

	with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/pokedexwmoves.json") as pdex:
		dex = json.load(pdex)


	partySize = 7
	validsizes = ["1", "2", "3", "4", "5", "6"]
	while partySize not in validsizes:
		partySize = input("Contestants, decide and enter how many Pokemon you will both have in your parties\n")


	isRandom = ""
	while isRandom.lower() != "y" and isRandom.lower() != "n":
		isRandom = input("EVs are set to be maxed by default, would you like them to be randomised instead? [y/n]")
	isRandom = isRandom.lower()


	name1 = input("\nTrainer #1, please enter your name:\n(up to 10 characters)\n")
	#check input is valid, if not, prompt again until valid
	while(len(name1) >10):
		name1 = input("\nTrainer#1, please enter your name:\n(up to 10 characters)\n")
	t1 = trainer.Trainer(name)

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
			print("\n".join("{name: <15}{mtype: <10}{power: <10}{accuracy: <7}{pp: <5}".format(name = str(g1moves[key]["name"]), mtype = str(g1moves[key]["type"]), power = str(g1moves[key]["basePower"]), accuracy = str(g1moves[key]["accuracy"]), pp = str(g1moves[key]["pp"])) for key in sorted(g1moves[pname]["learnset"].keys())))
			poke = t1.party[-1]
			#trainer now makes 4 choices on moves
			while len(poke.moves) < 4:
				#trainer can input any combination of capitalisation spaces and hyphens, can input individually or as comma separated list in terminal
				movechoices = "buffer"	
				movechoices = input("\n{trainerName}, please complete your choice of moves for {name} (comma separated)\nYou have {places} moves left to choose:\n".format(trainerName = trainerName, name = poke.name, places = 4 - len(poke.moves)))
				movechoices = movechoices.lower().split(",")
				movechoices = [move.replace(" ", "").replace("-", "") for move in movechoices]
				if len(poke.moves) != len(g1moves[pname]["learnset"]):
					for move in movechoices:
						if move in g1moves[pname]["learnset"].keys() and move not in names:
							if len(poke.moves) <4:
								if len(poke.moves) == 0:
									print("You chose {move} as {pkmn}'s first move!".format(move = g1moves[pname]["learnset"][move], pkmn = poke.name))	
								elif len(poke.moves) == 1:
									print("You chose {move} as {pkmn}'s second move!".format(move = g1moves[pname]["learnset"][move], pkmn = poke.name))
								elif len(poke.moves) == 2:
									print("You chose {move} as {pkmn}'s third move!".format(move = g1moves[pname]["learnset"][move], pkmn = poke.name))
								elif len(poke.moves) == 3:
									print("You chose {move} as {pkmn}'s final move!".format(move = g1moves[pname]["learnset"][move], pkmn = poke.name))
								poke.moves.append(moves.Move(move))
								names.append(move)
				#prints current moveset to remind trainer as moves can only be added to moveset once each
				print("\nCurrent moveset:")
				poke.printMoves()				
		else:
			for key in g1moves[pname]["learnset"].keys():
				poke.moves.append(moves.Move(key))
				print("{name} has 4 or less moves in their moveset, you can have 'em all!\n".format(name = g1moves[pname]["name"]))
		pname = ""
		moves = "buffer"


	name2 = input("\nTrainer #2, please enter your name:\n(up to 10 characters)\n")

	#check input is valid, if not, prompt again until valid
	while(len(name2) >10):
		name2 = input("\nTrainer#2, please enter your name:\n(up to 10 characters)\n")

	put("\nTrainer #1, please enter your name:\n(up to 10 characters)\n")
	#check input is valid, if not, prompt again until valid
	while(len(name2) >10):
		name2 = input("\nTrainer#1, please enter your name:\n(up to 10 characters)\n")
	t2 = trainer.Trainer(name2)

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
			print("\n".join("{name: <15}{mtype: <10}{power: <10}{accuracy: <7}{pp: <5}".format(name = str(g1moves[key]["name"]), mtype = str(g1moves[key]["type"]), power = str(g1moves[key]["basePower"]), accuracy = str(g1moves[key]["accuracy"]), pp = str(g1moves[key]["pp"])) for key in sorted(g1moves[pname]["learnset"].keys())))
			poke = t2.party[-1]
			#trainer now makes 4 choices on moves
			while len(poke.moves) < 4:
				#trainer can input any combination of capitalisation spaces and hyphens, can input individually or as comma separated list in terminal
				movechoices = "buffer"	
				movechoices = input("\n{trainerName}, please complete your choice of moves for {name} (comma separated)\nYou have {places} moves left to choose:\n".format(trainerName = trainerName, name = poke.name, places = 4 - len(poke.moves)))
				movechoices = movechoices.lower().split(",")
				movechoices = [move.replace(" ", "").replace("-", "") for move in movechoices]
				if len(poke.moves) != len(g1moves[pname]["learnset"]):
					for move in movechoices:
						if move in g1moves[pname]["learnset"].keys() and move not in names:
							if len(poke.moves) <4:
								if len(poke.moves) == 0:
									print("You chose {move} as {pkmn}'s first move!".format(move = g1moves[pname]["learnset"][move], pkmn = poke.name))	
								elif len(poke.moves) == 1:
									print("You chose {move} as {pkmn}'s second move!".format(move = g1moves[pname]["learnset"][move], pkmn = poke.name))
								elif len(poke.moves) == 2:
									print("You chose {move} as {pkmn}'s third move!".format(move = g1moves[pname]["learnset"][move], pkmn = poke.name))
								elif len(poke.moves) == 3:
									print("You chose {move} as {pkmn}'s final move!".format(move = g1moves[pname]["learnset"][move], pkmn = poke.name))
								poke.moves.append(moves.Move(move))
								names.append(move)
				#prints current moveset to remind trainer as moves can only be added to moveset once each
				print("\nCurrent moveset:")
				poke.printMoves()				
		else:
			for key in g1moves[pname]["learnset"].keys():
				poke.moves.append(moves.Move(key))
				print("{name} has 4 or less moves in their moveset, you can have 'em all!\n".format(name = g1moves[pname]["name"]))
		pname = ""
		moves = "buffer"

	t1.showParty()
	t2.showParty()

	
except Exception as e:
	raise e