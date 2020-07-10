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
	if "boosts" in g1m[key].keys():
		movestargettypes.append(key)


print(sorted(movestargettypes))
# ['acidarmor', 'agility', 'amnesia', 'barrier', 'bide', 'defensecurl', 'doubleteam', 'focusenergy', 'growth', 'harden', 'haze', 'lightscreen', 'meditate', 'metronome', 'minimize', 'recover', 'reflect', 'rest', 'sharpen', 'softboiled', 'splash', 'substitute', 'swordsdance', 'teleport', 'withdraw']
# ['acidarmor', 'agility', 'amnesia', 'barrier', 'defensecurl', 'doubleteam', 'flash', 'growl', 'growth', 'harden', 'kinesis', 'leer', 'meditate', 'minimize', 'sandattack', 'screech', 'sharpen', 'smokescreen', 'stringshot', 'swordsdance', 'tailwhip', 'withdraw']
movestargettypes = []
for key in g1m.keys():
	if "movetype" not in g1m[key].keys():
		movestargettypes.append(key)
	


print(sorted(movestargettypes))
status = None

if not status:
	print("we in this")

#normal target 0 basePower
# ['confuseray', 'conversion', 'disable', 'flash', 'glare', 'growl', 'hypnosis', 'kinesis', 'leechseed', 'leer', 'lovelykiss', 'mimic', 'mist', 'poisongas', 'poisonpowder', 'roar', 'sandattack', 'screech', 'sing', 'sleeppowder', 'smokescreen', 'spore', 'stringshot', 'stunspore', 'supersonic', 'tailwhip', 'thunderwave', 'toxic', 'transform', 'whirlwind']


# moveswithboost
# ['acidarmor', 'agility', 'amnesia', 'barrier', 'defensecurl', 'doubleteam', 'flash' offensive, 'growl', 'growth', 'harden', 'kinesis', 'leer', 'meditate', 'minimize', 'sandattack', 'screech', 'sharpen', 'smokescreen', 'stringshot', 'swordsdance', 'tailwhip', 'withdraw']

# target types
# ['allAdjacent', 'allAdjacentFoes', 'allySide', 'any', 'normal', 'randomNormal', 'scripted', 'self']

#pure statmods
# ['acidarmor', 'agility', 'amnesia', 'barrier', 'defensecurl', 'doubleteam', 'focusenergy', 'growth', 'harden', 'haze', 'lightscreen', 'meditate', 'metronome', 'minimize', 'recover', 'reflect', 'rest', 'sharpen', 'softboiled', 'splash', 'substitute', 'swordsdance', 'teleport', 'withdraw']

# ['acidarmor', 'acidarmor', 'agility', 'agility', 'amnesia', 'amnesia', 'barrier', 'barrier', 'defensecurl', 'defensecurl', 'doubleteam', 'doubleteam', 'flash', 'focusenergy', 'growl', 'growth', 'growth', 'harden', 'harden', 'haze', 'kinesis', 'leer', 'lightscreen', 'meditate', 'meditate', 'metronome', 'minimize', 'minimize', 'recover', 'reflect', 'rest', 'sandattack', 'screech', 'sharpen', 'sharpen', 'smokescreen', 'softboiled', 'splash', 'stringshot', 'substitute', 'swordsdance', 'swordsdance', 'tailwhip', 'teleport', 'withdraw', 'withdraw']