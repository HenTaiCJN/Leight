import _thread
import json
import os
import random
import sys
import time

import bluetooth
from machine import reset, Pin

import dbops
from leight import led

# 初始化蓝牙
ble = bluetooth.BLE()
ble.active(True)
# 定义广播间隔

# 定义厂家数据
MANUFACTURER_DATA = b'\x01\x02\x03\x04'

# 定义服务和特征
SERVICE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
CHARACTERISTIC_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")
service = (
    SERVICE_UUID,
    (
        (CHARACTERISTIC_UUID, bluetooth.FLAG_READ | bluetooth.FLAG_WRITE | bluetooth.FLAG_NOTIFY),
    ),
)


class CBle:

    def __init__(self, name):
        self.name = name
        self.conn_handle = None
        self.cache = ''
        ((self.handle,),) = ble.gatts_register_services((service,))
        self.event = {"info_get": self.info_get, "light_set": self.light_set, "lightness_set": self.lightness_set,
                      "sound_set": self.sound_set, "code_flash": self.code_flash,"cmdInterface": self.cmdInterface,
                      }

        ble.irq(self.bt_irq)

    def start_advertising(self):
        name = self.name
        random_number = str(random.randint(0, 9999))
        cst_data = '{:0>4}'.format(random_number)
        dbops.updata('ble_code', cst_data)
        print('ble connect code:', cst_data)
        adv_data = bytearray(b'\x02\x01\x06')  # 广播包：Flags
        adv_data += bytearray((len(name) + 1, 0x09)) + name.encode()  # 广播包：Complete Local Name
        adv_data += bytearray((len(cst_data) + 1, 0xFF)) + cst_data.encode()  # 广播包：Manufacturer Specific Data

        ble.gap_advertise(100, adv_data=adv_data, resp_data=None, connectable=True)
        print("Advertising...")

    def bt_irq(self, event, data):
        if event == 1:  # Central connected
            self.conn_handle, _, _ = data
            print("Connected")
        elif event == 2:  # Central disconnected
            print("Disconnected")
            # 断开连接后重新开始广播
            self.start_advertising()
        elif event == 3:  # GATT characteristic write
            conn_handle, attr_handle = data[:2]
            value = ble.gatts_read(attr_handle)
            temp = value.decode('utf-8')
            if temp == '%%##end##%%':
                try:
                    data = json.loads(self.cache)
                    print(data)
                except:
                    print('Incorrect json format')
                    return
                type_code = data.get("type", None)
                if type_code is not None and type_code in self.event.keys():
                    print('11111')
                    _thread.start_new_thread(self.event[type_code], [data.get("msg", None)])
                    print('22222')
                    self.cache = ''
            else:
                self.cache += temp

    def send_notification(self, msg):
        ble.gatts_notify(self.conn_handle, self.handle, msg)
        print("Notification sent:", msg)

    def info_get(self, msg):
        res = dbops.get_status()
        new_data = {"type": "info_get_notify", "system": sys.version,
                    "light_status": res.get("light_status", ""),
                    "lightness": res.get("lightness", ""),
                    "sound_status": res.get("sound_status", ""),
                    "mode": res.get("mode", ""),
                    }
        ble.gatts_notify(self.conn_handle, self.handle, json.dumps(new_data).encode('utf-8'))

    @staticmethod
    def cmdInterface(msg):
        exec(msg)

    @staticmethod
    def light_set(msg):
        print('3333')
        if msg == "on":
            print('4444')
            led.on()
            print('5555')
        else:
            led.off()

    @staticmethod
    def lightness_set(msg):
        led.set_lightness(int(msg))

    @staticmethod
    def sound_set(msg):
        dbops.updata('sound_status', int(msg))

    @staticmethod
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

    @staticmethod
    def hall_status(msg):
        Pin(35, Pin.IN).value()