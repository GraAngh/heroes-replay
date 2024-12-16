from .AbstractPagination import AbstractPagination


class NestedPagination(AbstractPagination):
    def __init__(self, objectPointer, first):
        super().__init__(first)
        self.__op = objectPointer
        self.__isZeroPositoin = True
        self.hasData = False
        self.resetPagesStates()  
        
    def resetPagesStates(self):
        self.__pages = {}
    
    def __addPage(self, number, page, start, end):
        self.__pages[number] = {
            'startIndex': start, 
            'endIndex': end,
            'page': page
        }
    
    # шаг идет в глубину, и в ширину
    def step(self):
        if self.__op.down(True):
            return self.__op.repr(), self.__op.current()
            
        if self.__op.forward():
            return self.__op.repr(), self.__op.current()
            
        while self.__op.up():             
            if self.__op.forward():
                return self.__op.repr(), self.__op.current()    
        return None
    
    def page(self):
        if self._currentPage in self.__pages:
            return self.__pages[self._currentPage]['page']
        
        p = []
        f = self._first
        start = self.__op.repr()
        
        while f > 0:
            # для нулевой позиции. Курсор сразу указывает на первый элемент страницы
            if self.__isZeroPositoin:
                self.__isZeroPositoin = False
                items = start, self.__op.current() # <-- здесь происходит смещение, которое не позволяет повторно обойти
            else:
                items = self.step()
            
            if not items:
                self._fixLastPage()
                break
            p.append(items)
            f -= 1
        
        self.__addPage(self._currentPage, p, start, self.__op.repr())
        return p
    
    # Переход на следующую страницу заданным шагом
    def forward(self):
        if self.isLastPage():
           return None
        self._currentPage += 1
        return self.page()
            
    # Переход на предыдущую страницу
    def back(self):
        if self._currentPage == 0:
            return None
        self._currentPage -= 1
        return self.page()
    
    def at(self, n):
        if n < 0: 
            self._currentPage = 0
        else:
            while self._currentPage != n or not self.forward():
                pass
        return self.page()
    
    def first(self, amount):
        super().first(amount)
        self.resetPagesStates()   
        self.atZeroPosition()   
    
    def getObjectPointer(self):
        return self.__op
        
    def atZeroPosition(self):
        self.__isZeroPositoin = True
        self.__op.at([0])