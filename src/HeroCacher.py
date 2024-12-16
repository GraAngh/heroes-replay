from os import path
import json

# @TODO
# Переделать в обычную реализацию, где разбивается по папкам внутри корневой папки кэша
class HeroCacher:
    def __init__(self, dir):
        self._dir = dir
       
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
    
    def replayKey(self, file):
        base =  path.basename( file )
        return path.splitext( base )[0]
    
    # создание пути к файлу хранения кэша
    def makePath(self, sourceFile, subdir):
        key = self.replayKey(sourceFile)
        return path.join(self._dir, subdir, key + '.json')

    # запись кэша
    def write(self, sourceFile, arg, data):
        cacheFile = self.makePath(sourceFile, arg)
        with open(cacheFile, 'w', encoding="utf-8") as f:
            f.write( json.dumps(data, default=HeroCacher.__defaultJsonHandler, indent=4) )

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
                