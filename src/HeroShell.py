import cmd, getopt, re, sys
from .Commands import *
from .Config import Config
from .Supplying.ReplayCreater import ReplayCreater
from .Supplying.CommonStorageSupplyingStrategy import CommonStorageSupplyingStrategy
from .Supplying.CommonReplaySupplyingStrategy import CommonReplaySupplyingStrategy

class HeroShell(cmd.Cmd):
    WRONG_CMD_PREFIX = '__not_relevant_cmd__'
   
   #COMMANDS CONSTS
    CMD_EXIT = 'exit'
    CMD_HELP = 'help'
    CMD_RETURN = 'return'
    
    CMD_SEARCH = 'search'
    CMD_ACCOUNTS = 'accounts'
    CMD_ACCOUNT = 'account'
    CMD_TOON = 'toon'
    CMD_REPLAY = 'replay'
    CMD_PLAYER = 'player'
    CMD_FILTER = 'filter'
    CMD_SORT = 'sort'
    
    CMD_FORWARD = 'forward'
    CMD_BACK = 'back'
    CMD_FIRST = 'first'
    CMD_AT = 'at'
    
    CMD_TOOGLE = 'toogle'
    
    # MODE CONSTS
    MODE_INIT = 0
    MODE_SEARCH = 1
    MODE_PLAYER = 2
    MODE_REPLAY = 3
    MODE_ACCOUNTS = 4
    MODE_ACCOUNT = 5
    MODE_TOON = 6
    
    # PRMOMPT CONSTS
    PROMPT_REPLAY_MODE = 'replay>'
    PROMPT_PLAYER_MODE = 'player>'
    PROMPT_ACCOUNTS_MODE = 'accs>'
    PROMPT_ACCOUNT_MODE = 'acc>'
    PROMPT_TOON_MODE = 'toon>'
    PROMPT_SEARCH_MODE = 'search>'
    PROMPT_INIT_MODE = '>'
    
    intro = 'Обозреватель повторов Heroes of the Storm\n'
    aliaces = {}
    
    generalCommands = None
    pageCommands = None
    initCommands = None
    searchCommands = None
    accountsCommands = None
    accountCommands = None
    toonCommands = None
    playerCommands = None
    replayCommands = None
    toogleCommands = None
    
    def __init__(self, replayCreater):
        super().__init__(self) 
        self._replayCreater = replayCreater
        self._lastRepr = None
        self._modeStack = []
        
        # группа первичной инициализации и определения через метод
        self._mode = None
        # self.prompt = ''
        self.switchMode(self.MODE_INIT)
        
        # предварительные проверки 
        self._assertNoCmdAliacesConflict()
        
    
    def _assertNoCmdAliacesConflict(self):
        reversedMap = {}
        for cmd, names in self.aliaces.items():
            for name in names:
                # хоть одно совпадение
                if name in reversedMap:
                    raise Exception(f'комманда `{cmd}` имеет конфликт псевдонимов с командой `{reversedMap[name]}`')
                reversedMap[name] = cmd
                
    def getCreater(self):
        return self._replayCreater
    
    def default(self, prefixed_cmd):
        command = prefixed_cmd.removeprefix(self.WRONG_CMD_PREFIX)
        super().default(command)
    
    def emptyline(self):
        if self._mode != self.MODE_INIT:
            super().emptyline()
        else:
            self.do_help('')            
    
    
    def precmd(self, line):
        glue = ' '
        chunks = []
        
        for v in filter( lambda v: v, line.split(glue) ):
            chunks.append(v)
                
        if not len(chunks):
            # выход к дефолтному поведению
            return ''
        
        # обработка псевдонимов
        command = self.resolveAliace( chunks[0].lower() )
        if self.isActualCommand(command):
            # нормальный рабочий выход
            return glue.join( [command] + chunks[1:] )
        
        # выход с нерелевантной командой
        return self.WRONG_CMD_PREFIX + command
    
    def parseLine(self, argsLine):
        args = []
        regex = r"""
            (?P<SPACE> \s+ ) |
            (?P<ESCAPE> \\(?P<ESCAPED_CHAR> . ) ) |
            (?P<QUOTE> ['"`] ) |
            (?P<WORD> [^\s'"`\\]+ )
        """
        # Состояние захвата строки в кавычках
        is_str_capturing = False 
        open_quote = ''
        str = ''
            
        for match in re.finditer(regex, argsLine, re.I | re.X):
            # print(match.lastgroup, match.group()) #DEBUG
            if not is_str_capturing:
                if match.lastgroup == 'QUOTE':
                    open_quote = match.group()
                    is_str_capturing = True
                elif match.lastgroup == 'WORD':
                    str += match.group()
                elif match.lastgroup == 'ESCAPE':
                    str += match.group('ESCAPED_CHAR')
                elif match.lastgroup == 'SPACE':
                    # flush string
                    if str:
                        args.append( str )
                        str = ''
            else:
                if match.lastgroup == 'QUOTE':
                    if match.group() == open_quote:                  
                        open_quote = ''
                        is_str_capturing = False
                    else:
                        str += match.group()
                elif match.lastgroup == 'ESCAPE':
                    str += match.group('ESCAPED_CHAR')
                else:
                    str += match.group()
            
        # flush string в конце, когда тригер в виде разделителя не передан
        if str:
            args.append( str )
        
        return args
    
    # 
    # 
    #  Определение опций команд
    # 
    # 
    def parseArgs(self, command, args):
        try:
            if command == self.CMD_SEARCH:
                return getopt.getopt(
                    args
                  , 'ip:t:h:r:'
                  , [
                        '--ptr'
                      , '--ptr-only'
                      , '--NA'
                      , '--EU'
                      , '--AS'
                    ]
                )
            
            if command == self.CMD_ACCOUNTS:
                return getopt.getopt(
                    args
                  , 'ra:d:o:'
                )
            
            if command == self.CMD_SORT:
                return getopt.getopt(
                    args
                  , 'rntm'
                )
            
            """ 
            данная ветка приводит к общему виду, 
            когда дополнительных опций и нет 
            """
            if (
                command == self.CMD_FIRST or
                command == self.CMD_AT or
                command == self.CMD_REPLAY or
                command == self.CMD_TOOGLE 
            ):
                return [[], args]
        except getopt.GetoptError as err:
            print(err)
            
        return [ [], [] ]
    
    def parse(self, command, line):
        args = self.parseLine(line)
        return self.parseArgs(command, args)
    
    def resolveAliace(self, aliace):
        for command in self.aliaces:
            if aliace == command or aliace in self.aliaces[command]:
                return command
        # это означает, что псевдонима нет
        return aliace
    
    def isActualCommand(self, command):
        # общие команды        
        if command in self.generalCommands:
            return True
        
        # команды по режимам
        if self._mode == HeroShell.MODE_INIT:
            if command in self.initCommands: 
                return True
        
        elif self._mode == HeroShell.MODE_SEARCH:
            if (
                command in self.searchCommands or
                command in self.pageCommands
            ):
                return True   
        
        elif self._mode == HeroShell.MODE_ACCOUNTS:
            if (
                command in self.accountsCommands or
                command in self.pageCommands or
                command in self.toogleCommands
            ):
                return True   
        
        elif self._mode == HeroShell.MODE_ACCOUNT:
            if (
                command in self.accountCommands or
                command in self.toogleCommands
            ) :
                return True   
        
        elif self._mode == HeroShell.MODE_TOON:
            if (
                command in self.toonCommands or
                command in self.toogleCommands
            ) :
                return True   
        
        elif self._mode == HeroShell.MODE_PLAYER:
            if command in self.playerCommands:
                return True   
        
        elif self._mode == HeroShell.MODE_REPLAY:
            if command in self.replayCommands:
                return True   
        
        return False
    
    # рутинная установка и смена рабочего режима
    def switchMode(self, newMode):
        if self._mode == newMode:
            return False
        
        if newMode == HeroShell.MODE_INIT:
            self.prompt = self.PROMPT_INIT_MODE
        
        elif newMode == HeroShell.MODE_SEARCH:
            self.prompt = self.PROMPT_SEARCH_MODE
        
        elif newMode == HeroShell.MODE_ACCOUNTS:    
            self.prompt = self.PROMPT_ACCOUNTS_MODE
       
        elif newMode == HeroShell.MODE_TOON:    
            self.prompt = self.PROMPT_TOOM_MODE
        
        elif newMode == HeroShell.MODE_PLAYER:    
            self.prompt = self.PROMPT_PLAYER_MODE
        
        elif newMode == HeroShell.MODE_REPLAY:    
            self.prompt = self.PROMPT_REPLAY_MODE
        
        
        # прямая установка
        self._mode = newMode
        return True
    
    def pushOldMode(self, newMode, newRepr):
        # добавление в стэк
        item = self._mode, self._lastRepr
        if self.switchMode( newMode ):
            self._lastRepr = newRepr
            self._modeStack.append( item )    
            
    def popOldMode(self):
        if not len( self._modeStack ):
            return False
            
        item = self._modeStack.pop()    
        # проверку успешного переключения переводить не нужно,
        # т.к. уже наполненность последовательности режимов в стэке
        # исключает их повторение, что значит, что откат режима будет уникальным
        # относительно текущего. Исполнение `pushOldMode` уже сделало эту проверку
        self.switchMode( item[0] )
        self._lastRepr = item[1]
        return True
    
    """***************************** 
    "
    "
    "     ОБЛАСТЬ КОМАНД
    "
    "
    *****************************"""
    
    
    def do_exit(self, line):
        """
    Выход из программы 
    (С сохранением результата работы)
    
    :Псевдонимы: x
    :Доступен в режиме: общий(General)
        """
        
        # возможно сохранить состояния
        Config.saveAll()
        sys.exit(0)
        
    def do_search(self, line):
        """
    Поиск игрока
    
    :Псевдонимы команды: s
    :Доступный режим команды: обычный(MODE_INIT)
            
    -i          игнорировать регистр 
    -p          поиск по имени игрока
    -h          поиск по названию  героя [ждет реализации]
    -t          поиск по toon.id [ждет реализации]
    --NA        регион Северной Америки
    --EU        регион Европы
    --AS        регион Азии
    --ptr       realm: включить в поиск тестовый сервер
    --ptr-only  включить в поиск только тестовый сервер 
    
    -t, -p взаимоисключающие параметры
        """
        # 1. выполнение команды
        userStates = Config.getInstance(Config.USER_STATES)
        cmd = Search( 
            CommonReplaySupplyingStrategy( 
                self._replayCreater
              , userStates.get('DISABLED_ACCOUNTS')
              , userStates.get('DISABLED_TOONS')
            ) 
        )
        repr = cmd.exec( *self.parse(self.CMD_SEARCH, line) )
        
        # 2. проверка наличия результата, если параметры неправильные
        if not repr:
            return
        
        # 3. Еще проверка, если вдруг результат нулевой
        if not repr.hasData():
            repr.show()
            return
        
        # 4. Стадия вывода результата и обработка состояния программы
        self.pushOldMode(self.MODE_SEARCH, repr)
        repr.show()
        
    def do_accounts(self, line):
        """
    Вывод списка доступных аккаунтов на устройстве, с возможностью выбора
    какой аккаунт обходить
    
    :Псевдонимы команды: aa
    :Доступный режим команды: MODE_SEARCH, MODE_ACCOUNTS
        """
        cmd = Accounts( CommonStorageSupplyingStrategy() )
        repr = cmd.exec( *self.parse(self.CMD_ACCOUNTS, line) )
        
        self.pushOldMode(self.MODE_ACCOUNTS, repr)
        repr.show()
    
    def do_forward(self, line):
        """
    Следующая набор данных
    
    :Псевдонимы команды: f
    :Доступный режим команды: MODE_SEARCH, MODE_ACCOUNTS
        """
        repr = self._lastRepr
        repr.forward()
        
    def do_back(self, line):
        """
    предыдущая набор данных
    
    :Псевдонимы команды: b
    :Доступный режим команды: MODE_SEARCH, MODE_ACCOUNTS
        """
        repr = self._lastRepr
        repr.back()
        
    def do_first(self, line):
        """
    Задает количество опций на страницу
    
    :Псевдонимы команды: ft
    :Доступный режим команды: MODE_SEARCH, MODE_ACCOUNTS
        """
        args, rest = self.parse(self.CMD_FIRST, line)
        try:
            amount = int(rest[0])
        except:
            print('[ERROR] неверно заданное количество первым аргументом')
            return
        config = Config.getInstance(Config.MAIN)
        if self._mode == self.MODE_SEARCH:
            config.set('PAGE_FIRST_ITEMS_REPR', amount)        
        elif self._mode == self.MODE_ACCOUNTS:
            config.set('ACCOUNTS_FIRST_ITEMS_REPR', amount)        
        else:
            raise Exception(f'Исполнение команды в контексте невалидного режима программы {self._mode}')
        
        repr = self._lastRepr
        repr.first(amount)
        repr.show()
    
    def do_return(self, line):
        """
    Выход из текущего режима
    
    :Доступный режим команды: not MODE_INIT
        """
        # проверка на удачное исполнение
        if not self.popOldMode():
            return 
            
        if self._lastRepr:
            self._lastRepr.show()
    
    def do_at(self, line):
        """
    Переход на позицию опции
    
    :Доступный режим команды: команды со страничной презентацией
        """
        repr = self._lastRepr
        if not repr:
            return
        
        args, rest = self.parse(self.CMD_AT, line)
        
        try:
            index = int(rest[0])
        except:
            return
        
        repr.at(index)
        repr.show()
        
    def do_filter(self, line):
        """
    Фильтрация списка результатов по заданным параметрам
    
    :Псевдонимы команды: fr
    :Доступный режим команды: 
        """
        print('Not implemented')
    
    def do_toogle(self, line):
        """
    Задействовать аккаунт или тун при обычном обходе повторов
        """
        cmd = AccountToonToogler()
 
        if self._mode == self.MODE_ACCOUNTS:
            args, rest = self.parse(self.CMD_TOOGLE, line)
            cmd.toogleByPointer( 
                *self.parse(self.CMD_TOOGLE, line)
              , self._lastRepr.getPagination().getObjectPointer()
            )
        elif self._mode == self.MODE_ACCOUNT:
            cmd.execForAccount( self._lastRepr.getAccount() )
        elif self._mode == self.MODE_TOON:
            cmd.execForToon( self._lastRepr.getToon() )
        self._lastRepr.show()
    
    def do_sort(self, line):
        args, rest = self.parse(self.CMD_SORT, line)
        self._lastRepr.sort(args)
        self._lastRepr.show()
    
    def do_replay(self, line):
        args, rest = self.parse(self.CMD_REPLAY, line)
        pag = self._lastRepr.getPagination()
        if self._mode == self.MODE_SEARCH:
            cmd = ReplayPicker( pag.getResult(), pag.getResultLength() )
        repr = cmd.exec(args, rest)
        if not repr:
            return
        self.pushOldMode(self.MODE_REPLAY, repr)
        repr.show()
        
    def do_player(self, line):
        print('Not implemented')
    
    def do_account(self, line):
        print('Not implemented')
    
