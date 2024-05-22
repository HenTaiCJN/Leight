import db
import ws2812
import action
import led1
import time
from machine import Timer,Pin,PWM
import wavetest
import random
pwm = PWM(Pin(23),freq=80000)
'读取用户设置值'
# start_code_state=bool(int(db.read_db(b'start_code_state')[1]))
light_state=bool(int(db.read_db(b'light_state')[1]))
duty=int(db.read_db(b'duty')[1])
sound_state=bool(int(db.read_db(b'sound_state')[1]))
'运行时状态控制'
state={'BT':False,'WIFI':False,'HALL':False,'DisplayMode':0}
x=[[0 for i in range(64)],
   [0,0,0,1,1,0,0,0, 
   0,0,0,1,1,0,0,0,
   0,0,0,1,1,0,0,0,
   1,1,1,1,1,1,1,1,
   1,1,1,1,1,1,1,1,
   0,0,0,1,1,0,0,0,
   0,0,0,1,1,0,0,0,
   0,0,0,1,1,0,0,0
    ],
   [0,0,1,1,1,1,0,0,
   0,0,1,1,1,1,0,0,
   1,1,1,1,1,1,1,1,
   1,1,1,1,1,1,1,1,
   1,1,1,1,1,1,1,1,
   1,1,1,1,1,1,1,1,
   0,0,1,1,1,1,0,0,
   0,0,1,1,1,1,0,0
   ],
   [1 for i in range(64)]]

y1=[0,0,0,0,0,0,0,0,
   0,0,0,0,0,0,0,0,
   0,0,1,1,1,1,0,0,
   0,0,1,1,1,1,0,0,
   0,0,1,1,1,1,0,0,
   0,0,1,1,1,1,0,0,
   0,0,0,0,0,0,0,0,
   0,0,0,0,0,0,0,0,
    ]

start_animation_p1=[]  
def update_state():
    if state['WIFI']:
        ws2812.ws2812_ctl([0,2],0,255,0)
    else:
        ws2812.ws2812_ctl([0,2],0,0,0)
    if state['HALL']:
        ws2812.ws2812_ctl([1],0,255,255)
    else:
        ws2812.ws2812_ctl([1],0,0,255)
'满天星'
def blink_star(self):
    if not state['DisplayMode']==2:
        return
    d=[0 for i in range(64)]
    for i in range(4):
        for j in range(4):
            dx,dy=random.randint(0,1),random.randint(0,1)
            d[(i*2+dy)*8+j*2+dx]=1
    led1.led_ctrl_multiple(d)   
    led1.show()
    time.sleep(0.1)
    for i in range(duty,1000,100):
        pwm.duty(i)
        time.sleep(1/20)
'运行模式改变'
def change_state():
    global duty
    if state['DisplayMode']==0:
        Timer(4).deinit()
        pwm.duty(duty)
        led1.led_ctrl_multiple(x[3])
        led1.show()       
    elif state['DisplayMode']==1:
        Timer(4).deinit()
        pwm.duty(duty)
        led1.led_ctrl_multiple(y1)
        led1.show()      
    else:
        Timer(4).init(period=300, mode=Timer.PERIODIC, callback=blink_star)
    
'触摸事件'
'A单击开灯'
def fAC():
    global light_state
    global duty
    duty=int(db.read_db(b'duty')[1])
    light_state=bool(int(db.read_db(b'light_state')[1]))
    ws2812.ws2812_ctl([1],255,255,255)
    time.sleep(1/10)
    update_state()
    pwm.duty(duty)
    if not light_state:
        animation_player(x,1)
        light_state=True
        db.update_db(b'light_state','1')

