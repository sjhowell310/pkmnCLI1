import random
import math
import json
import moveset
import battle
import trainer
import pokemon
import moveset

with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/pokedexwmoves.json") as pdex:
	dex = json.load(pdex)

with open("/home/stephen/Documents/coding/python3/pkmnCLI1/data/final/gen1moves.json") as g1mov:
	g1m = json.load(g1mov)
 	
t1 = trainer.Trainer("Steve")
t2 = trainer.Trainer("Jon")
thisbattle = battle.Battle(t1,t2)

thisbattle.t1.party.append(pokemon.Pokemon(dex["tentacruel"], "n"))
thisbattle.t1.party[0].moves.append(moveset.Move("surf"))

thisbattle.t2.party.append(pokemon.Pokemon(dex["geodude"], "n"))
thisbattle.t2.party[0].moves.append(moveset.Move("rockslide"))
t1.showPartywMoves()
t2.showPartywMoves()
off = thisbattle.t1.party[0]
att = thisbattle.t1.party[0].moves[0]
dfn = thisbattle.t2.party[0]
print(thisbattle.getDamage(off, att, dfn))
print(thisbattle.takeConfusionDamage(thisbattle.t1.party[0]))
movestargettypes = []
for key in g1m.keys():
	if g1m[key]["basePower"] == 0 and g1m[key]["target"] == "self":
		movestargettypes.append(key)
print(sorted(movestargettypes))

# moveswithboost
# ['acidarmor', 'agility', 'amnesia', 'barrier', 'defensecurl', 'doubleteam', 'flash' offensive, 'growl', 'growth', 'harden', 'kinesis', 'leer', 'meditate', 'minimize', 'sandattack', 'screech', 'sharpen', 'smokescreen', 'stringshot', 'swordsdance', 'tailwhip', 'withdraw']

# target types
# ['allAdjacent', 'allAdjacentFoes', 'allySide', 'any', 'normal', 'randomNormal', 'scripted', 'self']