import dbops
from leight import led


class char:
    @classmethod
    def display(cls, text):
        d1 = array_ops.array_2d_to_1d(dbops.get_font(text))
        led.led_ctrl_multiple(d1)
