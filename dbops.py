import json

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
    key = str(key).encode('utf-8')

    try:
        f = open("db", "r+b")
    except OSError:
        f = open("db", "w+b")

    db = btree.open(f)
    res = db[key]
    db.close()
    f.close()

    return res.decode('utf-8')


def get_int(key):
    res = get(key)

    return int(res)


def get_font(key):
    key = str(key).encode('utf-8')

    try:
        f = open("font/fontdb", "rb")
    except OSError:
        f = open("font/fontdb", "wb")

    db = btree.open(f)
    res = db[key]
    db.close()
    f.close()

    return json.loads(res.decode('utf-8'))
