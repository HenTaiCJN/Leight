import _thread
import os
import time

from machine import Pin, reset

import dbops
from leight import led, rgb, speaker

powerOnTimeCnt = time.time()
light_mode = -1
event_user = {'touch1_click': None, 'touch1_dclick': None, 'touch1_longClick': None,
              'touch2_click': None, 'touch2_dclick': None, 'touch2_longClick': None,
              'touch1_to_touch2': None, 'touch2_to_touch1': None, 'touch1_and_touch2': None,
              }

"""touch1为B，touch2为A"""


# b单击,关灯
def touch1_click():
    def rgb_change():
        rgb.write([0, 2], 255, 255, 255)
        time.sleep_ms(50)
        rgb.write([0, 2], 0, 0, 0)
        rgb.write([1], 255, 255, 255)
        time.sleep_ms(50)
        rgb.write([0, 1, 2], 0, 0, 0)
        time.sleep_ms(50)
        rgb.write([1], 0, 0, 255)

    speaker.click_tone("frameclick")
    if event_user['touch1_click'] is not None:
        event_user['touch1_click']()
    else:
        _thread.start_new_thread(rgb_change, [])
        time.sleep_ms(10)
        led.off()


# b双击,最小亮度
def touch1_dclick():
    def rgb_change():
        rgb.write([1], 255, 255, 255)
        time.sleep_ms(50)
        rgb.write([1], 0, 0, 0)
        time.sleep_ms(50)
        rgb.write([1], 255, 255, 255)
        time.sleep_ms(50)
        rgb.write([1], 0, 0, 255)

    speaker.click_tone("framedclick")
    if event_user['touch1_dclick'] is not None:
        event_user['touch1_dclick']()
    else:
        _thread.start_new_thread(rgb_change, [])
        time.sleep_ms(10)
        led.set_lightness(0)


# b长按
def touch1_longClick():
    speaker.click_tone("framepress")
    if event_user['touch1_longClick'] is not None:
        event_user['touch1_longClick']()
    else:
        global light_mode
        light_mode += 1
        led.light_mode(light_mode%3)


# a单击,开灯
def touch2_click():
    def rgb_change():
        rgb.write([1], 255, 255, 255)
        time.sleep_ms(50)
        rgb.write([1], 0, 0, 255)

    speaker.click_tone("frameclick")
    if event_user['touch1_click'] is not None:
        event_user['touch1_click']()
    else:
        _thread.start_new_thread(rgb_change, [])
        time.sleep_ms(10)
        led.on()


# a双击,最大亮度
def touch2_dclick():
    def rgb_change():
        rgb.write([1], 255, 255, 255)
        time.sleep_ms(50)
        rgb.write([1], 0, 0, 0)
        time.sleep_ms(50)
        rgb.write([1], 255, 255, 255)
        time.sleep_ms(50)
        rgb.write([1], 0, 0, 255)

    speaker.click_tone("framedclick")
    if event_user['touch1_dclick'] is not None:
        event_user['touch1_dclick']()
    else:
        _thread.start_new_thread(rgb_change, [])
        time.sleep_ms(10)
        led.set_lightness(100)


# a长按
def touch2_longClick():
    speaker.click_tone("framepress")
    if event_user['touch1_longClick'] is not None:
        event_user['touch1_longClick']()
    else:
        global light_mode
        light_mode -= 1
        led.light_mode(light_mode%3)


# 下滑，降低亮度
def touch1_to_touch2():
    def rgb_change():
        rgb.write([0, 2], 255, 255, 255)
        time.sleep_ms(50)
        rgb.write([0, 2], 0, 0, 0)
        rgb.write([1], 255, 255, 255)
        time.sleep_ms(50)
        rgb.write([0, 1, 2], 0, 0, 0)
        time.sleep_ms(50)
        rgb.write([1], 0, 0, 255)

    speaker.click_tone("frameup")
    if event_user['touch1_to_touch2'] is not None:
        event_user['touch1_to_touch2']()
    else:
        _thread.start_new_thread(rgb_change, [])
        time.sleep_ms(10)
        led.down()


