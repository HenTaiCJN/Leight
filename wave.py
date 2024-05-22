from machine import DAC,Pin
import math
import time
import data
dac=DAC(Pin(26))
#f = wave.open('wuwu_R_01_01~1.wav')
#frame=f.readframes(f.getnframes())
# print(frame)
# frame=[123, 123, 123, 123, 128, 139, 150, 156, 150, 144, 139, 128, 128, 117, 112, 106, 106, 100, 106, 117, 128, 128, 133, 144, 150, 150, 144, 139, 133, 128, 123, 112, 106, 100, 106, 106, 112, 123, 128, 133, 139, 144, 144, 150, 144, 128, 128, 123, 112, 95, 95, 100, 100, 112, 117, 128, 133, 144, 156, 156, 156, 150, 139, 128, 123, 106, 100, 95, 100, 106, 106, 117, 128, 133, 144, 150, 144, 150, 144, 133, 128, 123, 117, 112, 100, 100, 106, 117, 123, 128, 133, 144, 150, 156, 144, 139, 128, 123, 117, 112, 100, 100, 106, 112, 117, 128, 128, 139, 144, 144, 150, 150, 139, 128, 128, 117, 106, 95, 100, 100, 100, 112, 123, 128, 139, 150, 156, 161, 156, 144, 133, 128, 117, 106, 100, 100, 95, 106, 112, 117, 128, 133, 144, 150, 144, 150, 144, 133, 128, 123, 117, 100, 95, 100, 106, 112, 123, 128, 139, 150, 161, 156, 144, 139, 128, 117, 106, 106, 100, 95, 100, 112, 117, 128, 139, 144, 150, 156, 156, 144, 144, 139, 128, 112, 100, 95, 89, 89, 100, 112, 123, 133, 150, 161, 161, 161, 156, 144, 128, 123, 112, 89, 84, 89, 100, 112, 117, 133, 144, 144, 150, 156, 156, 150, 144, 133, 117, 106, 100, 89, 84, 84, 100, 112, 128, 144, 156, 156, 161, 161, 156, 144, 128, 123, 100, 84, 78, 89, 95, 106, 123, 128, 144, 156, 156, 156, 156, 150, 133, 128, 123, 112, 95, 84, 72, 84, 100, 128, 150, 161, 161, 161, 161, 150, 150, 139, 123, 106, 100, 95, 84, 84, 100, 106, 117, 133, 156, 161, 167, 167, 167, 144, 133, 123, 100, 89, 78, 78, 84, 89, 112, 128, 139, 150, 167, 172, 172, 161, 150, 139, 128, 106, 89, 72, 67, 78, 89, 106, 123, 139, 150, 167, 178, 184, 184, 167, 133, 117, 95, 78, 67, 61, 67, 78, 100, 123, 139, 167, 184, 189, 195, 184, 167, 139, 117, 95, 67, 50, 44, 55, 78, 106, 128, 156, 172, 189, 195, 195, 184, 161, 128, 106, 84, 61, 55, 61, 67, 89, 112, 133, 161, 178, 189, 189, 178, 167, 144, 128, 106, 84, 61, 61, 67, 84, 100, 123, 144, 161, 178, 189, 189, 178, 161, 128, 112, 89, 72, 61, 61, 67, 84, 112, 128, 150, 172, 189, 195, 195, 178, 156, 128, 106, 84, 55, 44, 44, 61, 89, 123, 144, 167, 184, 201, 201, 201, 184, 156, 123, 95, 72, 50, 44, 44, 61, 84, 112, 144, 172, 189, 206, 206, 195, 172, 150, 128, 100, 67, 50, 44, 50, 61, 89, 123, 150, 178, 195, 206, 201, 189, 167, 139, 123, 100, 72, 50, 44, 39, 55, 84, 117, 150, 178, 189, 206, 217, 212, 195, 161, 133, 95, 61, 33, 22, 22, 44, 72, 112, 150, 184, 201, 212, 217, 212, 195, 161, 128, 89, 55, 39, 27, 33, 55, 84, 123, 156, 189, 206, 217, 223, 201, 178, 139, 106, 72, 44, 16, 10, 27, 55, 95, 133, 178, 212, 240, 251, 234, 206, 167, 123, 78, 39, 0, 0, 0, 39, 78, 128, 184, 217, 246, 251, 234, 201, 172, 128, 84, 39, 16, 0, 5, 39, 78, 128, 167, 206, 234, 246, 246, 223, 178, 133, 95, 50, 10, 0, 0, 22, 67, 117, 161, 201, 234, 246, 240, 229, 201, 150, 112, 61, 16, 0, 0, 10, 44, 100, 144, 184, 229, 251, 251, 234, 212, 167, 123, 78, 44, 5, 0, 0, 16, 61, 117, 161, 212, 251, 255, 255, 251, 201, 133, 78, 22, 0, 0, 0, 0, 50, 100, 150, 212, 255, 255, 255, 255, 189, 128, 72, 5, 0, 0, 0, 27, 100, 156, 212, 255, 255, 255, 251, 195, 128, 55, 5, 0, 0, 0, 22, 84, 139, 212, 255, 255, 255, 255, 212, 144, 72, 10, 0, 0, 0, 10, 84, 139, 212, 255, 255, 255, 255, 212, 128, 50, 0, 0, 0, 0, 10, 84, 150, 229, 255, 255, 255, 255, 240, 161, 95, 27, 0, 0, 0, 0, 50, 128, 206, 255, 255, 255, 255, 229, 139, 55, 0, 0, 0, 0, 0, 89, 184, 255, 255, 255, 255, 255, 189, 112, 22, 0, 0, 0, 0, 39, 128, 206, 255, 255, 255, 255, 246, 156, 72, 0, 0, 0, 0, 0, 78, 167, 234, 255, 255, 255, 255, 206, 123, 44, 0, 0, 0, 0, 44, 123, 201, 255, 255, 255, 255, 217, 133, 55, 0, 0, 0, 0, 39, 117, 189, 255, 255, 255, 255, 229, 150, 72, 5, 0, 0, 0, 22, 95, 172, 246, 255, 255, 255, 240, 167, 89, 10, 0, 0, 0, 10, 84, 161, 234, 255, 255, 255, 246, 172, 95, 22, 0, 0, 0, 10, 67, 144, 223, 255, 255, 255, 246, 178, 100, 27, 0, 0, 0, 10, 72, 139, 201, 255, 255, 255, 251, 189, 123, 50, 0, 0, 0, 0, 50, 117, 189, 251, 255, 255, 251, 195, 133, 67, 5, 0, 0, 5, 61, 128, 195, 251, 255, 255, 246, 195, 123, 55, 0, 0, 0, 16, 72, 139, 206, 255, 255, 255, 223, 161, 100, 33, 0, 0, 0, 39, 106, 167, 229, 255, 255, 251, 201, 133, 72, 16, 0, 0, 10, 55, 123, 184, 240, 255, 255, 234, 178, 123, 50, 0, 0, 0, 27, 89, 150, 212, 246, 255, 255, 217, 156, 89, 33, 0, 0, 0, 39, 106, 161, 223, 255, 255, 251, 206, 144, 84, 22, 0, 0, 10, 61, 128, 184, 234, 255, 251, 223, 172, 112, 55, 10, 0, 5, 39, 95, 161, 212, 246, 255, 234, 195, 139, 78, 33, 0, 0, 22, 72, 128, 189, 234, 255, 251, 217, 156, 95, 39, 5, 0, 10, 61, 117, 172, 223, 251, 251, 229, 172, 117, 55, 10, 0, 10, 39, 100, 161, 217, 251, 251, 229, 184, 123, 61, 16, 0, 5, 39, 95, 150, 206, 246, 251, 240, 195, 133, 72, 22, 0, 5, 27, 78, 139, 195, 240, 255, 240, 201, 139, 84, 33, 5, 5, 27, 78, 133, 189, 234, 255, 240, 206, 150, 95, 39, 10, 5, 27, 67, 128, 172, 217, 246, 240, 206, 161, 112, 55, 16, 0, 16, 55, 112, 161, 212, 246, 246, 217, 172, 117, 61, 27, 10, 22, 55, 106, 150, 195, 229, 234, 217, 178, 128, 78, 39, 22, 22, 50, 89, 139, 189, 217, 234, 217, 184, 139, 95, 50, 27, 22, 44, 84, 128, 178, 212, 229, 223, 189, 144, 100, 55, 27, 22, 39, 72, 123, 167, 206, 229, 223, 195, 156, 112, 67, 39, 27, 39, 67, 117, 150, 195, 217, 223, 201, 167, 123, 78, 44, 27, 33, 61, 106, 144, 189, 217, 229, 212, 172, 128, 84, 44, 33, 39, 67, 106, 139, 178, 206, 212, 206, 172, 128, 95, 61, 44, 44, 61, 95, 128, 167, 195, 212, 201, 178, 139, 112, 78, 50, 50, 61, 84, 123, 156, 184, 201, 201, 184, 150, 117, 78, 61, 50, 55, 78, 117, 150, 184, 201, 201, 184, 156, 123, 89, 67, 55, 55, 78, 112, 139, 167, 195, 201, 184, 161, 128, 100, 72, 55, 61, 72, 100, 128, 161, 184, 195, 189, 161, 133, 106, 78, 61, 61, 72, 95, 128, 156, 178, 195, 189, 167, 144, 117, 84, 67, 61, 72, 89, 123, 144, 172, 189, 184, 172, 144, 123, 95, 72, 67, 67, 89, 117, 139, 161, 178, 184, 172, 156, 128, 106, 84, 72, 67, 84, 106, 128, 156, 178, 184, 178, 161, 133, 112, 89, 72, 78, 84, 100, 123, 150]
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
def click():
    for i in range(0,len(data.frameclick)):
        dac.write(data.frameclick[i])
        time.sleep_us(int(1000000/6000))
def dclick():
    for i in range(0,len(data.framedclick)):
        dac.write(data.framedclick[i])
        time.sleep_us(int(1000000/6000))
def scrolldown():
    for i in range(0,len(data.framedown)):
        dac.write(data.framedown[i])
        time.sleep_us(int(1000000/8000))
def scrollup():
    for i in range(len(data.framedown)-1,-1,-1):
        dac.write(data.framedown[i])
        time.sleep_us(int(1000000/8000))
def press():
    for i in range(0,len(data.framepress)):
        dac.write(data.framepress[i])
        time.sleep_us(int(1000000/6000))
def speaker(frequency=[2000], duration1=1):
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
