import _thread
import math
import time

import gc
from machine import Pin, DAC

import dbops


class speaker:
    def __init__(self):
        Pin(15, Pin.OUT, value=0)
        self.dac = DAC(Pin(26))
        self.dac.write(0)

    def tone(self, freq, durl=150, duty=512):
        Pin(15, Pin.OUT, value=0)
        sample_rate = 6000  # 采样率
        sample_size = int(sample_rate * (durl or 1000) / 1000)  # 根据持续时间计算采样点数
        data = bytearray(sample_size)  # 用于存储声音数据的字节数组
        for f in freq:
            for i in range(sample_size):
                t = i / sample_rate
                data[i] += int(127.5 * math.sin(2 * math.pi * f * t))

        for i in range(sample_size):
            self.dac.write(data[i])  # 写入 DAC 输出
            time.sleep_us(int(1000000 / sample_rate))
        self.dac.write(0)
        Pin(15, Pin.OUT, value=1)
        gc.collect()

    def click_tone(self, framename):
        if not dbops.get_int('sound_status'):
            return
        _thread.start_new_thread(self.tone_thread, [framename])

    def tone_thread(self, framename):
        if framename == "frameup":
            frame = dbops.get_font("framedown")
        else:
            frame = dbops.get_font(framename)
        Pin(15, Pin.OUT, value=0)

        if framename == "frameup":
            for i in range(len(frame) - 1, -1, -1):
                self.dac.write(frame[i])
                time.sleep_us(int(1000000 / 8000))
        else:
            for i in frame:
                self.dac.write(i)
                time.sleep_us(int(1000000 / 6000))

        self.dac.write(0)
        Pin(15, Pin.OUT, value=1)
        gc.collect()
        _thread.exit()
