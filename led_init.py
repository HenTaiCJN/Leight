import dbops
from button_action import touch
from leight import ble, led, rgb, speaker

touch.action_change("touch1_click", None)  # 占位符，防止import被忽略

# 初始化灯的开关
if int(dbops.get('light_status')):
    led.on()
else:
    led.off()

# 初始化灯的亮度
led.set_lightness(int(dbops.get('lightness')))

# 初始化rgb
rgb.write([0, 2], 0, 0, 0)
if dbops.get('mode') == 'defaultmode':
    rgb.write([1], 0, 0, 255)
else:
    rgb.write([1], 0, 255, 0)

# 开启蓝牙
ble()

speaker.tone([1000], 300)
