# import json
#
# from ft import font, frameclick, framedown, framepress, framedclick
# import btree
#
# try:
#     f = open("fontdb", "r+b")
# except OSError:
#     f = open("fontdb", "w+b")
#
# db = btree.open(f)
# keys = font.keys()
#
# for i in keys:
#     db[i.encode('utf-8')] = json.dumps(font[i]).encode('utf-8')
# db[b'frameclick'] = json.dumps(frameclick).encode('utf-8')
# db[b'framedown'] = json.dumps(framedown).encode('utf-8')
# db[b'framepress'] = json.dumps(framepress).encode('utf-8')
# db[b'framedclick'] = json.dumps(framedclick).encode('utf-8')
#
# db.flush()
# db.close()
# f.close()
import dbops
import fontdb
print(dbops.get_font('a'))