class AbstractPagination:
    def __init__(self, first):
        self._first = first
        self._lastPageFound = False
        self._lastPage = 0
        self._currentPage = 0
    
    def _fixLastPage(self):
        if self._lastPageFound:
            return
        self._lastPageFound = True
        if not(self._lastPage == self._currentPage):
            self._lastPage = self._currentPage
    
    def isLastPage(self):
        return self._lastPageFound and self._currentPage == self._lastPage
        
    def first(self, amount):
        self._lastPageFound = False
        self._first = amount
    
    # Переход на следующую страницу заданным шагом
    def forward(self):
        raise(Exception('not implemented'))
            
    # Переход на предыдущую страницу
    def back(self):
        raise(Exception('not implemented'))
    
    # Переход на указанную страницу
    def at(self, n):
        raise(Exception('not implemented'))
    
    def page(self):
        raise(Exception('not implemented'))
    
    def getPagesAmount(self):
        raise(Exception('not implemented'))
    
    def currentNumber(self):
        return self._currentPage