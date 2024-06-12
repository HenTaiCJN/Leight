import dbops
from leight import led
import array_ops
import time


class char:
    @classmethod
    def display(cls, text):
        d1 = array_ops.array_2d_to_1d(dbops.get_font(text))
        time.sleep(1)
        led.led_ctrl_multiple(d1)
