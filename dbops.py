import btree


def updata(key, value):
    key = str(key).encode('utf-8')
    value = str(value).encode('utf-8')
    try:
        f = open("db", "r+b")
    except OSError:
        f = open("db", "w+b")
    db = btree.open(f)
    db[key] = value
    db.flush()
    db.close()
    f.close()


def get(key):
    try:
        f = open("db", "r+b")
    except OSError:
        f = open("db", "w+b")

    key = str(key).encode('utf-8')
    db = btree.open(f)
    res = db[key]
    db.close()
    f.close()

    return res.decode('utf-8')


def get_int(key):
    res = get(key)

    return int(res)
