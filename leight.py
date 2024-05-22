import neopixel
import machine
from machine import DAC,Pin,Timer,PWM,ADC
from time import sleep_ms
import math
import time
import data
import led1
import db
import json
import fontdatac
from wavetest import dac
'light Pin'
pwm = PWM(Pin(23, Pin.OUT))
'ws2812 Pin'
p=Pin(22, Pin.OUT)

n = neopixel.NeoPixel(p, 3)
def RGB(num,rgb):
    for i in range(len(num)):
        if num[i]==0:
            num[i]=2
        elif num[i]==2:
            num[i]=0
    if type(rgb)==list:
        for i in num:
            n[i]=(rgb[0],rgb[1],rgb[2])
            n.write()
    elif type(rgb)==str:
        if rgb=="blue":
            for i in num:
                n[i]=(0,0,255)
                n.write()
        elif rgb=="red":
            for i in num:
                n[i]=(255,0,0)
                n.write()
        elif rgb=="green":
            for i in num:
                n[i]=(0,255,0)
                n.write()
        elif rgb=="off":
            for i in num:
                n[i]=(0,0,0)
                n.write()



B0 = 31
C1 = 33
CS1 = 35
D1 = 37
DS1 = 39
E1 = 41
F1 = 44
FS1 = 46
G1 = 49
GS1 = 52
A1 = 55
AS1 = 58
B1 = 62
C2 = 65
CS2 = 69
D2 = 73
DS2 = 78
E2 = 82
F2 = 87
FS2 = 93
G2 = 98
GS2 = 104
A2 = 110
AS2 = 117
B2 = 123
C3 = 131
CS3 = 139
D3 = 147
DS3 = 156
E3 = 165
F3 = 175
FS3 = 185
G3 = 196
GS3 = 208
A3 = 220
AS3 = 233
B3 = 247
C4 = 262
CS4 = 277
D4 = 294
DS4 = 311
E4 = 330
F4 = 349
FS4 = 370
G4 = 392
GS4 = 415
A4 = 440
AS4 = 466
B4 = 494
C5 = 523
CS5 = 554
D5 = 587
DS5 = 622
E5 = 659
F5 = 698
FS5 = 740
G5 = 784
GS5 = 831
A5 = 880
AS5 = 932
B5 = 988
C6 = 1047
CS6 = 1109
D6 = 1175
DS6 = 1245
E6 = 1319
F6 = 1397
FS6 = 1480
G6 = 1568
GS6 = 1661
A6 = 1760
AS6 = 1865
B6 = 1976
C7 = 2093
CS7 = 2217
D7 = 2349
DS7 = 2489
E7 = 2637
F7 = 2794
FS7 = 2960
G7 = 3136
GS7 = 3322
A7 = 3520
AS7 = 3729
B7 = 3951
C8 = 4186
CS8 = 4435
D8 = 4699
DS8 = 4978
def sound_click():
    Pin(15,Pin.OUT,value=0)
    for i in range(0,len(data.frameclick)):
        dac.write(data.frameclick[i])
        time.sleep_us(int(1000000/6000))
    Pin(15,Pin.OUT,value=1)
def sound_dclick():
    Pin(15,Pin.OUT,value=0)
    for i in range(0,len(data.framedclick)):
        dac.write(data.framedclick[i])
        time.sleep_us(int(1000000/6000))
    Pin(15,Pin.OUT,value=1)
def sound_scrolldown():
    Pin(15,Pin.OUT,value=0)
    for i in range(0,len(data.framedown)):
        dac.write(data.framedown[i])
        time.sleep_us(int(1000000/8000))
    Pin(15,Pin.OUT,value=1)
def sound_scrollup():
    Pin(15,Pin.OUT,value=0)
    for i in range(len(data.framedown)-1,-1,-1):
        dac.write(data.framedown[i])
        time.sleep_us(int(1000000/8000))
    Pin(15,Pin.OUT,value=1)
def sound_press():
    Pin(15,Pin.OUT,value=0)
    for i in range(0,len(data.framepress)):
        dac.write(data.framepress[i])
        time.sleep_us(int(1000000/6000))
    Pin(15,Pin.OUT,value=1)
