# main.py
import time
import network
from machine import Timer
from umqtt.robust import MQTTClient#导入同目录下的umqttrobust.py文件

clientID = "ESP32"	#连接ID
server = "192.168.1.126"	#MQTT服务器地址
port = 1883	#MQTT服务器端口号
userName = "admin"	#MQTT登录用户名
passWord = "admin"	#MQTT登录密码
keepAlive = 60	#心跳周期
wifiSSID = "renplus"	#WIFI SSID
wifiPassWord = "lh123456"	#WIFI密码
subTopic = "esp32sub"	#订阅的主题
pubTopic = "esp32pub"	#发布的主题
num = 0
msg_=""
actions={'subCallBack':[]}
def set_callback(action,function,args=None):
    if not action in actions:
        print("%s error!action name must in subCallBack"%(action))
        return False
    actions[action]=[function]
    return True

def msg_test(msg):
    if msg=='hello':
        print('mission success')
'连接WLAN'
def wifiConnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("开始连接...")
        wlan.connect(wifiSSID, wifiPassWord)
        i = 1
        while not wlan.isconnected():
            print("正在连接中...".format(i))
            i += 1
            time.sleep(1)
    print("网络信息为：", wlan.ifconfig())
 
 
 
'订阅主题回调函数及用户回调函数 收到消息时在此处理'
def subCallBack(subTopic, msg):
    global num
    global msg_
    fs=actions['subCallBack']
    print(subTopic.decode('utf-8','ignore'), msg.decode('utf-8','ignore'))
    num=num+1
    msg_=msg.decode('utf-8','ignore')
    mqtt.publish(pubTopic,str(num)+'  copy that')	#推送消息至发布的主题
    try:
        fs[0](msg_)
    except:
        print('function erro')
        pass
'启动mqtt'
def mqtt_run():
    global mqtt
    wifiConnect()
    mqtt = MQTTClient(clientID,server,port,userName,passWord,keepAlive)
    mqtt.set_callback(subCallBack)
    mqtt.connect()
    mqtt.subscribe(subTopic)
    print("订阅成功")
'周期函数回调'
def mqtt_(self):
    global mqtt
    mqtt.check_msg()
'周期性接收mqtt订阅' 
def mqtt_periodic(period_=1000):
    Timer(3).init(period=period_, mode=Timer.PERIODIC, callback=mqtt_)
'从旧到新依次接收一次mqtt订阅队列内的消息' 
def mqtt_oneshot():
    global mqtt
    mqtt.check_msg()
'暂停自动接收mqtt订阅'
def mqtt_suspend():
    Timer(3).deinit()
