import telebot
import requests
import json

from db_func import *
from pprint import pprint


req = 'https://api.kinopoisk.dev/v1.4/movie'
key = 'token=FVQYY6Y-K264HH1-PV9YAN9-WE1SKJD'
FlagFilmToMemory = False
FlagFilmToVote = False
FlagFilmToNotif = False
score = 0
films_list = []

db_session.global_init('db/telebot_db')

KinoMan = telebot.TeleBot('6553146441:AAF9PphxsXn_HWt3orI73ceFfCxR987pOBI')
CommandList = {
    'top_movie': 'Эта команда выведет топ фильмов',
    'top_cartoon': 'Эта команда выведет топ мультфильмов',
    'top_series': 'Эта команда выведет топ сериалов',
    'top_animated_series': 'Эта команда выведет топ мультсериалов',
    'top_anime': 'Эта команда выведет топ аниме',
    'vote (Оценка) (Название)': 'Эта команда поставит оценку выбраному вами фильму(Внутри ТГ бота)',
    'kino_for_me': 'Эта команда подберет для вас кино',
    'top_bot_kino': 'Выведет топ фильмов из нашей базы данных',
    'kino_info (Название фильма)': 'Выведет подробную информацию о выбранном фильме',
    'add_to_notification (Название)': 'Поставит выход выбранного на уведомление',
    'remove_from_notification (Название)': 'Удалит выбранное из списка уведомлений',
    'print_notif': 'Выводит список поставленного на уведомление',
    'add_to_memory (Название)': 'Добавит выбранное в список отложенного',
    'remove_from_memory (Название)': 'Удалит выбранное из списка отложенного',
    'print_memory': 'Выведет список отложенного'
}


@KinoMan.message_handler(commands=['start'])
def start(msg):
    KinoMan.send_message(msg.chat.id, f'Какие приказания <b>Босс</b>? Не знаешь? Пропиши команду /help',
                         parse_mode='html')
    check_user(msg.from_user.id, msg.chat.id)


@KinoMan.message_handler(commands=['help'])
def help(msg):
    for command in CommandList:
        KinoMan.send_message(msg.chat.id, f'/{command}: {CommandList[command]}', parse_mode='html')


@KinoMan.message_handler(commands=['vote'])
def vote(msg):
    global FlagFilmToVote, films_list, score
    score = msg.text.split()[1:2]
    response = requests.get(f'{req}/search?page=1&limit=5&query={" ".join(msg.text.split()[2:])}&{key}')
    response = json.loads(response.content)
    films_list = []
    ID_kino = 0
    FlagFilmToVote = True
    for kino in response['docs']:
        ID_kino += 1
        films_list.append(kino)
        KinoMan.send_message(msg.chat.id, f'=======================', parse_mode='html')
        KinoMan.send_message(msg.chat.id, f'Number {ID_kino}', parse_mode='html')
        KinoMan.send_message(msg.chat.id, '====Постер====', parse_mode='html')
        if 'poster' in kino:
            if 'url' in kino['poster']:
                if kino['poster']['url']:
                    KinoMan.send_photo(msg.chat.id, kino["poster"]["url"], parse_mode='html')
                else:
                    KinoMan.send_message(msg.chat.id, 'Постер отсутствует', parse_mode='html')

        if kino['name']:
            KinoMan.send_message(msg.chat.id, f'Название: {kino["name"]}\nВозрастное ограничение: {kino["ageRating"]}+',
                                 parse_mode='html')
    KinoMan.send_message(msg.chat.id,
                         '======================\nВ следующем сообщении напишите только номер нужного вам фильма',
                         parse_mode='html')


@KinoMan.message_handler(commands=['top_bot_kino'])
def TopBotKino(msg):
    if top_5_users_film():
        for KinoId in top_5_users_film():
            response = requests.get(f'{req}?{KinoId}&{key}')
            response = json.loads(response.content)
            for kino in response['docs']:
                KinoMan.send_message(msg.chat.id, '====Постер====', parse_mode='html')
                if 'poster' in kino:
                    if 'url' in kino['poster']:
                        if kino['poster']['url']:
                            pprint(kino['poster']['url'])
                            KinoMan.send_photo(msg.chat.id, kino["poster"]["url"], parse_mode='html')
                        else:
                            KinoMan.send_message(msg.chat.id, 'Постер отсутствует', parse_mode='html')
                if kino['name']:
                    KinoMan.send_message(msg.chat.id, f'Название: {kino["name"]}', parse_mode='html')
    else:
        KinoMan.send_message(msg.chat.id, 'Бот еще не составил топ фильмов!', parse_mode='html')


