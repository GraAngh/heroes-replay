from src.comparisons import *
	
def __teamBy(input, details, listGetter, comparesing):
	teamA, teamB = details.teams()
	soughtFor = None
	
	if every( input, listGetter( teamA ), comparesing ):	
		soughtFor = teamA
	elif every( input, listGetter( teamB ), comparesing ):	
		soughtFor = teamB
	
	return soughtFor

# для совпадения id Должна быть в общем списке, значит будет искать её в toon.id
def teamByToon(ids, details):
	return __teamBy( 
		ids
	  , details
	  , lambda team: team.toonIds()
	  , lambda a,b,strategy: strategy(a,b) 
	)
	
def teamByPlayers(players, details):
	return __teamBy( 
		players
	  , details
	  , lambda team: team.players()
	  , lambda a,b,strategy: a == b 
	)

def teamByPlayerNames(names, details, caseSensitive = False):
	return __teamBy( 
		names
	  , details
	  , lambda team: team.playerNames()
	  , lambda a,b,strategy: strategy(a,b,caseSensitive) 
	)

def teamByHeroes(names, details, caseSensitive = False):
	return __teamBy( 
		names
	  , details
	  , lambda team: team.heroes() 
	  , lambda a,b,strategy: strategy(a,b,caseSensitive) 
	)
		
# todo 
# поиск toon id по нику
# поиск имен по toon id
# ? контроль уникальности сущностей для игроков
# 

