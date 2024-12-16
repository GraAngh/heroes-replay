import src.finders

### Полнота совпадений заданного набора имен на множестве повторов
def namesCompletness(details, names):
    data = {
        'replays': 0,
        'coincidence': {},
        'totalCoincidence': 0
    }
    
    for n in names:
        data['concidence'][n] = 0
    
    for d in details:
        data['replays'] += data['replays']
        if finders.somePlayer( names, d ):
            data['concidence'][ name ] += data['concidence'][ name ]
            data['totalCoincidence'] += data['totalCoincidence']
            
