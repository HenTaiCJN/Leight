"""
不建议对_led类做任何修改
"""
import _thread
import random

import gc
import neopixel
import time
from machine import Pin, PWM, ADC

import dbops

animation = [
    [0 for i in range(64)],
    [0, 0, 0, 1, 1, 0, 0, 0,
     0, 0, 0, 1, 1, 0, 0, 0,
     0, 0, 0, 1, 1, 0, 0, 0,
     1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1,
     0, 0, 0, 1, 1, 0, 0, 0,
     0, 0, 0, 1, 1, 0, 0, 0,
     0, 0, 0, 1, 1, 0, 0, 0
     ],
    [0, 0, 1, 1, 1, 1, 0, 0,
     0, 0, 1, 1, 1, 1, 0, 0,
     1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1,
     0, 0, 1, 1, 1, 1, 0, 0,
     0, 0, 1, 1, 1, 1, 0, 0
     ],
    [1 for i in range(64)]
]
animation2 = [0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 1, 1, 1, 1, 0, 0,
              0, 0, 1, 1, 1, 1, 0, 0,
              0, 0, 1, 1, 1, 1, 0, 0,
              0, 0, 1, 1, 1, 1, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              ]

blink_star_stop = False


def linear_map(x, in_min, in_max, out_min, out_max):
    # Clamp the input value to the input range
    if x < in_min:
        x = in_min
    elif x > in_max:
        x = in_max

    # Perform the linear mapping
    result = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return result


# led的移位控制
class _led:
    def __init__(self):
        self.lightness = PWM(Pin(23, Pin.OUT))
        # 定义引脚数组和LED数组
        Pin_Array = [12, 13, 14, 25, 16, 27, 32, 33, 17, 19, 18]
        self.A = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7']
        self.CP = ['CP0', 'CP1']
        self.DT = ['DT']
        self.Led_Array = [0] * 64

        # 初始化引脚
        self.DT[0] = Pin(Pin_Array[8], Pin.OUT)
        self.CP[0] = Pin(Pin_Array[9], Pin.OUT)
        self.CP[1] = Pin(Pin_Array[10], Pin.OUT)

        for i in range(8):
            self.A[i] = Pin(Pin_Array[i], Pin.OUT)
            self.A[i].value(0)

    def __cp(self):
        self.CP[0].value(0)
        self.CP[0].value(1)
        self.CP[0].value(0)

    # 控制信号CP1
    def __rf(self):
        self.CP[1].value(0)
        self.CP[1].value(1)
        self.CP[1].value(0)

    # 地址选择
    def __ad(self, r: int):
        self.A[r].value(1)
        self.A[r].value(0)

    # 显示LED矩阵
    def __show(self):
        for i in range(8):
            for j in range(8):
                self.DT[0].value(0 if self.Led_Array[i * 8 + 7 - j] else 1)
                self.__cp()
            self.__rf()
            self.__ad(i)

    # 控制单个LED
    def led_ctrl_single(self, x: int, y: int, state: bool):
        self.Led_Array[x * 8 + y] = int(state)
        self.__show()

    # 控制多个LED
    def led_ctrl_multiple(self, args: list):
        for i in range(len(args)):
            self.Led_Array[i] = args[i]
        self.__show()

    """以上方法通过移位寄存器实现对64个弹珠的控制。除非懂得原理且完全理解代码，否则不建议做任何改动"""

    def init(self):  # 终止所有其他线程对灯光的控制
        global blink_star_stop
        blink_star_stop = True  # 停止满天星
        carousel().stop()  # 停止跑马灯

    def animate(self, status):
        if status:
            for i in animation:
                self.led_ctrl_multiple(i)
                time.sleep_ms(50)
        else:
            for i in reversed(animation):
                self.led_ctrl_multiple(i)
                time.sleep_ms(50)
        _thread.exit()

    def on(self):
        self.init()

        _thread.start_new_thread(self.animate, [1])
        dbops.updata('light_status', 1)

    def off(self):
        self.init()

        _thread.start_new_thread(self.animate, [0])
        dbops.updata('light_status', 0)

    def set_lightness(self, num):
        new_num = linear_map(num, 0, 100, 1000, 0)

        self.lightness.duty(int(new_num))

        dbops.updata('lightness', num)

    def up(self):
        self.set_lightness(dbops.get_int('lightness') + 20)

    def down(self):
        self.set_lightness(dbops.get_int('lightness') - 20)

    def blink_star(self):
        while not blink_star_stop:
            d = [0 for i in range(64)]
            for i in range(4):
                for j in range(4):
                    dx, dy = random.randint(0, 1), random.randint(0, 1)
                    d[(i * 2 + dy) * 8 + j * 2 + dx] = 1
            self.set_lightness(random.randint(0, 100))
            self.led_ctrl_multiple(d)
            time.sleep_ms(300)
        _thread.exit()

    def light_mode(self, mode):
        self.init()

        if mode == 0:
            self.led_ctrl_multiple(animation2)
        elif mode == 1:
            self.led_ctrl_multiple(animation[1])
        elif mode == 2:
            global blink_star_stop
            blink_star_stop = False
            _thread.start_new_thread(self.blink_star, [])

    @staticmethod
    def get_lightness():
        return dbops.get_int('lightness')


