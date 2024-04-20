from data import db_session
from data.notification import *
from data.memory import *
from data.score import *
from data.user import *
from sqlalchemy import *


# Добавить пользователя
def create_user(usID, chID):
    user = User()
    user.user_id = usID
    user.chat_id = chID
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


# Проверка наличия пользователя в базе
def check_user(usID, chID):
    db_sess = db_session.create_session()
    dell = db_sess.query(User).filter(User.user_id == usID,
                                      User.chat_id == chID).first()
    if not dell:
        create_user(usID, chID)


# Добавить фильм в список отложенных фильмов
def add_memory(usID, chID, film_name):
    db_sess = db_session.create_session()
    list = Memory()
    list.user_id = usID
    list.chat_id = chID
    list.film_name = film_name
    db_sess.add(list)
    db_sess.commit()


# Удалить фильм из списка отложенных фильмов
def remove_memory(usID, chID, film_name):
    db_sess = db_session.create_session()
    dell = db_sess.query(Memory).filter(Memory.user_id == usID,
                                        Memory.chat_id == chID,
                                        Memory.film_name == film_name).first()
    if dell:
        db_sess.delete(dell)
        db_sess.commit()
    else:
        return 'ERROR'


# Выдать список отложенных фильмов
def take_memory(usID, chID):
    db_sess = db_session.create_session()
    dell = db_sess.execute(select(Memory.film_name).where(Memory.user_id == usID,
                                                          Memory.chat_id == chID)).all()
    if dell:
        return dell


# Добавить уведомление
def add_notification(usID, chID, film_name):
    db_sess = db_session.create_session()
    notif = Notification()
    notif.user_id = usID
    notif.chat_id = chID
    notif.film_name = film_name
    db_sess.add(notif)
    db_sess.commit()


# Удалить уведомление
def remove_notification(usID, chID, film_name):
    db_sess = db_session.create_session()
    dell = db_sess.query(Notification).filter(Notification.user_id == usID,
                                              Notification.chat_id == chID,
                                              Notification.film_name == film_name).first()
    if dell:
        db_sess.delete(dell)
        db_sess.commit()
    else:
        return 'ERROR'


# Выдать список уведомлений
def take_notification(usID, chID):
    db_sess = db_session.create_session()
    dell = db_sess.execute(select(Notification.film_name).where(Notification.user_id == usID,
                                                                Notification.chat_id == chID)).all()
    if dell:
        return dell


# Поставить баллы фильму
def vote_score(usID, chID, film_name, score, genre):
    db_sess = db_session.create_session()
    SCORE = Score()
    SCORE.user_id = usID
    SCORE.chat_id = chID
    SCORE.film_name = film_name
    SCORE.score = score
    SCORE.genre = genre
    db_sess.add(SCORE)
    db_sess.commit()


# Выдать топ 5 любимых фильмов пользователей бота
def top_5_users_film():
    db_sess = db_session.create_session()
    dell = db_sess.execute(select(Score.film_name, Score.score)).all()
    if dell:
        slov_film = {}
        for fl_name, sc in dell:
            if fl_name not in slov_film:
                slov_film[fl_name] = [sc, 1]
            else:
                slov_film[fl_name] = [slov_film[fl_name][0] + sc,
                                      slov_film[fl_name][1] + 1]
        slov_film_right = []
        for i in slov_film:
            slov_film_right += [[i, round(slov_film[i][0] / slov_film[i][1], 1)]]
        slov_film_right.sort(key=lambda x: x[-1], reverse=True)
        return slov_film_right[:5]


# Выдача топ 5 любимых жанров пользователя
def top_user_genre(usID, chID):
    db_sess = db_session.create_session()
    dell = db_sess.execute(select(Score.score, Score.genre).where(Score.user_id == usID,
                                                                  Score.chat_id == chID)).all()
    if dell:
        slov_genre = {}
        for sc, gr in dell:
            if gr not in slov_genre:
                slov_genre[gr] = [sc, 1]
            else:
                slov_genre[gr] = [slov_genre[gr][0] + sc,
                                  slov_genre[gr][1] + 1]
        slov_genre_right = []
        for i in slov_genre:
            slov_genre_right += [[i, round(slov_genre[i][0] / slov_genre[i][1], 1)]]
        slov_genre_right.sort(key=lambda x: x[-1], reverse=True)
        return slov_genre_right[:5]
