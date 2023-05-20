import telebot
import webbrowser
import requests
import json

bot = telebot.TeleBot('6250122740:AAEDp8i0TI3YFfPQxbT9jAzCucmNN2yf7xg')
API = '5e364448-2bb1-4f9d-9395-a6b8a19fb20c'

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} введите номер рейса')


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open(f'https://ru.flightaware.com/live/')


@bot.message_handler(content_types=['text'])
def get_flight(message):
    flight = message.text.strip().lower()
    res = requests.get(f'https://airlabs.co/api/v9/flight?flight_iata={flight}&api_key={API}')
    data = json.loads(res.text)
    bot.reply_to(message, f'Рейс: {data["response"]["flight_number"]}\n'
                          f'Время прибытия(местное): {data["response"]["arr_time"]}\n'
                          f'Аэропорт прилета: {data["response"]["arr_iata"]}\n'
                          f'Самолет: {data["response"]["aircraft_icao"]}\n'
                          f'Авиалинии:{data["response"]["airline_iata"]}'
                          f'')

bot.polling(none_stop=True)