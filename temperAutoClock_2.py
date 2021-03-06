# -*- coding: UTF-8 -*-
# Author:Cq
# cron: 15 16 * * *
# version:1.0
# Date:2022/03/17 17:06
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
topic = ''
token = ''  # pushplustoken
Authorizationtmp = ''
bottoken = ''
userid = ''

# 变量赋值
if "WX_KEY" in os.environ and os.environ["WX_KEY"]:
    Authorizationtmp = os.environ["WX_KEY"]
if "PUSH_PLUS_TOKEN" in os.environ and os.environ["PUSH_PLUS_TOKEN"]:
    token = os.environ["PUSH_PLUS_TOKEN"]
if "PUSH_PLUS_USER" in os.environ and os.environ["PUSH_PLUS_USER"]:
    topic = os.environ["PUSH_PLUS_USER"]
if "TG_BOT_TOKEN" in os.environ and os.environ["TG_BOT_TOKEN"]:
    bottoken = os.environ["TG_BOT_TOKEN"]
if "TG_USER_ID" in os.environ and os.environ["TG_USER_ID"]:
    userid = os.environ["TG_USER_ID"]

topic = ''
if len(Authorizationtmp) != 0:
    Authorizationtmp = Authorizationtmp.split("&")
else:
    Authorizationtmp = ''
logs = "现在是" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"

#龙岗传习教育
#22.704582,114.255385
#22.704389,114.255953

location_lat = []
location_lng = []
# 第一个 罗坑
location_lat.append(round(random.uniform(22.70438, 22.70458), 5))

location_lng.append(round(random.uniform(114.25538, 114.25595), 5))

# 第二个 泰和碧桂园
location_lat.append(round(random.uniform(22.70438, 22.70458), 5))

location_lng.append(round(random.uniform(114.25538, 114.25595), 5))

# 第三个 童家 28.540699,118.075623  28.540447,118.076346
location_lat.append(round(random.uniform(22.70438, 22.70458), 5))

location_lng.append(round(random.uniform(114.25538, 114.25595), 5))

for i in range(len(Authorizationtmp)):
    # time.sleep(random.randint(1, 60))
    Authorization = 'Bearer ' + Authorizationtmp[i]
    lat = location_lat[i]
    lng = location_lng[i]
    url = 'https://apis.map.qq.com/ws/geocoder/v1/?coord_type=5&get_poi=0&output=json&key=JJRBZ-DW2RQ-M2F5M-GDBDP-WEKUZ-RTFE5&location=' + str(
        lat) + '%2C' + str(lng)
    headers = {'Host': 'apis.map.qq.com', 'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
               'content-type': 'application/json',
               'Referer': 'https://servicewechat.com/wx91da385bdd520809/145/page-frame.html',
               'Accept-Encoding': 'gzip, deflate, br'}

    html = requests.get(url, headers=headers)
    html = json.loads(html.text)
    address = html.get("result").get("address")
    province = html.get("result").get("address_component").get("province")
    city = html.get("result").get("address_component").get("city")
    district = html.get("result").get("address_component").get("district")
    street = html.get("result").get("address_component").get("street")

    url = 'https://xsgzgl.zxhnzq.com/api/EducationAPI/GetDqXqInfo?isrefresh=true&scode=10410&sccode=1041001'
    headers = {'Host': 'xsgzgl.zxhnzq.com', 'Connection': 'keep-alive',
               'Authorization': Authorization,
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
               'content-type': 'application/json', 'env': 'production', 'positionID': '', 'terminal': 'miniprogram',
               'version': '2.0.44', 'Referer': 'https://servicewechat.com/wx91da385bdd520809/145/page-frame.html',
               'Accept-Encoding': 'gzip, deflate, br'}
    html = requests.get(url, headers=headers)
    html = json.loads(html.text)
    if 'XueQi' not in str(html):
        logs = logs + "异常 " + str(html)
        continue
    xh = html.get("data").get("XueQi")

    biztime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    url = 'https://xsgzgl.zxhnzq.com/api/PositionInfo/AddOrEditPosition'
    data = {"usercode": "20191799", "xq": xh, "typeid": 5, "remark": "体温打卡", "biztime": biztime, "lat": lat,
            "lng": lng, "address": address, "province": province, "city": city,
            "district": district, "street": street, "scode": "10410", "sccode": "1041001"}
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
    xh = html.get("data").get("xh")
    if html.get("code") == 200:
        logs = logs + '学号获取 √ ' + '****' + xh[-2:] + '\n'
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
    data = {"batchid": 7122, "positionid": positionID, "verifystate": 0,
            "health_Student": {"xh": xh, "registerdate": registerdate, "bodytemperature": bodytemperature,
                               "bodystatus": "正常",
                               "bodyabnormalinfo": "无异常", "xsremark": "", "status": 0, "quarantinestate": "无隔离",
                               "quarantineplace": "无", "isverify": 0, "verifytext": "", "iscontractxinguan": "否",
                               "period": 0}, "scode": "10410", "sccode": "1041001"}
    data = json.dumps(data)
    html = requests.post(url, headers=headers, data=data)  # 发送体温登记请求

    html = json.loads(html.text)
    if html.get("code") == 200:
        logs = logs + '体温登记 √ \n'
    else:
        logs = logs + '体温登记 × ' + html.get("msg") + '\n'

    # 位置参数
    logs = logs + '位置模拟 √ \nlat:' + str(lat) + ' lng:' + str(
        lng) + '\n' + province + city + district + street + '\n\n'

if logs.count("体温登记 √") == 3:
    logs = "√√√已全部完成打卡√√√\n" + logs
else:
    logs = "×××还有" + str(len(Authorizationtmp) - logs.count("体温登记 √")) + "人未打卡×××\n" + logs
title = "体温打卡通知"
url = "http://pushplus.hxtrip.com/send"
data = {
    'topic': topic,
    'token': token,
    'title': title,
    'content': logs,
    'template': 'txt'
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

def post_tg(message):
    telegram_message = f"{message}"

    params = (
        ('chat_id', userid),
        ('text', telegram_message),
        ('parse_mode', "html"), #可选Html或Markdown
        ('disable_web_page_preview', "yes")
    )   

    telegram_url = "https://api.telegram.org/bot" + bottoken + "/sendMessage"
    telegram_req = requests.post(telegram_url, params=params)
    telegram_status = telegram_req.status_code  

    if telegram_status == 200:
        print("TG推送成功")
    else:
        # print(telegram_req) 出问题再取消注释
        # print(telegram_status)
        print("TG推送失败")

if (bottoken != "" and userid != ""):
    post_tg(logs)
else:
    print("未填写bottoken和userid , 取消TG推送")
