import time
from machine import Pin
import machine
from machine import Timer
import os
import ws2812
import wavetest
import BLE_MAC_GET2
import db
# import buzzer
try:
    sound_state=bool(int(db.read_db(b'sound_state')[1]))
except:
    sound_state=True
Touch_Pin1=Pin(4, machine.Pin.IN)
Touch_Pin2=Pin(2, machine.Pin.IN)
actions={'A_click':[],'A_dclick':[],'A_hold':[],
        'B_click':[],'B_dclick':[],'B_hold':[],
        'scroll_up':[],'scroll_down':[]}
que=[["",0],["",0],["",0]]
start_time=time.ticks_ms()
def set_callback(action,function,args=None):
    if not action in actions:
        print("%s error!action name must in A_click,A_dclick,A_hold,B_click,B_dclick,B_hold,scroll_up,scroll_down"%(action))
        return False
    actions[action]=[function]
    return True


'A单击事件'
def t1_click():
    fs=actions['A_click']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.click()
'A双击事件'
def t1_dclick():
    fs=actions['A_dclick']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.dclick()
'A滑动事件'
def t1_scroll():
    fs=actions['scroll_down']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.scrolldown()
'A长按事件'
def t1_longclick():
    fs=actions['A_hold']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.press()

'B单击事件'
def t2_click():
    fs=actions['B_click']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.click()
'B双击事件'
def t2_dclick():
    fs=actions['B_dclick']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.dclick()
'B滑动事件'
def t2_scroll():
    fs=actions['scroll_up']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.scrollup()
'B长按事件'
def t2_longclick():
    fs=actions['B_hold']
    try:
        fs[0]()
    except:
        pass
    if sound_state:
        wavetest.press()
'定时器回调事件'
def clock(self):
    if que[-1][0]=='1d' and time.ticks_ms()-que[-1][1]>2000:
        if Touch_Pin2.value() == 1:
            if (time.ticks_ms()-start_time)<5000:
                print('pairing')
                BLE_MAC_GET2.tim4.init(period=200,mode=Timer.PERIODIC,callback=BLE_MAC_GET2.merry_go_round)
            else:
                pass
#                 ws2812.ws2812_ctl([0,1,2],255,0,0)
#                 if 'main2.py' in os.listdir('/'):
#                     os.rename("main.py","main1.py")
#                     os.rename("main2.py","main.py")
#                     machine.reset()
#                 elif 'main1.py' in os.listdir('/'):
#                     os.rename("main.py","main2.py")
#                     os.rename("main1.py","main.py")
#                     machine.reset()
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
                BLE_MAC_GET2.tim4.init(period=200,mode=Timer.PERIODIC,callback=BLE_MAC_GET2.merry_go_round)
            else:
                pass
#                 ws2812.ws2812_ctl([0,1,2],255,0,0)
#                 if 'main2.py' in os.listdir('/'):
#                     os.rename("main.py","main1.py")
#                     os.rename("main2.py","main.py")
#                     machine.reset()
#                 elif 'main1.py' in os.listdir('/'):
#                     os.rename("main.py","main2.py")
#                     os.rename("main1.py","main.py")
#                     machine.reset()
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


Touch_Pin1.irq(trigger=machine.Pin.IRQ_RISING|machine.Pin.IRQ_FALLING,handler =t1)
Touch_Pin2.irq(trigger=machine.Pin.IRQ_RISING|machine.Pin.IRQ_FALLING,handler =t2)

machine.Timer(1).init(period=100, mode=machine.Timer.PERIODIC, callback=clock)
