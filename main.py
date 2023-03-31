from datetime import date, datetime
from time import time, localtime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
from requests import get, post
import cityinfo
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday_she = os.environ['BIRTHDAY_SHE']
birthday_he = os.environ['BIRTHDAY_HE']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id_1 = os.environ["USER_ID_1"]
user_id_2 = os.environ["USER_ID_2"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather(city="成都", province="四川"):
    # 城市id    
    city_id = cityinfo.cityInfo[province][city]["AREAID"]  
    # city_id = 101280101
    # 毫秒级时间戳
    t = (int(round(time() * 1000)))
    headers = {
        "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    response_json = eval(response_data)
    # print(response_json)
    weatherinfo = response_json["weatherinfo"]
    # 天气
    weather = weatherinfo["weather"]
    # 最高气温
    temp = weatherinfo["temp"]
    # 最低气温
    tempn = weatherinfo["tempn"]
    return weather, temp, tempn

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday(who):
  if who:                        
    next = datetime.strptime(str(date.today().year) + "-" + birthday_she, "%Y-%m-%d")
  else:
    next = datetime.strptime(str(date.today().year) + "-" + birthday_he, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weather_, max_temperature, min_temperature = get_weather(city="成都", province="四川")
data = {
  "date": {
    "value": today.strftime('%Y年%m月%d日')
  },
  "city": {
    "value": city
  },
  "weather":{
    "value":weather_,
    "color": get_random_color()
  },
  "highest":{
    "value":max_temperature,
    "color": get_random_color()
  },
  "lowest":{
    "value":min_temperature,
    "color": get_random_color()
  },
  "love_days":{
    "value":get_count(),
    "color": get_random_color()
  },
  "birthday_she":{
    "value":get_birthday(True)
  },
  "birthday_he":{
    "value":get_birthday(False)
  },
  "words":{
    "value":get_words(), 
    "color":get_random_color()
  }
}
res_1 = wm.send_template(user_id_1, template_id, data)
print(res_1)
res_2 = wm.send_template(user_id_2, template_id, data)
print(res_2)