def speaker(frequency=[2000], duration1=1):
    Pin(15,Pin.OUT,value=0)
    duration=duration1
    sample_rate = 6000
    sample_size = int(sample_rate * 0.01)
    data=[]
    for i in range(sample_size):
        value=0
        for j in frequency:
            t = i / sample_rate
            value += int(math.sin(2 * math.pi * j * t) * 127.5 )
        if value>127.5:
            value=127.5
        elif value<-127.5:
            value=-127.5
        value=int(value+127.5)
        data.append(value)
    for i in range(duration//0.01):
        for j in range(len(data)):
            dac.write(data[j])
            time.sleep_us(1000000//6000)
    Pin(15,Pin.OUT,value=1)




'读取用户设置值'
start_animation_state=bool(int(db.read_db(b'start_animation_state')[1]))
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
   1,1,1,1,1,1,1,1,
   1,1,1,1,1,1,1,1,
   1,1,1,1,1,1,1,1,
   1,1,1,1,1,1,1,1,
   0,0,0,0,0,0,0,0,
   0,0,0,0,0,0,0,0,
    ]
'开灯'
def on():
    global light_state
    global duty
    light_state=bool(int(db.read_db(b'light_state')[1]))
    duty=int(db.read_db(b'duty')[1])
    time.sleep(1/10)
    pwm.duty(duty)
    if not light_state:
        animation_player(x,1)
        light_state=True
        db.update_db(b'light_state','1')
'关灯'    
def off():
    global light_state
    global duty
    light_state=bool(int(db.read_db(b'light_state')[1]))
    duty=int(db.read_db(b'duty')[1])
    time.sleep(1/10)
    pwm.duty(duty)
    if light_state:
        light_state=False
        animation_player(x,0)
        db.update_db(b'light_state','0')
'调高亮度'
def up():
    global duty
    duty=int(db.read_db(b'duty')[1])
    duty-=200
    if duty<0:
        duty=0
    pwm.duty(duty)
    db.update_db(b'duty',bytes(str(duty),'utf-8'))
'调低亮度'
def down():
    global duty
    duty=int(db.read_db(b'duty')[1])
    duty+=200
    if duty>1000:
        duty=1023
    pwm.duty(duty)
    db.update_db(b'duty',bytes(str(duty),'utf-8'))
'无极调光'
def light_bright(brightness:int=-1):
    if brightness<0 or brightness>100:
        if brightness<0 and brightness!=-1:
            brightness=0
        elif brightness>100:
            brightness=100
    if brightness>=0 and brightness<=100:
        global duty
        duty=(100-brightness)*10
        pwm.duty(duty)
    elif brightness==-1:
        return (100-duty//10)
    db.update_db(b'duty',bytes(str(duty),'utf-8'))
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





tim4 = Timer(4)
cnt=0
font_ditc={'1':fontdatac.one,'2':fontdatac.two,'3':fontdatac.three,'4':fontdatac.four,'5':fontdatac.five,
          '6':fontdatac.six,'7':fontdatac.seven,'8':fontdatac.eight,'9':fontdatac.nine,'0':fontdatac.zero,
          'A':fontdatac.A,'B':fontdatac.B,'C':fontdatac.C,'D':fontdatac.D,'E':fontdatac.E,
          'F':fontdatac.F,'G':fontdatac.G,'H':fontdatac.H,'I':fontdatac.I,'J':fontdatac.J,
          'K':fontdatac.K,'L':fontdatac.L,'M':fontdatac.M,'N':fontdatac.N,'O':fontdatac.O,
          'P':fontdatac.P,'Q':fontdatac.Q,'R':fontdatac.R,'S':fontdatac.S,'T':fontdatac.T,
          'U':fontdatac.U,'V':fontdatac.V,'W':fontdatac.W,'X':fontdatac.X,'Y':fontdatac.Y,
          'Z':fontdatac.Z,' ':fontdatac.block0,'a':fontdatac.a,'b':fontdatac.b,'c':fontdatac.c,
          'd':fontdatac.d,'e':fontdatac.e,'f':fontdatac.f,'g':fontdatac.g,'h':fontdatac.h,
          'i':fontdatac.i,'j':fontdatac.j,'k':fontdatac.k,'l':fontdatac.l,'m':fontdatac.m,
          'n':fontdatac.n,'o':fontdatac.o,'p':fontdatac.p,'q':fontdatac.q,'r':fontdatac.r,
          's':fontdatac.s,'t':fontdatac.t,'u':fontdatac.u,'v':fontdatac.v,'w':fontdatac.w,
          'x':fontdatac.x,'y':fontdatac.y,'z':fontdatac.z,'@':fontdatac.xiao,'#':fontdatac.ku,'$':fontdatac.ai,
          '%':fontdatac.feng,'^':fontdatac.cat,'&':fontdatac.dog,
          }

display_list = [0] * 64
col = 0
ndata="1234567890"
# 组合并返回偏移一列后的64长度一维数组
def move_left(ori_list, shift_list):
    for r in range(8):
        for c in range(7):
            ori_list[c + r * 8] = ori_list[c + r * 8 + 1]
        ori_list[7 + r * 8] = shift_list[r]
    return ori_list
def display_num(ndata):
    global code
    num_data=ndata
    num_list=[]
    '根据传入字符串组合列表'
    for i in num_data:
        num_list.extend(font_dit[i])
    code=num_list
'跑马灯主函数'
def memery_go(self):
    global col
    global display_list
    # 判断在第几个数组
    cnt = int(col / 8) % len(ndata)
    cntcol=col-cnt*8
    shift_list = []
    # 取出要插入的列
#     a=json.loads(db.read_db(ndata[cnt])[1])
    a=font_ditc[ndata[cnt]]
#     print(cnt)
    for i in range(8):
        shift_list.append(a[i+i*7+cntcol])
    col += 1
    # 获取下一刻要展示的64长度一维数组
    display_list = move_left(display_list, shift_list)
    # print数组，实际使用时直接吧display_list给函数
    led1.led_ctrl_multiple(display_list)
    led1.show()
    if col>=len(ndata)*8:
        col=0

def DispChar(char:str):
    if len(char)==1:
        if char in font_ditc:
            led1.led_ctrl_multiple(font_ditc[char])
            led1.show()
        else:
            print("char '"+char+"' non-existent")
    else:
        print("The type must be a char with a length of one and not another")
def DispMat(lis:list):
    if len(lis)<65:
        led1.led_ctrl_multiple(lis)
        led1.show()
    else:
        print("The list length must be less than 65")
def Scroll(char:str,speed:int=9):
    checknum=0
    global ndata
    for i in char:
        if i in font_ditc:
            checknum+=1
        else:
            print("char '"+i+"' non-existent")
    if checknum==len(char):
        if speed>0 and speed<11:
            ndata=char
            tim4.init(period=(11-speed)*100,mode=Timer.PERIODIC,callback=memery_go)
        else:
            print("The speed must be within the range of 1-10")
def deScroll():
    tim4.deinit()
def DispClear(state=0):
    if state==0:
        led1.led_ctrl_multiple([0 for i in range(64)])
        led1.show()
    elif state==1:
        led1.led_ctrl_multiple([1 for i in range(64)])
        led1.show()
    else:
        pass




Light_ADC=ADC(Pin(34, machine.Pin.IN))
Light_ADC.atten(ADC.ATTN_11DB)
Sound_Pin=Pin(21, machine.Pin.IN)
Hall_Pin=Pin(35, machine.Pin.IN)
Human_Radar=Pin(5, machine.Pin.IN)
Touch_Pin1=Pin(4, machine.Pin.IN)
Touch_Pin2=Pin(2, machine.Pin.IN)

def brightness():
    return Light_ADC.read()
def sound():
    return bool(Sound_Pin.value())
def hall():
    return bool(Hall_Pin.value())
def key_A():
    return bool(Touch_Pin1.value())
def key_B():
    return bool(Touch_Pin2.value())
def radar():
    return bool(Human_Radar.value())
'9.5修改'
