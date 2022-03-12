import time
import qrcode
import requests
import json
import numpy as np

# 登录凭证
Authorization = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTg3MDAwNTA2MyIsImlhdCI6MTY0Njk3NTA2NCwiZXhwIjoxNjQ3NTc5ODY0fQ.oiMl7wVLKEuqgEHE0jQH3_yGWPdk9V18DbmPL6XltTqXsmKvc0kBjCWalvZHzuC17h0nWs8K2MURH4rY-vmNbg"
# 这个sig貌似可有可无
sig = ""
# 支付密码
pwd = ""
# 账户余额(商品价格小于账户余额时自动使用账户余额付款，大于时使用支付宝付款)
amount = '0'

# 单个商品ID 喵喵:'c25a2cb16eac4a38185da2b6aacd514f'
commodityId = ''

# 一类商品ID STIM:'a746be51feeffd2948cbd599213218b9'  胖脸:'5dd2e3a1d7da35558dcf957cd9f64f3a'
commodityCategoryId = 'a746be51feeffd2948cbd599213218b9'

commodityCategoryId_dict = {"STIM": "a746be51feeffd2948cbd599213218b9",
                            "胖脸": "5dd2e3a1d7da35558dcf957cd9f64f3a",
                            "华风少女":"a0d8c5870311ed889ada2874b5ba8785",
                            "虎虎生福": "cfa9cbfcc1fe2d32f339cbe573456458",
                            "苏小妹": "33730097fb8a15a1d6288016bd39ed8b",
                            "CBA": "1cd3f36f741163056f450fe505bfdacf",
                            "仙剑奇侠传": "f1c6fef1fba38dec9749a5b2059942e3",
                            "大熊猫和花": "a47add35a27e980232f48ad1ab48bdb0",
                            "故宫宫苑": "01227f24c9225b5ccfa9b1cedb3571e3",
                            "萌芽熊": "7cfbfb38560d59787c87b27d2cc73ef3",
                            "汤姆猫": "ef8f3d2142d53e580bde61c25fffb672",
                            "敦煌": "9d0822c5c9a9166dbd91497b02850160",
                            "丰子恺": "5a2831f6c7c4962d26ac1ce42a570bc0",
                            "大运会": "069dca8f57c0d8264419d6c3c5ce70cc",
                            "鲁道夫": "91ce94e0b00e2f383e8a7ce396320cc0",
                            "三尺童子": "95799f1c36d335ea8c104c7e1a5841dc",
                            "涂涂猫": "2a5c710ac3223f9722f3a05d97c77933",
                            "捞世界": "9c89a72f59767642ff0019dbf182d8e0"}

commodityId_dict = {'喵喵': 'c25a2cb16eac4a38185da2b6aacd514f',
                    "艾迪": '11397a877704d43d9601c6e02ed23e2d',
                    "绿马": "d75c62aed2efba678efa38bd1a4d3492",
                    "芝麻球": "4a95a81c96d03c13279028755023522c",
                    "团团圆圆": "a310b668e251aaf6506e5c858eb7d274"
                    }

meanprice_dict = {}

# pushplus推送token
token = 'd711ca4aafd44f34b680a32b96286418'
#token = ['788942ad0f734ae88dfd6a3728fc4f0f', 'd711ca4aafd44f34b680a32b96286418','e34699ee2158458ab4d5ae41c40b1656']

# 价格线(低于此价格自动下单)
N = 200

# 刷新等待时间(单位:秒)
wait_time = 1.1


def get_info(id, type):
    url = "https://api.theone.art/market/api/saleRecord/list"
    commodityId = ""
    commodityCategoryId = ""
    if (type == 1):
        commodityCategoryId = id
    else:
        commodityId = id
    payload = json.dumps({
        "authorId": None,
        "chainContract": None,
        "commodityCategoryId": commodityCategoryId,
        "commodityId": commodityId,
        "highPrice": None,
        "lowPrice": None,
        "pageCount": 1,
        "pageSize": 5,
        "seriesWorks": None,
        "seriesWorksId": None,
        "sort": {
            "field": 2,
            "upOrDown": 1
        },
        "statusSell": 1,
        "topicId": None,
        "typeMarket": 2
    })

    headers = {"sig": sig,
               "Authorization": Authorization,
               "referer": "https://theone.art/app",
               "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
               "Content-Type": "application/json;charset=UTF-8",
               "Content-Length": "292",
               "Host": "api.theone.art",
               "Connection": "Keep-Alive",
               "Accept-Encoding": "gzip"
               }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    return response.text


