class SearchRepr:
    def __init__(self, pagination):
        self._pagination = pagination
    
    def __show(self, page):
        if not page:
            return
        for i, data in page:
            name = data['replay'].getName()
            player = data['player'].toString()
            print(f'{i}. {player} {name}')
        pagesLen = self._pagination.getPagesAmount() - 1
        currentPage = self._pagination.currentNumber()
        print(f'--- {currentPage}/{pagesLen} ---')
            
    def show(self):
        self.__show(self._pagination.page())
        
    
    def sortByDate(self, asce = True):
        self._result = sorted(
            self._result
          , key=lambda r: r['replay'].getDetails().getDatetime() 
        )
        
    def hasData(self):
        return self._pagination.getResultLengh()
        
    def forward(self):
        self.__show(self._pagination.forward())
    
    def back(self):
        self.__show(self._pagination.back())
        
    def at(self, num):
        self.__show(self._pagination.at(num))
        
    def first(self, amount):
        self._pagination.first(amount)