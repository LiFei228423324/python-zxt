import socket
from threading import Thread
from time import sleep,ctime
import json
import random
import time

# 发送请求连接消息
def conn():
    connect = {"t":1,"device":"shebiojioaf","key":"50b59e4f68474056abc49908642c779a","ver":"v1.1"}
    skt.send(bytes(json.dumps(connect),encoding="utf8"))
  
is_connect = False
# 

msgid = 1000
def send_data():
    while True:
        time.sleep(3)
        global msgid
        temp = random.randint(-40,60)
        hum = random.randint(0,100)
        light = random.randint(0,10000)
        msgid = msgid + 1
        data = {"t":3,"datatype":1,"datas":{"temp":str(temp),"hum":str(hum),"light":str(light)},"msgid":msgid}
        skt.send(bytes(json.dumps(data),encoding="utf8"))
        print(data)


def _recv_data():
    data = json.loads(skt.recv(1024))
    if data['t']==2: 
        print(data)
        print("连接成功")
        is_connect=True
    while is_connect==True:
        data = json.loads(skt.recv(1024))
        print(data)
        if data['t']==3:
            print("数据上报成功")
        elif data['t']==5:
            if data['data'] == 1:
                print("on")
            elif data['data'] == 0:
                print("off")
        

if __name__ == '__main__':
    url = ("121.37.241.174",8600)
    global skt
    skt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    skt.connect(url)
    
    conn() 


    t = Thread(target=_recv_data)
    t2 = Thread(target=send_data)
    t.start()
    t2.start()
    
    
    

    

    


    




