import umqtt_simple as mqtt
from machine import Timer
class MQTTClient:
    
    msg_list={}
    
    def __init__(self):
        pass
        
    @classmethod
    def connect(self,server,port,client_id,user='',password=''):
        self.client = mqtt.MQTTClient(client_id=client_id, server=server, port=port, user=user, password=password,keepalive=60)
        self.client.connect()
        if self.client:
            print('mqtt服务器连接成功')
            self.client.set_callback(self.callback)            
            Timer(4).init(period=1000, mode=Timer.PERIODIC, callback=self.check_msg)
        else:
            print('连接失败，请检查wifi是否开启')
            
    @classmethod
    def connected(self):
        if self.client:
            return True        
        return False    
            
    @classmethod
    def disconnect(self):
        if self.client:
            self.client.disconnect()
            
    @classmethod
    def publish(self, topic, message):
        if self.client:
            self.client.publish(topic, message)
            print('推送成功')
            
    @classmethod
    def subscribe(self, topic):
        if self.client:
            self.client.subscribe(topic)
            print('订阅成功')
            
    @classmethod
    def check_msg(self,a):
        MQTTClient.msg_list={}
        if self.client:
            self.client.ping()
            self.client.check_msg()
            
    @classmethod
    def callback(self,topic,msg):
        topic=topic.decode('utf-8')
        msg=msg.decode('utf-8')
        MQTTClient.msg_list[topic]=msg
        self.callback_func()
        
    @classmethod
    def receive(self,topic):
        msg=MQTTClient.msg_list.get(topic,None)
        return msg
    
    @classmethod
    def Received(self,topic,callback):
        if self.client:            
            self.client.subscribe(topic)
            self.callback_func=callback
