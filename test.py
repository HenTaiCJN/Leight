import time
from machine import Timer


def test(_):
    print(111)
    time.sleep(1)


Timer(3).init(period=500, mode=Timer.PERIODIC, callback=test)