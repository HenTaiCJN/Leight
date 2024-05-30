import random

import bluetooth
import struct

import dbops

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


# 添加服务


class CBle:

    def __init__(self, name):
        self.name = name
        ble.gatts_register_services((service,))
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
            conn_handle, _, _ = data
            print("Connected")
        elif event == 2:  # Central disconnected
            conn_handle, _, _ = data
            print("Disconnected")
            # 断开连接后重新开始广播
            self.start_advertising()
