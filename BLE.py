import machine
from time import sleep_ms
import ubluetooth  # 导入BLE功能模块
import os
import MD5
import ujson
import random
import wificonnect as wc
import sys
import db
import gc
from leight import on,off,duty,light_bright,sound_state,speaker
ble = ubluetooth.BLE()  # 创建BLE设备
ble.active(True)  # 打开BLE

bt_data = {}
filecont = ""

# 创建要使用的UUID
SERVER_1_UUID = ubluetooth.UUID(0x9011)
CHAR_A_UUID = ubluetooth.UUID(0x9012)
CHAR_B_UUID = ubluetooth.UUID(0x9013)

# 创建特性并设置特性的读写权限
CHAR_A = (CHAR_A_UUID, ubluetooth.FLAG_READ | ubluetooth.FLAG_WRITE | ubluetooth.FLAG_NOTIFY,)
CHAR_B = (CHAR_B_UUID, ubluetooth.FLAG_READ | ubluetooth.FLAG_WRITE | ubluetooth.FLAG_NOTIFY,)

SERVER_1 = (SERVER_1_UUID, (CHAR_A, CHAR_B,),)  # 把特性A和特性B放入服务1
SERVICES = (SERVER_1,)  # 把服务1放入服务集和中
((char_a, char_b),) = ble.gatts_register_services(SERVICES)  # 注册服务到gatts

# 设置BLE广播数据并开始广播
num_data = str(random.randint(0, 9999))
while True:
    if len(num_data) >= 4:
        break
    num_data = "0" + num_data
num_data_byter = num_data.encode('utf-8')
print(num_data)
num_data=num_data+" "
db.update_db(b'num_data',bytes(num_data,'utf-8'))
adv_data = b'\x02\x01\x06\x03\x09\x41\x42'
adv_data = adv_data + b'\x05\xFF' + num_data_byter
ble.gap_advertise(100, adv_data=adv_data, resp_data=None, connectable=True)

def split_string(string, length):
    return [string[i:i + length] for i in range(0, len(string), length)]


'''下面的def均为根据type来触发，'''
def wifi_get(char_handle,ble_data):
    global filecont
    try:        
        wc.start()
        scan = wc.scan()
        data_list = []
        for i in scan:
            if i[0] == b'':
                continue
            data_list.append(i[0])
            data_list.append(i[1].hex())
            data_list.append(i[3])
            if len(str(data_list))>530:
                data_list.pop()
                data_list.pop()
                data_list.pop()
                break
        json_data = {"type": "WIFI GET SUCCESS", "msg": data_list}
        new_value = bytearray(ujson.dumps(json_data).encode())
        ble.gatts_write(char_handle, new_value)        
    except:
        json_data = {"type": "WIFI GET BAD"}
        new_value = bytearray(ujson.dumps(json_data).encode())
        ble.gatts_write(char_handle, new_value)
    finally:
        filecont = ''

def wifi_conn(char_handle,ble_data):
    global filecont
    try:
        wc.start()
        ssid = ble_data['ssid']
        password = ble_data['password']

        res = wc.connect(ssid, password)
        new_value = bytearray(ujson.dumps({"type": res}).encode())
        ble.gatts_write(char_handle, new_value)
    except:
        json_data = {"type": "WLAN CONNECT BAD"}
        new_value = bytearray(ujson.dumps(json_data).encode())
        ble.gatts_write(char_handle, new_value)
    finally:
        filecont = ''

def wifi_close(char_handle,ble_data):
    global filecont
    try:
        wc.close()
        new_data = {"type": "WIFI CLOSE SUCCESS"}
        new_value = bytearray(ujson.dumps(new_data).encode())
        ble.gatts_write(char_a, new_value)
    except:
        json_data = {"type": "WIFI CLOSE BAD"}
        new_value = bytearray(ujson.dumps(json_data).encode())
        ble.gatts_write(char_handle, new_value)
    finally:
        filecont = ''

'main1 usercode 0,main2 default code 1'
def set_start_user(char_handle,ble_data):
    global filecont
    try:
        '''
        TODO:开机改为用户程序
        '''
#         os.rename("main.py","main2.py")
#         os.rename("main1.py","main.py")
        if 'main1.py' in os.listdir('/'):
            try:
                os.rename("main.py","main2.py")
                os.rename("main1.py","main.py")
            except:
                json_data = {"type": "SET START USER BAD"}
                new_value = bytearray(ujson.dumps(json_data).encode())
                ble.gatts_write(char_handle, new_value)
            else:          
#                 maincode.start_animation_state=False
                db.update_db(b'start_code_state',b'0')
                new_data = {"type": "SET START USER SUCCESS"}
                new_value = bytearray(ujson.dumps(new_data).encode())
                ble.gatts_write(char_a, new_value)
        elif 'main2.py' in os.listdir('/'):