def send_info(message):
    title = "订单通知"
    url = "https://www.pushplus.plus/send"
    data = {
        'topic':'temper',
        'token': token,
        'title': title,
        'content': message,
        'template': 'txt'
    }
    data = json.dumps(data)

    r = requests.post(url, data).text

    if '成功' in r:
        print("推送成功")
    else:
        print(r)
        print("推送失败")


def test():
    while True:
        # time.sleep(wait_time)
        for name in commodityCategoryId_dict.keys():
            time.sleep(wait_time)
            mmlist = get_info(commodityCategoryId_dict.get(name), 1)

            # print(get_info())
            try:
                text = json.loads(mmlist)
            except Exception as r:
                print(r)
                print("---------------------")
                print(text)
                return
            # print(text)
            if '成功' not in text.get('message'):
                return text.get('message')
            global cuowuchishu
            cuowuchishu = 0
            price_arr = []  # 存储价格
            for i in range(5):
                price = float(text.get("data").get("records")[i].get("price"))
                price_arr.append(price)
                sale_id = text.get("data").get("records")[i].get("id")
                time.sleep(0.2)

                print(float(price))

            mean_price = np.mean(price_arr)  # 前五个的均价
            print(name + "均价:" + str(mean_price))
            if (name not in meanprice_dict.keys()):
                meanprice_dict[name] = mean_price
            else:
                before_price = meanprice_dict.get(name)
                if (before_price != 0 and mean_price / before_price > 1.1):
                    message = name + "涨价了,之前均价为" + str(before_price) + "现在均价为" + str(mean_price)
                    print(name + "涨价了,之前均价为" + str(before_price) + "现在均价为" + str(mean_price))
                    meanprice_dict[name] = mean_price
                    send_info(message)
                if (before_price != 0 and mean_price / before_price < 0.85):
                    message = name + "大跌了,之前均价为" + str(before_price) + "现在均价为" + str(mean_price)
                    print(name + "大跌了,之前均价为" + str(before_price) + "现在均价为" + str(mean_price))
                    meanprice_dict[name] = mean_price
                    for i in range(len(token)):
                        send_info(message)
            print('------')

        for name in commodityId_dict.keys():
            time.sleep(wait_time)
            mmlist = get_info(commodityId_dict.get(name), 2)

            # print(get_info())
            text = json.loads(mmlist)
            # print(text)
            if '成功' not in text.get('message'):
                return text.get('message')
            price_arr = []  # 存储价格
            for i in range(5):
                price = float(text.get("data").get("records")[i].get("price"))
                price_arr.append(price)
                sale_id = text.get("data").get("records")[i].get("id")
                time.sleep(0.2)

                print(float(price))

            mean_price = np.mean(price_arr)  # 前五个的均价
            print(name + "均价:" + str(mean_price))
            if (name not in meanprice_dict.keys()):
                meanprice_dict[name] = mean_price
            else:
                before_price = meanprice_dict.get(name)
                if (before_price != 0 and mean_price / before_price > 1.1):
                    message = name + "涨价了,之前均价为" + str(before_price) + "现在均价为" + str(mean_price)
                    print(name + "涨价了,之前均价为" + str(before_price) + "现在均价为" + str(mean_price))
                    meanprice_dict[name] = mean_price
                    send_info(message)
                if (before_price != 0 and mean_price / before_price < 0.85):
                    message = name + "大跌了,之前均价为" + str(before_price) + "现在均价为" + str(mean_price)
                    print(name + "大跌了,之前均价为" + str(before_price) + "现在均价为" + str(mean_price))
                    meanprice_dict[name] = mean_price
                    send_info(message)
            print('------')
        print(list(meanprice_dict.items()))


# 入口
if __name__ == "__main__":
    cuowuchishu = 0  # 记录错误次数
    while True:
        try:
            print(cuowuchishu)
            test()
            print(cuowuchishu)
        except Exception as r:
            cuowuchishu += 1
            if (cuowuchishu <= 3):
                print(r)
                send_info(str(r))
            print("网络错误")
            time.sleep(5)
