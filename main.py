import telebot
import requests
import const
import json
from time import sleep
from datetime import datetime

global last_update_id
last_update_id = 0
token = const.token
URL = "https://api.telegram.org/bot" + token + "/"

def getUpdates():
    url = URL + "getupdates"
    r = requests.get(url)
    return r.json()

def getMessage():
    data = getUpdates()
    update_id = data["result"][-1]["update_id"]

    global last_update_id
    if last_update_id != update_id:
        last_update_id = update_id
        text = data["result"][-1]["message"]["text"]
        chat_id = data["result"][-1]["message"]["chat"]["id"]

        message = {"chat_id" : chat_id,
               "text" : text}
        return message
    else:
        return None


def sendMessage(chat_id, text="..."):
    url = URL + "sendmessage?chat_id={}&text={}".format(str(chat_id), text)
    requests.get(url)


def getWeather():
    url = "http://api.openweathermap.org/data/2.5/forecast?id=515012&APPID=b9504d6840b98ed4f7a3ce397358d42b"
    url_json = requests.get(url).json()
    now_temp = url_json["list"][0]["main"]["temp"] - 273
    weather = url_json["list"][0]["weather"][0]["description"]
    wind = url_json["list"][1]["wind"]["speed"]
    date = url_json["list"][0]["dt_txt"]

    message = {"temp" :
                   {"now_temp" : now_temp},
               "weather" : weather,
               "wind" : wind,
               "date" : date
               }
    return message

def main():
    while True:
        answer = getMessage()
        if answer != None:
            data = getWeather()
            chat_id = answer["chat_id"]
            text = answer["text"]

            if "Погода" or "погода" in text:
                sendMessage(chat_id, "Текущая температура - " + str(int(data["temp"]["now_temp"])) + "°С\n"
                            + "Состояние неба - " + str(data["weather"] + "\n")
                            + "Скорость ветра - " + str(data["wind"]) + "м/с\n"
                            + "Текущая дата и время прогноза - " + str(data["date"] + "\n"))
        else:
            continue

if __name__ == "__main__":
    main()