@KinoMan.message_handler(commands=['kino_for_me'])
def kino_for_me(msg):
    if top_user_genre(msg.from_user.id, msg.chat.id):
        for genre in top_user_genre(msg.from_user.id, msg.chat.id):
            response = requests.get(f'{req}?limit=1&type=movie&genres.name={genre[0]}&rating.kp=8.5-10&{key}')
            response = json.loads(response.content)
            for kino in response['docs']:
                genr = []
                KinoMan.send_message(msg.chat.id, '====Постер====', parse_mode='html')
                if 'poster' in kino:
                    if 'url' in kino['poster']:
                        if kino['poster']['url']:
                            KinoMan.send_photo(msg.chat.id, kino["poster"]["url"], parse_mode='html')
                        else:
                            KinoMan.send_message(msg.chat.id, 'Постер отсутствует', parse_mode='html')
                if kino['name']:
                    KinoMan.send_message(msg.chat.id, f'Название: {kino["name"]}', parse_mode='html')
                KinoMan.send_message(msg.chat.id, '====Жанры====', parse_mode='html')
                for genres in kino['genres']:
                    genr.append(genres['name'])
                KinoMan.send_message(msg.chat.id, '\n'.join(genr), parse_mode='html')
                KinoMan.send_message(msg.chat.id,
                                     f'====Рейтинг====\n{kino["rating"]["kp"]}\nОценили {kino["votes"]["kp"]} человек\n====Описание====\n{kino["description"]}',
                                     parse_mode='html')
    else:
        KinoMan.send_message(msg.chat.id, 'У вас не достаточно оценок в ТГ боте!', parse_mode='html')


@KinoMan.message_handler(commands=['print_memory'])
def print_memory(msg):
    if take_memory(msg.from_user.id, msg.chat.id):
        for kino in take_memory(msg.from_user.id, msg.chat.id):
            response = requests.get(f'{req}/search?page=1&limit=5&query={kino[0]}&{key}')
            response = json.loads(response.content)
            for kin in response['docs']:
                KinoMan.send_message(msg.chat.id, '====Постер====', parse_mode='html')
                if 'poster' in kin:
                    if 'url' in kin['poster']:
                        if kino['poster']['url']:
                            KinoMan.send_photo(msg.chat.id, kino["poster"]["url"], parse_mode='html')
                        else:
                            KinoMan.send_message(msg.chat.id, 'Постер отсутствует', parse_mode='html')
                if kin['name']:
                    KinoMan.send_message(msg.chat.id,
                                         f'Название: {kin["name"]}\nВозрастное ограничение: {kin["ageRating"]}+',
                                         parse_mode='html')
    else:
        KinoMan.send_message(msg.chat.id, 'У вас нет поставленных на уведомление фильмов!', parse_mode='html')


@KinoMan.message_handler(commands=['remove_from_memory'])
def remove_from_memory(msg):
    remove_memory(msg.from_user.id, msg.chat.id, " ".join(msg.text.split()[1:]))


@KinoMan.message_handler(commands=['add_to_memory'])
def add_to_memory(msg):
    global FlagFilmToMemory, films_list
    response = requests.get(f'{req}/search?page=1&limit=5&query={" ".join(msg.text.split()[1:])}&{key}')
    response = json.loads(response.content)
    films_list = []
    ID_kino = 0
    FlagFilmToMemory = True
    for kino in response['docs']:
        ID_kino += 1
        films_list.append(kino)
        KinoMan.send_message(msg.chat.id, f'=======================', parse_mode='html')
        KinoMan.send_message(msg.chat.id, f'Number {ID_kino}', parse_mode='html')
        KinoMan.send_message(msg.chat.id, '====Постер====', parse_mode='html')
        if 'poster' in kino:
            if 'url' in kino['poster']:
                if kino['poster']['url']:
                    KinoMan.send_photo(msg.chat.id, kino["poster"]["url"], parse_mode='html')
                else:
                    KinoMan.send_message(msg.chat.id, 'Постер отсутствует', parse_mode='html')

        if kino['name']:
            KinoMan.send_message(msg.chat.id, f'Название: {kino["name"]}\nВозрастное ограничение: {kino["ageRating"]}+',
                                 parse_mode='html')
        KinoMan.send_message(msg.chat.id,
                             '======================\nВ следующем сообщении напишите только номер нужного вам фильма',
                             parse_mode='html')


