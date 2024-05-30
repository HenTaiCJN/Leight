import _thread
import time


def thread1():
    while 1:
        print(11)
        time.sleep(1)


def thread2(t_id):
    i = 0
    while i < 5:
        i += 1
        time.sleep(1)
    _thread.exit()


a = _thread.start_new_thread(thread1, [])
_thread.start_new_thread(thread2, [])

while 1:
    time.sleep(1)
