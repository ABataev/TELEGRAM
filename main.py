import telebot
import requests
import json
from pprint import pprint


req = 'https://api.kinopoisk.dev/v1.4/movie'
key = 'token=FVQYY6Y-K264HH1-PV9YAN9-WE1SKJD'


Types = {'фильм': "movie",
         'сериал': "tv-series",
         'мультфильм': "cartoon",
         'мультсериал': "animated-series",
         'аниме': "anime"
         }
flagTop = False


KinoMan = telebot.TeleBot('6553146441:AAF9PphxsXn_HWt3orI73ceFfCxR987pOBI')
CommandList = {
    'start': 'Обязательная команда, поднимающая бота из спячки',
    'top': 'Эта команда выведет топ фильмов, мультфтльмов или сериалов',
    'vote': 'Эта команда поставит оценку выбраному вами фильму(Внутри ТГ бота)',
    'kino_for_me': 'Эта команда подберет для вас кино(Необходимо поставить минимум 15 оценок для разных фильмов)',
    'kino_info': 'Выведет информацию о выбранном фильме'
}


@KinoMan.message_handler(commands=['start'])
def start(msg):
    KinoMan.send_message(msg.chat.id, f'Какие приказания <b>Босс</b>?', parse_mode='html')


@KinoMan.message_handler(commands=['help'])
def help(msg):
    for i in CommandList:
        KinoMan.send_message(msg.chat.id, f'/{i}: {CommandList[i]}', parse_mode='html')


@KinoMan.message_handler(commands=['top'])
def ShowTop(msg):
    global flagTop
    KinoMan.send_message(msg.chat.id, 'Какой жанр? (фильм, мультфильм, сериал, мультсериал, аниме) ((Пиши правильно, а то я тебя не пойму!))', parse_mode='html')
    flagTop = True


@KinoMan.message_handler()
def LeftMessage(msg):
    global flagTop
    if flagTop:
        response = requests.get(f'{req}?limit=10&type={Types[msg.text.lower()]}&rating.kp=8.5-10&{key}')
        response = json.loads(response.content)
        count = 0
        for kino in response['docs']:
            genr = []
            cntr = []
            count += 1
            KinoMan.send_message(msg.chat.id, f'Top {count}', parse_mode='html')
            if kino['name']:
                KinoMan.send_message(msg.chat.id, f'Название: {kino["name"]}\nВозрастное ограничение: {kino["ageRating"]}+', parse_mode='html')
            KinoMan.send_message(msg.chat.id, '====Жанры====', parse_mode='html')
            for genre in kino['genres']:
                genr.append(genre['name'])
            print(genr)
            KinoMan.send_message(msg.chat.id, '\n'.join(genr), parse_mode='html')
            KinoMan.send_message(msg.chat.id, '====Страны====', parse_mode='html')
            for country in kino['countries']:
                cntr.append(country['name'])
            print(cntr)
            KinoMan.send_message(msg.chat.id, '\n'.join(cntr), parse_mode='html')
            KinoMan.send_message(msg.chat.id, f'Длительность: {kino["movieLength"]} минут\n====Рейтинг====\n{kino["rating"]["kp"]}\nОценили {kino["votes"]["kp"]} человек\n====Описание====\n{kino["description"]}', parse_mode='html')
            KinoMan.send_message(msg.chat.id, '====Постер====', parse_mode='html')
            KinoMan.send_photo(msg.chat.id, kino["poster"]["url"], parse_mode='html')
    else:
        KinoMan.send_message(msg.chat.id, 'Я бы и рад с вами поболтать <b>Босс</b>, но давайте перейдем к делу. Дайте мне команду. Не знаете какую? Используйте /help!', parse_mode='html')

KinoMan.polling(none_stop=True)