led = _led()


class _speaker:
    def __init__(self):
        from lib.speaker import speaker
        self.speaker = speaker()

    def tone(self, freq, durl=1000):
        self.speaker.tone(freq, durl)

    def click_tone(self, framename):
        self.speaker.click_tone(framename)


speaker = _speaker()


class carousel:
    def __init__(self):
        from lib.carousel import carousel as merry
        self.merry = merry()

    def loop(self, text, speed):
        self.merry.loop(text, speed)

    def stop(self):
        self.merry.stop()


class ble:
    def __init__(self):
        from lib.ble import CBle
        self.ble = CBle('leight')
        self.ble.start_advertising()


class _rgb:
    def __init__(self):
        p = Pin(22)
        self.n = neopixel.NeoPixel(p, 3)

    def write(self, index, r, g, b):
        for i in index:
            self.n[i] = (r, g, b)
        self.n.write()


rgb = _rgb()


class ldr:
    def __init__(self):
        self.adc = ADC(Pin(34, Pin.IN))
        self.adc.width(ADC.WIDTH_12BIT)
        self.adc.atten(ADC.ATTN_11DB)

    def read(self):
        return self.adc.read()


class hall:
    def __init__(self):
        self.pin = Pin(35, Pin.IN)

    def read(self):
        return self.pin.value()


class radar:
    def __init__(self):
        self.pin = Pin(5, Pin.IN)

    def read(self):
        return self.pin.value()


class char:
    @classmethod
    def display(cls, text):
        from lib.dispchar import char
        char.display(text)
        gc.collect()


class matrix:
    @classmethod
    def display(cls, m):
        led.led_ctrl_multiple(m)


class wifi:
    import lib.wificonnect as wc
    def __init__(self):
        pass

    @classmethod
    def connect(cls, ssid, psd, timeout=10000):
        cls.wc.start()
        cls.wc.connect(ssid, psd, timeout)
        gc.collect()

    @classmethod
    def close(cls):
        cls.wc.close()
        gc.collect()

    @classmethod
    def status(cls):
        cls.wc.status()

    @classmethod
    def info(cls):
        cls.wc.info()


class mqttclient:
    from lib.mqtt import MQTTClient
    def __init__(self):
        pass

    @classmethod
    def connect(cls, server, port, client_id='', user='', psd=''):
        cls.MQTTClient.connect(server=server, port=port, client_id=client_id, user=user, psd=psd)

    @classmethod
    def connected(cls):
        return cls.MQTTClient.connected()

    @classmethod
    def publish(cls, topic, content):
        cls.MQTTClient.publish(topic=topic, content=content)

    @classmethod
    def message(cls, topic):
        return cls.MQTTClient.receive(topic=topic)

    @classmethod
    def received(cls, topic, callback):
        cls.MQTTClient.Received(topic=topic, callback=callback)
