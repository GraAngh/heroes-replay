class ReplayRepr:
    def __init__(self, replay):
        self.__replay = replay
        
    def show(self):
        r = self.__replay
        a, b = r.getTeams()
        aPlayers = a.getPlayers()
        bPlayers = b.getPlayers()
       
        lines = [
            f'>>> {r.getTitle()}',
            f'>>> {r.getDate()}'
        ]
        
        # Строка победителя
        if a.isWon():
            lines.append(
                '{:>5}'.format('WIN')
            )
        else:
            lines.append(
                '{:>42}'.format('WIN')
            )
        lines.append('  {:->70}'.format(' '))
        # Вертикальный вывод 
        pAmount = len(aPlayers) 
        i = 0
        while i < pAmount:
            a_p = aPlayers[i]
            a_hero = a_p.getHero()
            a_name = a_p.getName()
            a_slot = a_p.getSlot()
            
            b_p = bPlayers[i]
            b_hero = b_p.getHero()
            b_name = b_p.getName()
            b_slot = b_p.getSlot()
            lines.append(
                f' {a_slot:>2}. {a_name:<12} : {a_hero:<18}{b_slot:>2}. {b_name:<12} : {b_hero:<10}'
                .format()
            )    
            i += 1
        lines.append('')
        print('\n'.join(lines))
    
    def getResult(self):
        return self.__replay