@KinoMan.message_handler(commands=['print_notif'])
def print_notif(msg):
    if take_notification(msg.from_user.id, msg.chat.id):
        for kino in take_notification(msg.from_user.id, msg.chat.id):
            response = requests.get(f'{req}/search?page=1&limit=5&query={kino[0]}&{key}')
            response = json.loads(response.content)
            for kin in response['docs']:
                KinoMan.send_message(msg.chat.id, '====Постер====', parse_mode='html')
                if 'poster' in kin:
                    if 'url' in kin['poster']:
                        if kin['poster']['url']:
                            KinoMan.send_photo(msg.chat.id, kin["poster"]["url"], parse_mode='html')
                        else:
                            KinoMan.send_message(msg.chat.id, 'Постер отсутствует', parse_mode='html')

                if kin['name']:
                    KinoMan.send_message(msg.chat.id,
                                         f'Название: {kin["name"]}\nВозрастное ограничение: {kin["ageRating"]}+',
                                         parse_mode='html')
    else:
        KinoMan.send_message(msg.chat.id, 'У вас нет поставленных на уведомление фильмов!', parse_mode='html')


@KinoMan.message_handler(commands=['remove_from_notification'])
def remove_from_notification(msg):
    remove_notification(msg.from_user.id, msg.chat.id, " ".join(msg.text.split()[1:]))


@KinoMan.message_handler(commands=['add_to_notification'])
def add_to_notif(msg):
    global FlagFilmToNotif, films_list
    response = requests.get(f'{req}/search?page=1&limit=5&query={" ".join(msg.text.split()[1:])}&{key}')
    response = json.loads(response.content)
    films_list = []
    ID_kino = 0
    FlagFilmToNotif = True
    for kino in response['docs']:
        ID_kino += 1
        films_list.append(kino)
        KinoMan.send_message(msg.chat.id, f'=======================', parse_mode='html')
        KinoMan.send_message(msg.chat.id, f'Number {ID_kino}', parse_mode='html')
        KinoMan.send_message(msg.chat.id, '====Постер====', parse_mode='html')
        if 'poster' in kino:
            if 'url' in kino['poster']:
                if kino['poster']['url']:
                    KinoMan.send_photo(msg.chat.id, kino["poster"]["url"], parse_mode='html')
                else:
                    KinoMan.send_message(msg.chat.id, 'Постер отсутствует', parse_mode='html')

        if kino['name']:
            KinoMan.send_message(msg.chat.id, f'Название: {kino["name"]}\nВозрастное ограничение: {kino["ageRating"]}+',
                                 parse_mode='html')
    KinoMan.send_message(msg.chat.id, '======================\nВ следующем сообщении напишите только номер нужного вам фильма', parse_mode='html')


@KinoMan.message_handler(commands=['top_movie'])
def ShowTopMovie(msg):
    response = requests.get(f'{req}?limit=5&type=movie&rating.kp=8.5-10&{key}')
    response = json.loads(response.content)
    top = 0
    for kino in response['docs']:
        genr = []
        top += 1
        KinoMan.send_message(msg.chat.id, '====Постер====', parse_mode='html')
        if 'poster' in kino:
            if 'url' in kino['poster']:
                if kino['poster']['url']:
                    KinoMan.send_photo(msg.chat.id, kino["poster"]["url"], parse_mode='html')
                else:
                    KinoMan.send_message(msg.chat.id, 'Постер отсутствует', parse_mode='html')
        KinoMan.send_message(msg.chat.id, f'Top {top}', parse_mode='html')
        if kino['name']:
            KinoMan.send_message(msg.chat.id, f'Название: {kino["name"]}', parse_mode='html')
        KinoMan.send_message(msg.chat.id, '====Жанры====', parse_mode='html')
        for genre in kino['genres']:
            genr.append(genre['name'])
        KinoMan.send_message(msg.chat.id, '\n'.join(genr), parse_mode='html')
        KinoMan.send_message(msg.chat.id,
                             f'====Рейтинг====\n{kino["rating"]["kp"]}\nОценили {kino["votes"]["kp"]} человек\n====Описание====\n{kino["description"]}',
                             parse_mode='html')