#             print("It's already in user mode")
#             maincode.start_animation_state=False
            db.update_db(b'start_code_state',b'0')
            new_data = {"type": "SET START USER SUCCESS"}
            new_value = bytearray(ujson.dumps(new_data).encode())
            ble.gatts_write(char_a, new_value)
        else:
#             print('no user code')
#             maincode.start_animation_state=True
            with open("main1.py","w") as file:
                pass
            os.rename("main.py","main2.py")
            os.rename("main1.py","main.py")
            db.update_db(b'start_code_state',b'0')
            new_data = {"type": "SET START USER SUCCESS"}
            new_value = bytearray(ujson.dumps(new_data).encode())
            ble.gatts_write(char_a, new_value)
    except:
        json_data = {"type": "SET START USER BAD"}
        new_value = bytearray(ujson.dumps(json_data).encode())
        ble.gatts_write(char_handle, new_value)
    finally:
        filecont = ''
        
        
def set_start_default(char_handle,ble_data):
    global filecont
    try:
        '''
        TODO:开机改为默认程序
        '''
#         os.rename("main.py","main1.py")
#         os.rename("main2.py","main.py")
        if 'main2.py' in os.listdir('/'):
            try:
                os.rename("main.py","main1.py")
                os.rename("main2.py","main.py")
            except:
                json_data = {"type": "SET START DEFAULT BAD"}
                new_value = bytearray(ujson.dumps(json_data).encode())
                ble.gatts_write(char_handle, new_value)
            else:          
#                 maincode.start_animation_state=True
                db.update_db(b'start_code_state',b'1')
                new_data = {"type": "SET START DEFAULT SUCCESS"}
                new_value = bytearray(ujson.dumps(new_data).encode())
                ble.gatts_write(char_a, new_value)
        elif 'main1.py' in os.listdir('/'):
#             print("It's already in default mode")
#             maincode.start_animation_state=True
            db.update_db(b'start_code_state',b'1')
            new_data = {"type": "SET START DEFAULT SUCCESS"}
            new_value = bytearray(ujson.dumps(new_data).encode())
            ble.gatts_write(char_a, new_value)
        else:
#             print('no default code')
#             maincode.start_animation_state=False
            db.update_db(b'start_code_state',b'0')
            new_data = {"type": "SET START USER BAD"}
            new_value = bytearray(ujson.dumps(new_data).encode())
            ble.gatts_write(char_a, new_value) 
    except:
        json_data = {"type": "SET START DEFAULT BAD"}
        new_value = bytearray(ujson.dumps(json_data).encode())
        ble.gatts_write(char_handle, new_value)
    finally:
        filecont = ''
        

def set_sound_open(char_handle,ble_data):
    global filecont
    try:
        '''
        TODO:开启声音
        '''
        db.update_db(b'sound_state',b'1')
        new_data = {"type": "SET SOUND OPEN SUCCESS"}
        new_value = bytearray(ujson.dumps(new_data).encode())
        ble.gatts_write(char_a, new_value)
    except Exception as e:
        print(e)
        json_data = {"type": "SET SOUND OPEN BAD"}
        new_value = bytearray(ujson.dumps(json_data).encode())
        ble.gatts_write(char_handle, new_value)
    finally:
        filecont = ''
        
        
def set_sound_close(char_handle,ble_data):
    global filecont
    try:
        '''
        TODO:静音
        '''
        db.update_db(b'sound_state',b'0')       
        new_data = {"type": "SET SOUND CLOSE SUCCESS"}
        new_value = bytearray(ujson.dumps(new_data).encode())
        ble.gatts_write(char_a, new_value)
        
    except Exception as e:
        print(e)
        json_data = {"type": "SET SOUND CLOSE BAD"}
        new_value = bytearray(ujson.dumps(json_data).encode())
        ble.gatts_write(char_handle, new_value)
    finally:
        filecont = ''
        
        
def set_led_open(char_handle,ble_data):
    global filecont
    try:
        '''
        TODO:开灯
        '''
        on()
        new_data = {"type": "SET LED OPEN SUCCESS"}
        new_value = bytearray(ujson.dumps(new_data).encode())
        ble.gatts_write(char_a, new_value)
    except:
        json_data = {"type": "SET LED OPEN BAD"}
        new_value = bytearray(ujson.dumps(json_data).encode())
        ble.gatts_write(char_handle, new_value)
    finally:
        filecont = ''


def set_led_close(char_handle,ble_data):
    global filecont
    try:
        '''
        TODO:关灯
        '''        
        off()
        light_state=False
        new_data = {"type": "SET LED CLOSE SUCCESS"}
        new_value = bytearray(ujson.dumps(new_data).encode())
        ble.gatts_write(char_a, new_value)
    except:
        json_data = {"type": "SET LED CLOSE BAD"}
        new_value = bytearray(ujson.dumps(json_data).encode())
        ble.gatts_write(char_handle, new_value)
    finally:
        filecont = ''


