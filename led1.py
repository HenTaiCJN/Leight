#A0 12 A1 13 A2 14 A3 25 A4 26 A5 27 A6 32 A7 33 DT 17 CP0 19 CP1 18
#12,13,14,25,26,27,32,33,17,19,18
from machine import Pin,ADC,PWM
import time
Pin_Array=[12,13,14,25,16,27,32,33,17,19,18]
A=['A0','A1','A2','A3','A4','A5','A6','A7']
CP=['CP0','CP1']
DT=['DT']
# Light_ADC=ADC(Pin(34))
# Light_ADC.atten(ADC.ATTN_11DB)
# Hall_Pin=Pin(35)
# Touch_Pin1=Pin(4)
# Touch_Pin2=Pin(2)
# Buzzer_Pin=PWM(Pin(15))
Led_Array=[0 for i in range(64)]
CP[0]=Pin(Pin_Array[9],Pin.OUT)
CP[1]=Pin(Pin_Array[10],Pin.OUT)
DT[0]=Pin(Pin_Array[8],Pin.OUT)
for i in range(8):
    A[i]=Pin(Pin_Array[i],Pin.OUT)
    A[i].value(0)
def cp():
    CP[0].value(0)
    CP[0].value(1)
    time.sleep_us(1)
    CP[0].value(0)
def rf():
    CP[1].value(0)
    CP[1].value(1)
    time.sleep_us(1)
    CP[1].value(0)
def ad(r:int):
    A[r].value(0)
    A[r].value(1)
    time.sleep_us(1)
    A[r].value(0)
def show():
    for i in range(8):
        for j in range(8):
            if Led_Array[i*8+7-j]==0:
                DT[0].value(1)
            else:
                DT[0].value(0)
            cp()
        rf()
        ad(i)
def led_ctrl_single(x:int,y:int,state:bool):
    Led_Array[x*8+y]=int(state)
def led_ctrl_multiple(args:list):
    for i in range(len(args)):
        Led_Array[i]=args[i]
# def light_sensor():
# #     return Light_ADC.read_uv()/1000
#     return Light_ADC.read()
# def hall_sensor():
#     return Hall_Pin.value()
# def touch_sensor():
#     return Touch_Pin1.value(),Touch_Pin2.value()
# def buzzer(duty:int):
#     Buzzer_Pin.duty(duty)