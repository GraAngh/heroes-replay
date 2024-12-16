import cache, os

def move(dirA, dirB, oldExt, newExt):
	for it in os.scandir(dirA):
		base, ext = os.path.splitext( os.path.split(it.path)[1] )
		if ext == oldExt:
			print('rename', os.path.split( it )[1], 'to', os.path.split( base + newExt )[1])
			os.rename( it.path, os.path.join(dirB, base + newExt) )

dirA = 'cache'
dirB = os.path.join( dirA, 'details' )
oldExt = '.repr'
newExt = '.json'
move(dirB, dirB, oldExt, newExt)


