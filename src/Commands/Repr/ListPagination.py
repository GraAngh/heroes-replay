from .AbstractPagination import AbstractPagination
import math

class ListPagination(AbstractPagination):
    def __init__(self, result, first):
        super().__init__(first)
        self.__result = result
        self.__resultLen = len(self.__result)
        
    def page(self):
        p = []
        offset = 0
        start = self._currentPage * self._first # начальная позиция страницы
        
        while offset < self._first:
            i = start + offset
            # когда данных больше нет в наборе для страницы
            if i >= self.__resultLen:
                self._fixLastPage()
                return p
            p.append( (str(i), self.__result[i]) )
            offset += 1 
        
        # особый случай, когда последняя страница полностью заполняется по длине,
        # то переход на новую будет нулевой длины
        # Значит здесь нужн проверить, что данных дальше нет, так не было 
        # преждевременного заверешения
        if (self._currentPage + 1)* self._first == self.__resultLen:
            self._fixLastPage()
        return p
    
    def forward(self):
        if self.isLastPage():
            return None
        self._currentPage += 1
        return self.page()
        
    def back(self):
        if self._currentPage == 0:
            return None
        self._currentPage -= 1
        return self.page()
        
    def at(self, n):
        if n < 0:
            self._currentPage = 0
        elif n * self._first > self.__resultLen:
            self._currentPage = self.getPagesAmount() - 1
        else: 
            self._currentPage = n
        return self.page()
    
    def getPagesAmount(self):
        return math.ceil(self.__resultLen / self._first)
    
    def getResult(self):
        return self.__result
        
    def getResultLengh(self):
        return self.__resultLen
        
        