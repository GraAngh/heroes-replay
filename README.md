# heroes-replay

Local  command-line **Blizzard/Heroes of the Storm** replays observer

## Requirements

- python 3.10 

## Install

Depends on submodule [GraAngh/heroprotocol](https://github.com/GraAngh/heroprotocol.git)

```bash
git clone --recurse-submodules <url>
```

or

```bash
git clone <url>
cd heroes-replay
./bin/setup-heroprotocol.bat
```

## Runing
```bash
python ./cli.py
```
or  
```bash
./bin/heroes-replay.bat
```

## Configuration

By default replays traversed in `%USERPROFILE%\\Documents\\Heroes of the Storm`.
If you have other dir with the same structure of tree by default inside, 
just add path in array for property `HERO_USERS_DATA_DIRS` in `config.josn` in file at root of repo:
```
"HERO_USERS_DATA_DIRS": [
    "%USERPROFILE%\\Documents\\Heroes of the Storm",
    "E:\\Games\\Heroes of the Storm\\UsersData",
    "C:\\OtherHOTSData"
 ],
```

## Using

*TODO: description, commands, how to use*

``` 
Commands:
    
    search [-p <regpattern_name>] [-i] 
        
        Description: поиск игрока по заданным параметрам.
        Alias: s 
        
        s -i -p player  Выдаст список повторов для игрока name
                        и переведет оболочку в режим serach
                        
    player
    
    replay
    
    accounts
    
    return
    
    exit
    
    help