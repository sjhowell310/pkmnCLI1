import pokemon
import json
import math
import string
import moveset
import time

#Trainer class for use in pkmnCLI1, contained by Arena class, contains Pokemon in party (none of these classes extend one another)
class Trainer():

	#declare init for instantiation
	def __init__(self, name):
		#take name as in put from command line
		self.name = name.capitalize()
		print("Welcome to the game, {name}!\n".format(name = self.name))
		self.party = []
		self.activePokemon = None

		
	#function which prints entire party to terminal along with each members moveset
	def showParty(self):
		print("\n{name}'s party:".format(name = self.name))
		i = 0
		for pokemon in self.party:
			i +=1
			print("\n{pos: <5} {name: <12}{type: <18}{hp: <4}{atk: <7}{dfn: <8}{spa: <8}{spe: <8}".format(pos = str(i) + ")", name = "NAME", type = "TYPE(s)", hp = "HP", atk = "ATTACK", dfn = "DEFENCE", spa = "SPECIAL", spe = "SPEED"))
			print("{pos: <6}{name: <12}{type: <18}{hp: <4}{atk: <7}{dfn: <8}{spa: <8}{spe: <8}\n".format(pos= "", name = pokemon.name, type = ", ".join(pokemon.type), hp = str(pokemon.battHP), atk = str(pokemon.battAtk), dfn = str(pokemon.battDef), spa = str(pokemon.battSpa), spe = str(pokemon.battSpe)))


	#function to succinctly show status of party during battle (i.e. less details than are output during initial config)
	def battleShowParty(self):
		i = 0
		options = ["a","b","c","d","e","f"]
		for pokemon in self.party:
			print("\n{pos: <5} {name: <12}{type: <18}{hp: <4}\n".format(pos = options[i] + ")", name = "NAME", type = "TYPE(s)", hp = "HP"))
			print("{pos: <6}{name: <12}{type: <18}{hp: <4}\n".format(pos= "", name = pokemon.name, type = ", ".join(pokemon.type), hp = str(pokemon.battHP)))
			i +=1
	

	#function which prints entire party to terminal along with each members moveset
	def showPartywMoves(self):
		print("\n{name}'s party and their movesets:".format(name = self.name))
		i = 0
		for pokemon in self.party:
			i +=1
			print("\n{pos: <5} {name: <12}{type: <18}{hp: <4}{atk: <7}{dfn: <8}{spa: <8}{spe: <8}".format(pos = str(i) + ")", name = "NAME", type = "TYPE(s)", hp = "HP", atk = "ATTACK", dfn = "DEFENCE", spa = "SPECIAL", spe = "SPEED"))
			print("{pos: <6}{name: <12}{type: <18}{hp: <4}{atk: <7}{dfn: <8}{spa: <8}{spe: <8}".format(pos= "", name = pokemon.name, type = ", ".join(pokemon.type), hp = str(pokemon.battHP), atk = str(pokemon.battAtk), dfn = str(pokemon.battDef), spa = str(pokemon.battSpa), spe = str(pokemon.battSpe)))
			pokemon.printMoves()


	#function that switches a party member into battle
	def switchIn(self, pokemon):
		if self.activePokemon == None and pokemon.battHP != 0:
			self.activePokemon = pokemon
			pokemon.active = True
			index = self.party.index(pokemon)
			time.sleep(1)
			print("{tname} placed {current} at the front of their party!\n".format(tname = self.name, current = self.activePokemon.name))
			holder = self.party[0]
			self.party[0] = pokemon
			if len(self.party) > 1:
				for i in range(1, len(self.party)):
					self.party[index] = holder
		elif pokemon.battHP <=0:
			time.sleep(1)
			print("{name} has fainted and doesn't have any energy to battle!\n".format(name = pokemon.name))
		elif self.activePokemon.idtag == pokemon.idtag and self.activePokemon.battHP == pokemon.battHP:
			time.sleep(1)
			print("{name} is already in battle!\n".format(name = pokemon.name))
		else:
			time.sleep(1)
			print("{tname} switched {current} out for {switch}!\n".format(tname = self.name, current = self.activePokemon.name, switch = pokemon.name))
			self.activePokemon.active = False
			self.activePokemon.isConfused = False
			self.activePokemon.isConfusedCount = 0
			self.activePokemon.willFlinch = False
			index = self.party.index(pokemon)
			pokemon.active = True
			self.activePokemon = pokemon
			holder = self.party[0]
			self.party[0] = pokemon
			if len(self.party) > 1:
				for i in range(1, len(self.party)):
					self.party[index] = holder

