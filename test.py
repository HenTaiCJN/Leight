import btree
import gc

def get_status():
    try:
        f = open("db", "r+b")
    except OSError:
        f = open("db", "w+b")
    db = btree.open(f)

    res = {}

    res['light_status'] = int(db[b'light_status'].decode('utf-8'))
    res['lightness'] = int(db[b'lightness'].decode('utf-8'))
    res['sound_status'] = int(db[b'sound_status'].decode('utf-8'))
    res['mode'] = db[b'mode'].decode('utf-8')

    print(gc.mem_free())
    db.close()
    f.close()

    return res


res = get_status()
print(res)
