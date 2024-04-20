from data import db_session
from data.notification import *
from data.list import *
from data.score import *
from data.user import *


# Добавить пользователя
def create_user(usID, chID):
    user = User()
    user.user_id = usID
    user.chat_id = chID
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


# Добавить фильм в список отложенных фильмов
def add_list(usID, chID, film_name):
    db_sess = db_session.create_session()
    list = List()
    list.user_id = usID
    list.chat_id = chID
    list.film_name = film_name
    db_sess.add(list)
    db_sess.commit()


# Удалить фильм из списка отложенных фильмов
def remove_list(usID, chID, film_name):
    db_sess = db_session.create_session()
    dell = db_sess.query(List).filter(List.user_id == usID,
                                      List.chat_id == chID,
                                      List.film_name == film_name).first()
    if dell:
        db_sess.delete(dell)
        db_sess.commit()
    else:
        return 'ERROR'


# Выдать список отложенных фильмов
def take_list(usID, chID):
    db_sess = db_session.create_session()
    return db_sess.query(List).filter(List.user_id == usID,
                                      List.chat_id == chID).all()


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
    return db_sess.query(Notification).filter(Notification.user_id == usID,
                                              Notification.chat_id == chID).all()


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
