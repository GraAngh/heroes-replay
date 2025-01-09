import json
import os
from pathlib import Path
import sys

class Config:
    # Некоторые преодпределенные имена для экземпляра кофигураций
    # передаваемые в фабричный метод
    MAIN = 'MAIN'
    USER_STATES = 'USER_STATES'
    
    # on file action permissions
    F_WRITE  = 0b1
    F_DELETE = 0b10
    F_ALL = 0b11
    
    _instancesHub = {}
    
    @staticmethod
    def getInstance(name, *args, **kw):
        if name not in Config._instancesHub:
            Config._instancesHub[name] = Config(*args, **kw)
        return Config._instancesHub[name]
    
    @staticmethod
    def saveAll():
        for name in Config._instancesHub:
            Config._instancesHub[name].save()
    
    def __init__(self, file, f_permissions = 0, *, file_required = False):
        self.__config = {}
        self.__f_permissions = f_permissions
        self.__file_required = file_required
        self.__file = self.__expandvars( file )
        
    def load(self, f_expand = True):
        has_loaded = False
        try:        
            with open( self.__file, 'r', encoding="utf-8" ) as f:
                conf = json.load( f )
                has_loaded = True
            for p in conf:
                self.set(p, conf[p], f_expand)
        except FileNotFoundError as e:
            print(f"{e}", file=sys.stderr)
        except json.decoder.JSONDecodeError as e:
            print(f"{self.__file}\n{e}", file=sys.stderr)
            self.__deleteFile()
        finally:
            if not has_loaded and self.__file_required:
                print("[INFO] Обязательный файл")
                sys.exit(1)
        
    def save(self):
        if self.__f_permissions & Config.F_WRITE:
            with open( self.__file, 'w', encoding="utf-8" ) as f:
                json.dump(self.__config, f)
                    
    def __deleteFile(self):
        if self.__f_permissions & Config.F_DELETE:  
            print('[SHELL] Удаление файла')
            Path(self.__file).unlink()
            
    """ 
    Предварительная обработка значений перед установкой
    Основное назначение: разрешение подстановочных параметров окружения
    """
    def __expandvars(self, v):
        if type(v) is str:
            return os.path.expandvars(v)
        
        if type(v) is list:
            result = []
            for it in v:
                result.append( self.__expandvars( it ) )
            return result
            
        if type(v) is dict:
            result = {}
            for prop in v:
                result[prop] = self.__expandvars( v[prop] )
            return result
            
        return v
        
    def set(self, p, v, f_expand = False ):
        if f_expand:
            self.__config[p] = self.__expandvars(v)
        else:
            self.__config[p] = v
        
    def get(self, p):
        if p in self.__config:
            return self.__config[p]
        return None
        
    def initDefaultProps(self, items, f_expand = False):
        for item in items:
            if item[0] not in self.__config:
                self.set( item[0], item[1], f_expand )
    