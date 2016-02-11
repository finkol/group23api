from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Numeric, Time
from sqlalchemy.orm import relationship, backref
from database import Base
from sqlalchemy.dialects.postgresql import ARRAY
import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    sex = Column(String(5), unique=False)
    age = Column(Integer, unique=False)

    def __init__(self, name=None, sex=None, age=None):
        self.name = name
        self.sex = sex
        self.age = age

    def __repr__(self):
        return '<User ' + str(self.id) + ' %r>' % self.name

    def get_object(self):
        return {'id': self.id, 'name': self.name, 'sex': self.sex, 'age': self.age}


class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), unique=False)
    reaction_time = Column(Time(timezone=False), unique=False)
    distance_from_centre = Column(Numeric(asdecimal=False), unique=False)
    number_of_drinks = Column(Integer, unique=False)
    timestamp = Column(DateTime(timezone=False), unique=False, default=datetime.datetime.now)

    def __init__(self, user_id=None, reaction_time=None, distance_from_centre=None, number_of_drinks=None):
        self.user_id = user_id
        self.reaction_time = reaction_time
        self.distance_from_centre = distance_from_centre
        self.number_of_drinks = number_of_drinks

    def __repr__(self):
        return '<Result ' + str(self.id) + ' %r>' % self.user_id

    def get_object(self):
        return {'id': self.id, 'user_id': self.user_id, 'reaction_time': self.reaction_time,
                'distance_from_centre': self.distance_from_centre, 'number_of_drinks': self.number_of_drinks}

