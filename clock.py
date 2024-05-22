from machine import RTC,Timer
import time,ntptime
rtc = RTC()
global date_time
user_fun={}
actions={'timer':[],'alarm':[]}
delay_=0
delay_num=0
alarm_flag=0
def set_callback(action,function,args=None):
    if not action in actions:
        print("%s error!action name must in alarm1,alarm2"%(action))
        return False
    actions[action]=[function]
    return True


'同步时间'
def sync(NTPhost="ntp1.aliyun.com"):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        try:
            ntptime.host=NTPhost
            ntptime.settime()
            (year, month, day, weekday, hours, minutes, seconds, subseconds) = rtc.datetime()
            rtc.datetime((year, month, day, weekday, hours+8, minutes, seconds, subseconds))
        except Exception as e:
            print("同步时间失败",repr(e))
        else:
            print("同步时间成功",time.localtime())
    else:
        print("Please connect to WiFi first")
def now_time():
    return rtc.datetime()[0:7]
# def alarm((h,m,s))
def ticker(action,delay:int=1):
    global delay_
    delay_=delay
    if type(action)==type(alarm):
        set_callback("timer",action)
        try:
            Timer(2).init(period=1000,mode=Timer.PERIODIC,callback=timer_callback)
        except:
            pass
    else:
        print("action must be a function")
def timer_callback(self):
    global delay_num
    global delay_
    global alarm_flag
    fsti=actions['timer']
    fsal=actions['alarm']
    try:
        if delay_num>=delay_:
            fsti[0]()
            delay_num=0
        else:
            delay_num+=1
    except:
        pass
    try:
        if alarm_check() and not alarm_flag==1:
            fsal[0]()
            alarm_flag=1
    except:
        pass
def detimer():
    Timer(2).deinit()
def alarm_check():
    global date_time
    time=rtc.datetime()
    if date_time[0]*3600+date_time[1]*60+date_time[2] <time[4]*3600+time[5]*60+time[6]:
        return True
    else:
        return False
def alarm(datetime,action):
    global date_time
    global alarm_flag
    alarm_flag=0
    date_time=datetime
    if type(action)==type(alarm):
        set_callback("alarm",action)
        try:
            Timer(2).init(period=1000,mode=Timer.PERIODIC,callback=timer_callback)
        except:
            pass
    else:
        print("action must be a function")
    
def myfun():
    print("时间到")