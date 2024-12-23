import os
import re
from src.comparisons import *
import src.finders

def __checkTeamRestriction(names):
	if len( names ) > 5:
		raise Exception('не больше 5 человек в команде')
	

def __checkOwnMatchRestriction(names):
	if len( names ) > 15:
		raise Exception('не больше 15 человек в собственной игре(с обозревателями)')

def __checkMatchRestriction(names):
	if len( names ) > 10:
		raise Exception('не больше 10 человек в матче')

 # к примеру такой набор 
 # [ 'ромашка', re.compile('^(thao(sha)?|regarpominki)$', re.I) ]
def players(names, details, caseSensitive = False):
	return every(
		names,
		details.playerNames(),
		lambda a, b, strategy: strategy(a, b, caseSensitive)
	)

def somePlayers(names, details, caseSensitive = False):
	return some(
		names,
		details.playerNames(),
		lambda a, b, strategy: strategy(a, b, caseSensitive)
	)

def matchPlayers(names, details, flags):
	return every(
		names,
		details.playerNames(),
		lambda template, name, strategy: strategy(template, name, flags)
	)

def heroes(names, details, caseSensitive = False):
	return every(
		names,
		details.heroes(),
		lambda a, b, strategy: strategy(a, b, caseSensitive)
	)
	
def toonIds(ids, details):
	return every(
		names,
		details.toonIds(),
		lambda a, b, strategy: strategy(a, b)
	)

def opponentPlayers(names_a, names_b, details, caseSensitive = False):
	team = finders.teamByPlayerNames(names_a, details)
	if not team:
		return False
	
	result = every(
		names_b,
		team.oppositeTeam().playerNames(),
		lambda a, b, strategy: strategy(a, b, caseSensitive)
	)
	return result
	
def allyPlayers(names, details):
	return bool( finders.teamByPlayerNames(names, details) )
	
def allyHeroes(names, details):
	return bool( finders.teamByHeroes(names, details) )

def opponentHeroes(names, details):
	pass
	
def includingMaps(maps, details):
	return some(
		[ details.getMap() ],
		maps,
		lambda a, b, strategy: strategy(a, b, False)
	)
	
def excludingMaps(maps, details):
	pass

def isTeamWin(names, details):
	pass

def isTeamLose(names, details):
	pass

def isPlayersWin(names, details):
	pass

def isPlayersLose(names, details):
	pass

def isTeamate(a, b, details):
	pass

def isOppenent(a, b, details):
	pass

# коллекция из имен не более 5 и не меннее 2
def isTeamates(names, details):
	pass
	
def isOppenents( player, names, details ):
	pass

# это внешняя проверка, не гарантирующая, что файл является реплеем.
# Т.е. прредположим, что внутри данные реплея
def isReplaySource( path ):
	basename, ext = os.path.splitext( path )
	return ext == '.StormReplay'