#################################    
#
#    STATIC DEF
#    
#################################    

# Псевдонимы команд
HeroShell.aliaces = {
    # general
    HeroShell.CMD_EXIT: ['x'],
    HeroShell.CMD_HELP: ['h'],
    HeroShell.CMD_RETURN: ['r'],
    
    # common mode
    HeroShell.CMD_SEARCH: ['s'],
    HeroShell.CMD_ACCOUNTS: ['aa'],
    HeroShell.CMD_ACCOUNT: ['a'],
    HeroShell.CMD_TOON: ['t'],
    HeroShell.CMD_REPLAY: ['rp'],
    HeroShell.CMD_PLAYER: ['p'],
        
    # paged mode
    HeroShell.CMD_FORWARD: ['f'],
    HeroShell.CMD_FIRST: ['ft'],
    HeroShell.CMD_BACK: ['b'],
    HeroShell.CMD_AT: ['g'],
    
    # switch mode
    HeroShell.CMD_TOOGLE: ['tgl'],
    
    #misc
    HeroShell.CMD_FILTER: ['fr']
}

# Набор комманд по облостям

HeroShell.generalCommands = [ 
    HeroShell.CMD_EXIT,
    HeroShell.CMD_HELP,
    HeroShell.CMD_RETURN
]

HeroShell.initCommands = [ 
    HeroShell.CMD_SEARCH, 
    HeroShell.CMD_ACCOUNTS,
    HeroShell.CMD_PLAYER,
    HeroShell.CMD_REPLAY,
    HeroShell.CMD_TOON
]

HeroShell.searchCommands = [ 
    HeroShell.CMD_FILTER,
    HeroShell.CMD_PLAYER,
    HeroShell.CMD_REPLAY,
    HeroShell.CMD_SORT
]

HeroShell.accountsCommands = [ 
    HeroShell.CMD_ACCOUNT
]

HeroShell.accountCommands = [ 
  
]

HeroShell.pageCommands = [
    HeroShell.CMD_FORWARD, 
    HeroShell.CMD_BACK, 
    HeroShell.CMD_FIRST,
    HeroShell.CMD_AT
]

HeroShell.replayCommands = [ 

]

HeroShell.playerCommands = [ 

]

HeroShell.toogleCommands = [
    HeroShell.CMD_TOOGLE
]
