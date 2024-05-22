import time
import machine
import os
from machine import Pin
from machine import Timer
import ws2812
import wavetest
import db
# import BLE_MAC_GET2
from leight import sound,hall,key_A,key_B,radar,Scroll,deScroll,on
# import buzzer
try:
    sound_state=bool(int(db.read_db(b'sound_state')[1]))
except:
    sound_state=True
Touch_Pin1=Pin(2, machine.Pin.IN)
Touch_Pin2=Pin(4, machine.Pin.IN)
Hall_Pin=Pin(35, machine.Pin.IN)
Human_Radar=Pin(5, machine.Pin.IN)
actions={'key_A_click':[],'key_A_dclick':[],'key_A_press':[],
        'key_B_click':[],'key_B_dclick':[],'key_B_press':[],
        'slide_up':[],'slide_down':[],'base_on':[],
         'base_off':[],'human_exist':[],'human_unexist':[]}
que=[["",0],["",0],["",0]]
start_time=time.ticks_ms()
def bind(action,function,args=None):
    if not action in actions:
        print("%s error!action name must in A_click,A_dclick,A_hold,B_click,B_dclick,B_hold,scroll_up,scroll_down,Hall_action_approach,Hall_action_aloof,Radar_action_approach,Radar_action_aloof"%(action))
        return False
    actions[action]=[function]
    return True

def unbind(action,args=None):
    if not action in actions:
        print("%s error!action name must in A_click,A_dclick,A_hold,B_click,B_dclick,B_hold,scroll_up,scroll_down,Hall_action_approach,Hall_action_aloof,Radar_action_approach,Radar_action_aloof"%(action))
        return False
    actions[action]=[]
    return True
def myfun():
    print("111")
'A单击事件'
def t1_click():
    fs=actions['key_A_click']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.click()
'A双击事件'
def t1_dclick():
    fs=actions['key_A_dclick']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.dclick()
'A滑动事件'
def t1_scroll():
    fs=actions['slide_down']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.scrolldown()
'A长按事件'
def t1_longclick():
    fs=actions['key_A_press']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.press()

'B单击事件'
def t2_click():
    fs=actions['key_B_click']
    try:
        if bool(db.read_db('pairing')):
            deScroll()
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.click()
'B双击事件'
def t2_dclick():
    fs=actions['key_B_dclick']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.dclick()
'B滑动事件'
def t2_scroll():
    fs=actions['slide_up']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.scrollup()
'B长按事件'
def t2_longclick():
    fs=actions['key_B_press']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.press()


'传感器事件'
def Hall_action_approach():
    fs=actions['base_on']
    try:
        fs[0]()
    except:
        pass
def Hall_action_aloof():
    fs=actions['base_off']
    try:
        fs[0]()
    except:
        pass

def Radar_action_approach():
    fs=actions['human_exist']
    try:
        fs[0]()
    except:
        pass
def Radar_action_aloof():
    fs=actions['human_unexist']
    try:
        fs[0]()
    except:
        pass



'定时器回调事件'
def clock(self):
    if que[-1][0]=='1d' and time.ticks_ms()-que[-1][1]>2000:
        if Touch_Pin2.value() == 1:
            if (time.ticks_ms()-start_time)<5000:
                print('pairing')
                on()
                from BLE import num_data
#                 Scroll(db.read_db(b'num_data')[1].decode())
                Scroll(num_data)
            else:
                if 'main2.py' in os.listdir('/'):
                    ws2812.ws2812_ctl([0, 1, 2], 255, 0, 0)
                    db.update_db(b'start_code_state',b'1')
                    os.rename("main.py","main1.py")
                    os.rename("main2.py","main.py")
                    machine.reset()
                elif 'main1.py' in os.listdir('/'):
                    ws2812.ws2812_ctl([0, 1, 2], 255, 0, 0)
                    db.update_db(b'start_code_state',b'0')
                    os.rename("main.py","main2.py")
                    os.rename("main1.py","main.py")
                    machine.reset()
        else:
            t1_longclick()
        for i in range(3):
            que.pop(0)
            que.append(["",time.ticks_ms()])
    if (que[-3][0]=='1u' and que[-2][0]=='2d' and que[-1][0]=='2u') or (que[-3][0]=='2d' and que[-2][0]=='1u' and que[-1][0]=='2u'):
        if que[-1][1]-que[-3][1]<300:
            t1_scroll()
