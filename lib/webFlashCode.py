import os
import time

from machine import reset

import dbops


def code_flash(msg):
    import binascii
    if 'defaultmode' in os.listdir('/'):
        os.remove('/defaultmode')
        with open('usermode', 'w') as f:
            f.write('')
        dbops.updata('mode', 'usermode')

    code = binascii.a2b_base64(msg)
    with open('/user.py', 'w') as f:
        f.write(code.decode('utf-8'))
    time.sleep_ms(50)
    reset()