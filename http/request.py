import requests
import json
import time
token = ""
# 登录并返回Token
def login(name,password):
    params = {"Account":name,
             "Password":password,
             "IsRememberMe":True}
    response = requests.post(url='http://api.nlecloud.com/Users/Login',data=params)
    if response.status_code==200:
        # print(response.json())
        data = json.loads(response.text)
        return data['ResultObj']['AccessToken']
    else: return ""

def get_sensor():
    while True:
        
        data = {"AccessToken":token}
        header = {"Content-Type":"Application/json"}
        response = requests.get( url='http://api.nlecloud.com/Devices/Datas?devIds=716756'
                           ,params=data ,headers=header)
                                                                    
        if response.status_code == 200:
            d = json.loads(response.text)
            a = ["0","0","0"]
            
            for i in range(4):
                if d['ResultObj'][0]['Datas'][i]['ApiTag'] == 'temp':
                    a[0] = d['ResultObj'][0]['Datas'][i]['Value']
                elif d['ResultObj'][0]['Datas'][i]['ApiTag'] == 'hum':
                    a[1] = d['ResultObj'][0]['Datas'][i]['Value']
                elif d['ResultObj'][0]['Datas'][i]['ApiTag'] == 'light':
                    a[2] = d['ResultObj'][0]['Datas'][i]['Value']
                
            print(a)
        time.sleep(3)
    

if __name__ == '__main__':

    token = login("17691115647","hf200080")
    
    get_sensor()

    