# 上划，提高亮度
def touch2_to_touch1():
    def rgb_change():
        rgb.write([1], 255, 255, 255)
        time.sleep_ms(50)
        rgb.write([1], 0, 0, 0)
        rgb.write([0, 2], 255, 255, 255)
        time.sleep_ms(50)
        rgb.write([0, 1, 2], 0, 0, 0)
        time.sleep_ms(50)
        rgb.write([1], 0, 0, 255)

    speaker.click_tone("framedown")
    if event_user['touch2_to_touch1'] is not None:
        event_user['touch2_to_touch1']()
    else:
        _thread.start_new_thread(rgb_change, [])
        time.sleep_ms(10)
        led.up()


# 双长按
def touch1_and_touch2():
    speaker.click_tone("framepress")
    if time.ticks_diff(time.time(), powerOnTimeCnt) < 6:
        led.on()
        led.set_lightness(100)
        from leight import carousel
        carousel().loop(dbops.get('ble_code'), 10)
    else:
        if 'defaultmode' in os.listdir('/'):
            os.remove('defaultmode')
            with open('usermode', 'w') as f:
                f.write('')
            dbops.updata('mode', 'usermode')
        else:
            os.remove('usermode')
            with open('defaultmode', 'w') as f:
                f.write('')
            dbops.updata('mode', 'defaultmode')
        time.sleep(0.5)
        reset()


def ignore():
    pass


class touchEvent:
    def __init__(self):
        self.event = {'touch1_click': touch1_click, 'touch1_dclick': touch1_dclick, 'touch1_longClick': touch1_longClick,
                      'touch2_click': touch2_click, 'touch2_dclick': touch2_dclick, 'touch2_longClick': touch2_longClick,
                      'touch1_to_touch2': touch1_to_touch2, 'touch2_to_touch1': touch2_to_touch1, 'touch1_and_touch2': touch1_and_touch2,
                      'ignore': ignore
                      }

        self.touch1Event = ''
        self.touch2Event = ''
        self.touch1 = Pin(2, Pin.IN)
        self.touch2 = Pin(4, Pin.IN)

        self.touch1.irq(trigger=Pin.IRQ_RISING, handler=self.handleBtnA)
        self.touch2.irq(trigger=Pin.IRQ_RISING, handler=self.handleBtnB)

    def handleBtnA(self, pin):
        # 双击中的第二次点击回调会被第一次中的while延迟到双击事件结束后执行，所以如果上一次为事件为双击，则会额外出发一次单击，这个单击必须忽略
        if self.touch1Event == 'touch1_dclick':
            self.touch1Event = 'ignore'
            return
        # 初始化事件为单击
        self.touch1Event = 'touch1_click'

        had_release = False  # 判断按键是否松开过，用于判断双击
        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < 400:
            if pin.value() == 0:
                had_release = True  # 记录按钮是否松开过
                if self.touch2.value() == 1:
                    self.touch1Event = 'touch1_to_touch2'  # 如果松开过且按下了另一个按钮则为滑动事件
                    break
            if had_release and pin.value() == 1:  # 如果松开过且又点击，判定为双击
                self.touch1Event = 'touch1_dclick'
                break

        if not had_release:
            if self.touch2.value() == 1:
                self.touch1Event = 'touch1_and_touch2'  # 如果从未松开且按键b被按下则判定为双按键长按
            else:
                self.touch1Event = 'touch1_longClick'  # 如果从未松开且按键b没被按下则判定为单按键长按

        if self.touch2Event == 'touch2_to_touch1':  # touch2触发滑动时忽略touch1的事件
            self.touch2Event = 'ignore'
            return

        self.event[self.touch1Event]()

    def handleBtnB(self, pin):
        if self.touch2Event == 'touch2_dclick':
            self.touch2Event = 'ignore'
            return

        self.touch2Event = 'touch2_click'

        had_release = False
        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < 400:
            if pin.value() == 0:
                had_release = True
                if self.touch1.value() == 1:
                    self.touch2Event = 'touch2_to_touch1'
                    break
            if had_release and pin.value() == 1:
                self.touch2Event = 'touch2_dclick'
                break

        if not had_release:
            self.touch2Event = 'touch2_longClick'

        if self.touch2Event == 'touch2_longClick' and self.touch1.value() == 1:
            self.touch2Event = 'ignore'  # 防止双长按重复触发

        if self.touch1Event == 'touch1_to_touch2':
            self.touch1Event = 'ignore'
            return

        self.event[self.touch2Event]()

    @staticmethod
    def action_change(action, func):
        global event_user
        event_user[action] = func


touch = touchEvent()
