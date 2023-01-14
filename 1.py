# -*- coding: UTF-8 -*-
import requests as req
import json,sys,time
import random
import datetime,pytz
#先注册azure应用,确保应用有以下权限:
#files:	Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
#user:	User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
#mail:  Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
#注册后一定要再点代表xxx授予管理员同意,否则outlook api无法调用






path=sys.path[0]+r'/1.txt'
num1=0

api_list = [
    r'https://graph.microsoft.com/v1.0/me/drive/root',
    r'https://graph.microsoft.com/v1.0/me/drive',
    r'https://graph.microsoft.com/v1.0/drive/root',
    r'https://graph.microsoft.com/v1.0/users',
    r'https://graph.microsoft.com/v1.0/me/messages',
    r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
    r'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
    r'https://graph.microsoft.com/v1.0/me/drive/root/children',
    r'https://graph.microsoft.com/v1.0/me/mailFolders',
    r'https://graph.microsoft.com/v1.0/me/outlook/masterCategories'
]

def gettoken(refresh_token):
    headers={'Content-Type':'application/x-www-form-urlencoded'
            }
    data={'grant_type': 'refresh_token',
          'refresh_token': refresh_token,
          'client_id':id,
          'client_secret':secret,
          'redirect_uri':'http://localhost:53682/'
         }
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token',data=data,headers=headers)
    jsontxt = json.loads(html.text)
    refresh_token = jsontxt['refresh_token']
    access_token = jsontxt['access_token']
    with open(path, 'w+') as f:
        f.write(refresh_token)
    return access_token
def main():
    fo = open(path, "r+")
    refresh_token = fo.read()
    fo.close()
    global num1
    localtime = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
    access_token=gettoken(refresh_token)
    headers={
    'Authorization':access_token,
    'Content-Type':'application/json'
    }
    
    random.shuffle(api_list)  # 执行洗牌算法，使得每次相邻调用的顺序不一致

    try:
        for api_url in api_list:
            time.sleep(random.randrange(2, 15))
            if req.get(api_url, headers=headers).status_code == 200:
                print("调用成功: ", api_url)
            else:
                print("调用异常: ", api_url)
        num1++
        print('第'+str(num1)+'次运行结束时间为: ', localtime)
    except:
        print("调用出现异常，pass")
        pass

for _ in range(random.randrange(2, 6)):
    time.sleep(10 * random.randrange(1, 8))
    main()

