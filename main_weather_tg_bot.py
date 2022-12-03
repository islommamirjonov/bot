import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("***Assalomu alekum*** \n Bu botda ob-havo ma'lumotini bilishingiz mumkin\n Shahar nomini yozing \nMASALAN TOSHKENT!")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Havo ochiq \U00002600",
        "\n"
        "Clouds": "Bulutli \U00002601",
        "\n"
        "Rain": "Yomg'ir \U00002614",
        "\n"
        "Drizzle": "Yom'gir \U00002614",
        "\n"
        "Thunderstorm": "Shamol \U000026A1",
        '\n'
        "Snow": "Qor \U0001F328",
        '\n'
        "Mist": "Tuman \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Ob-havo shaharda: {city}\nHavo harorati: {cur_weather}C° {wd}\n"
              f"Namlik darajasi: {humidity}%\nHavo bosimi: {pressure} мм.рт.ст\nShamol: {wind} м/с\n"
              f"Quyosh chiqishi: {sunrise_timestamp}\nQuyosh botishi: {sunset_timestamp}\nKun davomiyligi: {length_of_the_day}\n"
              f"***KUNINGIZ HAYRLI O'TSIN!***"
              )

    except:
        await message.reply("\U00002620 SHAHAR NOMINI TO'G'I YOZING \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)