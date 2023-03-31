from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
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


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res[b'data'][b'list'][0]
  return weather['weather'], math.floor(weather['high']), math.floor(weather['low'])

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
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, high, low = get_weather()
data = {
  "date": {
    "value": today.strftime('%Y年%m月%d日')
  },
  "city": {
    "value": city
  },
  "weather":{
    "value":wea,
    "color": get_random_color()
  },
  "highest":{
    "value":high,
    "color": get_random_color()
  },
  "lowest":{
    "value":low,
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