@KinoMan.message_handler(commands=['top_cartoon'])
def ShowTopCartoon(msg):
    response = requests.get(f'{req}?limit=5&type=cartoon&rating.kp=8.5-10&{key}')
    response = json.loads(response.content)
    top = 0
    for kino in response['docs']:
        genr = []
        top += 1
        KinoMan.send_message(msg.chat.id, '====Постер====', parse_mode='html')
        if 'poster' in kino:
            if 'url' in kino['poster']:
                if kino['poster']['url']:
                    KinoMan.send_photo(msg.chat.id, kino["poster"]["url"], parse_mode='html')
                else:
                    KinoMan.send_message(msg.chat.id, 'Постер отсутствует', parse_mode='html')
        KinoMan.send_message(msg.chat.id, f'Top {top}', parse_mode='html')
        if kino['name']:
            KinoMan.send_message(msg.chat.id, f'Название: {kino["name"]}', parse_mode='html')
        KinoMan.send_message(msg.chat.id, '====Жанры====', parse_mode='html')
        for genre in kino['genres']:
            genr.append(genre['name'])
        KinoMan.send_message(msg.chat.id, '\n'.join(genr), parse_mode='html')
        KinoMan.send_message(msg.chat.id,
                             f'====Рейтинг====\n{kino["rating"]["kp"]}\nОценили {kino["votes"]["kp"]} человек\n====Описание====\n{kino["description"]}',
                             parse_mode='html')


@KinoMan.message_handler(commands=['top_series'])
def ShowTopSeries(msg):
    response = requests.get(f'{req}?limit=5&type=tv-series&rating.kp=8.5-10&{key}')
    response = json.loads(response.content)
    top = 0
    for kino in response['docs']:
        genr = []
        top += 1
        KinoMan.send_message(msg.chat.id, '====Постер====', parse_mode='html')
        if 'poster' in kino:
            if 'url' in kino['poster']:
                if kino['poster']['url']:
                    KinoMan.send_photo(msg.chat.id, kino["poster"]["url"], parse_mode='html')
                else:
                    KinoMan.send_message(msg.chat.id, 'Постер отсутствует', parse_mode='html')
        KinoMan.send_message(msg.chat.id, f'Top {top}', parse_mode='html')
        if kino['name']:
            KinoMan.send_message(msg.chat.id, f'Название: {kino["name"]}', parse_mode='html')
        KinoMan.send_message(msg.chat.id, '====Жанры====', parse_mode='html')
        for genre in kino['genres']:
            genr.append(genre['name'])
        KinoMan.send_message(msg.chat.id, '\n'.join(genr), parse_mode='html')
        KinoMan.send_message(msg.chat.id,
                             f'====Рейтинг====\n{kino["rating"]["kp"]}\nОценили {kino["votes"]["kp"]} человек\n====Описание====\n{kino["description"]}',
                             parse_mode='html')


@KinoMan.message_handler(commands=['top_animated_series'])
def ShowTopAnimatedSeries(msg):
    response = requests.get(f'{req}?limit=5&type=animated-series&rating.kp=8.5-10&{key}')
    response = json.loads(response.content)
    top = 0
    for kino in response['docs']:
        genr = []
        top += 1
        KinoMan.send_message(msg.chat.id, '====Постер====', parse_mode='html')
        if 'poster' in kino:
            if 'url' in kino['poster']:
                if kino['poster']['url']:
                    KinoMan.send_photo(msg.chat.id, kino["poster"]["url"], parse_mode='html')
                else:
                    KinoMan.send_message(msg.chat.id, 'Постер отсутствует', parse_mode='html')
        KinoMan.send_message(msg.chat.id, f'Top {top}', parse_mode='html')
        if kino['name']:
            KinoMan.send_message(msg.chat.id, f'Название: {kino["name"]}', parse_mode='html')
        KinoMan.send_message(msg.chat.id, '====Жанры====', parse_mode='html')
        for genre in kino['genres']:
            genr.append(genre['name'])
        KinoMan.send_message(msg.chat.id, '\n'.join(genr), parse_mode='html')
        KinoMan.send_message(msg.chat.id,
                             f'====Рейтинг====\n{kino["rating"]["kp"]}\nОценили {kino["votes"]["kp"]} человек\n====Описание====\n{kino["description"]}',
                             parse_mode='html')


@KinoMan.message_handler(commands=['top_anime'])
def ShowTopAnime(msg):
    response = requests.get(f'{req}?limit=5&type=anime&rating.kp=8.5-10&{key}')
    response = json.loads(response.content)
    top = 0
    for kino in response['docs']:
        genr = []
        top += 1
        KinoMan.send_message(msg.chat.id, '====Постер====', parse_mode='html')
        if 'poster' in kino:
            if 'url' in kino['poster']:
                if kino['poster']['url']:
                    KinoMan.send_photo(msg.chat.id, kino["poster"]["url"], parse_mode='html')
                else:
                    KinoMan.send_message(msg.chat.id, 'Постер отсутствует', parse_mode='html')
        KinoMan.send_message(msg.chat.id, f'Top {top}', parse_mode='html')
        if kino['name']:
            KinoMan.send_message(msg.chat.id, f'Название: {kino["name"]}', parse_mode='html')
        KinoMan.send_message(msg.chat.id, '====Жанры====', parse_mode='html')
        for genre in kino['genres']:
            genr.append(genre['name'])
        KinoMan.send_message(msg.chat.id, '\n'.join(genr), parse_mode='html')
        KinoMan.send_message(msg.chat.id,
                             f'====Рейтинг====\n{kino["rating"]["kp"]}\nОценили {kino["votes"]["kp"]} человек\n====Описание====\n{kino["description"]}',
                             parse_mode='html')


