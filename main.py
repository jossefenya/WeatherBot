import telebot
import requests
import const
import json
from time import sleep
import datetime
from bot import Bot

token = const.token
bot = Bot(token)
now = datetime.datetime.now()

def main():
    hour = now.hour

    while True:

        answer = bot.getMessage()
        if answer != None:
            data = bot.getWeather()
            chat_id = answer["chat_id"]
            text = answer["text"]

            if hour % 3 == 0:
                bot.sendMessage(chat_id, "Текущая температура - " + str(int(data["temp"]["now_temp"])) + "°С\n"
                            + "Состояние неба - " + str(data["weather"] + "\n")
                            + "Скорость ветра - " + str(data["wind"]) + "м/с\n"
                            + "Текущая дата и время прогноза - " + str(data["date"] + "\n"))
        else:
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
