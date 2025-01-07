class PlayerRepr:
    def __init__(self, player):
        self.__player = player
        
    def show(self):
        p = self.__player
        t = p.getToon()
        names = []
        print( ' TOON: ' + str(t.getId()) + '' )
        print( ' -----------------' )
        for p in t.getPlayers():
            name = p.getName() 
            if name not in names:
                names.append(name)
                print(' ' + str(len(names)) + '. ' + name)
        