#             print(que)
            for i in range(3):
                que.pop(0)
                que.append(["",time.ticks_ms()])
    if que[-2][0]=='1d' and que[-1][0]=='1u':
        if 200<que[-1][1]-que[-2][1]<1000:
#             print(que)
            t1_click()
            for i in range(3):
                que.pop(0)
                que.append(["",time.ticks_ms()])
    if que[-3][0]=='1u' and que[-2][0]=='1d' and que[-1][0]=='1u':
        if que[-1][1]-que[-3][1]<300:
#             print(que)
            t1_dclick()
            for i in range(3):
                que.pop(0)
                que.append(["",time.ticks_ms()])
    #---------------------------------------------------------------
    if que[-1][0]=='2d' and time.ticks_ms()-que[-1][1]>2000:
        if Touch_Pin1.value() == 1:
            if (time.ticks_ms()-start_time)<5000:
                print('pairing')
                on()
                from BLE import num_data
#                 Scroll(db.read_db(b'num_data')[1].decode())
                Scroll(num_data)
            else:
                if 'main2.py' in os.listdir('/'):
                    ws2812.ws2812_ctl([0, 1, 2], 255, 0, 0)
                    db.update_db(b'start_code_state',b'1')
                    os.rename("main.py","main1.py")
                    os.rename("main2.py","main.py")
                    machine.reset()
                elif 'main1.py' in os.listdir('/'):
                    ws2812.ws2812_ctl([0, 1, 2], 255, 0, 0)
                    db.update_db(b'start_code_state',b'0')
                    os.rename("main.py","main2.py")
                    os.rename("main1.py","main.py")
                    machine.reset()
        else:
            t2_longclick()
        for i in range(3):
            que.pop(0)
            que.append(["",time.ticks_ms()])
    if (que[-3][0]=='2u' and que[-2][0]=='1d' and que[-1][0]=='1u') or (que[-3][0]=='1d' and que[-2][0]=='2u' and que[-1][0]=='1u'):
        if que[-1][1]-que[-3][1]<300:
            t2_scroll()
#             print(que)
            for i in range(3):
                que.pop(0)
                que.append(["",time.ticks_ms()])
    if que[-2][0]=='2d' and que[-1][0]=='2u':
        if 200<que[-1][1]-que[-2][1]<1000:
#             print(que)
            t2_click()
            for i in range(3):
                que.pop(0)
                que.append(["",time.ticks_ms()])
    if que[-3][0]=='2u' and que[-2][0]=='2d' and que[-1][0]=='2u':
        if que[-1][1]-que[-3][1]<300:
#             print(que)
            t2_dclick()
            for i in range(3):
                que.pop(0)
                que.append(["",time.ticks_ms()])
'A触摸回调事件'
def t1(self):
    global que
    if Touch_Pin1.value() == 1:
        que.pop(0)
        que.append(["1d",time.ticks_ms()])
    else:
        que.pop(0)
        que.append(["1u",time.ticks_ms()])
'B触摸回调事件'  
def t2(self):
    if Touch_Pin2.value() == 1:
        que.pop(0)
        que.append(["2d",time.ticks_ms()])
    else:
        que.pop(0)
        que.append(["2u",time.ticks_ms()])

'霍尔回调事件'
def Hall_irq(self):
    if hall():
        Hall_action_approach()
    else:
        Hall_action_aloof()
'雷达回调事件'
def Radar_irq(self):
    if radar():
        Radar_action_approach()
    else:
        Radar_action_aloof()



Touch_Pin1.irq(trigger=machine.Pin.IRQ_RISING|machine.Pin.IRQ_FALLING,handler =t1)
Touch_Pin2.irq(trigger=machine.Pin.IRQ_RISING|machine.Pin.IRQ_FALLING,handler =t2)
Hall_Pin.irq(trigger=machine.Pin.IRQ_RISING|machine.Pin.IRQ_FALLING,handler =Hall_irq)
Human_Radar.irq(trigger=machine.Pin.IRQ_RISING|machine.Pin.IRQ_FALLING,handler =Radar_irq)

machine.Timer(1).init(period=100, mode=machine.Timer.PERIODIC, callback=clock)
'9.1改'