from os import path
from pathlib import Path
import json


class HeroesCacher:
    # default json handler callback 
    @classmethod
    def __defaultJsonHandler(obj):
        try:
            if type( obj ) is bytes:
                return obj.decode('utf-8')    
            return obj
        except:
            if type( obj ) is bytes:
                return obj.hex()
            return None
    
    def __init__(self, cacheRootdir):
        self.__cacheRootDir = cacheRootdir
        if not Path(cacheRootdir).is_dir():
            raise FileNotFoundError(cacheRootdir)
    
    def getReplayName(self, file):
        base =  path.basename( file )
        return path.splitext( base )[0]
    
    # создание пути к файлу хранения кэша
    def makePath(self, sourceFile, subdir):
        replayName = self.getReplayName(sourceFile)
        return path.join(self.__cacheRootDir, subdir, replayName + '.json')

    # запись кэша
    def write(self, sourceFile, arg, data):
        cacheFile = self.makePath(sourceFile, arg)
        with open(cacheFile, 'w', encoding="utf-8") as f:
            f.write( json.dumps(data, default=HeroesCacher.__defaultJsonHandler, indent=4) )

    # чтение кэша
    def read(self, sourceFile, arg):
        cacheFile = self.makePath(sourceFile, arg)
        f = None
        try:
            f = open(cacheFile, 'r', encoding = "utf-8")
            data = f.read()
            return json.loads(data)
        except FileNotFoundError as err:
            return None
        finally:
            if f != None:
                f.close()
    
    # есть необходимость создать директории для отедльынх команд динамически
    # актуально только для первично пустой корневой директории кэша
    def prepareDir(self, name):
        try:
            Path(f'{self.__cacheRootDir}/{name}').mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            pass