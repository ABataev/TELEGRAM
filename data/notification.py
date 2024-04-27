import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Notification(SqlAlchemyBase):
    __tablename__ = 'notification'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                )

    chat_id = sqlalchemy.Column(sqlalchemy.Integer,
                                )

    film_id = sqlalchemy.Column(sqlalchemy.Integer)
