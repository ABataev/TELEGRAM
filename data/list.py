import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class List(SqlAlchemyBase):
    __tablename__ = 'list'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                )

    chat_id = sqlalchemy.Column(sqlalchemy.Integer,
                                )

    film_name = sqlalchemy.Column(sqlalchemy.String)


