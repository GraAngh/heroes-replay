#
# ** ЗАДАЧА
#
# Используя пакет heroprotocol извлечь данные о матчах и 
# осуществить поиск матчей по заданным параметрам
#
# ** ВСПОМОГАТЕЛЬНЫЕ ДЕЙСТВИЯ
#
# - информация извлекается в формате json. Можно закешировать её результат или оставить в памяти  
# - 

import sys
from os import path

from src.Config import Config
from src.DataExtracter import DataExtracter
from src.Supplying.ReplayCreater import ReplayCreater
from src.HeroesCacher import HeroesCacher
from src.HeroesShell import HeroesShell

# https://pypi.org/project/colorama/
from colorama import just_fix_windows_console

ROOT_DIR = path.split(__file__)[0]
MAIN_CONFIG_FILE = f'{ROOT_DIR}\config.json'
CACHE_DIR = 'cache'
USER_STATES_FILE = f'%TMP%\heroes-replay-user-states.json'

if __name__ == '__main__':
    try:
        just_fix_windows_console()
        
        config = Config.getInstance( 
            Config.MAIN, 
            MAIN_CONFIG_FILE,
            file_required=True
        )
        config.load()
        config.set( 'CACHE_DIR', path.join( ROOT_DIR, CACHE_DIR) )
        
        userStates = Config.getInstance( 
            Config.USER_STATES, 
            USER_STATES_FILE, 
            Config.F_ALL
        )
        userStates.load(False)
        userStates.initDefaultProps([
            ('DISABLED_ACCOUNTS', {}),
            ('DISABLED_TOONS', {})
        ])
        
        cacher = HeroesCacher( config.get('CACHE_DIR') )
        dataExtracter = DataExtracter(cacher)
        shell = HeroesShell( ReplayCreater( dataExtracter ) )
        config.set('HERO_SHELL', shell)
        
        # запуск
        shell.cmdloop()
    except KeyboardInterrupt as err:
        print(err)
        sys.exit(1)