'A双击最大亮度'
def fADC():
    global duty
    duty=int(db.read_db(b'duty')[1])
    ws2812.ws2812_ctl([1],255,255,255)
    time.sleep(1/20)
    ws2812.ws2812_ctl([1],0,0,0)
    time.sleep(1/15)
    ws2812.ws2812_ctl([1],255,255,255)
    time.sleep(1/20)
    update_state()
    for i in range(duty//100-1):
        duty-=100
        pwm.duty(duty)
        time.sleep(1/20)
    duty=0
    pwm.duty(duty)
    db.update_db(b'duty',bytes(str(duty),'utf-8'))
'A长按向上切换模式'
def fAH():
    print(state)
    state['DisplayMode']=(state['DisplayMode']+1)%3
    change_state()
'B单击关灯'
def fBC():
    global light_state
    global duty
    duty=int(db.read_db(b'duty')[1])
    light_state=bool(int(db.read_db(b'light_state')[1]))
    ws2812.ws2812_ctl([1],255,255,255)
    time.sleep(1/10)
    update_state()
#     Timer(2).deinit()
    pwm.duty(duty)
    if light_state:
        light_state=False
        animation_player(x,0)
        db.update_db(b'light_state','0')
'B双击最低亮度'
def fBDC():
    global duty
    duty=int(db.read_db(b'duty')[1])
    ws2812.ws2812_ctl([1],255,255,255)
    time.sleep(1/20)
    ws2812.ws2812_ctl([1],0,0,0)
    time.sleep(1/15)
    ws2812.ws2812_ctl([1],255,255,255)
    time.sleep(1/20)
    update_state()
    for i in range(duty,1000,100):
        pwm.duty(i)
        time.sleep(1/20)
    duty=1000
    pwm.duty(duty)
    db.update_db(b'duty',bytes(str(duty),'utf-8'))
'B长按向下切换模式'
def fBH():
    print(state)
    state['DisplayMode']=(state['DisplayMode']-1)%3
    change_state()
'上划提高亮度'
def fUP():
    ws2812.ws2812_ctl([1],255,255,255)
    time.sleep(1/10)
    ws2812.ws2812_ctl([1],0,0,0)
    ws2812.ws2812_ctl([0,2],255,255,255)
    time.sleep(1/10)
    ws2812.ws2812_ctl([0,1,2],0,0,0)
    update_state()
    global duty
    global light_state
    duty=int(db.read_db(b'duty')[1])
    light_state = bool(int(db.read_db(b'light_state')[1]))
    duty-=200
    if duty<0:
        duty=0
    pwm.duty(duty)
    if not light_state:
        animation_player(x,1)
        light_state=True
        db.update_db(b'light_state','1')
    db.update_db(b'duty',bytes(str(duty),'utf-8'))

'下划降低亮度'
def fDOWN():
    ws2812.ws2812_ctl([0,2],255,255,255)
    time.sleep(1/10)
    ws2812.ws2812_ctl([0,2],0,0,0)
    ws2812.ws2812_ctl([1],255,255,255)
    time.sleep(1/10)
    ws2812.ws2812_ctl([0,1,2],0,0,0)
    update_state()
    global duty
    duty=int(db.read_db(b'duty')[1])
    duty+=200
    if duty>1000:
        duty=1000
    pwm.duty(duty)
    db.update_db(b'duty',bytes(str(duty),'utf-8'))
'无极调光'
def brightness_control(brightness:int):
    global duty
    duty=brightness
    pwm.duty(duty)
    db.update_db(b'duty',bytes(str(duty),'utf-8'))
'自动保存回调函数'
def state_save():
#     if not start_code_state==bool(int(db.read_db(b'start_code_state')[1])):
#         db.update_db(b'start_code_state',bytes(str(int(start_code_state)),'utf-8'))
#         print('saving start_code_state')
    if not light_state==bool(int(db.read_db(b'light_state')[1])):
        db.update_db(b'light_state',bytes(str(int(light_state)),'utf-8'))
#         print('saving light_state')
#     elif not sound_state==bool(int(db.read_db(b'sound_state')[1])):
#         db.update_db(b'sound_state',bytes(str(int(sound_state)),'utf-8'))
#         print('saving sound_state')
    elif not duty==int(db.read_db(b'duty')[1]):
        db.update_db(b'duty',bytes(str(duty),'utf-8'))
#         print('saving duty')
'开机动画'
def start_animation():
    if not light_state:
        animation_player(x,0)
    else:
        animation_player(x,0)
        animation_player(x,1)
    for i in range(1000,duty,100):
        pwm.duty(i)
        time.sleep(1/20)
    pwm.duty(duty)
'动画播放'
def animation_player(x,dirc):
    if dirc==1:
        for i in range(len(x)):
            led1.led_ctrl_multiple(x[i])
            led1.show()
            time.sleep(1/10)
    else:
        for i in range(len(x)-1,-1,-1):
            led1.led_ctrl_multiple(x[i])
            led1.show()
            time.sleep(1/10)
'注册触摸回调函数'
action.bind('key_A_click',fAC)
action.bind('key_A_dclick',fADC)
action.bind('key_A_press',fAH)
action.bind('key_B_click',fBC)
action.bind('key_B_dclick',fBDC)
action.bind('key_B_press',fBH)
action.bind('slide_up',fUP)
action.bind('slide_down',fDOWN)
ws2812.ws2812_ctl([1],0,0,16)
'自动保存'
# Timer(3).init(period=5000, mode=Timer.PERIODIC, callback=state_save)
'用一个一次循环防止程序开机时无视延时（无视原因未知可能与MPY开机加载文件顺序有关）'
i=0
while i<1:
    i+=1
    start_animation()
'8.25 15:09'