"""

    Курсор [N0, N1, .., Ni]
    CNi - уровень (будем писать как Ci)
    Ni - значение индекса на уровне Ci

"""

class ObjectPointer:
    def __init__(self, rootList, childrenGetters, lvls = 1):
        if lvls < 1:
            raise Exception('размерность курсора должна быть больше 0')
        # количество геттеров должно быть на одно меньше, чем количество возможных уровней
        # т.к. на последнем уровне геттер не нужен
        if len(childrenGetters) + 1 < lvls:
            raise Exception('недостаточный набор геттеров дочерних списков')
            
        #Многоуровенвый указатель
        self._lvls = lvls
        self._childrenGetters = childrenGetters
        self._rootList = rootList
        # поля состояний
        self.__resetStates()
    
    def getRootList(self):
        return self._rootList
    
    def __resetPointer(self):
        self._currentLvl = 0
        self._pointer = [0] * self._lvls
    
    def __resetStates(self):
        self.__resetPointer()
        self._prevLists = []
        self._currentList = self._rootList
        self.__initCurrentObject()
    
# попытка текущей позиции извлечь объет для и его дочерний список
    """ По факту мне необходим некий родительский список для текущего уровня
        Зависит от self._currentList, достает значение по индексу для данного списка
    """
    def __initCurrentObject(self):
        self._currentObject = self.__fetchCurrentObj()
        self.__initCurrentChildren()
        return self._currentObject
    
    def __initCurrentChildren(self):
        childrenGetter = self.__getCurrentChildrenGetter()
        if childrenGetter and self._currentObject:
            self._children = childrenGetter( self._currentObject )
        else:
            self._children = None
        return self._children
    """
    @return AbstractObject|None
    """
    def __fetchCurrentObj(self):
        i = self.__currentIndex() 
        if i >= 0 and i < len(self._currentList):
            return self._currentList[i]
        return None
    
    """
    @return callabale|None
    """
    def __getCurrentChildrenGetter(self):
        if self._currentLvl >= len(self._childrenGetters):
            return None
        return self._childrenGetters[ self._currentLvl ]
    
    def __currentIndex(self):
        return self._pointer[self._currentLvl]
    
    def __iterateCurrentIndex(self):
        i = self._pointer[self._currentLvl] 
        if i >= len(self._currentList) - 1:
            return False
        self._pointer[self._currentLvl] = i + 1
        return True
        
    def __deterateCurrentIndex(self):
        i = self._pointer[self._currentLvl] 
        if i == 0:
            return False
        self._pointer[self._currentLvl] = i - 1
        return True
    
    def __resetCurrentIndex(self):
        self.__setCurrentIndex(0)
    
    def __setCurrentIndex(self, index):
        self._pointer[self._currentLvl] = index
    
    def current(self):
        return self._currentObject
    
    def __atLastLvl(self):
        self._currentLvl = self._lvls - 1
        
    def up(self):
        if self._currentLvl == 0:
            return None
        self._currentLvl -= 1
        self._children = self._currentList
        self._currentList = self._prevLists.pop()
        self.__initCurrentObject()
        return self._currentObject
            
    def down(self, resetIndex = False):
        if self._currentLvl + 1 >= self._lvls:
            return None       
        
        oldList = self._currentList
        # при переходе ниже дочерний заменит текущий список список объектов
        if not self._currentObject:
            return None
        
        if self._children:
            newList = self._children
        else:
            newList = self.__getCurrentChildrenGetter()( self._currentObject )
        
        # места мутаций объекта:
        
        # манипуляции с указателем
        self._currentLvl += 1
        # изменения состояния списков
        self._currentList = newList
        
        # проверка режима сброса индекса после установки нового уровня
        if resetIndex:
            self.__resetCurrentIndex()
        
        # инициализация объекта
        if not self.__initCurrentObject():
            # откат
            self._currentList = oldList
            return None
        
        self._prevLists.append(oldList)
        return self._currentObject
    
    def forward(self):
        if not self.__iterateCurrentIndex(): 
            return None
        self.__initCurrentObject()
        return self._currentObject
    
    def back(self):
        if not self.__deterateCurrentIndex(): 
            return None
        self.__initCurrentObject()
        return self._currentObject
        
    # @todo добавить возможность перехода по свободно установленному курсору
    def at(self, pointer):
        lvls = len(pointer)
        if lvls > self._lvls:
            raise Exception('размерность курсора больше дозволенного')
        self.__resetStates()
        self._pointer = self.__normalizePointer(pointer)
        while True:
            if not self.__initCurrentObject():
                return None
            if self._currentLvl >= lvls - 1:
                break
            if not self.down():
                break
        return self._currentObject
        
    def repr(self):
        p = self._pointer[:self._currentLvl + 1]
        return '.'.join( map(lambda x: str(x), p) )
        
    def parse(self, serializedCursor):
        p = list( map(lambda x: int(x), serializedCursor.split('.') ) )
        return self.at(p)
    
    def __normalizePointer(self, p):
        return p + [0] * (self._lvls - len(p))
    