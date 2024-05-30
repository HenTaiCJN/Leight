import gc
import os
from flashbdev import bdev
import btree

try:
    if bdev:
        os.mount(bdev, "/")
except OSError:
    import inisetup

    vfs = inisetup.setup()

if 'db' not in os.listdir('/'):
    try:
        f = open("db", "r+b")
    except OSError:
        f = open("db", "w+b")

    db = btree.open(f)
    db[b'light_status'] = b'1'
    db[b'lightness'] = b'100'
    db[b'sound_status'] = b'1'
    db[b'mode'] = b'defaultmode'
    db[b'ble_code']=b' '
    db.flush()
    db.close()
    f.close()

if 'leight.vi' not in os.listdir('/'):
    with open("leight.vi", "w") as f:
        f.write("leight 2023/8/9 0.1")

if 'defaultmode' not in os.listdir('/') and 'usermode' not in os.listdir('/'):
    with open("defaultmode", "w") as f:
        f.write('')
    with open("default.py", "w") as f:
        f.write('')
    with open("user.py", "w") as f:
        f.write('')

if 'main.py' not in os.listdir('/'):
    with open("main.py", "w") as f:
        f.write(
            "import os\n"
            "import led_init\n"
            "if 'defaultmode' in os.listdir('/'):\n"
            "    import default\n"
            "else:\n"
            "    import user\n"
        )

gc.collect()
