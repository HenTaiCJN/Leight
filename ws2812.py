import neopixel
from machine import Pin

p=Pin(22)
n = neopixel.NeoPixel(p, 3)
# # Draw a red gradient.
# n[0] = (255, 0, 0)
# n[1] = (0, 255, 0)
# n[2] = (0, 0, 255)
# # Update the strip.
# n.write()
def ws2812_ctl(num,r,g,b):
    for i in num:
        n[i]=(r,g,b)
        n.write()
ws2812_ctl([0,1,2],0,0,0)