def set_led_light(char_handle,ble_data):
    global filecont
    try:
        light=ble_data['light'] #亮度（5-100）
        '''
        TODO:设置亮度
        '''
        light_bright(light)
        duty=light
        new_data = {"type": "SET LED LIGHT SUCCESS"}
        new_value = bytearray(ujson.dumps(new_data).encode())
        ble.gatts_write(char_a, new_value)
    except Exception as e:
        print(e)
        json_data = {"type": "SET LED LIGHT BAD"}
        new_value = bytearray(ujson.dumps(json_data).encode())
        ble.gatts_write(char_handle, new_value)
    finally:
        filecont = ''

'main1 usercode 0,main2 default code 1'
def code_upload(char_handle,ble_data):
    global filecont
    try:
        if MD5.digest(ble_data["code"].encode()) == ble_data["md5"]:
            print(db.read_db(b'start_code_state'))
            if db.read_db(b'start_code_state')[1]==b'1':
                with open("main1.py", "w") as file:
                    file.write(ble_data["code"])
                json_data = {"type": "CODE UPLOAD SUCCESS"}
                new_value = bytearray(ujson.dumps(json_data).encode())
                ble.gatts_write(char_handle, new_value)
            else:
                with open("main.py", "w") as file:
                    file.write(ble_data["code"])
                json_data = {"type": "CODE UPLOAD SUCCESS"}
                new_value = bytearray(ujson.dumps(json_data).encode())
                ble.gatts_write(char_handle, new_value)
            machine.reset()
        else:
            print('code_upload erro')
            ble.gatts_notify(0, char_handle, 'erro')  # 回复erro
    except:
        json_data = {"type": "CODE UPLOAD BAD"}
        new_value = bytearray(ujson.dumps(json_data).encode())
        ble.gatts_write(char_handle, new_value)
    finally:
        filecont = ''

def reset(char_handle,ble_data):
    print('重启')
    machine.reset()

def information_init(char_handle,ble_data):
    global filecont
    try:
        new_data = {"type": "information init",
                    "msg": sys.version,
                    "start_status":bool(int(db.read_db(b'start_code_state')[1])),
                    "sound_status":bool(int(db.read_db(b'sound_state')[1])),
                    "led_status":bool(int(db.read_db(b'light_state')[1])),
                    "light_status":int(db.read_db(b'duty')[1])
                    }
        new_value = bytearray(ujson.dumps(new_data).encode())
        ble.gatts_write(char_a, new_value)
    except Exception as e:
        print(e)
    finally:
        filecont = ''
     
type_dict = {
    "WIFI GET": wifi_get,
    "WIFI CLOSE":wifi_close,
    "WIFI CONN": wifi_conn,
    "SET START USER":set_start_user,
    "SET START DEFAULT":set_start_default,
    "SET SOUND OPEN":set_sound_open,
    "SET SOUND CLOSE":set_sound_close,
    "SET LED OPEN":set_led_open,
    "SET LED CLOSE":set_led_close,
    "SET LED LIGHT":set_led_light,
    "CODE UPLOAD": code_upload,
    "MISSION FINISH":reset,
    "information init":information_init
}

def ble_irq(event, data):  # 蓝牙中断函数
    if event == 1:  # 蓝牙已连接
        global bt_data
        global filecont
        print("BLE 连接成功")
        new_data = {"type": "information init",
                    "msg": sys.version,
                    "start_status":bool(int(db.read_db(b'start_code_state')[1])),
                    "sound_status":bool(int(db.read_db(b'sound_state')[1])),
                    "led_status":bool(int(db.read_db(b'light_state')[1])),
                    "light_status":int(db.read_db(b'duty')[1])
                    }
        new_value = bytearray(ujson.dumps(new_data).encode())
        ble.gatts_write(char_a, new_value)

    elif event == 2:  # 蓝牙断开连接
        print("BLE 断开连接")
        ble.gap_advertise(100, adv_data=adv_data, resp_data=None, connectable=True)
        # print(filecont) #打印消息内容

    elif event == 3:  # 收到数据
        onn_handle, char_handle = data  # 判断是来自那个特性的消息
        buffer = ble.gatts_read(char_handle)  # 读取接收到的消息

        msg = str(buffer, 'utf-8')
        msg_type = ''
        # print(filecont)
        # print(MD5.digest(filecont))
        if msg != "MSG DOWN":
            filecont += msg
        else:
            try:
                ble_data = ujson.loads(filecont)
                msg_type = ble_data['type']
            except:
                filecont = ""
                print('error')
            if msg_type in type_dict:
                code = type_dict[msg_type]
                code(char_handle,ble_data)
            else:
                json_data = {"type": "TYPE NOT FOUND"}
                new_value = bytearray(ujson.dumps(json_data).encode())
                ble.gatts_write(char_handle, new_value)
                filecont=''


import action
ble.irq(ble_irq)
speaker([1000],0.3)
if bool(db.read_db(b'light_state')[1]):
    on()
else:
    off()
gc.collect()