import telebot

KinoMan = telebot.TeleBot('6553146441:AAF9PphxsXn_HWt3orI73ceFfCxR987pOBI')
CommandList = {
    'start': 'Обязательная команда, поднимающая бота из спячки',
    'all_top_list': 'Эта команда нужна для вывода списка фильмов находящихся в топе за все время',
    'now_top_list': 'Эта команда нужна для вывода списка фильмов находящихся в тренде',
    'kino_for_me': 'Эта команда подберет для вас кино(Необходимо поставить минимум 15 оценок для разных фильмов)',
}


@KinoMan.message_handler(commands=['start'])
def start(msg):
    KinoMan.send_message(msg.chat.id, f'Какие приказания <b>Босс</b>?', parse_mode='html')


@KinoMan.message_handler(commands=['help'])
def help(msg):
    for i in CommandList:
        KinoMan.send_message(msg.chat.id, f'{i}: {CommandList[i]}', parse_mode='html')


@KinoMan.message_handler()
def LeftMessage(msg):
    KinoMan.send_message(msg.chat.id, 'Я бы и рад с вами поболтать <b>Босс</b>, но давайте перейдем к делу. Дайте мне команду. Не знаете какую? Используйте /help!', parse_mode='html')


KinoMan.polling(none_stop=True)