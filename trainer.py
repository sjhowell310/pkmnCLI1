import pokemon
import json
import math
import string
import moves

#Trainer class for use in pkmnCLI1, contained by Arena class, contains Pokemon in party (none of these classes extend one another)
class Trainer():

	#declare init for instantiation
	def __init__(self, name):
		#take name as in put from command line
		self.name = name.capitalize()
		self.party = []
		self.activePokemon = None

		
	#function which prints entire party to terminal along with each members moveset
	def showParty(self):
		print("\n{name}'s current party:".format(name = self.name))
		i = 0
		for pokemon in self.party:
			i +=1
			print("\n{pos: <5} {name: <12}{type: <18}{hp: <4}{atk: <7}{dfn: <8}{spa: <8}{spe: <8}".format(pos = str(i) + ")", name = "NAME", type = "TYPE(s)", hp = "HP", atk = "ATTACK", dfn = "DEFENCE", spa = "SPECIAL", spe = "SPEED"))
			print("{pos: <6}{name: <12}{type: <18}{hp: <4}{atk: <7}{dfn: <8}{spa: <8}{spe: <8}\n".format(pos= "", name = pokemon.name, type = ", ".join(pokemon.type), hp = str(pokemon.battHP), atk = str(pokemon.battAtk), dfn = str(pokemon.battDef), spa = str(pokemon.battSpa), spe = str(pokemon.battSpe)))

	#function which prints entire party to terminal along with each members moveset
	def showPartywMoves(self):
		print("\n{name}'s party and their movesets:".format(name = self.name))
		i = 0
		for pokemon in self.party:
			i +=1
			print("\n{pos: <5} {name: <12}{type: <18}{hp: <4}{atk: <7}{dfn: <8}{spa: <8}{spe: <8}".format(pos = str(i) + ")", name = "NAME", type = "TYPE(s)", hp = "HP", atk = "ATTACK", dfn = "DEFENCE", spa = "SPECIAL", spe = "SPEED"))
			print("{pos: <6}{name: <12}{type: <18}{hp: <4}{atk: <7}{dfn: <8}{spa: <8}{spe: <8}\n".format(pos= "", name = pokemon.name, type = ", ".join(pokemon.type), hp = str(pokemon.statHP), atk = str(pokemon.statAtk), dfn = str(pokemon.statDef), spa = str(pokemon.statSpa), spe = str(pokemon.statSpe)))
			pokemon.printMoves()

	#function that switches a party member into battle
	def switchIn(self, pokemon):
		if self.activePokemon == None:
			self.activePokemon = pokemon
			pokemon.active = True
		elif pokemon.statHP <=0:
			print("{name} has fainted and doesn't have any energy to battle!".format(pokemon.name))
		else:
			print("{tname} switched {current} out for {switch}!".format(tname = self.name, current = self.activePokemon.name, switch = pokemon.name))
			self.activePokemon.active = False
			pokemon.active = True
			self.activePokemon = pokemon

