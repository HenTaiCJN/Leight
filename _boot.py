import gc
import uos
import inisetup
from flashbdev import bdev

try:
    if bdev:
        uos.mount(bdev, "/")
except OSError:
    import inisetup

    vfs = inisetup.setup()

gc.collect()
with open("boot.py", "w") as f:
         f.write(
             """\
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import machine
machine.freq(240000000)
import BLE
 """
         )
f.close()
if 'main.py' not in uos.listdir('/'):
    try:
        uos.remove("main1.py")
        uos.remove("main2.py")
    except:
        pass
    with open("main.py", "w") as f1:
         f1.write(
             """\
import maincode
"""
         )
    f1.close()
    with open("main1.py","w") as f2:
        f2.write("""\
#User code
"""
        )
    f2.close()
if 'leight.vi' not in uos.listdir('/'):
    try:
        with open("leight.vi", "w") as f3:
            f3.write("leight 2023/8/9 0.1")
        f3.close()
    except:
        pass