@KinoMan.message_handler(commands=['kino_info'])
def KinoInfo(msg):
    FilmName = msg.text[11:]
    response = requests.get(f'{req}/search?page=1&limit=1&query={FilmName}&{key}')
    response = json.loads(response.content)
    if len(response) > 0:
        kino = json.loads(response.content)['docs'][0]
        genr = []
        country = []

        KinoMan.send_message(msg.chat.id, '====Постер====', parse_mode='html')
        if 'poster' in kino:
            if 'url' in kino['poster']:
                if kino['poster']['url']:
                    KinoMan.send_photo(msg.chat.id, kino["poster"]["url"], parse_mode='html')
                else:
                    KinoMan.send_message(msg.chat.id, 'Постер отсутствует', parse_mode='html')
        if kino['name']:
            KinoMan.send_message(msg.chat.id, f'Название: {kino["name"]}\nВозрастное ограничение: {kino["ageRating"]}+',
                                 parse_mode='html')
        KinoMan.send_message(msg.chat.id, '====Жанры====', parse_mode='html')
        for genre in kino['genres']:
            if kino[genre]:
                genr.append(genre['name'])
        KinoMan.send_message(msg.chat.id, '\n'.join(genr), parse_mode='html')
        KinoMan.send_message(msg.chat.id, '====Страны====', parse_mode='html')
        for nations in kino['countries']:
            country.append(nations['name'])
        KinoMan.send_message(msg.chat.id, '\n'.join(country), parse_mode='html')
        KinoMan.send_message(msg.chat.id,
                             f'Длительность: {kino["movieLength"]} минут\n====Рейтинг====\n{kino["rating"]["kp"]}\nОценили {kino["votes"]["kp"]} человек\n====Описание====\n{kino["description"]}',
                             parse_mode='html')


@KinoMan.message_handler()
def LeftMessage(msg):
    global FlagFilmToNotif, films_list, FlagFilmToMemory, FlagFilmToVote, score
    if FlagFilmToVote:
        try:
            FlagFilmToVote = False
            vote_score(msg.chat.id, msg.from_user.id, films_list[int(msg.text) - 1]['id'], int(score[0]),
                       films_list[int(msg.text) - 1]['genres'][0]['name'])
            KinoMan.send_message(msg.chat.id, 'Успешно!', parse_mode='html')
        except ValueError:
            KinoMan.send_message(msg.chat.id,
                                 'Ошибка! Нужно написать только цифру! Попробуй еще разок.',
                                 parse_mode='html')
            FlagFilmToVote = True
        except IndexError:
            KinoMan.send_message(msg.chat.id, 'Команда введена некорректно', parse_mode='html')

    elif FlagFilmToMemory:
        try:
            FlagFilmToMemory = False
            add_memory(msg.chat.id, msg.from_user.id, films_list[int(msg.text) - 1]['id'])
            KinoMan.send_message(msg.chat.id, 'Успешно!', parse_mode='html')
        except ValueError:
            KinoMan.send_message(msg.chat.id,
                                 'Ошибка! Нужно написать только цифру! Попробуй еще разок.',
                                 parse_mode='html')
            FlagFilmToMemory = True

    elif FlagFilmToNotif:
        try:
            FlagFilmToNotif = False
            add_notification(msg.chat.id, msg.from_user.id, films_list[int(msg.text) - 1]['id'])
            KinoMan.send_message(msg.chat.id, 'Успешно!', parse_mode='html')
        except ValueError:
            KinoMan.send_message(msg.chat.id,
                                 'Ошибка! Нужно написать только цифру! Попробуй еще разок.',
                                 parse_mode='html')
            FlagFilmToNotif = True

    else:
        KinoMan.send_message(msg.chat.id, 'Я бы и рад с вами поболтать, <b>Босс</b>, но давайте перейдем к делу. Дайте мне команду. Не знаете какую? Используйте /help!', parse_mode='html')


KinoMan.polling(none_stop=True)
