import re

def equalsStrings(a, b, caseSensitive):
	if not caseSensitive:
		a = a.lower()
		b = b.lower()
	return a == b

def equalsNums(a, b, *rest):
	return a == b

def mathcRegExp(pattern, str, *rest):
	return pattern.search(str)


def chooseComparisonStrategy(a):
	t = type(a)
		
	if t is re.Pattern:
		return mathcRegExp
	elif t is int:
		return equalsNums
	elif t is str :
		return equalsStrings
	else:
		raise TypeError('отсутсвует подходящая стратегия сравнения для %s и %s' % (t_a, t_b) )
	

def every(needles, stack, comparison):
	for needle in needles:
		has = False
		for straw in stack:
			strategy = chooseComparisonStrategy(needle)
			if comparison(needle, straw, strategy):
				has = True
				break
				
		if not has:
			return False
			
	return True

def some(needles, stack, comparison):
	for needle in needles:
		for straw in stack:
			strategy = chooseComparisonStrategy(needle)
			if comparison(needle, straw, strategy):
				return True
	return False
