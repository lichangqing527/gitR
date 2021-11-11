# -*- coding: UTF-8 -*-
# cron: 30 7 * * *
# 项目名称: gitR/temperAutoClock123
import json
import random
import time
import requests
import sys
import os

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)

# 初始化变量
token = ''  # pushplustoken
Authorization = ''

# 变量赋值
if "WX_KEY" in os.environ and os.environ["WX_KEY"]:
    Authorization = 'Bearer ' + os.environ["WX_KEY"]
if "PUSH_PLUS_TOKEN" in os.environ and os.environ["PUSH_PLUS_TOKEN"]:
    token = os.environ["PUSH_PLUS_TOKEN"]

logs = ""

url = 'https://xsgzgl.zxhnzq.com/api/EducationAPI/GetDqXqInfo?isrefresh=true&scode=10410&sccode=1041001'
headers = {'Host': 'xsgzgl.zxhnzq.com', 'Connection': 'keep-alive',
           'Authorization': Authorization,
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
           'content-type': 'application/json', 'env': 'production', 'positionID': '', 'terminal': 'miniprogram',
           'version': '2.0.44', 'Referer': 'https://servicewechat.com/wx91da385bdd520809/145/page-frame.html',
           'Accept-Encoding': 'gzip, deflate, br'}
html = requests.get(url, headers=headers)
html = json.loads(html.text)
xh = html.get("data").get("XueQi")

biztime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
url = 'https://xsgzgl.zxhnzq.com/api/PositionInfo/AddOrEditPosition'
data = {"usercode": "20191799", "xq": xh, "typeid": 5, "remark": "体温打卡", "biztime": biztime, "lat": 28.68202,
        "lng": 115.85794, "address": "江西省南昌市红谷滩区世贸路144号(红谷滩区南昌市人民政府(世贸路))", "province": "江西省", "city": "南昌市",
        "district": "红谷滩区", "street": "世贸路", "scode": "10410", "sccode": "1041001"}
data = json.dumps(data)
html = requests.post(url, headers=headers, data=data)  # 发送获取位置id的请求
html = json.loads(html.text)
positionID = html.get("data")  # positionID
if html.get("code") == 200:
    logs = logs + '位置获取 √ \n'
else:
    logs = logs + '位置获取 × ' + html.get("msg") + '\n'
    print(logs)
    exit(0)

url = 'https://xsgzgl.zxhnzq.com/api/ScancodeRegister/GetMyScanCode?scode=10410&sccode=1041001'
headers = {'Host': 'xsgzgl.zxhnzq.com', 'Connection': 'keep-alive',
           'Authorization': Authorization,
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
           'content-type': 'application/json', 'env': 'production', 'positionID': str(positionID),
           'terminal': 'miniprogram',
           'version': '2.0.44', 'Referer': 'https://servicewechat.com/wx91da385bdd520809/145/page-frame.html',
           'Accept-Encoding': 'gzip, deflate, br'}

html = requests.get(url, headers=headers)
html = json.loads(html.text)
xh = html.get("data").get("student_Dormitory").get("xh")
if html.get("code") == 200:
    logs = logs + '学号获取 √ \n'
else:
    logs = logs + '学号获取 × ' + html.get("msg") + '\n'
    print(logs)
    exit(0)

# 时间格式转换
registerdate = time.time() - 60 * 60 * 8
registerdate = time.strftime(
    "%Y-%m-%dT%H:%M:%S" + "." + str(int(round(registerdate - int(registerdate), 3) * 1000)) + "Z",
    time.localtime(registerdate))

url = 'https://xsgzgl.zxhnzq.com/api/BatchSignin/Add'

bodytemperature = str(round(random.uniform(36.3, 37), 1))  # 随机生成体温
data = {"batchid": 10, "positionid": positionID, "verifystate": 0,
        "health_Student": {"xh": xh, "registerdate": registerdate, "bodytemperature": bodytemperature,
                           "bodystatus": "正常",
                           "bodyabnormalinfo": "无异常", "xsremark": "", "status": 0, "quarantinestate": "无隔离",
                           "quarantineplace": "无", "isverify": 0, "verifytext": "", "iscontractxinguan": "否",
                           "period": 0}, "scode": "10410", "sccode": "1041001"}
data = json.dumps(data)
html = requests.post(url, headers=headers, data=data)  # 发送体温登记请求

html = json.loads(html.text)
if html.get("code") == 200:
    logs = logs + '体温登记 √ '
else:
    logs = logs + '体温登记 × ' + html.get("msg")

title = "体温打卡通知"
url = "http://pushplus.hxtrip.com/send"
data = {
    'token': token,
    'title': title,
    'content': logs,
    'template': ''
}
data = json.dumps(data)
r = requests.post('http://pushplus.hxtrip.com/send', data).text

print(logs)
if '发送消息成功' in r:
    print("推送成功")
else:
    r = requests.post('https://www.pushplus.plus/send', data).text
    if '请求成功' in r:
        print("推送成功")
    else:
        print("推送失败")


