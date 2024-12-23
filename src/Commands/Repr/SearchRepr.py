class SearchRepr:
    def __init__(self, pagination):
        self.__pagination = pagination
    
    def __show(self, page):
        if not page:
            return
        for i, data in page:
            name = data['replay'].getName()
            player = data['player'].toString()
            print(f'{i}. {player} {name}')
        pagesLen = self.__pagination.getPagesAmount() - 1
        currentPage = self.__pagination.currentNumber()
        print(f'--- {currentPage}/{pagesLen} ---')
            
    def show(self):
        self.__show(self.__pagination.page())
    
    def hasData(self):
        return self.__pagination.getResultLength()
        
    def forward(self):
        self.__show(self.__pagination.forward())
    
    def back(self):
        self.__show(self.__pagination.back())
        
    def at(self, num):
        self.__show(self.__pagination.at(num))
        
    def first(self, amount):
        self.__pagination.first(amount)
        
    def sort(self, args = []):
        reverse = False
        sortType = '-d'
        for o, v in args:
            if o == '-r':
                reverse = True
            elif o == '-n':
               sortType = '-n'
            elif o == '-t':
               sortType = '-t'
            elif o == '-m':
               sortType = '-m'
        
        def sortCb(data):
            if sortType == '-d':
                return self.__sortByDate(data, reverse)
            elif sortType == '-n':
                return self.__sortByName(data, reverse)
            elif sortType == '-t':
                return self.__sortByToon(data, reverse)
            elif sortType == '-m':
                return self.__sortByMap(data, reverse)
            return data
        
        self.__pagination.sort( sortCb )
    
    def __sortByDate(self, data, reverse):
        return sorted(
            data
          , key = lambda item: item['replay'].getDetails().getDatetime() 
          , reverse = reverse
        )
    
    def __sortByName(self, data, reverse):
        return sorted(
            data
          , key = lambda item: item['player'].getName()
          , reverse = reverse
        )
        
    def __sortByToon(self, data, reverse):
        return sorted(
            data
          , key = lambda item: item['player'].getToon().getRepr()
          , reverse = reverse
        )
        
    def __sortByMap(self, data, reverse):
        return sorted(
            data
          , key = lambda item: item['replay'].getTitle()
          , reverse = reverse
        )
        
    def getPagination(self):
        return self.__pagination