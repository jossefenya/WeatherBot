import telebot
import requests
import json

global last_update_id
last_update_id = 0

class Bot:


    def __init__(self, token):
        self.token = token
        self.URL = "https://api.telegram.org/bot" + token + "/"


    def getUpdates(self):
        url = self.URL + "getupdates"
        r = requests.get(url)
        return r.json()


    def getMessage(self):
        data = Bot.getUpdates(self)
        update_id = data["result"][-1]["update_id"]

        global last_update_id
        if last_update_id != update_id:
            last_update_id = update_id
            text = data["result"][-1]["message"]["text"]
            chat_id = data["result"][-1]["message"]["chat"]["id"]
            name = data["result"][-1]["message"]["chat"]["first_name"]

            message = {"chat_id": chat_id,
                       "text": text,
                       "name" : name}
            return message
        else:
            return None


    def sendMessage(self, chat_id, text="..."):
        url = self.URL + "sendmessage?chat_id={}&text={}".format(str(chat_id), text)
        requests.get(url)


    def getWeather(self):
        url = "http://api.openweathermap.org/data/2.5/forecast?id=515012&APPID=b9504d6840b98ed4f7a3ce397358d42b"
        url_json = requests.get(url).json()
        now_temp = url_json["list"][0]["main"]["temp"] - 273
        weather = url_json["list"][0]["weather"][0]["description"]
        wind = url_json["list"][1]["wind"]["speed"]
        date = url_json["list"][0]["dt_txt"]

        message = {"temp":
                       {"now_temp": now_temp},
                   "weather": weather,
                   "wind": wind,
                   "date": date
                   }
        return message