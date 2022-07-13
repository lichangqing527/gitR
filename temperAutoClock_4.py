# -*- coding: UTF-8 -*-
# Author:Cq
# cron:15 7 * * *
# version:1.1
# Date:2022/07/13 16:18
import json
import random
import time
import requests
import sys
import os


class A:
    def __init__(self):
        # 将环境变量的值加到系统环境变量中
        cur_path = os.path.abspath(os.path.dirname(__file__))
        root_path = os.path.split(cur_path)[0]
        sys.path.append(root_path)

        # token初始化
        self.topic = ''  # pushplus群组编码
        self.token = ''  # pushplus token
        self.Authorizationtmp = ''  # 微信小程序身份凭证
        self.location = ''  # 地址信息
        self.bottoken = ''  # tgbot token
        self.userid = ''  # tgbot userid
        self.logs = ''

    # 获取系统环境变量中的数据并赋值到对应变量中
    def get_tokens(self):
        # 变量赋值
        if "WX_KEY" in os.environ and os.environ["WX_KEY"]:
            self.Authorizationtmp = os.environ["WX_KEY"]
            # 对多个凭证进行切分
            if len(self.Authorizationtmp) != 0:
                self.Authorizationtmp = self.Authorizationtmp.split("&")
                for i in range(len(self.Authorizationtmp)):
                    self.Authorizationtmp[i] = "Bear " + self.Authorizationtmp[i].replace(" ","")
        if "location" in os.environ and os.environ["location"]:
            self.location = os.environ["location"]
            # 对多个位置进行切分
            if len(self.location) != 0:
                self.location = self.location.replace(" ","").split("&")
        if "PUSH_PLUS_TOKEN" in os.environ and os.environ["PUSH_PLUS_TOKEN"]:
            self.token = os.environ["PUSH_PLUS_TOKEN"]
        if "PUSH_PLUS_USER" in os.environ and os.environ["PUSH_PLUS_USER"]:
            self.topic = os.environ["PUSH_PLUS_USER"]
        if "TG_BOT_TOKEN" in os.environ and os.environ["TG_BOT_TOKEN"]:
            self.bottoken = os.environ["TG_BOT_TOKEN"]
        if "TG_USER_ID" in os.environ and os.environ["TG_USER_ID"]:
            self.userid = os.environ["TG_USER_ID"]

    # 根据经纬度随机生成附近位置并获取位置信息  使用腾讯地图的api
    # 获取位置id
    def get_locationInfo(self, token, lat, lng, xh, xq):
        lat = round(random.uniform(float(lat) - 0.0005, float(lat) + 0.0005), 5)
        lng = round(random.uniform(float(lng) - 0.0005, float(lng) + 0.0005), 5)
        url = 'https://apis.map.qq.com/ws/geocoder/v1/?coord_type=5&get_poi=0&output=json&key=JJRBZ-DW2RQ-M2F5M-GDBDP-WEKUZ-RTFE5&location=' + str(
            lat) + '%2C' + str(lng)
        headers = {'Host': 'apis.map.qq.com', 'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
                   'content-type': 'application/json',
                   'Accept-Encoding': 'gzip, deflate, br'}

        html = requests.get(url, headers=headers)
        html = json.loads(html.text)
        address = html.get("result").get("address")
        province = html.get("result").get("address_component").get("province")
        city = html.get("result").get("address_component").get("city")
        district = html.get("result").get("address_component").get("district")
        street = html.get("result").get("address_component").get("street")
        # print(html)
        # print(address + " " + province + " " + city + " " + district + " " + street + " ")

        # 获取小程序内位置id
        biztime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        headers = {'Host': 'xsgzgl.zxhnzq.com', 'Connection': 'keep-alive',
                   'Authorization': token,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
                   'content-type': 'application/json', 'env': 'production', 'positionID': '', 'terminal': 'miniprogram',
                   'version': '2.0.71',
                   'Accept-Encoding': 'gzip, deflate, br'}
        url = 'https://xsgzgl.zxhnzq.com/api/PositionInfo/AddOrEditPosition'
        data = {"usercode": xh, "xq": xq, "typeid": 5, "remark": "体温打卡", "biztime": biztime,
                "lat": lat,
                "lng": lng, "address": address, "province": province, "city": city,
                "district": district, "street": street, "scode": "10410", "sccode": "1041001"}
        data = json.dumps(data)
        html = requests.post(url, headers=headers, data=data)  # 发送获取位置id的请求
        html = json.loads(html.text)
        positionID = html.get("data")  # positionID

        if html.get("code") == 200:
            self.logs = self.logs + '位置获取 √ \n' + 'lat:' + str(lat) + ' lng:' + str(
                lng) + '\n' + address + '\n'
            return positionID
        else:
            self.logs = self.logs + '位置获取 × ' + html.get("msg") + '\n'

            return 0
            # exit(0)

    # 获取学期
    # return 0 异常
    def get_Xq(self, token):
        url = 'https://xsgzgl.zxhnzq.com/api/EducationAPI/GetDqXqInfo?isrefresh=true&scode=10410&sccode=1041001'
        headers = {'Host': 'xsgzgl.zxhnzq.com', 'Connection': 'keep-alive',
                   'Authorization': token,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
                   'content-type': 'application/json', 'env': 'production', 'positionID': '', 'terminal': 'miniprogram',
                   'version': '2.0.71',
                   'Accept-Encoding': 'gzip, deflate, br'}
        html = requests.get(url, headers=headers)
        html = json.loads(html.text)
        if 'XueQi' not in str(html):
            self.logs = self.logs + "异常 " + str(html)
            return 0
        else:
            return html.get("data").get("XueQi")


        # 获取学号
        # return 学号
        # return 0 异常

    def get_Xh(self, token):
        url = 'https://xsgzgl.zxhnzq.com/api/ScancodeRegister/GetMyScanCode?scode=10410&sccode=1041001'
        headers = {'Host': 'xsgzgl.zxhnzq.com', 'Connection': 'keep-alive',
                   'Authorization': token,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
                   'content-type': 'application/json', 'env': 'production',
                   'terminal': 'miniprogram',
                   'version': '2.0.71',
                   'Accept-Encoding': 'gzip, deflate, br'}

        html = requests.get(url, headers=headers)
        html = json.loads(html.text)

        xh = html.get("data").get("xh")
        if html.get("code") == 200:
            self.logs = self.logs + '学号获取 √ ' + xh + '\n'
            return xh
        else:
            self.logs = self.logs + '学号获取 × ' + html.get("msg") + '\n'
            return 0
            # exit(0)

    def get_tempId(self, token):
        url = 'https://zhxgapi.zxhnzq.com/api/Batch/GetBatchList?type=2&name=&scode=10410&sccode=1041001'
        headers = {'Host': 'zhxgapi.zxhnzq.com', 'Connection': 'keep-alive',
                   'Authorization': token,
                   'charset': 'utf-8', 'scode': '10410',
                   'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2012K11AC Build/SKQ1.220213.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3263 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/5452 MicroMessenger/8.0.16.2040(0x2800103B) Process/appbrand0 WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64 MiniProgramEnv/android',
                   'content-type': 'application/json', 'terminal': 'miniprogram',
                   'Accept-Encoding': 'gzip,compress,br,deflate', 'env': 'production', 'version': '2.0.71'}
        html = requests.get(url, headers=headers)
        html = json.loads(html.text)

        if '成功' not in str(html):
            self.logs = self.logs + "异常 " + str(html)
            return 0
        else:
            return html.get("data")[0].get("id")

    ##############################
    def batch_sign(self, xh, positionID, temperId, token):
        # 时间格式转换
        registerdate = time.time() - 60 * 60 * 8
        registerdate = time.strftime(
            "%Y-%m-%dT%H:%M:%S" + "." + str(int(round(registerdate - int(registerdate), 3) * 1000)) + "Z",
            time.localtime(registerdate))

        url = 'https://xsgzgl.zxhnzq.com/api/BatchSignin/Add'

        bodytemperature = str(round(random.uniform(36.3, 37), 1))  # 随机生成体温
        headers = {'Host': 'xsgzgl.zxhnzq.com', 'Connection': 'keep-alive',
                   'Authorization': token,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
                   'content-type': 'application/json', 'env': 'production',
                   'terminal': 'miniprogram',
                   'version': '2.0.71',
                   'Accept-Encoding': 'gzip, deflate, br'}
        data = {"batchid": temperId, "positionid": positionID, "verifystate": 0,
                "health_Student": {"xh": xh, "registerdate": registerdate, "bodytemperature": bodytemperature,
                                   "bodystatus": "正常",
                                   "bodyabnormalinfo": "无异常", "xsremark": "", "status": 0, "quarantinestate": "无隔离",
                                   "quarantineplace": "无", "isverify": 0, "verifytext": "", "iscontractxinguan": "否",
                                   "period": 0}, "scode": "10410", "sccode": "1041001"}
        data = json.dumps(data)
        html = requests.post(url, headers=headers, data=data)  # 发送体温登记请求

        html = json.loads(html.text)
        if html.get("code") == 200:
            self.logs = self.logs + '体温登记 √ \n\n'
        else:
            self.logs = self.logs + '体温登记 × ' + html.get("msg") + '\n\n'
            return 0

    def pushplus(self):
        title = "体温打卡通知"
        url = "http://pushplus.hxtrip.com/send"
        data = {
            'topic': self.topic,
            'token': self.token,
            'title': title,
            'content': self.logs,
            'template': 'txt'
        }
        data = json.dumps(data)

        r = requests.post('http://pushplus.hxtrip.com/send', data).text
        if '发送消息成功' in r:
            print("推送成功")
        else:
            r = requests.post('https://www.pushplus.plus/send', data).text
            if '请求成功' in r:
                print("推送成功")
            else:
                print("推送失败")

    def tg(self):
        telegram_message = f"{self.logs}"

        params = (
            ('chat_id', self.userid),
            ('text', telegram_message),
            ('parse_mode', "html"),  # 可选Html或Markdown
            ('disable_web_page_preview', "yes")
        )

        telegram_url = "https://api.telegram.org/bot" + self.bottoken + "/sendMessage"
        telegram_req = requests.post(telegram_url, params=params)
        telegram_status = telegram_req.status_code

        if telegram_status == 200:
            print("TG推送成功")
        else:
            # print(telegram_req) 出问题再取消注释
            # print(telegram_status)
            print("TG推送失败")

    def send(self):
        self.pushplus()
        if (self.bottoken != "" and self.userid != ""):
            self.tg()
        else:
            print("未填写bottoken和userid , 取消TG推送")
    # 多用户体温登记逻辑
    def run(self):
        flag = 0
        self.get_tokens()
        for i in range(len(self.Authorizationtmp)):

            #位置对应规则:
            #用户数量=位置数量  -->  用户与位置一一对应
            #用户数量<位置数量  -->  n个用户与前n个位置一一对应
            #用户数量>位置数量  -->  n个用户与n个位置一一对应,n以后的用户与第n个位置对应

            weizhi = ""
            if len(self.location) > 1:
                if i > (len(self.location)-1):
                    weizhi = self.location[len(self.location)-1].split(",")
                else:
                    weizhi = self.location[i].split(",")
            else:
                weizhi = self.location[0].split(",")
            Xq = self.get_Xq(self.Authorizationtmp[i])
            if Xq == 0:
                return
            Xh = self.get_Xh(self.Authorizationtmp[i])
            if Xh == 0:
                return
            positionId = self.get_locationInfo( self.Authorizationtmp[i], weizhi[0], weizhi[1], Xh, Xq)
            if positionId == 0:
                return
            temperId = self.get_tempId(self.Authorizationtmp[i])
            if temperId == 0:
                return
            result = self.batch_sign(Xh, positionId, temperId, self.Authorizationtmp[i])
            if result != 0:
                flag += 1
        self.logs = "体温登记编号:" + str(temperId) + "\n" + self.logs
        self.logs = str(flag)+"人成功打卡\n\n" + self.logs
        print(self.logs)
        self.send()


if __name__ == '__main__':
    operate = A()
    operate.run()


